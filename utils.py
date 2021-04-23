from base64 import b64encode
from os import environ


def artist_albums_url(id):
    return f"{environ['API_URL']}/artists/{id}/albums"

def artist_tracks_url(id):
    return f"{environ['API_URL']}/artists/{id}/tracks"

def artist_url(id):
    return f"{environ['API_URL']}/artists/{id}"

def album_url(id):
    return f"{environ['API_URL']}/albums/{id}"

def album_tracks_url(id):
    return f"{environ['API_URL']}/albums/{id}/tracks"

def track_url(id):
    return f"{environ['API_URL']}/tracks/{id}"


def artist_mapper(artist):
    return {
        "id": artist.id,
        "name": artist.name,
        "age": artist.age,
        "albums": artist_albums_url(artist.id),
        "tracks": artist_tracks_url(artist.id),
        "self": artist_url(artist.id)
    }

def album_mapper(album):
    # print(album.artist.id)
    return {
        "id": album.id,
        "artist_id": album.artist.id,
        "name": album.name,
        "genre": album.genre,
        "artist": artist_url(album.artist.id),
        "tracks": album_tracks_url(album.id),
        "self": album_url(album.id)
    }

def track_mapper(track):
    # print(track.artist.id)
    return {
        "id": track.id,
        "album_id": track.album.id,
        "name": track.name,
        "duration": track.duration,
        "artist": artist_url(track.album.artist.id),
        "album": album_url(track.album.id),
        "self": track_url(track.id)
    }

def get_id(name):
    return b64encode(name.encode()).decode('utf-8')[:22]