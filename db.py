import sqlite3
import json

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


def get_apart_by_floors(floors):
    request_params = (str(floors),)
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT apt_count FROM houses
                    WHERE floors = ?
                    AND apt_count <> 0
                    ORDER BY apt_count""", request_params)
    request_results = cur.fetchall()
    result = []
    for element in request_results:
        result.append(element[0])
    return result


def update_apart(update_value, floors):
    request_params = (str(update_value), str(floors))
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()
    cur.execute("""UPDATE houses SET apt_count = ?
                        WHERE floors = ?
                        AND apt_count = 0""", request_params)
    conn.commit()


def create_table_apt_count():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS apt_count(
       id INTEGER PRIMARY KEY,
       apt_count INTEGER);
    """)
    conn.commit()


def fill_apt_count():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM houses""")

    request_results = cur.fetchall()

    for element in request_results:
        request_params = (str(element[0]), str(element[5]))
        cur.execute("INSERT INTO apt_count VALUES(?, ?);", request_params)

    conn.commit()


def create_table_weights():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS weights(
       id INTEGER PRIMARY KEY,
       weight INTEGER);
    """)
    conn.commit()


def weight_data():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()
    weights = [
        {
            'value': 1,
            'l': 1,
            'h': 11
        },
        {
            'value': 2,
            'l': 12,
            'h': 14
        },
        {
            'value': 3,
            'l': 15,
            'h': 29
        },
        {
            'value': 4,
            'l': 30,
            'h': 45
        },
        {
            'value': 5,
            'l': 46,
            'h': 60
        },
        {
            'value': 6,
            'l': 61,
            'h': 80
        },
        {
            'value': 7,
            'l': 81,
            'h': 102
        },
        {
            'value': 8,
            'l': 103,
            'h': 166
        },
        {
            'value': 9,
            'l': 167,
            'h': 261
        },
        {
            'value': 10,
            'l': 262,
            'h': 10000
        }
    ]
    for weight in weights:
        request_params = (str(weight['l']), str(weight['h']))

        cur.execute("""SELECT id FROM houses
                    WHERE apt_count >= ?
                    AND apt_count <= ?""", request_params)

        request_results = cur.fetchall()

        for element in request_results:
            request_params_2 = (str(element[0]), str(weight['value']))
            cur.execute("INSERT INTO weights VALUES(?, ?);", request_params_2)

    conn.commit()


def save_data():
    conn = sqlite3.connect('mingkh_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM houses""")

    request_results = cur.fetchall()
    export_list = []

    for element in request_results:
        export_list.append({
                    'id': str(element[0]),
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [element[9], element[8]]
                    },
                    'properties': {
                        'weight': element[5]
                    }
        })

    res = json.dumps(export_list)
    a=1
