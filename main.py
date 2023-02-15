from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrodHandler
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
app.title = "My FastAPI Application"
app.version = "0.0.1"

# Creates the `.sqlite` database with the specified tables
Base.metadata.create_all(bind=engine)

# Middlewares
app.add_middleware(ErrodHandler)

# Routes
app.include_router(movie_router)
app.include_router(user_router)


@app.get('/', tags=['home'])
def get_message():
    return HTMLResponse('<h1>Hello There!</h1>')
