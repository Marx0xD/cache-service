from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from backend.src.models.payload import Payload


class PayloadService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, payload_id: int) -> Payload | None:
        query = select(Payload).where(Payload.id == payload_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_by_request_hash(self, request_hash: str) -> Payload | None:
        query = select(Payload).where(Payload.request_hash == request_hash)
        result = self.db.execute(query)

        return result.scalar_one_or_none()

    def create(self, request_hash: str, output: str) -> Payload:
        try:
            payload = Payload(request_hash=request_hash, output=output)
            self.db.add(payload)
            self.db.commit()
            self.db.refresh(payload)
            return payload
        except IntegrityError:
            self.db.rollback()
            raise

        except SQLAlchemyError:
            self.db.rollback()
            raise
