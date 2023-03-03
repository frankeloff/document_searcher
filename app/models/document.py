from sqlalchemy import Column, Integer, ARRAY, String, Text, DateTime

from . import Base


class Document(Base):
    __tablename__ = "documents"

    doc_id = Column(Integer, primary_key=True)
    rubrics = Column(ARRAY(String))
    text = Column(Text)
    created_date = Column(DateTime)
