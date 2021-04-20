from base64 import b64encode
from os import environ


def artist_albums_url(id):
    return f"{environ['API_URL']}/artists/{id}/albums"

def artist_tracks_url(id):
    return f"{environ['API_URL']}/artists/{id}/tracks"

def artist_url(id):
    return f"{environ['API_URL']}/artists/{id}"


def artist_mapper(artist):
    return {
        "id": artist.id,
        "name": artist.name,
        "age": artist.age,
        "albums": artist_albums_url(artist.id),
        "tracks": artist_tracks_url(artist.id),
        "self": artist_url(artist.id)
    }

def get_id(name):
    return b64encode(name.encode()).decode('utf-8')