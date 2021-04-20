from pony import orm
from pony.orm.serialization import to_dict, to_json
from utils import artist_mapper, get_id


db = orm.Database()
db.bind(provider='postgres', user='db_admin', password='pwd0123456789', host='localhost', database='db_postgre')

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

if __name__ == '__main__':
    
    # add_artist(id="3232iii3", name="Test4", age=10, albums="aaa", tracks="aaa", self_="aaa")
    # print_artist_names()
    # delete_artist("124")
    print_artist_names()