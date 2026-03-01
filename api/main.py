from fastapi import FastAPI
from routers import data_router

# Declaring the FastAPI framework
app = FastAPI()

app.include_router(data_router.router)