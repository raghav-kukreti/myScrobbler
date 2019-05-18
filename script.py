import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "eaaaf83e6d3647548dcb9a8c3ffa1149"
CLIENT_SECRET = "5d8a3852d8ec457ca10d6bfab06a6701"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='weezer', limit=20)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])