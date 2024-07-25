from sqlalchemy.orm import Session
from movies_recommendation import models, schemas
import pandas as pd
import os

def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(
        userid=rating.userid,
        movieid=rating.movieid,
        rating=rating.rating,
        timestamp=rating.timestamp
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def load_data_from_file(model, file_path: str, db: Session):
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    # Load the file into a DataFrame
    col_names = {'ratings': ['userid', 'movieid', 'rating', 'timestamp'],
                 'movies': ['movieid','title'],
                 'hasagenre': ['movieid','genreid'],
                 'genres': ['genreid','name'],
                 'taginfo': ['tagid','content'],
                 'tags': ['userid', 'movieid','tagid','timestamp'],
                 'users': ['userid','name']}
    df = pd.read_csv(file_path, delimiter='%', header=None, names=col_names[model])

    if model == 'ratings':
        for index, row in df.iterrows():
            rating_data = schemas.RatingCreate(
                userid=row['userid'],
                movieid=row['movieid'],
                rating=row['rating'],
                timestamp=row['timestamp']
            )
            create_rating(db, rating_data)

    elif model =='users':
        for index, row in df.iterrows():
            user_data = schemas.UserCreate(
                userid=row['userid'],
                name=row['name'],
            )
            create_user(db, user_data)

    elif model =='movies':
        for index, row in df.iterrows():
            movie_data = schemas.MovieCreate(
                movieid=row['movieid'],
                title=row['title'],
            )
            create_movie(db, movie_data)




def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, userid=user.userid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(title=movie.title, movieid=movie.movieid)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def create_taginfo(db: Session, taginfo: schemas.TagInfoCreate):
    db_taginfo = models.TagInfo(content=taginfo.content)
    db.add(db_taginfo)
    db.commit()
    db.refresh(db_taginfo)
    return db_taginfo

def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(
        userid=tag.userid,
        movieid=tag.movieid,
        tagid=tag.tagid,
        timestamp=tag.timestamp
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
