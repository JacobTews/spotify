"""
The purpose of this script is to retrieve the needed information from the Spotify API.

"""

from datetime import datetime
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3


# tasks:
# retrieve Spotify data for 20 artists (must be at least 1000 songs)
# includes
#   artist info
#   album info
#   track info
#   track features

def get_artist_info(artist_name: str) -> dict:

    # Here is the list of artist features required:
    # needed_items = [
    #     'id',
    #     'name',
    #     'genres',
    #     'external_urls',
    #     'images',
    #     'followers',
    #     'popularity',
    #     'uri'
    # ]

    # create a spotipy object using the credentials stored on local machine as environment variables
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    # search for artist by name
    results = spotify.search(q=f'artist: {artist_name}', type='artist')
    items = results['artists']['items']
    # if the search returns no results, 'items' will be an empty list
    if len(items) > 0:
        artist = items[0]
    else:
        return None

    # create dictionary of artist details
    # each item is validated before being inserted into the artist_info dictionary
    artist_info = {'type': 'artist'}

    artist_id = artist['id']
    # artist_id must be a string, otherwise we'll insert a null
    if isinstance(artist_id, str) and len(artist_id) > 0:
        artist_info['artist_id'] = artist_id
    else:
        artist_info['artist_id'] = None

    # artist_name must be a string, otherwise we'll insert a null
    name = artist['name']
    if isinstance(name, str) and len(name) > 0:
        artist_info['artist_name'] = name
    else:
        artist_info['artist_name'] = None

    # artist_name must be a single string, otherwise we'll insert a null
    # for artists with multiple genres, we'll just choose the first one
    genre = artist['genres']
    if isinstance(genre, list):
        if len(genre) > 0:
            artist_info['genre'] = genre[0]
        else:
            artist_info['genre'] = None
    elif isinstance(genre, str) and len(genre) > 0:
        artist_info['genre'] = genre
    else:
        artist_info['genre'] = None

    # external_url must be a single string, otherwise we'll insert a null
    # for artists with multiple urls, we will use the spotify one
    artist_url = artist['external_urls']['spotify']
    if len(artist_url) > 0:
        artist_info['external url'] = artist_url
    else:
        artist_info['external url'] = None

    # image_url must be a single string, otherwise we'll insert a null
    # for artists with multiple images, we'll just choose the first one
    artist_image = artist['images']
    if isinstance(artist_image, dict) and len(artist_image) > 0:
        artist_info['image_url'] = artist_image['url']
    elif isinstance(artist_image, list) and len(artist_image) > 0:
        artist_info['image_url'] = artist_image[0]['url']
    else:
        artist_info['image_url'] = None

    # followers must be an integer, otherwise we'll insert a null
    try:
        artist_followers = int(artist['followers']['total'])
    except:
        artist_followers = None
    artist_info['followers'] = artist_followers

    # popularity must be an integer, otherwise we'll insert a null
    try:
        artist_popularity = int(artist['popularity'])
    except:
        artist_popularity = None
    artist_info['popularity'] = artist_popularity

    # artist_uri must be a string, otherwise we'll insert a null
    artist_uri = artist['uri']
    if isinstance(artist_uri, str) and len(artist_uri) > 0:
        artist_info['artist_uri'] = artist_uri
    else:
        artist_info['artist_uri'] = None

    return artist_info

def make_artist_table(artist_names: list) -> pd.DataFrame:
    artist_dict = {}

    for name in artist_names:
        artist_info = get_artist_info(name)
        artist_dict[artist_info['artist_id']] = artist_info

    artist_table = pd.DataFrame.from_dict(artist_dict, orient='index')

    return artist_table

def get_artist_ids(artist_table: pd.DataFrame) -> list:

    artist_ids = artist_table['artist_id'].tolist()

    return artist_ids

def get_album_info(artist_id: str) -> dict:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = spotify.artist_albums(artist_id=artist_id, album_type='album', country='US', limit=50)
    albums = results['items']

    # if the search returns no results, items will be an empty list
    if len(albums) == 0:
        # raise Exception('No albums returned for this artist')
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

    return complete_albums_dict

def make_album_table(artist_ids: list) -> pd.DataFrame:
    album_dict = {}

    for id in artist_ids:
        album_info = get_album_info(id)
        for album_id in album_info.keys():
            album_dict[album_id] = album_info[album_id]

    album_table = pd.DataFrame.from_dict(album_dict, orient='index')

    return album_table

def get_album_ids(album_table: pd.DataFrame) -> list:

    album_ids = album_table['album_id'].tolist()

    return album_ids

def ingest(artist_list: list):

    # Here's the pipeline!
    # First we create a pd.DataFrame of all the artist info
    artist = make_artist_table(artist_list)

    # In order to retrieve album info, we need artist ids in a list
    artist_ids = get_artist_ids(artist)

    # Next we create a pd.DataFrame of all the album info (multiple albums per artist)
    album = make_album_table(artist_ids)

    # In order to retrieve track info, we need album ids in a list
    album_ids = get_album_ids(album)

    # Next we create a pd.DataFrame of all the track info (multiple tracks per album)
    

if __name__ == '__main__':
    artist_list = ['Ben Folds', 'Earth, wind, and fire', 'hilary hahn']
    ingest(artist_list)
