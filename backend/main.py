from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import logs
from routers import errors
from routers import stats


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.177.130:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(logs.router)
app.include_router(errors.router)
app.include_router(stats.router)
