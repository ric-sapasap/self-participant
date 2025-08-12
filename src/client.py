#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn", "sqlmodel"]
# ///
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import getpass

from sqlmodel import SQLModel, create_engine, Session, select

from models import Ejeweje

# - DB config
DB_PATH = Path("data/self.db")
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pneumonoultrafinalisekaiquestonlinefantasyoftheeastconiosis3.online"
]


# - Ensure DB exists on startup
@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    name: str | None = None


@app.get("/api/user")
async def get_user() -> User:
    return User(name=getpass.getuser())


def get_session():
    with Session(engine) as session:
        yield session

@app.get("/api/something")
async def get_something(session: Session = Depends(get_session)):
    statement = select(Ejeweje)
    results = session.exec(statement).all()
    return results

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
