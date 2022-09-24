import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

def get_album_info(artist_id):
    pass

if __name__ == '__main__':

    artist_list = [
        'Ben Folds',
        'Chicago',
        'Elliott Miles McKinley',
        'Guarneri Quartet',
        'Hilary Hahn',
        'Arnold Schoenberg',
        'elliott carter',
        'augusta read thomas',
        'michael foumai',
        'mozart',
        'kanye',
        'justin bieber',
        'taylor swift'
    ]

    # create a spotipy object using the credentials stored on local machine as environment variables
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    for artist in artist_list:
        # search for artist by name
        results = spotify.search(q=f'artist: {artist}', type='artist')
        items = results['artists']['items']
        # if the search returns no results, items will be an empty list
        if len(items) > 0:
            artist = items[0]

        # create dictionary of artist details
        artist_info = {'type': 'artist'}

        # each item is validated
        artist_id = artist['id']

        print(artist_id)

    print('Run completed')