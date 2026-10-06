import hashlib
import json


# Keep both lists distinct so different input structures cannot produce the same hash.
# # SHA-256 provides a  low-collision identifier for the request contents.
def hash_request(list_1: list[str], list_2: list[str]) -> str:
    data = json.dumps(
        {"list_1": list_1, "list_2": list_2},
        separators=(",", ":"),
    )

    return hashlib.sha256(data.encode()).hexdigest()
