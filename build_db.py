import sqlite3 as sql

conn = sql.connect('locations.db')
curs = conn.cursor()

curs.execute('CREATE TABLE restaurants (name text, \
                                        street_address text, \
                                        locality text, \
                                        region text, \
                                        zip_ text)')