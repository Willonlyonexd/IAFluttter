from flask import Flask, jsonify, request
from flask_cors import CORS
from spotify_utils import get_tracks_by_genre, generate_song_json

app = Flask(__name__)
CORS(app)

@app.route('/api/genre/<genre>', methods=['GET'])
def get_songs_by_genre(genre):
    try:
        track_ids = get_tracks_by_genre(genre)
        songs_data = generate_song_json(track_ids)
        return jsonify(songs_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
