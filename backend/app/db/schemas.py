from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, index=True)
    href = Column(String)
    title = Column(String)
    artist = Column(String)

    duration = Column(Integer)
    category = Column(String)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    difficulty = Column(String)
    muscle = Column(String)

    equipment = Column(String)
    instructions = Column(String)

    exercise_track_id = Column(Integer, ForeignKey("exercises_tracks.id"))
    exercise_track = relationship("ExerciseTrack", back_populates="exercises")


class ExerciseTrack(Base):
    __tablename__ = "exercises_tracks"

    id = Column(Integer, primary_key=True, index=True)

    track_id = Column(String, ForeignKey("tracks.id"))
    track = relationship("Track")

    exercises = relationship("Exercise", back_populates="exercise_track")

    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    playlist = relationship("Playlist", back_populates="exercises_tracks")


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)

    exercises_tracks = relationship(
        "ExerciseTrack", back_populates="playlist")
