#Crea dataframe de 50 canciones del mismo genero, de acuerdo a las variables genera 5 canciones del genero (clave)
np.random.seed()
tf.random.set_seed(np.random.randint(1, 1000))

def get_tracks_by_genre(genre, limit=50):
    results = sp.search(q=f'genre:{genre}', type='track', limit=limit)
    tracks = results['tracks']['items']
    track_ids = [track['id'] for track in tracks]
    return track_ids, tracks

def get_track_features(track_id, genre):
    features = sp.audio_features([track_id])[0]
    track = sp.track(track_id)
    return {
        'id': track_id,  # Añadir el ID de la pista
        'genre': genre,  # Incluir el género que estás buscando
        'danceability': features['danceability'],
        'energy': features['energy'],
        'key': features['key'],
        'loudness': features['loudness'],
        'mode': features['mode'],
        'speechiness': features['speechiness'],
        'acousticness': features['acousticness'],
        'instrumentalness': features['instrumentalness'],
        'liveness': features['liveness'],
        'valence': features['valence'],
        'tempo': features['tempo']
    }

def get_artist_name(track_id):
    track_info = sp.track(track_id)
    artist_name = track_info['artists'][0]['name']
    return artist_name

# Obtener tracks y sus características
genre = 'edm'
track_ids, tracks = get_tracks_by_genre(genre, limit=50)
track_features = [get_track_features(track_id, genre) for track_id in track_ids]

# Convertir a DataFrame
df_tracks = pd.DataFrame(track_features)
print("DataFrame de características de las pistas:")
print(df_tracks.head())

# Normalizar los datos (excluyendo la columna 'id' y 'genre')
scaler = StandardScaler()
df_tracks_scaled = scaler.fit_transform(df_tracks.drop(columns=['id', 'genre']))

# Convertir a DataFrame nuevamente
df_tracks_scaled = pd.DataFrame(df_tracks_scaled, columns=df_tracks.columns[2:])  # Excluyendo 'id' y 'genre'