from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.document import DocumenIn, DocumenOut
from app.schemas.success_response import SuccessResponse
from app.api.depends import get_session, get_es
from app.services.services import add_doc, delete_doc, search_doc
from typing import List

router = APIRouter()


@router.post("/add/", response_model=DocumenOut)
async def add_document(
    document: DocumenIn,
    session: AsyncSession = Depends(get_session),
    es=Depends(get_es),
):
    """
    Adding a new document to the database.
    """
    new_document = await add_doc(db=session, es=es, doc=document)

    return new_document


@router.delete("/delete/", response_model=SuccessResponse)
async def delete_document(
    doc_id: int, session: AsyncSession = Depends(get_session), es=Depends(get_es)
):
    """
    Removing a document from the database.
    """
    await delete_doc(db=session, es=es, doc_id=doc_id)

    return {"status_code": 200, "message": "success"}


@router.get("/search/", response_model=List[DocumenOut])
async def search_document(
    pattern: str, session: AsyncSession = Depends(get_session), es=Depends(get_es)
):
    """
    Searching for the first 20 entries that contain a pattern
    """
    result = await search_doc(session, es, pattern)

    return result
