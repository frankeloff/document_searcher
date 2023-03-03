from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)

from .document import Document

__all__ = [
    "metadata",
    "Document",
]
