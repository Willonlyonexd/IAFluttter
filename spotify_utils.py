import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Configuración de credenciales
client_id = '7bfdd56301ca4eceadbe8ec3cd44b215'
client_secret = 'c8ad40e17b5343bf829be31054385383'

# Inicialización del cliente de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_tracks_by_genre(genre, limit=50):
    """
    Obtiene una lista de IDs de pistas basadas en un género específico.

    Args:
        genre (str): El género musical.
        limit (int): El número máximo de pistas a recuperar.

    Returns:
        list: Una lista de diccionarios con datos básicos de las pistas.
    """
    results = sp.search(q=f'genre:{genre}', type='track', limit=limit)
    tracks = results['tracks']['items']

    # Filtrar canciones para que no se repitan artistas
    unique_artists = set()
    unique_tracks = []
    for track in tracks:
        primary_artist = track['artists'][0]['id']
        if primary_artist not in unique_artists:
            unique_artists.add(primary_artist)
            unique_tracks.append(track)
        if len(unique_tracks) == 5:  # Limitar a 5 canciones únicas
            break

    return unique_tracks

def generate_song_json(tracks):
    """
    Genera un JSON con detalles de las canciones, excluyendo el campo 'available_markets'.

    Args:
        tracks (list): Lista de pistas recuperadas.

    Returns:
        list: Una lista de diccionarios con los datos de las canciones.
    """
    songs_data = []
    for track in tracks:
        song_data = {
            'id': track['id'],
            'name': track['name'],
            'artists': [
                {
                    'name': artist['name'],
                    'id': artist['id'],
                    'uri': artist['uri'],
                    'external_urls': artist['external_urls']
                } for artist in track['artists']
            ],
            'album': {
                'id': track['album']['id'],
                'name': track['album']['name'],
                'images': track['album']['images'],
                'release_date': track['album']['release_date'],
                'release_date_precision': track['album']['release_date_precision'],
                'total_tracks': track['album']['total_tracks'],
                'uri': track['album']['uri'],
                'external_urls': track['album']['external_urls']
            },
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'external_ids': track.get('external_ids', {}),
            'popularity': track['popularity'],
            'preview_url': track['preview_url'],
            'uri': track['uri']
        }
        songs_data.append(song_data)
    return songs_data

if __name__ == '__main__':
    genre = 'edm'  # Cambia este género según lo necesites

    # Obtiene los datos de las pistas
    tracks = get_tracks_by_genre(genre)

    # Genera el JSON de las canciones
    songs_json = generate_song_json(tracks)

    # Imprime el JSON resultante
    import json
    print(json.dumps(songs_json, indent=4))
