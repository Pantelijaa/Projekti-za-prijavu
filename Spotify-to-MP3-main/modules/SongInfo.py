from dataclasses import dataclass

@dataclass
class SongInfo:
    name: str = None
    name_valid: str = None
    artist: str = None
    number: int = None
    search_pattern: str = None
    file_path: str = None
    album = {
        "name": str, 
        "name_valid": str,
        "release_date": int,
        "img_url": str,
        "img_download_url": str
    }