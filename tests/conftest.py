from app.api.depends import get_session, get_es
from app.main import app
from app.models import Document


class FakeAll:
    """
    Fake sqlalchemy scalars().all() method
    """

    def __init__(self):
        pass

    @staticmethod
    def first():
        return [
            {
                "rubrics": [""],
                "text": "text",
                "created_date": "2023-03-03 17:42:06.800305",
                "doc_id": 1,
            }
        ]

    @staticmethod
    def all():
        return [
            {
                "rubrics": ["new_string"],
                "text": "new_string",
                "created_date": "2023-03-03 17:42:06.800305",
                "doc_id": 10,
            }
        ]


class FakeScalars:
    """
    Fake sqlalchemy scalars() method
    """

    def __init__(self):
        pass

    def scalars(self):
        return FakeAll


class FakeDatabase:
    """
    Simulating a database for testing purposes
    """

    def __init__(self):
        pass

    def add(self, new_document: Document):
        new_document.doc_id = 1
        return new_document

    async def commit(self):
        pass

    async def refresh(self, new_document: Document):
        pass

    async def execute(self, query):
        return FakeScalars()

    async def delete(self, document: Document):
        pass


class FakeEs:
    """
    Simulating a elasticsearch for testing purposes
    """

    def __init__(self):
        pass

    def index(self, index, id, document):
        pass

    def search(self, index, body, size):
        return {"hits": {"hits": []}}

    def delete(self, index, id):
        pass


async def override_get_session() -> FakeDatabase:
    return FakeDatabase()


async def override_get_es() -> FakeEs:
    return FakeEs()


app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_es] = override_get_es
