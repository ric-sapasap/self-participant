from uuid import UUID

from sqlmodel import SQLModel, Field


class Ejeweje(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    value: str
