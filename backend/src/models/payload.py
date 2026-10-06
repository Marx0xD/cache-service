from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.db import Base
from backend.src.utils.utc_now import utc_now

# Stores generated payloads so identical requests can reuse the same payload ID.


class Payload(Base):
    __tablename__ = "payload"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    request_hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    output: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
