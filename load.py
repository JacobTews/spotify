import os
import pandas as pd
import sqlite3

def create_connection():
    try:
        con = sqlite3.connect('database/music_data.sqlite')
        return con
    except sqlite3.Error as e:
        print(e)

    return con

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

def load_tables(tables: dict):
    con = create_connection()
    for table in tables.keys():
        tables[table].to_sql(table, con, if_exists='replace')
        con.execute(f'DROP TABLE IF EXISTS {table}')
        con.execute(f"""
                    CREATE TABLE {table} AS
                    SELECT * FROM {tables[table]} 
                    """
                    )
    con.close

if __name__ == '__main__':
    load_tables(make_table_dict_from_df('cleaned_data'))

    # con = sqlite3.connect('database/music_data.sqlite')
    # cur = con.cursor()