import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.db import Base, get_db
from backend.src.models.payload import Payload  # noqa: F401
from backend.src.models.transformers import TransformCache  # noqa: F401
from backend.src.routes.router import router


@pytest.fixture
def db_session(tmp_path):
    database_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine)

    with test_session() as session:
        yield session

    engine.dispose()


@pytest.fixture
def api_client(db_session):
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
