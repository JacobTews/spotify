from datetime import datetime
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

    # create dictionary of album details
    complete_albums_dict = {}

    for album in albums:
        album_dict = {}
        # each item is validated before being inserted into the album_dict dictionary

        if len(album['id']) > 0 and isinstance(album['id'], str):
            album_dict['album_id'] = album['id']
        else:
            raise Exception('Album does not have a unique identifier.')

        if len(album['name']) > 0 and isinstance(album['name'], str):
            album_dict['album_name'] = album['name']
        else:
            album_dict['album_name'] = None

        if len(album['external_urls']['spotify']) > 0 and isinstance(album['external_urls']['spotify'], str):
            album_dict['external_url'] = album['external_urls']['spotify']
        else:
            album_dict['external_url'] = None

        if len(album['images'][0]['url']) > 0 and isinstance(album['images'][0]['url'], str):
            album_dict['image_url'] = album['images'][0]['url']
        else:
            album_dict['image_url'] = None

        # Album release dates vary in precision
        release_str = album['release_date']
        if len(release_str) == 4:
            # release date is year only
            album_dict['release_date'] = datetime.strptime(release_str, '%Y')
        elif len(release_str) == 7:
            # release date is year and month only
            album_dict['release_date'] = datetime.strptime(release_str, '%Y-%m')
        elif len(release_str) == 10:
            # release date is year, month, and day
            album_dict['release_date'] = datetime.strptime(release_str, '%Y-%m-%d')
        else:
            album_dict['release_date'] = None

        if isinstance(album['total_tracks'], int):
            album_dict['total_tracks'] = album['total_tracks']
        else:
            album_dict['total_tracks'] = None

        if len(album['album_type']) > 0 and isinstance(album['album_type'], str):
            album_dict['type'] = album['album_type']
        else:
            album_dict['type'] = None

        if len(album['uri']) > 0 and isinstance(album['uri'], str):
            album_dict['album_uri'] = album['uri']
        else:
            album_dict['album_uri'] = None

        album_dict['artist_id'] = artist_id

        complete_albums_dict[album['id']] = album_dict

def make_album_table(artist_ids: list) -> pd.DataFrame:
    album_dict = {}

    for id in artist_ids:
        album_info = get_album_info(id)
        album_dict[album_info['album_id']] = album_info

    album_table = pd.DataFrame.from_dict(album_dict, orient='index')

    return album_table

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

    print(make_album_table([hilary_id]))

    print('Run completed')