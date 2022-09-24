import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

# needed_features = [
#     FEATURE_NAME ('API ACCESS NAME')
#     album_id ('id')
#     album_name ('name')
#     external_url ('external_urls'['spotify'])
#     image_url ('images'[0]['url'])
#     release_date ('release_date') NOTE: the API sends a string, needs to be converted to a date for SQLite)
#     total_tracks ('total_tracks')
#     type ('album_type')
#     album_uri ('uri')
#     artist_id
# ]

def get_album_info(artist_id: str) -> dict:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = spotify.artist_albums(artist_id=artist_id, album_type='album', country='US', limit=50)
    albums = results['items']

    # if the search returns no results, items will be an empty list
    if len(albums) == 0:
        return None

    complete_albums_dict = {}

    for album in albums:
        album_dict = {}

        album_id = album['id']
        album_dict['album_id'] = album_id



        complete_albums_dict[album['id']] = album_dict


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
        'taylor swift',
        'korey konkol',
        'jacob tews'
    ]

    # for name in artist_list:
    #     # search for artist by name
    #     results = spotify.search(q=f'artist: {name}', type='artist')
    #     items = results['artists']['items']
    #     # if the search returns no results, items will be an empty list
    #     if len(items) > 0:
    #         artist = items[0]
    #
    #     artist_id = artist['id']

        # print(f'{artist["name"]} id: {artist_id}')

    hilary_id = '5JdT0LYJdlPbTC58p60WTX'

    get_album_info(hilary_id)

    print('Run completed')