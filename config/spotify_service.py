# Configuración de las credenciales
client_id = '7bfdd56301ca4eceadbe8ec3cd44b215'
client_secret = 'c8ad40e17b5343bf829be31054385383'

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))