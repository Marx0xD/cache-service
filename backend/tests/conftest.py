import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.db import Base
from backend.src.models.payload import Payload  # noqa: F401
from backend.src.models.transformers import TransformCache  # noqa: F401


@pytest.fixture
def db_session(tmp_path):
    database_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine)

    with test_session() as session:
        yield session

    engine.dispose()
