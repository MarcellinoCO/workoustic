import os
import requests
import random
import math

from ..models import Exercise, ExerciseTrack, Track

api_root = "https://api.api-ninjas.com/v1/exercises"
headers = {"X-Api-Key": os.getenv("API_NINJAS_API_KEY")}


def fetch_exercises(exercise_type: str | None = None, difficulty: str | None = None, muscle: str | None = None):
    query = api_root

    if exercise_type != None:
        query += f"?type={exercise_type}"

    if difficulty != None:
        query += "?" if query == api_root else "&"
        query += f"difficulty={difficulty}"

    if muscle != None:
        query += "?" if query == api_root else "&"
        query += f"muscle={muscle}"

    response = requests.get(query, headers=headers)
    if response.status_code != requests.codes.ok:
        return None

    exercises: list[Exercise] = [e for e in response.json()]
    return exercises


def recommend_by_track(track: Track, difficulty: str | None = None, muscle: str | None = None):
    exercises: list[Exercise] = []

    # 30 seconds per set, 10 seconds break
    exercise_count = math.ceil(track.duration / 40)

    if track.category == "low":
        exercises += fetch_exercises("stretching", difficulty, muscle)

    if track.category == "medium":
        exercises += fetch_exercises("strength", difficulty, muscle)
        exercises += fetch_exercises("cardio", difficulty, muscle)

        # 90 seconds per set, 10 seconds break
        exercise_count = math.ceil(track.duration / 100)

    if track.category == "high":
        exercises += fetch_exercises("plyometrics", difficulty, muscle)

    return random.sample(exercises, exercise_count)


def recommend_by_tracks(tracks: list[Track], difficulty: str | None = None, muscle: str | None = None):
    exercises: list[ExerciseTrack] = []
    for track in tracks:
        exercises.append(ExerciseTrack(
            track=track, exercises=recommend_by_track(track, difficulty, muscle)))

    return exercises
