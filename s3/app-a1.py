

# Standard library modules
import csv
import logging
import os
import sys
import uuid

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request

# Local modules
import unique_code

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/playlist.csv'

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}


def load_db():
    global database
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for playlist, genre, id in rdr:
            database[id] = (playlist,genre)


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/', methods=['GET'])
def list_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Playlist': value[0], 'Genre': value[1], 'playlist_id': id}
             for id, value in database.items()]
    }
    return response


@bp.route('/<playlist_id>', methods=['GET'])
def get_song(playlist_id):
    global database
    if playlist_id in database:
        value = database[playlist_id]
        response = {
            "Count": 1,
            "Items":
                [{'Playlist': value[0],
                  'Genre': value[1],
                  'playlist_id': playlist_id}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/', methods=['POST'])
def create_song():
    global database
    try:
        content = request.get_json()
        Playlist = content['Playlist']
        Genre = content['Genre']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    playlist_id = str(uuid.uuid4())
    database[playist_id] = (Playlist, Genre)
    response = {
        "playlist_id": playlist_id
    }
    return response


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_song(playlist_id):
    global database
    if playlist_id in database:
        del database[playlist_id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}


@bp.route('/test', methods=['GET'])
def test():
    # This value is for user scp756-221
    if ('a1bee2439e8046eb5a00852c77492d6267458d81204436651e75a696f2736ce1' !=
            ucode):
        raise Exception("Test failed")
    return {}


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    load_db()
    app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
