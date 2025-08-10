#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn"]
# ///

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str | None = None

@app.get("/user")
async def get_user() -> User:
    return User(name="James")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "client:app",
        host="127.0.0.1",
        port=56789,
        reload=True,
        ssl_keyfile="server.key",
        ssl_certfile="server.crt",
    )