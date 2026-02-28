from fastapi import FastAPI
from routers import data_router

app = FastAPI()

app.include_router(data_router.router)