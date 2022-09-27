import os
import pandas as pd
import sqlite3
import sqlalchemy

def create_connection():
    try:
        conn = sqlite3.connect('database/music_data.sqlite')
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def make_table_dict_from_df(directory_path):
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

if __name__ == '__main__':
    # create_and_load_tables(make_table_dict_from_df('cleaned_data'))

    conn = sqlite3.connect('database/music_data.sqlite')
    cur = conn.cursor()
    sql_statement = """
        SELECT *
        FROM artist
        LIMIT 5
        """
    cur.execute(sql_statement)
    results = cur.fetchall()
    for row in results:
        print(row)
    