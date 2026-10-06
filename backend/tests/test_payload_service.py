from backend.src.service.payload_service import PayloadService


def test_create_payload(db_session):
    service = PayloadService(db_session)

    payload = service.create("request-hash", "payload-output")

    assert payload.id is not None
    assert payload.request_hash == "request-hash"
    assert payload.output == "payload-output"


def test_get_payload_by_id(db_session):
    service = PayloadService(db_session)
    created = service.create("request-hash", "payload-output")

    payload = service.get_by_id(created.id)

    assert payload is not None
    assert payload.id == created.id
    assert payload.request_hash == "request-hash"
    assert payload.output == "payload-output"


def test_get_payload_by_request_hash(db_session):
    service = PayloadService(db_session)
    created = service.create("request-hash", "payload-output")

    payload = service.get_by_request_hash("request-hash")

    assert payload is not None
    assert payload.id == created.id
    assert payload.request_hash == "request-hash"
    assert payload.output == "payload-output"
