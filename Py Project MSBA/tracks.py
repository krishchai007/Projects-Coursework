import db_base
import functions as func
import db_base as db
import xml.etree.ElementTree as ET

class Tracks(db.DBbase):

    def __init__(self):
        super().__init__("tracksdb.sqlite")

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Artist;
            DROP TABLE IF EXISTS Album;
            DROP TABLE IF EXISTS Track;

            CREATE TABLE Artist (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name    TEXT UNIQUE
            );

            CREATE TABLE Album (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                artist_id  INTEGER,
                title   TEXT UNIQUE
            );

            CREATE TABLE Track (
                id  INTEGER NOT NULL PRIMARY KEY
                    AUTOINCREMENT UNIQUE,
                title TEXT  UNIQUE,
                album_id  INTEGER,
                len INTEGER, rating INTEGER, count INTEGER
            ); """

        super().execute_script(sql)

    def load_database(self,fname):
        stuff = ET.parse(fname)
        all_item = stuff.findall("dict/dict/dict")
        print("Dict count:", len(all_item))

        for entry in all_item:
            if func.lookup(entry,"Name") is None: continue

            name = func.lookup(entry, "Name")
            artist = func.lookup(entry, "Artist")
            album = func.lookup(entry, "Album")
            count = func.lookup(entry, "Play Count")
            rating = func.lookup(entry, "Rating")
            length = func.lookup(entry, "Total Time")

            if name is None or artist is None or album is None:
                continue
            print(name,artist,album,count,rating,length)


            cur = super().get_cursor

            cur.execute('''INSERT OR IGNORE INTO Artist (name)
                VALUES ( ? )''', (artist,))

            cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
            artist_id = cur.fetchone()[0]

            cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
                VALUES ( ?, ? )''', (album, artist_id))

            cur.execute('SELECT id FROM Album WHERE title = ? ', (album,))
            album_id = cur.fetchone()[0]

            cur.execute('''INSERT OR REPLACE INTO Track
                (title, album_id, len, rating, count)
                VALUES ( ?, ?, ?, ?, ? )''',
                        (name, album_id, length, rating, count))

            super().get_connection.commit()

tracks = Tracks()
tracks.load_database("Library.xml")
tracks.close_db()
print("Completed")
