from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .utils import exercise, spotify

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/")
async def root(tracks: str, difficulty: str = "beginner", muscle: str | None = None):
    if len(tracks) == 0:
        raise HTTPException(status_code=400, detail="parameter tracks missing")

    tracks = tracks.split(",")
    if len(tracks) > 50:
        raise HTTPException(
            status_code=400, detail="parameter tracks over limit")

    if difficulty not in ["beginner", "intermediate", "expert"]:
        raise HTTPException(
            status_code=400, detail="parameter difficulty invalid")

    if muscle != None and muscle not in ["abdominals", "abductors", "adductors", "biceps", "calves", "chest",
                                         "forearms", "glutes", "hamstrings", "lats", "lower_back", "next",
                                         "quadriceps", "traps", "triceps"]:
        raise HTTPException(
            status_code=400, detail="parameter muscle invalid")

    tracks = spotify.analyze_tracks(tracks)
    if tracks == None:
        raise HTTPException(
            status_code=500, detail="error when analyzing tracks")

    exercises = exercise.recommend_by_tracks(tracks, difficulty, muscle)

    response = JSONResponse(content=jsonable_encoder(exercises))
    return response
