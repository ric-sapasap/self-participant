#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn"]
# ///

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str | None = None

@app.get("/user")
async def get_user() -> User:
    return User(name=None)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "client:app",                      # use the actual object
        host="127.0.0.1",
        port=56789,
        reload=True,
        ssl_keyfile="server.key",
        ssl_certfile="server.crt",
    )