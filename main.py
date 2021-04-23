from flask import Flask, g, make_response
from flask_restful import Resource, Api, reqparse
from pony import orm
from db import get_artists, delete_artist, add_artist, get_artist, get_albums, add_album, get_artist_albums, get_album, delete_album, add_track, get_tracks, delete_track
from os import environ
import json


def output_json(data, code, headers=None):
    data = json.dumps(data, ensure_ascii=False).encode('utf8')
    resp = make_response(data.decode(), code)
    resp.headers.extend(headers or {})
    return resp

class Api(Api):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }

app = Flask(__name__)
api = Api(app)

artist_parser = reqparse.RequestParser()
artist_parser.add_argument('name')
artist_parser.add_argument('age')

album_parser = reqparse.RequestParser()
album_parser.add_argument('name')
album_parser.add_argument('genre')

track_parser = reqparse.RequestParser()
track_parser.add_argument('name')
track_parser.add_argument('duration')

class Artists(Resource):
    def get(self):
        try:
            artists = get_artists()
            return artists
        except Exception as err:
            print(err)
            return []

    def post(self):
        args = artist_parser.parse_args()
        try:
            if not args.name or not args.age:
                return {}, 400
            artist, err = add_artist(args.name, args.age)
            if err:
                return artist, 409
            return artist, 201
        # except orm.core.TransactionIntegrityError as err:
        #     print(err)
        #     return {}, 409
        except Exception as err:
            print(type(err))
            return {}, 400
        # print(args)


class ArtistId(Resource):
    def get(self, artist_id):
        # print(artist_id)
        try:
            return get_artist(artist_id)
        except Exception as err:
            print(err)
            return {}, 404
    
    def delete(self, artist_id):
        try:
            delete_artist(artist_id)
            return {}, 204
        except Exception as err:
            print(err)
            return {}, 404


class Albums(Resource):
    def get(self):
        try:
            albums = get_albums()
            return albums
        except Exception as err:
            print(err)
            return []

class ArtistAlbums(Resource):
    def get(self, artist_id):
        try:
            return get_artist_albums(artist_id)
        except Exception as err:
            print(err)
            return {}, 404

    def post(self, artist_id):
        args = album_parser.parse_args()
        print(args)
        try:
            if not args.name or not args.genre:
                return {}, 400
            print("ok")
            album, err = add_album(artist_id, args.name, args.genre)
            print("ok", album, err)
            if err == 1:
                return {}, 422
            elif err == 2:
                return album, 409
            return album, 201
        except Exception as err:
            print(err)
            return {}, 400

class AlbumId(Resource):
    def get(self, album_id):
        # print(artist_id)
        try:
            return get_album(album_id)
        except Exception as err:
            print(err)
            return {}, 404
    
    def delete(self, album_id):
        try:
            delete_album(album_id)
            return {}, 204
        except Exception as err:
            print(err)
            return {}, 404

class AlbumTracks(Resource):
    def get(self, album_id):
        try:
            return get_tracks(album_id=album_id)
        except Exception as err:
            print(err)
            return {}, 404

    def post(self, album_id):
        args = track_parser.parse_args()
        print(args)
        try:
            if not args.name or not args.duration:
                return {}, 400
            print("ok")
            track, err = add_track(album_id, args.name, args.duration)
            print("ok", track, err)
            if err == 1:
                return {}, 422
            elif err == 2:
                return track, 409
            return track, 201
        except Exception as err:
            print(err)
            return {}, 400

class Tracks(Resource):
    def get(self):
        try:
            tracks = get_tracks()
            return tracks
        except Exception as err:
            print(err)
            return []

class TrackId(Resource):
    def get(self, track_id):
        # print(artist_id)
        try:
            return get_tracks(track_id=track_id)
        except Exception as err:
            print(err)
            return {}, 404
    
    def delete(self, track_id):
        try:
            delete_track(track_id)
            return {}, 204
        except Exception as err:
            print(err)
            return {}, 404

class ArtistTracks(Resource):
    def get(self, artist_id):
        try:
            return get_tracks(artist_id=artist_id)
        except Exception as err:
            print(err)
            return {}, 404
    

api.add_resource(Artists, '/artists')
api.add_resource(ArtistId, '/artists/<string:artist_id>')
api.add_resource(Albums, '/albums')
api.add_resource(ArtistAlbums, '/artists/<string:artist_id>/albums')
api.add_resource(AlbumId, '/albums/<string:album_id>')
api.add_resource(AlbumTracks, '/albums/<string:album_id>/tracks')
api.add_resource(Tracks, '/tracks')
api.add_resource(TrackId, '/tracks/<string:track_id>')
api.add_resource(ArtistTracks, '/artists/<string:artist_id>/tracks')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
