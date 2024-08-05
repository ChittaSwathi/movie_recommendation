from typing import Union

import pandas as pd
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from movies_recommendation import models, schemas, crud
from movies_recommendation.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import text
import math
import os

import json


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Mount the "templates" directory to serve static files
app.mount("/static", StaticFiles(directory="movies_recommendation/templates"), name="static")

# Create Jinja2Templates instance pointing to the "templates" directory
templates = Jinja2Templates(directory="movies_recommendation/templates")


movies = [
    {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "release_year": 1994,
        "genre": "Drama",
        "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "The Godfather",
        "director": "Francis Ford Coppola",
        "release_year": 1972,
        "genre": "Crime, Drama",
        "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    }
]

def get_all_movies_info(db):
    qry = """select m.movieid, m.title as title, g.name as genre, 
                                r.userid, r.rating, r.timestamp, u.name as username
                        from movies m 
                        inner join hasagenre hg on hg.movieid=m.movieid
                        inner join genres g on g.genreid=hg.genreid
                        inner join ratings r on r.movieid=m.movieid
                        inner join users u on u.userid=r.userid
                """
    movie_recs = db.execute(text(qry)).fetchall()
    cols = ['movieid', 'title', 'genre', 'userid', 'rating', 'timestamp', 'username']

    df = pd.DataFrame(movie_recs, columns=cols)
    grouped = df.groupby('movieid')

    result = {}
    for movieid, group in grouped:
        movie_info = group[['title', 'genre']].iloc[0].to_dict()
        movie_info['avg_rating'] = math.ceil(group[["rating"]].mean().rating)
        ratings_info = group[['rating', 'timestamp', 'userid', 'username']].to_dict(orient='records')
        result[movieid] = {**movie_info, 'ratings': ratings_info}
    return result


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Hello, World!</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a FastAPI application returning HTML content.</p>
        </body>
    </html>
    """


@app.get('/movies/all')
async def get_all_movies(db: Session = Depends(get_db)):
    result = get_all_movies_info(db)
    return json.dumps(result, indent=4, default=str)

@app.get("/movies")
async def movie_info(request: Request, db: Session = Depends(get_db)):
    result = get_all_movies_info(db)
    return templates.TemplateResponse("movie.html", {"request": request, "movies": result})

@app.get("/movies/{movieid}")
async def movie_details(request: Request, movieid: int, db: Session = Depends(get_db)):
    qry = """select m.movieid, m.title as title, g.name as genre, 
                    r.userid, r.rating, r.timestamp, u.name as username
            from movies m 
            inner join hasagenre hg on hg.movieid=m.movieid
            inner join genres g on g.genreid=hg.genreid
            inner join ratings r on r.movieid=m.movieid
            inner join users u on u.userid=r.userid
            where m.movieid=%s"""%(movieid)
    movie_recs = db.execute(text(qry)).fetchall()
    cols = ['movieid', 'title', 'genre', 'userid', 'rating', 'timestamp', 'username']

    df = pd.DataFrame(movie_recs, columns=cols)
    grouped = df.groupby('movieid')

    result = {}
    for movieid, group in grouped:
        movie_info = group[['title','genre']].iloc[0].to_dict()
        movie_info['avg_rating'] = math.ceil(group[["rating"]].mean().rating)
        ratings_info = group[['rating', 'timestamp', 'userid', 'username']].to_dict(orient='records')
        result[movieid] = {**movie_info, 'ratings': ratings_info}

    return templates.TemplateResponse("movie.html", {"request": request, "movies": result})



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



@app.get("/load_file/{model}")
async def load_ratings(model:str, db: Session = Depends(get_db)):
    if not os.path.isfile('movies_recommendation/data/'+model+'.dat'):
        return {"error": "File not found -- "+ model +'.dat'}

    try:
        crud.load_data_from_file(model, 'movies_recommendation/data/'+model+'.dat', db)
        return {"status": "file processed"}
    except Exception as e:
        return {"error": str(e)}

#todo: run using ---- uvicorn movies_recommendation.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)