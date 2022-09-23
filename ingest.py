"""
The purpose of this script is to retrieve the needed information from the Spotify API.

"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# tasks:
# retrieve Spotify data for 20 artists (must be at least 1000 songs)

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


if __name__ == '__main__':
    pass