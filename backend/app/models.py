from pydantic import BaseModel


class Track(BaseModel):
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
