from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, BigInteger, Table
from sqlalchemy.orm import relationship
from movies_recommendation.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association Table
hasagenre = Table(
    'hasagenre', Base.metadata,
    Column('movieid', Integer, ForeignKey('movies.movieid'), primary_key=True),
    Column('genreid', Integer, ForeignKey('genres.genreid'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ratings = relationship('Rating', back_populates='user')
    tags = relationship('Tag', back_populates='user')

class Movie(Base):
    __tablename__ = 'movies'
    movieid = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = relationship('Genre', secondary=hasagenre, back_populates='movies')
    ratings = relationship('Rating', back_populates='movie')
    tags = relationship('Tag', back_populates='movie')

class TagInfo(Base):
    __tablename__ = 'taginfo'
    tagid = Column(Integer, primary_key=True, index=True)
    content = Column(String)

class Genre(Base):
    __tablename__ = 'genres'
    genreid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    movies = relationship('Movie', secondary=hasagenre, back_populates='genres')

class Rating(Base):
    __tablename__ = 'ratings'
    userid = Column(Integer, ForeignKey('users.userid'), primary_key=True)
    movieid = Column(Integer, ForeignKey('movies.movieid'), primary_key=True)
    rating = Column(Numeric)
    timestamp = Column(BigInteger)
    movie = relationship('Movie', back_populates='ratings')
    user = relationship('User', back_populates='ratings')

class Tag(Base):
    __tablename__ = 'tags'
    userid = Column(Integer, ForeignKey('users.userid'), primary_key=True)
    movieid = Column(Integer, ForeignKey('movies.movieid'), primary_key=True)
    tagid = Column(Integer, ForeignKey('taginfo.tagid'), primary_key=True)
    timestamp = Column(BigInteger)
    user = relationship('User', back_populates='tags')
    movie = relationship('Movie', back_populates='tags')
    tag = relationship('TagInfo')


# ORM model for hasagenre
class HasAGenre(Base):
    __table__ = hasagenre
