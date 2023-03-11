from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import difficulties, muscles
from .utils import exercise, spotify

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/")
async def generate(tracks: str, difficulty: str = "beginner", muscle: str | None = None):
    if len(tracks) == 0:
        raise HTTPException(400, "parameter tracks missing")

    tracks = tracks.split(",")
    if len(tracks) > 50:
        raise HTTPException(400, "parameter tracks over limit")

    if difficulty not in difficulties:
        raise HTTPException(400, "parameter difficulty invalid")

    if muscle != None and muscle not in muscles:
        raise HTTPException(400, "parameter muscle invalid")

    tracks = spotify.fetch_tracks(tracks)
    if tracks == None:
        raise HTTPException(500, "error when analyzing tracks")

    exercises = exercise.recommend_by_tracks(tracks, difficulty, muscle)

    response = JSONResponse(content=jsonable_encoder(exercises))
    return response


@app.get("/search")
async def search(queries: str, difficulty: str = "beginner", muscle: str | None = None):
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

    tracks = spotify.search_tracks(queries)
    if len(tracks) == 0:
        raise HTTPException(
            status_code=404, detail="search results not found")

    exercises = exercise.recommend_by_tracks(tracks, difficulty, muscle)

    response = JSONResponse(content=jsonable_encoder(exercises))
    return response
