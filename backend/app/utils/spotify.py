from ..models import Track

from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = Spotify(auth_manager=auth_manager)


def fetch_tracks(tracks_id: list[str]):
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


def search_track(query: str):
    result = sp.search(f"track:{query}", limit=1)
    if result == None:
        return None

    if result["tracks"]["total"] <= 0:
        return None

    track = result["tracks"]["items"][0]
    return fetch_tracks([track["id"]])


def search_tracks(queries: list[str]):
    tracks: list[Track] = []
    for query in queries:
        result = search_track(query)
        if result == None:
            continue

        tracks += result

    return tracks
