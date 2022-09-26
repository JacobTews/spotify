import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

def get_track_info():
    pass

# needed_features = [
#     FEATURE_NAME ('API ACCESS NAME')
#     track_id ('id')
#     song_name ('name')
#     external_url ('external_urls'['spotify'])
#     duration_ms ('duration_ms')
#     explicit ('explicit')
#     disc_number ('disc_number')
#     type ('type')
#     song_uri ('uri')
#     album_id
# ]

def get_track_info(album_id: str) -> dict:
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
    track_dict = {}

    for id in album_ids:
        track_info = get_track_info(id)
        for track_id in track_info.keys():
            track_dict[track_id] = track_info[track_id]

    track_table = pd.DataFrame.from_dict(track_dict, orient='index')

    return track_table

if __name__ == '__main__':

    test_album_id = '2GLJLkriVbdfDi5W5e3LJM'

    print(make_track_table([test_album_id]))

    print('Run completed')