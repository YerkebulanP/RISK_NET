from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from config.database import engine
from models import internal_system_control
from routers.users_router import user_routers
from routers.reestr_router import reestr_routers
from routers.isc_router import isc_routers

from fastapi.middleware.cors import CORSMiddleware


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "reestr",
        "description": "Manage reestr."
    },
    {
        "name": "internal_system_control",
        "description": "Система внутренного контроля (СВК)"
    }
]

app = FastAPI(openapi_tags=tags_metadata)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

internal_system_control.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    internal_system_control.Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

app.include_router(user_routers)
app.include_router(reestr_routers)
app.include_router(isc_routers)