"""
The purpose of this script is to retrieve the needed information from the Spotify API.

"""

import time
from datetime import datetime
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# tasks:
# retrieve Spotify data for 20 artists (must be at least 1000 songs)
# includes
#   artist info
#   album info
#   track info
#   track features

# **********
# ARTIST functions

def get_artist_info(artist_name: str) -> dict:
    """
    Gets artist information from the Spotify API

    :param artist_name: artist/band name string to search
    :return: dictionary of all required features
    """

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
    artist_info = {}

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

    # external_url must be a single string, otherwise we'll insert a null
    # for artists with multiple urls, we will use the spotify one
    artist_url = artist['external_urls']['spotify']
    if len(artist_url) > 0:
        artist_info['external url'] = artist_url
    else:
        artist_info['external url'] = None

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

    # type must be the string 'artist'
    artist_info['type'] = 'artist'

    # artist_uri must be a string, otherwise we'll insert a null
    artist_uri = artist['uri']
    if isinstance(artist_uri, str) and len(artist_uri) > 0:
        artist_info['artist_uri'] = artist_uri
    else:
        artist_info['artist_uri'] = None

    return artist_info

def make_artist_table(artist_names: list) -> pd.DataFrame:
    """
    Takes the list of artist names supplied by the user and returns a pandas DataFrame of all artists

    :param artist_names: list of strings of artist/band names
    :return: pd.DataFrame of all artist info
    """

    artist_dict = {}

    for name in artist_names:
        artist_info = get_artist_info(name)
        artist_dict[artist_info['artist_id']] = artist_info

    artist_table = pd.DataFrame.from_dict(artist_dict, orient='index')

    # clean up the df
    artist_table.reset_index(inplace=True)
    artist_table.drop('index', axis=1, inplace=True)

    return artist_table

def get_artist_ids(artist_table: pd.DataFrame) -> list:
    """
    Retrieves the list of artist IDs for use elsewhere

    :param artist_table: pandas DataFrame of artist information
    :return: list of artist IDs as strings
    """

    artist_ids = artist_table['artist_id'].tolist()

    return artist_ids

# **********
# ALBUM functions

def get_album_info(artist_id: str) -> dict:
    """
    Gets album information from the Spotify API

    :param artist_id: ID (string) for artist as retrieved by get_artist_ids
    :return: dictionary of all available album information for artist
    """

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = spotify.artist_albums(artist_id=artist_id, country='US', limit=50)
    albums = results['items']

    # if the search returns no results, items will be an empty list
    if len(albums) == 0:
        raise Exception('No albums returned for this artist')

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
    """
    Takes the list of artist IDs and returns a pandas DataFrame of all albums

    :param artist_ids: list of strings of artist IDs
    :return: pd.DataFrame of all album info
    """

    album_dict = {}

    for id in artist_ids:
        album_info = get_album_info(id)
        for album_id in album_info.keys():
            album_dict[album_id] = album_info[album_id]

    album_table = pd.DataFrame.from_dict(album_dict, orient='index')

    # clean up the df
    album_table.reset_index(inplace=True)
    album_table.drop('index', axis=1, inplace=True)

    return album_table

def get_album_ids(album_table: pd.DataFrame) -> list:
    """
    Retrieves the list of album IDs for use elsewhere

    :param album_table: pandas DataFrame of album information
    :return: list of album IDs (strings)
    """

    album_ids = album_table['album_id'].tolist()

    return album_ids

# **********
# TRACK functions

def get_track_info(album_id: str) -> dict:
    """
    Gets track information from the Spotify API

    :param album_id: ID (string) for album as retrieved by get_album_ids
    :return: dictionary of all available track information for album
    """

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = spotify.album_tracks(album_id=album_id, limit=50)
    tracks = results['items']

    # if the search returns no results, items will be an empty list
    if len(tracks) == 0:
        # raise Exception('No tracks returned for this album')
        return None

    # create dictionary of track details
    complete_tracks_dict = {}

    for track in tracks:
        track_dict = {}
        # each item is validated before being inserted into the track_dict dictionary

        #     track_id ('id')
        if len(track['id']) > 0 and isinstance(track['id'], str):
            track_dict['track_id'] = track['id']
        else:
            raise Exception('Album does not have a unique identifier.')

        #     song_name ('name')
        if len(track['name']) > 0 and isinstance(track['name'], str):
            track_dict['song_name'] = track['name']
        else:
            track_dict['song_name'] = None

        #     external_url ('external_urls'['spotify'])
        if len(track['external_urls']['spotify']) > 0 and isinstance(track['external_urls']['spotify'], str):
            track_dict['external_url'] = track['external_urls']['spotify']
        else:
            track_dict['external_url'] = None

        #     duration_ms ('duration_ms')
        if isinstance(track['duration_ms'], int):
            track_dict['duration_ms'] = track['duration_ms']
        else:
            track_dict['duration_ms'] = None

        #     explicit ('explicit')
        if isinstance(track['explicit'], bool):
            track_dict['explicit'] = track['explicit']
        else:
            track_dict['explicit'] = None

        #     disc_number ('disc_number')
        if isinstance(track['disc_number'], int):
            track_dict['disc_number'] = track['disc_number']
        else:
            track_dict['disc_number'] = None

        #     type ('type')
        if len(track['type']) > 0 and isinstance(track['type'], str):
            track_dict['type'] = track['type']
        else:
            track_dict['type'] = None

        #     song_uri ('uri')
        if len(track['uri']) > 0 and isinstance(track['uri'], str):
            track_dict['song_uri'] = track['uri']
        else:
            track_dict['song_uri'] = None

        #     album_id
        track_dict['album_id'] = album_id

        complete_tracks_dict[track_dict['track_id']] = track_dict

    return complete_tracks_dict

def make_track_table(album_ids: list) -> pd.DataFrame:
    """
    Takes the list of album IDs and returns a pandas DataFrame of all tracks for all albums

    :param album_ids: list of strings of album IDs
    :return: pd.DataFrame of all track info
    """

    track_dict = {}

    for id in album_ids:
        track_info = get_track_info(id)
        for track_id in track_info.keys():
            track_dict[track_id] = track_info[track_id]

    track_table = pd.DataFrame.from_dict(track_dict, orient='index')

    # clean up the df
    track_table.reset_index(inplace=True)
    track_table.drop('index', axis=1, inplace=True)

    return track_table

def get_track_ids(track_table: pd.DataFrame) -> list:
    """
    Retrieves the list of track IDs for use elsewhere

    :param track_table: pandas DataFrame of track information
    :return: list of track IDs (strings)
    """

    track_ids = track_table['track_id'].tolist()

    return track_ids

# **********
# TRACK_FEATURE functions

def get_track_features_info(track_id: str) -> dict:
    """
    Gets track feature information from the Spotify API

    :param track_id: ID (string) for track as retrieved by get_track_ids
    :return: dictionary of all available track feature information for track
    """

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    track_features = spotify.audio_features(tracks=[track_id])[0]
    # track_features = results['items']

    # if the search returns no results, items will be an empty list
    if (track_features is None) or (len(track_features) == 0):
        # raise Exception('No tracks returned for this album')
        return {}

    track_features_dict = {}
    # each item is validated before being inserted into the track_features_dict dictionary

    #     track_id ('id')
    if len(track_features['id']) > 0 and isinstance(track_features['id'], str):
        track_features_dict['track_id'] = track_features['id']
    else:
        raise Exception('Album does not have a unique identifier.')

    #     danceability ('danceability')
    if isinstance(track_features['danceability'], float):
        track_features_dict['danceability'] = track_features['danceability']
    else:
        track_features_dict['danceability'] = None

    #     energy ('energy')
    if isinstance(track_features['energy'], float):
        track_features_dict['energy'] = track_features['energy']
    else:
        track_features_dict['energy'] = None

    #     instrumentalness ('instrumentalness')
    if isinstance(track_features['instrumentalness'], float):
        track_features_dict['instrumentalness'] = track_features['instrumentalness']
    else:
        track_features_dict['instrumentalness'] = None

    #     liveness ('liveness')
    if isinstance(track_features['liveness'], float):
        track_features_dict['liveness'] = track_features['liveness']
    else:
        track_features_dict['liveness'] = None

    #     loudness ('loudness')
    if isinstance(track_features['loudness'], float):
        track_features_dict['loudness'] = track_features['loudness']
    else:
        track_features_dict['loudness'] = None

    #     speechiness ('speechiness')
    if isinstance(track_features['speechiness'], float):
        track_features_dict['speechiness'] = track_features['speechiness']
    else:
        track_features_dict['speechiness'] = None

    #     tempo ('tempo')
    if isinstance(track_features['tempo'], float):
        track_features_dict['tempo'] = track_features['tempo']
    else:
        track_features_dict['tempo'] = None

    #     type ('type')
    if len(track_features['type']) > 0 and isinstance(track_features['type'], str):
        track_features_dict['type'] = track_features['type']
    else:
        track_features_dict['type'] = None

    #     valence ('valence')
    if isinstance(track_features['valence'], float):
        track_features_dict['valence'] = track_features['valence']
    else:
        track_features_dict['valence'] = None

    #     song_uri ('uri')
    if len(track_features['uri']) > 0 and isinstance(track_features['uri'], str):
        track_features_dict['song_uri'] = track_features['uri']
    else:
        track_features_dict['song_uri'] = None

    return track_features_dict

def make_track_features_table(track_ids: list) -> pd.DataFrame:
    """
    Takes the list of track IDs and returns a pandas DataFrame of all features for all tracks

    :param track_ids: list of strings of track IDs
    :return: pd.DataFrame of all track features
    """

    track_features_dict = {}

    for id in track_ids:
        track_features_info = get_track_features_info(id)
        track_features_dict[id] = track_features_info

    track_features_table = pd.DataFrame.from_dict(track_features_dict, orient='index')

    # clean up the df
    track_features_table.reset_index(inplace=True)
    track_features_table.drop('index', axis=1, inplace=True)

    return track_features_table

# **********
# INGEST pipeline

def ingest(artist_list: list):

    # Here's the pipeline!
    t0 = time.time()

    # First we create a pd.DataFrame of all the artist info
    t1 = time.time()
    artist = make_artist_table(artist_list)
    # Store the pd.DataFrame for transform access
    artist.to_feather('raw_data/artist.feather')
    print(f'Artist info for {artist.shape[0]} artists retrieved and stored successfully.\n'
          f'\tTotal time: {round(time.time() - t1, 2)}s')

    # In order to retrieve album info, we need artist ids from the artist table in a list
    artist_ids = get_artist_ids(artist)

    # Next we create a pd.DataFrame of all the album info (multiple albums per artist)
    t1 = time.time()
    album = make_album_table(artist_ids)
    album.to_feather('raw_data/album.feather')
    print(f'Album info for {album.shape[0]} albums retrieved and stored successfully.\n'
          f'\tTotal time: {round(time.time() - t1, 2)}s')

    # In order to retrieve track info, we need album ids from the album table in a list
    album_ids = get_album_ids(album)

    # Next we create a pd.DataFrame of all the track info (multiple tracks per album)
    t1 = time.time()
    track = make_track_table(album_ids)
    track.to_feather('raw_data/track.feather')
    print(f'Track info for {track.shape[0]} tracks retrieved and stored successfully.\n'
          f'\tTotal time: {round(time.time() - t1, 2)}s')

    # In order to retrieve track features, we need track ids from the track table in a list
    track_ids = get_track_ids(track)

    # Finally we create at pd.DataFrame of all the track features (multiple features per track)
    t1 = time.time()
    track_feature = make_track_features_table(track_ids)
    track_feature.to_feather('raw_data/track_feature.feather')
    print(f'Track feature info for {track_feature.shape[0]} tracks retrieved and stored successfully.\n'
          f'\tTotal time: {round(time.time() - t1, 2)}s')

    print(f'Ingest completed successfully. Total ingest time: {round(time.time() - t0, 2)}s')


if __name__ == '__main__':
    artist_list = [
        'hilary hahn',
        'ben folds',
        'jim brickman',
        'earth, wind, and fire',
        'chicago',
        'chris thile',
        'bela fleck',
        'fernando ortega',
        'elliott carter',
        'jacob collier',
        'deborah klemme',
        'michael thomas foumai',
        'augusta read thomas',
        'elliott miles mckinley',
        'jacob tews',
        'christopher walczak',
        'korey konkol',
        'clare longendyke',
        'erik rohde',
        '7 days a cappella'
    ]

    ingest(artist_list)
