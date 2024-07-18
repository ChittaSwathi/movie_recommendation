from typing import Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

