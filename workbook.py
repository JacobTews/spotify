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

def get_artist_info(artist_name: str) -> dict:

    needed_items = [
        'id',
        'name',
        'genres',
        'external_urls',
        'images',
        'followers',
        'popularity',
        'uri'
    ]

    # create a spotipy object using the credentials stored as environment variables
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    # search for artist by name
    results = spotify.search(q=f'artist: {artist_name}', type='artist')
    items = results['artists']['items']
    artist = items[0]

    # create dictionary of artist details
    artist_info = {'type': 'artist'}

    for i in needed_items:
        if i == 'external_urls':
            artist_info['external_url'] = artist[i]['spotify']
        elif i == 'images':
            if isinstance(artist[i], dict):
                artist_info['image_url'] = artist[i]['url']
            else:
                artist_info['image_url'] = artist[i][0]['url']
        elif i == 'followers':
            artist_info[i] = artist[i]['total']
        elif isinstance(artist[i], list) and len(artist[i]) > 0:
            artist_info[i] = artist[i][0]
        else:
            artist_info[i] = artist[i]

    return artist_info

def get_album_info():
    pass

def get_track_info():
    pass

def get_track_features():
    pass

def make_artist_table(artist_names: list) -> pd.DataFrame:
    artist_dict = {}

    for name in artist_names:
         artist_dict[name] = get_artist_info(name)

    artist_table = pd.DataFrame.from_dict(artist_dict)

    return artist_table

if __name__ == '__main__':
    # artist_info = get_artist_info('Ben Folds')
    # for k, v in artist_info.items():
    #     print(f'key: {k}\nvalue: {v}\n')

    test_table = make_artist_table(['Ben Folds', 'Chicago', 'Elliott Miles McKinley'])

    print(test_table)
    print('Run completed')