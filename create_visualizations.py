import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# import seaborn as sns


def create_followers_viz():
    artist_df = pd.read_feather('cleaned_data/cleaned_artist.feather')

def create_danceability_viz():
    fig, ax = plt.subplots(figsize=(17, 17))

    ax.scatter(x=df['duration_ms'] / 1000.0 / 60,
               y=df['danceability'] * 100,
               alpha=0.2,
               c='mediumblue'
               )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.tick_params(color='gray', labelcolor='gray')
    # ax.set_ylim(-2, 79)

    ax.set_title('Longer tracks are only slightly less "danceable"',
                 fontdict={
                     'weight': 'bold',
                     'size': 28,
                     'color': 'mediumblue'
                 },
                 loc='left')

    ax.set_xlabel('Track length (min)',
                  fontdict={
                      'size': 12,
                      'color': 'gray'
                  }
                  )

    ax.set_ylabel('Track danceability score (0.0-100.0)',
                  fontdict={
                      'size': 12,
                      'color': 'gray'
                  }
                  )

    dancetangle = matplotlib.patches.Rectangle((11.5, 61), 20.5, 13, linewidth=1, linestyle='--', edgecolor='gray',
                                               facecolor='none')
    ax.add_patch(dancetangle)

    ax.axhline(y=df['danceability'].mean() * 100, color='lightgray', linestyle='--')
    ax.annotate('Average danceability: 42.9',
                xy=(30, df['danceability'].mean() * 100),
                xytext=(25, 37),
                ha='left',
                color='gray',
                arrowprops={
                    'arrowstyle': '->',
                    'color': 'lightgray'
                }
                )

    ax.axvline(x=df['duration_ms'].mean() / 1000.0 / 60, color='lightgray', linestyle='--')
    ax.annotate('Average track length: 4\'27"',
                xy=(df['duration_ms'].mean() / 1000.0 / 60, 3),
                xytext=(0, -2),
                ha='left',
                color='gray',
                arrowprops={
                    'arrowstyle': '->',
                    'color': 'lightgray'
                }
                )

    ax.annotate('A band of reasonably danceable outliers',
                xy=(22, 74),
                xytext=(21, 80),
                ha='center',
                color='gray',
                arrowprops={
                    'arrowstyle': '->',
                    'color': 'gray'
                }
                )

    plt.savefig('./viz/danceability_vs_average_length.pdf', format='pdf')

if __name__ == '__main__':
    create_followers_viz()