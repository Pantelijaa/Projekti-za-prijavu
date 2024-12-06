# Python310\Lib\ssl.py, line 579 modified
from flask import Flask, request, url_for, session, redirect, render_template, abort
from modules.SongInfo import SongInfo
from modules.Spotify import Spotify
from modules.SpotifyOAuth import SpotifyOAuth
from pytube import  Search, Stream, YouTube
from moviepy.editor import AudioFileClip
from PIL import Image
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from time import time
from glob import glob
from re import search
from os import getenv, path, name, remove, rename, mkdir
from eyed3 import load, AudioFile
from requests import get

client_id: str = getenv('CLIENT_ID') # Spotify API Client ID
client_secret: str = getenv('CLIENT_SECRET') # Spotify API Client Secret

app = Flask(__name__)

app.secret_key = getenv('SECRET_KEY') # random
app.config['SESSION_COOKIE_NAME'] = 'Moj Kolacic'
TOKEN_INFO: str = "token_info"

# Home page
@app.route('/')
def home():
    """
    Login to personal spotify
    """
    return render_template('home.html')

# Spotify login page
@app.route('/login')
def login():
    spotify: SpotifyOAuth = create_spotify_oauth()
    auth_url: str = spotify.get_authorize_url()
    return redirect(auth_url)

# Redirect page after login
@app.route('/redirect')
def redirectPage():
    """
    Redirect to respond page with code
    """
    spotify: SpotifyOAuth = create_spotify_oauth()
    # clear seasion of previous data
    session.clear()
    code: str = request.args.get('code')
    token_info: dict = spotify.get_access_token(code)
    #store token for later
    session[TOKEN_INFO] = token_info
    return redirect(url_for('main', _external=True))

# Main app page
@app.route('/main', methods = ['POST', 'GET'])
def main():
    try:
        token_info: dict = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    spotify: Spotify = Spotify(auth=token_info["access_token"])
    me: dict = spotify.get_user_info()
    playlists: list = spotify.get_playlists_by_user_id(me["id"])
    me["playlists"] = extract_names(playlists)
    me["playlists_len"] = len(me["playlists"])
    if request.method == 'POST':
        search_value: str = request.form['search-value']
        search_type: str = request.form['search-type']
        if (search_value == 'liked'):
            result: dict = {'liked': spotify.get_saved_tracks()}
        else:
            result: dict = search_on_spotify(search_value, search_type, spotify) 
        try:
            return render_template('main.html', data=me, result=result)    
        except:
            abort(500, description=f"Failed to find {search_type} \"{search_value}\"")
    return render_template('main.html', data=me)

# Download page
@app.route('/download')
def download():
    # Init spotify API
    id: str = request.args.get('id')
    token_info: dict = get_token()
    spotify: Spotify = Spotify(auth=token_info["access_token"])
    download_dir: str = get_download_path() 

    make_download_dir(download_dir)

    # Collect song information
    song: dict = spotify.get_track_by_id(id)
    song_info: SongInfo = populate_song(song, download_dir)

    # Save cover image
    if not path.exists(song_info.album["img_download_url"]):
        album_img = Image.open(get(song_info.album["img_url"], stream=True).raw)
        album_img.save(song_info.album["img_download_url"])

    # Download song if it doesn't exist already
    if path.exists(song_info.file_path + ".mp3"):
        abort(500, description=f"{song_info.file_path} already exists")
    else:
        pytube_mp4_title: str = download_song(song_info.search_pattern, download_dir)
        escaped_pytube_mp4_title: str = remove_invalid_characters(pytube_mp4_title, ['.', "'", ',', '"', '/', ':', '*', '$', '?',])
        escaped_pytube_mp4_title: str = add_escape_characters(escaped_pytube_mp4_title, ['(', ')', '[', ']'], '\\')

        convert_mp4_to_mp3(song_info, download_dir, escaped_pytube_mp4_title)

        export_metadata(load(song_info.file_path + ".mp3" ), song_info)

    return render_template('download.html')

@app.route('/force_logout')
def force_logout():
    session[TOKEN_INFO] = None
    return '', 204

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error=e), 500

def search_playlist(name: str, spotify: Spotify) -> str:
    """
    Finds playlist with specific name.
    
    Returns
    --------
    id
        Spotify `id` of founded playlist.
    """
    me: dict = spotify.get_user_info()
    playlists: list = spotify.get_playlists_by_user_id(me["id"])
    for elem in playlists:
        for val in elem.values():
            if val == name:
                return elem['id']


    
def search_on_spotify(name: str, type: str, spotify: Spotify) -> dict:
    """
    Main function for searching Spotify
    
    Params
    -------
    name
        Name of `type` that is being searched.
    type
        Can be: track, album, artist, liked or any.
    spotify
        Spotify object with valid authorization token.
    """
    if type == 'any':
        type = 'track,album,artist'
    result: dict = spotify.search(query=name, search_type=type)
    if 'album' in type:
        albums = list()
        for item in result['albums']['items']:
            id: str = item['id']
            get_album: dict = spotify.get_album_by_id(id)
            for elem in get_album['tracks']['items']:
                elem['duration'] = convert_from_miliseconds_to_minutes(elem['duration_ms'])
            albums.append(get_album)
        result['albums'] =  albums
    elif type == 'playlist':
        playlist_id: str = search_playlist(name, spotify)
        result: dict = {'playlist': spotify.get_playlist_tracks_by_id(playlist_id)}
    return result

def add_escape_characters(string: str, substrings: list, char: str) -> str:
    counter: int = 0
    for i, letter in enumerate(string):
        for substr in substrings:
            if letter == substr:
                i += counter
                string = string[:i] + char + string[i:]
                counter += 1
    return string

def remove_invalid_characters(string: str, characters: list) -> str:
    for char in characters:
        while char in [*string]:
            index: int = string.index(char)
            string: str = string[:index] + string[index + 1:]
    return string

def convert_from_miliseconds_to_minutes(miliseconds: int) -> str:
    """
    Convert miliseconds to minues in string format `<minutes:seconds>`.
    """
    seconds: int = int(miliseconds/1000)
    minutes: int = 0
    while seconds >= 60:
        seconds -= 60
        minutes +=1
    if seconds < 10:
        seconds = '0' + str(seconds)
    return f'{minutes}:{seconds}'

def get_token() -> dict:
    """
    Get token or refresh if expired.
    """
    token_info: dict = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("Couldn't get access token")
    now: int = int(time())
    is_expired: bool = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify: SpotifyOAuth = create_spotify_oauth()
        token_info = spotify.refresh_access_token(token_info["access_token"])
    return token_info

def create_spotify_oauth() -> SpotifyOAuth:
    """
    Initialize spotify authorization.
    """
    return SpotifyOAuth(client_id=client_id,
        client_secret=client_secret,
        scope='playlist-read-private playlist-read-collaborative user-library-read',
        redirect_uri=url_for('redirectPage', _external=True))

def get_download_path() -> str:
    """
    Returns the default downloads path for linux or windows.
    """
    if name == 'nt':
        sub_key: str = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid: str = '{374DE290-123F-4565-9164-39C4925E467B}'
        with OpenKey(HKEY_CURRENT_USER, sub_key) as key:
            location: str = QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return path.join(path.expanduser('~'), 'downloads')
    
def download_song(search_pattern: str, download_dir: str) -> str:
    """ Downloads song from YouTube.

    Returns
    --------
    title
        Title of downloaded song.
    """
    s: Search = Search(search_pattern) # https://github.com/pytube/pytube/issues/1270
    video: Stream = s.results[0]
    video.use_oauth = True
    audio_mp4_only: YouTube = video.streams.filter(only_audio=True, file_extension='mp4')[-1] # https://github.com/pytube/pytube/issues/1954
    audio_mp4_only.download(output_path=download_dir)
    return audio_mp4_only.title

def populate_song(song: dict, download_dir: str) -> SongInfo:
    """
    Moves all song information into `SongInfo` object.
    
    Returns
    -
    SongInfo
        `SongInfo` object filled with data for specific song.
    """
    info = SongInfo()
    info.name = song["name"]
    info.name_valid = remove_invalid_characters(info.name, ['.', "'", ',', '"', '/', ':', '*', '$', '?'])
    info.artist = song["artists"][0]["name"]
    info.number = int(song["track_number"])
    info.album["name"] = song["album"]["name"]
    info.album["name_valid"] = remove_invalid_characters(info.album["name"], ['.', "'", ',', '"', '/', ':', '*', '$', '?'])
    info.album["release_date"] = int(song["album"]["release_date"][:4])
    info.album["img_url"] = song["album"]["images"][0]["url"]
    info.search_pattern = f"{info.artist} - {info.name}"
    info.album["img_download_url"] = f'{download_dir}\\covers\\{info.album["name_valid"]}.jpeg'
    info.file_path = f"{download_dir}\\{info.artist} - {info.name_valid} ({str(info.album["release_date"])})"

    return info

def extract_names(playlists: list) -> list:
    temp_list = list()
    for playlist in playlists:
        temp_list.append(playlist["name"])
    return temp_list

def make_download_dir(download_path: str) -> None:
    """
    Makes directory (if doesn't exist already) where song and song cover will be downloaded.
    """
    if not path.exists(download_path):
        mkdir(download_path)
    if not path.exists(f'{download_path}\\covers'):
        mkdir(f'{download_path}\\covers')

def export_metadata(audio_file: AudioFile, song_info: SongInfo) -> None:
    """
    Exports all song informations in `.mp3` file, such as title, artist, album name...
    """
    if (audio_file.tag == None):
        audio_file.initTag()
    audio_file.tag.title = song_info.search_pattern
    audio_file.tag.album = song_info.album["name"]
    audio_file.tag.artist = song_info.artist
    audio_file.tag.album_artist = song_info.artist
    audio_file.tag.track_num = song_info.number
    audio_file.tag.release_date = song_info.album["release_date"]
    audio_file.tag.save()

def convert_mp4_to_mp3(song_info: SongInfo, download_folder: str, title: str) -> None:
    """
    Writes audio data from `.mp4` to `.mp3` file and removes old `.mp4` file.
    """
    for file in glob(f"{download_folder}\\*.mp4"):
        if search(title, file):
            # Swap titles
            rename(file, song_info.file_path + ".mp4")
            mp4_file: str = song_info.file_path + ".mp4"
    mp3_file: str = song_info.file_path + ".mp3"      
    audio = AudioFileClip(mp4_file)
    audio.write_audiofile(mp3_file, logger=None)
    remove(mp4_file)

if __name__ == "__main__":
    app.run(debug=True)