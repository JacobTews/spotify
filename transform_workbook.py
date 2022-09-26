import pandas as pd

# ARTIST table cleaning

def clean_artist(artist_df: pd.DataFrame) -> pd.DataFrame:


def transform():

    # First, retrieve the four dataframes from the raw_data directory
    artist_df = pd.read_feather('raw_data/artist.feather')
    album_df = pd.read_feather('raw_data/album.feather')
    track_df = pd.read_feather('raw_data/track.feather')
    track_features_df = pd.read_feather('raw_data/track_feature.feather')

    # Next clean each dataframe
    cleaned_artist_df = clean_artist(artist_df)
    cleaned_album_df = clean_album(album_df)
    cleaned_track_df = clean_track(track_df)
    cleaned_track_features_df = clean_track_features(track_features_df)

    # Finally, store the cleaned dataframes as feathers in the clean_data directory


if __name__ == '__main__':
    print(artist_df.head)