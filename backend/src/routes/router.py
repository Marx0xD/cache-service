from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.src.db import get_db
from backend.src.routes.schema import PayloadRequest
from backend.src.service.payload_service import PayloadService
from backend.src.service.transform_cache_service import TransformCacheService
from backend.src.utils.hash import hash_request

router = APIRouter(
    prefix="/payload",
    tags=["payload"],
)


@router.post("")
def create_payload(
    payload: Annotated[PayloadRequest, Body()],
    db: Session = Depends(get_db),
):
    payload_service = PayloadService(db)
    transform_cache_service = TransformCacheService(db)

    request_hash = hash_request(payload.list_1, payload.list_2)

    existing_payload = payload_service.get_by_request_hash(request_hash)

    if existing_payload:
        return {"id": existing_payload.id}

    output = []

    for index, value_1 in enumerate(payload.list_1):
        value_2 = payload.list_2[index]

        cached_val_1 = transform_cache_service.get_by_input(value_1)
        cached_val_2 = transform_cache_service.get_by_input(value_2)

        if cached_val_1:
            output.append(cached_val_1.output)
        else:
            transformed = value_1.upper()
            transform_cache_service.create(value_1, transformed)
            output.append(transformed)

        if cached_val_2:
            output.append(cached_val_2.output)
        else:
            transformed = value_2.upper()
            transform_cache_service.create(value_2, transformed)
            output.append(transformed)

    final_output = ", ".join(output)

    created_payload = payload_service.create(
        request_hash=request_hash,
        output=final_output,
    )

    return {"id": created_payload.id}


@router.get("/{payload_id}")
def get_payload(
    payload_id: int,
    db: Session = Depends(get_db),
):
    payload_service = PayloadService(db)

    payload = payload_service.get_by_id(payload_id)

    if not payload:
        raise HTTPException(
            status_code=404,
            detail="Payload not found",
        )

    return {"output": payload.output}
