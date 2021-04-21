from pony import orm
from pony.orm.serialization import to_dict, to_json
from utils import artist_mapper, album_mapper, get_id
from os import environ
import re



DB_URL = environ["DATABASE_URL"][11:]
DB_URL.index(":")
user = DB_URL[:DB_URL.index(":")]
DB_URL = DB_URL[DB_URL.index(":")+1:]
password = DB_URL[:DB_URL.index("@")]
DB_URL = DB_URL[DB_URL.index("@")+1:]
print(DB_URL)
host = DB_URL[:DB_URL.index(":")]
DB_URL = DB_URL[DB_URL.index(":")+1:]
port = DB_URL[:DB_URL.index("/")]
database = DB_URL[DB_URL.index("/")+1:]
db = orm.Database()
db.bind(provider='postgres', user=user, password=password, host=host, port=port, database=database)

class Artist(db.Entity):
    id = orm.PrimaryKey(str)
    name = orm.Required(str)
    age = orm.Required(int)
    albums = orm.Set("Album")
    tracks = orm.Set("Track")

class Album(db.Entity):
    id = orm.PrimaryKey(str)
    name = orm.Required(str)
    genre = orm.Required(str)
    artist = orm.Required(Artist)
    tracks = orm.Set("Track")

class Track(db.Entity):
    id = orm.PrimaryKey(str)
    name = orm.Required(str)
    duration = orm.Required(float)
    t_played = orm.Required(int)
    artist = orm.Required(Artist)
    album = orm.Required(Album)


db.generate_mapping(create_tables=True)

@orm.db_session
def add_artist(name, age):
    try:
        if Artist.exists(id=get_id(name)):
            return artist_mapper(Artist[get_id(name)]), 1
        artist = Artist(id=get_id(name) ,name=name, age=age)
        return artist_mapper(artist), 0
    except Exception as err:
        return Artist[get_id(name)], err

@orm.db_session
def get_artists():
    artists = orm.select(p for p in Artist)[:]
    return [artist_mapper(artist) for artist in artists]

@orm.db_session
def get_artist(id):
    return artist_mapper(Artist[id])

@orm.db_session
def delete_artist(id):
    Artist[id].delete()

@orm.db_session
def get_albums():
    albums = orm.select(p for p in Album)[:]
    return [album_mapper(album) for album in albums]

@orm.db_session
def get_artist_albums(artist_id):
    return [album_mapper(album) for album in Artist[artist_id].albums]
    # return [album_mapper(album) for album in albums]

@orm.db_session
def add_album(artist_id, name, genre):
    print(artist_id, name, genre)
    try:
        if not Artist.exists(id=artist_id):
            return {}, 1
        else:
            artist = Artist[artist_id]
        if Album.exists(id=get_id(name)):
            return album_mapper(Album[get_id(name)]), 2
        album = Album(id=get_id(name) ,name=name, genre=genre, artist=artist)
        return album_mapper(album), 0
    except Exception as err:
        return {}, err


if __name__ == '__main__':
    
    # add_artist(id="3232iii3", name="Test4", age=10, albums="aaa", tracks="aaa", self_="aaa")
    # print_artist_names()
    # delete_artist("124")
    print_artist_names()