from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from .db import crud, schemas
from .db.database import SessionLocal, engine

from .models import difficulties, muscles
from .utils import exercise, spotify

load_dotenv()

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def generate(tracks: str, difficulty: str = "beginner", muscle: str | None = None, db: Session = Depends(get_db)):
    if len(tracks) == 0:
        raise HTTPException(400, "parameter tracks missing")

    tracks = tracks.split(",")
    if len(tracks) > 50:
        raise HTTPException(400, "parameter tracks over limit")

    if difficulty not in difficulties:
        raise HTTPException(400, "parameter difficulty invalid")

    if muscle != None and muscle not in muscles:
        raise HTTPException(400, "parameter muscle invalid")

    new_tracks = []
    available_tracks, missing_tracks_id = crud.get_tracks(db, tracks)
    if len(missing_tracks_id) > 0:
        new_tracks = spotify.analyze_tracks(missing_tracks_id)
        if new_tracks == None:
            raise HTTPException(500, "error when analyzing tracks")

        crud.add_tracks(db, new_tracks)

    exercises_tracks = exercise.recommend_by_tracks(
        [*available_tracks, *new_tracks], difficulty, muscle)

    db_playlist = crud.create_playlist(db)
    for exercise_track in exercises_tracks:
        db_exercise_track = crud.create_exercise_track(
            db, exercise_track, db_playlist.id)
        crud.add_exercises(db, exercise_track.exercises, db_exercise_track.id)

    return JSONResponse(content=jsonable_encoder({
        "id": db_playlist.id,
        "exercises_tracks": exercises_tracks
    }))


@app.get("/search")
async def search(queries: str, difficulty: str = "beginner", muscle: str | None = None, db: Session = Depends(get_db)):
    if len(queries) == 0:
        raise HTTPException(400, "parameter queries missing")

    queries = [query for query in queries.split(",") if query != "\""]
    if len(queries) <= 0:
        raise HTTPException(400, "parameter queries missing")
    elif len(queries) > 50:
        raise HTTPException(400, "parameter queries over limit")

    if difficulty not in difficulties:
        raise HTTPException(400, "parameter difficulty invalid")

    if muscle != None and muscle not in muscles:
        raise HTTPException(400, "parameter muscle invalid")

    tracks_ids = spotify.search_tracks(queries)

    new_tracks = []
    available_tracks, missing_tracks_id = crud.get_tracks(db, tracks_ids)
    if len(missing_tracks_id) > 0:
        new_tracks = spotify.analyze_tracks(missing_tracks_id)
        if new_tracks == None:
            raise HTTPException(500, "error when analyzing tracks")

        crud.add_tracks(db, new_tracks)

    exercises_tracks = exercise.recommend_by_tracks(
        [*available_tracks, *new_tracks], difficulty, muscle)

    db_playlist = crud.create_playlist(db)
    for exercise_track in exercises_tracks:
        db_exercise_track = crud.create_exercise_track(
            db, exercise_track, db_playlist.id)
        crud.add_exercises(db, exercise_track.exercises, db_exercise_track.id)

    return JSONResponse(content=jsonable_encoder({
        "id": db_playlist.id,
        "exercises_tracks": exercises_tracks
    }))
