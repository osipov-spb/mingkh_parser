import sqlite3

def create_table():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS houses(
       id INTEGER PRIMARY KEY,
       address TEXT,
       construction_year INTEGER,
       floors TEXT,
       house_type TEXT,
       apt_count INTEGER,
       emergency INTEGER,
       url TEXT,
       lng REAL,
       lat REAL);
    """)
    conn.commit()


def insert_data(house_data):
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()

    house_tuple = (str(house_data['id']),
                   str(house_data['address']),
                   str(house_data['construction_year']),
                   str(house_data['floors']),
                   str(house_data['house_type']),
                   str(house_data['apt_count']),
                   str(house_data['emergency']),
                   str(house_data['url']),
                   str(house_data['lng']),
                   str(house_data['lat']))
    cur.execute("INSERT INTO houses VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", house_tuple)
    conn.commit()


