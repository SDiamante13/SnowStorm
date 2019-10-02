from flask import Response, current_app, make_response, Blueprint, jsonify, request, session
from .stream import StreamService

STREAM = Blueprint('stream', __name__, url_prefix='/stream')


@STREAM.route('/skip')
def skip():
    current_app.config.get('stream').skip()
    return make_response('', 200)


@STREAM.route('/stream.mp3')
def stream():
    return Response(current_app.config.get('stream').listen(),
                    mimetype='audio/mpeg')

@STREAM.route('/')
def get_playing():
    title = current_app.config.get('stream').title.value.decode()
    artist = current_app.config.get('stream').artist.value.decode()
    return make_response(jsonify({'title': title, 'artist': artist}), 200)

@STREAM.route('/queue', methods = ['GET', 'POST'])
def queueSongs():
   if request.method == 'GET':
       return make_response(jsonify({'title': current_app.config.get('stream').song_queue.get()}, 200))
   elif request.method == 'POST':
       title = request.args.get('title', '')
       artist = request.args.get('artist', '')
       current_app.config.get('stream').add_song_to_queue(title)
       queue = current_app.config.get('stream').song_queue
       return make_response(jsonify({'title': title, 'artist': artist}), 200)   
