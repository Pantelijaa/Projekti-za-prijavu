from setuptools import find_packages, setup


# python -m  pipreqs.pipreqs --encoding utf-8 
requires = list()
with open("requirements.txt", "r") as f:
    for line in f:
        requires.append(line[:-1])

setup(
    name='SpotifyToMP3',
    version='1.0.0',
    description='Web App for downloading songs from Spotify',
    author='Nikola',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)

#install with python setup.py install