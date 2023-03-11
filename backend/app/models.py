from pydantic import BaseModel


difficulties = ["beginner", "intermediate", "expert"]
muscles = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms",
           "glutes", "hamstrings", "lats", "lower_back", "next", "quadriceps", "traps", "triceps"]


class Track(BaseModel):
    id: str
    href: str
    title: str
    artist: str

    duration: int
    category: str


class Exercise(BaseModel):
    name: str
    difficulty: str
    muscle: str

    equipment: str
    instructions: str


class ExerciseTrack(BaseModel):
    track: Track
    exercises: list[Exercise]


class Playlist(BaseModel):
    exercises_tracks: list[ExerciseTrack]
