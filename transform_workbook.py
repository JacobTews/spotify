import pandas as pd
import random
import time

# **********
# ARTIST table cleaning

def clean_artist(artist_df: pd.DataFrame) -> (pd.DataFrame, (list, list)):

    # Since I know the genres, I'll impute the missing values manually
    performers = ['Erik Rohde', 'Korey Konkol', 'Jacob Tews', 'Clare Longendyke']
    composers = ['Christopher Walczak', 'Michael-Thomas Foumai', 'Elliott Miles McKinley']

    # This pulls the index of each row where the genre is None
    none_indexes = artist_df.index[artist_df['genre'].isna()].tolist()

    for i in none_indexes:
        if artist_df.loc[i, 'artist_name'] in performers:
            artist_df.loc[i, 'genre'] = 'classical performance'
        elif artist_df.loc[i, 'artist_name'] in composers:
            artist_df.loc[i, 'genre'] = '21st century classical'
        elif artist_df.loc[i, 'artist_name'] == 'Deborah Klemme':
            artist_df.loc[i, 'genre'] = 'christian music'
        elif artist_df.loc[i, 'artist_name'] == '7 Days A Cappella':
            artist_df.loc[i, 'genre'] = 'college a cappella'

    # For use in imputing instrumentalness values in the track_feature table, I'll need the artist ids by type
    instrumentals = ['Hilary Hahn', 'Jim Brickman', 'Chris Thile', 'Béla Fleck', 'Elliott Carter',
                     'Michael-Thomas Foumai', 'Augusta Read Thomas', 'Elliott Miles McKinley', 'Jacob Tews',
                     'Christopher Walczak', 'Korey Konkol', 'Clare Longendyke', 'Erik Rohde']
    vocals = ['Ben Folds', 'Earth, Wind & Fire', 'Chicago', 'Fernando Ortega', 'Jacob Collier', 'Deborah Klemme',
              '7 Days A Cappella']

    instrumental_ids = [artist_df.loc[artist_df['artist_name'] == artist_name, 'artist_id'].item() for artist_name
                        in instrumentals]
    vocal_ids = [artist_df.loc[artist_df['artist_name'] == artist_name, 'artist_id'].item() for artist_name in
                 vocals]

    return artist_df, (instrumental_ids, vocal_ids)

# **********
# ALBUM table cleaning

def clean_album(album_df: pd.DataFrame, artist_ids: (list, list)) -> (pd.DataFrame, list, (list, list)):

    # We will treat albums with more than 60 tracks as outliers which can be removed.
    outlier_df = album_df[album_df['total_tracks'] > 60]
    # In order to remove from the tracks table all the tracks from these outlier albums, we save the ids
    outlier_ids = outlier_df['album_id'].tolist()
    album_df.drop(outlier_df.index, inplace=True)

    # For use in imputing instrumentalness values in the track_feature table, I'll need the album ids
    # from the albums sorted by whether the artist is primarily instrumental or vocal
    instrumental_album_ids = []
    instrumental_ids = artist_ids[0]
    for album_list in [album_df.loc[album_df['artist_id'] == artist_id, 'album_id'].tolist() for artist_id in
                       instrumental_ids]:
        for id in album_list:
            instrumental_album_ids.append(id)
    vocal_album_ids = []
    vocal_ids = artist_ids[1]
    for album_list in [album_df.loc[album_df['artist_id'] == artist_id, 'album_id'].tolist() for artist_id in
                       vocal_ids]:
        for id in album_list:
            vocal_album_ids.append(id)

    # To save as a feather, we need to reset the pandas index
    album_df.reset_index(inplace=True)

    return album_df, outlier_ids, (instrumental_album_ids, vocal_album_ids)

# **********
# TRACK table cleaning

def clean_track(track_df: pd.DataFrame, deleted_albums: list, sorted_album_ids: (list, list))\
        -> (pd.DataFrame, list, (list, list)):

    # Tracks from albums which have been removed should also be removed.
    outlier_tracks = track_df[track_df['album_id'].isin(deleted_albums)]
    # Just like with the album table, we need to save the ids of the outlier tracks
    outlier_track_ids = outlier_tracks['track_id'].tolist()
    track_df.drop(outlier_tracks.index, inplace=True)

    # For use in imputing instrumentalness values in the track_feature table, I'll need the track ids
    # sorted by whether the artist is primarily instrumental or vocal
    instrumental_track_ids = []
    instrumental_album_ids = sorted_album_ids[0]
    for album_list in [track_df.loc[track_df['album_id'] == album_id, 'track_id'].tolist() for album_id in
                       instrumental_album_ids]:
        for id in album_list:
            instrumental_track_ids.append(id)
    vocal_track_ids = []
    vocal_album_ids = sorted_album_ids[1]
    for album_list in [track_df.loc[track_df['album_id'] == album_id, 'track_id'].tolist() for album_id in
                       vocal_album_ids]:
        for id in album_list:
            vocal_track_ids.append(id)

    # To save as a feather, we reset the pandas index
    track_df.reset_index(inplace=True)

    return track_df, outlier_track_ids, (instrumental_track_ids, vocal_track_ids)


# **********
# TRACK_FEATURES table cleaning

def clean_track_features(track_features_df: pd.DataFrame, outlier_track_ids: list, track_ids: (list, list))\
        -> pd.DataFrame:

    # Tracks from which have been removed in the track table cleaning should also be removed.
    drop_indexes = track_features_df[track_features_df['track_id'].isin(outlier_track_ids)].index
    track_features_df.drop(drop_indexes, inplace=True)

    # Now we impute a random instrumentalness value for the nulls, based on the sorting done earlier in the pipeline
    instrumental_track_ids = track_ids[0]
    vocal_track_ids = track_ids[1]
    none_indexes = track_features_df.index[track_features_df['instrumentalness'].isna()].tolist()
    for index in none_indexes:
        if track_features_df.loc[index, 'track_id'] in instrumental_track_ids:
            track_features_df.loc[index, 'instrumentalness'] = random.uniform(0.7, 0.9959)
        elif track_features_df.loc[index, 'track_id'] in vocal_track_ids:
            track_features_df.loc[index, 'instrumentalness'] = random.uniform(0.0001, 0.3)

    # To save as a feather, we reset the pandas index
    track_features_df.reset_index(inplace=True)

    return track_features_df

# **********
# Transform pipeline

def transform():

    # Here's the pipeline!
    t0 = time.time()

    # First, retrieve the four dataframes from the raw_data directory
    artist_df = pd.read_feather('raw_data/artist.feather')
    album_df = pd.read_feather('raw_data/album.feather')
    track_df = pd.read_feather('raw_data/track.feather')
    track_features_df = pd.read_feather('raw_data/track_feature.feather')

    # Next clean each dataframe
    cleaned_artist_df, artist_ids = clean_artist(artist_df)
    cleaned_album_df, deleted_albums, album_ids = clean_album(album_df, artist_ids)
    cleaned_track_df, deleted_tracks, track_ids = clean_track(track_df, deleted_albums, album_ids)
    cleaned_track_features_df = clean_track_features(track_features_df, deleted_tracks, track_ids)

    # Finally, store the cleaned dataframes as feathers in the clean_data directory
    cleaned_artist_df.to_feather('cleaned_data/cleaned_artist.feather')
    cleaned_album_df.to_feather('cleaned_data/cleaned_album.feather')
    cleaned_track_df.to_feather('cleaned_data/cleaned_track.feather')
    cleaned_track_features_df.to_feather('cleaned_data/cleaned_track_features.feather')

    print(f'Transform completed successfully. Total transform time: {round(time.time() - t0, 2)}s')

if __name__ == '__main__':

    transform()