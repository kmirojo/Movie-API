from fastapi import APIRouter, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from models.movie import Movie as MovieModel
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200,
                  #   dependencies=[Depends(JWTBearer())]
                  )
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    # When setting a query parameter, we need to add a slash (/) in the end of the endpoint
    # get movie, from each movie in movies which category is `category`
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()

    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"Message": f"Movie '{movie.title}' was successfully created"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})

    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": f"The movie {movie.title} has been updated"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie was not found'})

    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": f"The movie {result.title} was deleted"})
