from flask import Flask, g, make_response
from flask_restful import Resource, Api, reqparse
from pony import orm
from db import get_artists, delete_artist, add_artist, get_artist
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


api.add_resource(Artists, '/artists')
api.add_resource(ArtistId, '/artists/<string:artist_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
