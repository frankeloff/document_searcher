import pytest
from httpx import AsyncClient
from tests.conftest import app


@pytest.mark.asyncio
async def test_add_document():
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        response = await ac.post(
            "api/add/", json={"rubrics": ["string"], "text": "math math"}
        )

    assert response.status_code == 200
    assert response.json()["rubrics"][0] == "string"
    assert response.json()["text"] == "math math"
    assert response.json()["doc_id"] == 1


@pytest.mark.asyncio
async def test_delete_document():
    delete_id = 11
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        response = await ac.delete(f"api/delete/", params={"doc_id": delete_id})
    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "success"


@pytest.mark.asyncio
async def test_search_document():
    pattern = "string"
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        response = await ac.get(f"api/search/", params={"pattern": pattern})
    assert response.status_code == 200
    for result in response.json():
        for rubric in result["rubrics"]:
            assert rubric == "new_string"
        assert result["text"] == "new_string"
        assert result["doc_id"] == 10
        assert result["created_date"] == "2023-03-03T17:42:06.800305"
