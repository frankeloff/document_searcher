from typing import List
from datetime import datetime
from pydantic import BaseModel


class Base(BaseModel):
    rubrics: List[str]
    text: str


class DocumenIn(Base):
    pass


class DocumenOut(Base):
    doc_id: int
    created_date: datetime

    class Config:
        orm_mode = True
