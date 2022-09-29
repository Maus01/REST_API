from fastapi import FastAPI
from .routers import users, articles, auth
from .import models, database
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()



app.include_router(users.router)
app.include_router(articles.router)
app.include_router(auth.router)