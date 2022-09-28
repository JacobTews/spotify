import ingest
import transform
import load

def etl(artist_list: list):

    # Here's the pipeline!
    t0 = time.time()

    # extract
    ingest.ingest(artist_list)

    # transform
    transform.transform()

    # load
    load.load('cleaned_data')

    print(f'ETL completed successfully. Total time: {round(time.time() - t0, 2)}s')


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

    etl(artist_list)
