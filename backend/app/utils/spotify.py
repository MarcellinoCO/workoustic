from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = Spotify(auth_manager=auth_manager)


async def get_track():
    return sp.track("http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6")
