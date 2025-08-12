#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn", "pyyaml"]
# ///
from contextlib import asynccontextmanager
from typing import Any

import yaml
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


def read_user_config():
    with open("configuration.yml", "r") as file:
        return yaml.safe_load(file)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
    user_config=read_user_config(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app.extra.get("user_config", {}).get("cors_origins", ""),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def user_config():
    return read_user_config()


@app.get("/api/user")
async def get_user(config: dict[str, Any] = Depends(user_config)):
    return config


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "client:app",
        host="127.0.0.1",
        port=56789,
        reload=True,
        ssl_keyfile="certs/server.key",
        ssl_certfile="certs/server.crt",
    )
