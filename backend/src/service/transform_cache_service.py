from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.src.models.transformers import TransformCache


class TransformCacheService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_input(self, input_value: str) -> TransformCache | None:
        query = select(TransformCache).where(TransformCache.input == input_value)
        result = self.db.execute(query)

        return result.scalar_one_or_none()

    def create(self, input_value: str, output: str) -> TransformCache:
        try:
            cached_result = TransformCache(
                input=input_value,
                output=output,
            )

            self.db.add(cached_result)
            self.db.commit()
            self.db.refresh(cached_result)

            return cached_result

        except SQLAlchemyError:
            self.db.rollback()
            raise
