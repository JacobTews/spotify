import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

def get_track_features_info(track_id: str) -> dict:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    track_features = spotify.audio_features(tracks=[track_id])[0]
    # track_features = results['items']

    # if the search returns no results, items will be an empty list
    if len(track_features) == 0:
        # raise Exception('No tracks returned for this album')
        return None

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
    track_features_dict = {}

    for id in track_ids:
        track_features_info = get_track_features_info(id)
        track_features_dict[id] = track_features_info

    track_features_table = pd.DataFrame.from_dict(track_features_dict, orient='index')

    return track_features_table

if __name__ == '__main__':

    # test_track_id = '3LptKjV3CVclsozwQ4pqBz'
    #
    # print(make_track_features_table([test_track_id]))
    #
    # print('Run completed')
    pass