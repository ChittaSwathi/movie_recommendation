from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    userid: int

class UserCreate(UserBase):
    userid: int
    name: str

class User(UserBase):
    userid: int
    name: str

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    movieid: int

    class Config:
        orm_mode = True

class TagInfoBase(BaseModel):
    tagid: int
    content: str

class TagInfoCreate(TagInfoBase):
    pass

class TagInfo(TagInfoBase):
    tagid: int
    content: str

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    genreid: int

    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    rating: float
    timestamp: int

class RatingCreate(RatingBase):
    userid: int
    movieid: int

class Rating(RatingBase):
    userid: int
    movieid: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    timestamp: int

class TagCreate(TagBase):
    userid: int
    movieid: int
    tagid: int

class Tag(TagBase):
    userid: int
    movieid: int
    tagid: int

    class Config:
        orm_mode = True
