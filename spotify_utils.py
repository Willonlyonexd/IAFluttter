import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Configuración de credenciales
client_id = '1d29336f6a00486e9c0d5ac46ba67c78'
client_secret = 'cce20ea8fc764f23b8fb50ba648e9e68'

class SpotifyAuthManager:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiration_time = None
        self.sp = None
        self.refresh_token()

    def get_spotify_client(self):
        """ Devuelve el cliente de Spotify, renovando el token si es necesario """
        if not self.token or self.is_token_expired():
            self.refresh_token()  # Renueva el token si ha expirado
        return self.sp

    def refresh_token(self):
        """ Renueva el token de acceso y actualiza el tiempo de expiración """
        auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        # El token se obtiene mediante el cliente de autenticación
        self.token = self.sp.auth_manager.get_access_token()
        self.token_expiration_time = time.time() + self.token['expires_in']  # Establece el tiempo de expiración

    def is_token_expired(self):
        """ Verifica si el token ha expirado """
        return time.time() >= self.token_expiration_time


# Inicializar el manejador de autenticación
auth_manager = SpotifyAuthManager(client_id, client_secret)

def get_tracks_by_genre(genre, limit=50):
    """
    Obtiene una lista de IDs de pistas basadas en un género específico.
    """
    sp = auth_manager.get_spotify_client()  # Usar el cliente con token válido
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
        if len(unique_tracks) == 10:  # Limitar a 10 canciones únicas
            break

    return unique_tracks

def generate_song_json(tracks):
    """
    Genera un JSON con detalles de las canciones, excluyendo el campo 'available_markets'.
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
