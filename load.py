import os
import pandas as pd
import sqlite3
import sqlalchemy
import time

def create_connection():
    try:
        conn = sqlite3.connect('database/music_data.sqlite')
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def make_table_dict_from_df(directory_path) -> dict:
    filenames = []
    for filename in os.listdir(directory_path):
        f = os.path.join(directory_path, filename)
        if os.path.isfile(f):
            filenames.append(f)

    table_dict = {}
    for name in filenames:
        feather_stripped_name = name.split('.')[0]
        table_name = feather_stripped_name[21:]
        table_dict[table_name] = pd.read_feather(name)

    return table_dict

def create_and_load_tables(tables: dict):
    engine = sqlalchemy.create_engine('sqlite:///database/music_data.sqlite')
    conn = create_connection()
    for table in tables.keys():
        tables[table].to_sql(table, engine, if_exists='replace', index=False)
    conn.close()

def load(directory_path: str):

    # Here's the pipeline!
    t0 = time.time()

    # First we take all the feather files in the cleaned_data directory and store in a dict of pd.DataFrames
    table_dict = make_table_dict_from_df(directory_path)

    # Then those pd.DataFrames can be loaded into the SQLite database using the SQLAlchemy engine
    # and the pandas native SQL support
    create_and_load_tables(table_dict)

    print(f'Load completed successfully. Total load time: {round(time.time() - t0, 2)}s')


if __name__ == '__main__':

    load('cleaned_data')