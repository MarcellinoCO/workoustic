from sqlalchemy.orm import Session

from . import schemas
from .. import models


def get_tracks(db: Session, tracks_id: list[str]):
    tracks: list[models.Track] = []
    missing_tracks_id: list[str] = []

    for track_id in tracks_id:
        track = db.query(schemas.Track).filter(
            schemas.Track.id == track_id).first()

        if track == None:
            missing_tracks_id.append(track_id)
            continue

        tracks.append(models.Track(id=track.id, href=track.href, title=track.title,
                      artist=track.artist, duration=track.duration, category=track.category))

    return tracks, missing_tracks_id


def add_tracks(db: Session, tracks: list[models.Track]):
    db_tracks: list[schemas.Track] = []
    for track in tracks:
        db_track = schemas.Track(**track.dict())
        db_tracks.append(db_track)
        db.add(db_track)

    db.commit()
    return db_track


def add_exercises(db: Session, exercises: list[models.Exercise], exercise_track_id: int):
    db_exercises: list[schemas.Exercise] = []
    for exercise in exercises:
        db_exercise = schemas.Exercise(
            **exercise.dict(), exercise_track_id=exercise_track_id)
        db_exercises.append(db_exercise)
        db.add(db_exercise)

    db.commit()
    return db_exercises


def create_exercise_track(db: Session, exercise_track: models.ExerciseTrack, playlist_id: int):
    db_exercise_track = schemas.ExerciseTrack(
        track_id=exercise_track.track.id, playlist_id=playlist_id)
    db.add(db_exercise_track)

    db.commit()
    db.refresh(db_exercise_track)

    return db_exercise_track


def get_playlist(db: Session, id: int):
    db_playlist = db.query(schemas.Playlist).filter(
        schemas.Playlist.id == id).first()
    if db_playlist == None:
        return None

    return models.Playlist(exercises_tracks=[
        models.ExerciseTrack(track=models.Track(id=et.track.id, href=et.track.href, title=et.track.title, artist=et.track.artist, duration=et.track.duration, category=et.track.category),
                             exercises=[models.Exercise(name=e.name, difficulty=e.difficulty, muscle=e.muscle, equipment=e.equipment, instructions=e.instructions)
                                        for e in et.exercises])
        for et in db_playlist.exercises_tracks])


def create_playlist(db: Session):
    db_playlist = schemas.Playlist()
    db.add(db_playlist)

    db.commit()
    db.refresh(db_playlist)

    return db_playlist
