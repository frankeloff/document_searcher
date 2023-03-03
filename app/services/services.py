from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.document import DocumenIn
from app.models.document import Document
from elasticsearch import Elasticsearch, NotFoundError
from fastapi import HTTPException, status
from sqlalchemy import select, desc
from elastic_transport import ConnectionError, ConnectionTimeout
from datetime import datetime
from typing import List


def make_elastic_structure_for_query(pattern: str) -> dict:
    """
    Creating a dictionary for a query in ElasticSearch search() method
    """
    return {"query": {"match": {"text": {"query": pattern, "minimum_should_match": 1}}}}

async def get_documents_in_ids_order_by_desc(db: AsyncSession, ids: List[int]) -> List[Document]:
    """
    Retrieving documents sorted by the field "created_date" with IDs that are in the list
    """
    query = (
        select(Document)
        .where(Document.doc_id.in_(ids))
        .order_by(desc(Document.created_date))
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_document_by_id(db: AsyncSession, document_id: int):
    """ """
    query = select(Document).where(Document.doc_id == document_id)
    result = await db.execute(query)
    return result.scalars().first()


async def add_doc(db: AsyncSession, es: Elasticsearch, doc: DocumenIn) -> Document:
    """
    Creating a new document and adding it to the database and elasticsearch index
    """
    new_document_db_model = Document(
        rubrics=doc.rubrics, text=doc.text, created_date=datetime.now()
    )

    db.add(new_document_db_model)
    await db.commit()
    await db.refresh(new_document_db_model)

    new_document_es_structure = {"text": new_document_db_model.text}
    try:
        es.index(
            index="doc-index",
            id=new_document_db_model.doc_id,
            document=new_document_es_structure,
        )
    except (ConnectionError, ConnectionTimeout):
        await db.delete(new_document_db_model)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to connect to search engine",
        )
    return new_document_db_model


async def delete_doc(db: AsyncSession, es: Elasticsearch, doc_id: int) -> None:
    """
    Deleting documents from a database and elasticsearch index.
    """
    document_to_delete = await get_document_by_id(db=db, document_id=doc_id)
    if not document_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document does not exist"
        )
    try:
        es.delete(index="doc-index", id=doc_id)
        await db.delete(document_to_delete)
        await db.commit()
    except (ConnectionError, ConnectionTimeout):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to connect to search engine",
        )


async def search_doc(
    db: AsyncSession, es: Elasticsearch, pattern: str
) -> List[Document]:
    """
    Searching for patterns in the text and returning the first 20 records, sorted in order from the earliest to the latest
    """
    result_arr = []
    es_query = make_elastic_structure_for_query(pattern=pattern)
    try:
        search_result = es.search(index="doc-index", body=es_query, size=20)
        ids = [int(obj["_id"]) for obj in search_result["hits"]["hits"]]
        result_arr = await get_documents_in_ids_order_by_desc(db=db, ids=ids)
    except (ConnectionError, ConnectionTimeout):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to connect to search engine",
        )

    if len(result_arr) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index does not exist."
        )

    return result_arr
