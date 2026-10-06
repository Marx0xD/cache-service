from backend.src.utils.hash import hash_request


def test_identical_inputs_produce_identical_hashes():
    first_hash = hash_request(["one", "two"], ["three", "four"])
    second_hash = hash_request(["one", "two"], ["three", "four"])

    assert first_hash == second_hash


def test_changed_content_produces_different_hash():
    original_hash = hash_request(["one", "two"], ["three", "four"])
    changed_hash = hash_request(["one", "changed"], ["three", "four"])

    assert original_hash != changed_hash


def test_changed_ordering_produces_different_hash():
    original_hash = hash_request(["one", "two"], ["three", "four"])
    reordered_hash = hash_request(["two", "one"], ["three", "four"])

    assert original_hash != reordered_hash
