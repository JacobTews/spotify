import pandas as pd
import time

# **********
# ARTIST table cleaning

def clean_artist(artist_df: pd.DataFrame) -> pd.DataFrame:

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

    return artist_df

# **********
# ALBUM table cleaning

def clean_album(album_df: pd.DataFrame) -> (pd.DataFrame, list):

    # We will treat albums with more than 60 tracks as outliers which can be removed.
    outlier_df = album_df[album_df['total_tracks'] > 60]
    # In order to remove from the tracks table all the tracks from these outlier albums, we save the ids
    outlier_ids = outlier_df['album_id'].tolist()
    album_df.drop(outlier_df.index, inplace=True)

    # To save as a feather, we need to reset the pandas index
    album_df.reset_index(inplace=True)

    return album_df, outlier_ids

# **********
# TRACK table cleaning

def clean_track(track_df: pd.DataFrame, deleted_albums: list) -> pd.DataFrame:

    pass

# **********
# TRACK_FEATURES table cleaning

def clean_track_features(track_features_df: pd.DataFrame) -> pd.DataFrame:

    pass

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
    cleaned_artist_df = clean_artist(artist_df)
    cleaned_album_df, deleted_albums = clean_album(album_df)
    # cleaned_track_df, deleted_tracks = clean_track(track_df, deleted_albums)
    # cleaned_track_features_df = clean_track_features(track_features_df, deleted_tracks)

    # Finally, store the cleaned dataframes as feathers in the clean_data directory
    cleaned_artist_df.to_feather('cleaned_data/cleaned_artist.feather')
    cleaned_album_df.to_feather('cleaned_data/cleaned_album.feather')
    # cleaned_track_df.to_feather('cleaned_data/cleaned_track.feather')
    # cleaned_track_features_df.to_feather('cleaned_data/cleaned_track_features.feather')

    print(f'Transform completed successfully. Total transform time: {round(time.time() - t0, 2)}s')

if __name__ == '__main__':

    transform()