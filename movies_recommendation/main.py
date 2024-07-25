from typing import Union
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from movies_recommendation import models, schemas, crud
from movies_recommendation.database import SessionLocal, engine
from sqlalchemy.orm import Session
import os
import pandas as pd


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


@app.get("/movie/{movie_id}", response_class=HTMLResponse)
async def read_movie_details(request: Request, movie_id: int):
    # Retrieve movie details based on movie_id (example using a list, replace with database query)
    try:
        movie = movies[movie_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Render movie_details.html with movie data dynamically using Jinja2
    return templates.TemplateResponse("movie.html", {"request": request, **movie})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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