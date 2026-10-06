from sqlalchemy import select

from backend.src.models.transformers import TransformCache


def test_post_payload_creates_payload_and_returns_id(api_client):
    response = api_client.post(
        "/payload",
        json={"list_1": ["hello"], "list_2": ["world"]},
    )

    assert response.status_code == 200
    assert isinstance(response.json()["id"], int)


def test_post_payload_reuses_id_for_identical_request(api_client):
    request_body = {"list_1": ["hello"], "list_2": ["world"]}

    first_response = api_client.post("/payload", json=request_body)
    second_response = api_client.post("/payload", json=request_body)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["id"] == first_response.json()["id"]


def test_post_payload_reuses_cached_transformer_results(api_client, db_session):
    first_response = api_client.post(
        "/payload",
        json={"list_1": ["shared"], "list_2": ["first"]},
    )
    assert first_response.status_code == 200

    cached_result = db_session.scalar(
        select(TransformCache).where(TransformCache.input == "shared")
    )
    assert cached_result is not None

    cached_result.output = "FROM CACHE"
    db_session.commit()

    second_response = api_client.post(
        "/payload",
        json={"list_1": ["shared"], "list_2": ["second"]},
    )
    assert second_response.status_code == 200

    payload_response = api_client.get(
        f"/payload/{second_response.json()['id']}"
    )

    assert payload_response.json() == {"output": "FROM CACHE, SECOND"}


def test_get_payload_returns_generated_output(api_client):
    create_response = api_client.post(
        "/payload",
        json={"list_1": ["hello"], "list_2": ["world"]},
    )
    payload_id = create_response.json()["id"]

    response = api_client.get(f"/payload/{payload_id}")

    assert response.status_code == 200
    assert response.json() == {"output": "HELLO, WORLD"}


def test_get_payload_returns_404_for_missing_payload(api_client):
    response = api_client.get("/payload/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Payload not found"}


def test_post_payload_rejects_lists_with_different_lengths(api_client):
    response = api_client.post(
        "/payload",
        json={"list_1": ["one", "two"], "list_2": ["three"]},
    )

    assert response.status_code == 422
