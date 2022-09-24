"""
The purpose of this script is to retrieve the needed information from the Spotify API.

"""

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

def make_artist_table(artist_names: list):
    artist_dict = {}

    for name in artist_names:
         artist_dict[name] = get_artist_info(name)[0]

    artist_table = pd.DataFrame.from_dict(artist_dict, orient='index')

    return artist_table

def ingest(artist_list: list):
    artist = make_artist_table(artist_list)


if __name__ == '__main__':
    artist_list = []
    ingest(artist_list)