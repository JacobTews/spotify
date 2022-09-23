import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def spotipy_sample():
    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

# features needed: https://github.com/onramp-io/vanguard_de_project/blob/main/README.md#artist

def get_artist_info():
    pass

def get_album_info():
    pass

def get_track_info():
    pass

def get_track_features():
    pass

if __name__ == '__main__':
    spotipy_sample()