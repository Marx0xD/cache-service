from backend.src.service.transform_cache_service import TransformCacheService


def test_create_transform_cache(db_session):
    service = TransformCacheService(db_session)

    cached_result = service.create("input-value", "output-value")

    assert cached_result.id is not None
    assert cached_result.input == "input-value"
    assert cached_result.output == "output-value"


def test_get_transform_cache_by_input(db_session):
    service = TransformCacheService(db_session)
    created = service.create("input-value", "output-value")

    cached_result = service.get_by_input("input-value")

    assert cached_result is not None
    assert cached_result.id == created.id
    assert cached_result.input == "input-value"
    assert cached_result.output == "output-value"
