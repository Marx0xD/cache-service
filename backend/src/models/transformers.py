from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.db import Base
from backend.src.utils import utc_now

# Persists transformer results to avoid repeating work for inputs already processed.


class TransformCache(Base):
    __tablename__ = "transformers"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    input: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    output: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
