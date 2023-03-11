from ..models import Track

from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = Spotify(auth_manager=auth_manager)


def analyze_tracks(tracks_id: list[str]):
    """ Find and analyze tracks provided their id

    Returns:
    list[Track]: list of analyzed tracks
    """

    tracks = sp.tracks(tracks_id)
    if tracks == None:
        return None

    tracks = tracks["tracks"]
    features_list = sp.audio_features(tracks_id)
    if features_list == None:
        return None

    analysis: list[Track] = []
    for i in range(len(tracks)):
        track = tracks[i]
        features = features_list[i]

        energy = features["energy"]
        category = "low" if energy < 0.5 else "medium" if energy < 0.85 else "high"

        duration = features["duration_ms"]
        duration = duration // 1000

        analysis.append(Track(
            id=track["id"],
            href=track["external_urls"]["spotify"],
            title=track["name"],
            artist=track["artists"][0]["name"],
            duration=duration,
            category=category))

    return analysis


def search_tracks(queries: list[str]):
    """
    Returns: 
    list[str]: list of tracks id
    """

    ids: list[str] = []
    for query in queries:
        search_result = sp.search(f"track:{query}", limit=1)
        if search_result == None:
            continue

        ids.append(search_result["tracks"]["items"][0]["id"])

    return ids
