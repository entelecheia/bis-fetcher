"""JSON Lines helpers (UTF-8, one ``json.dumps(..., ensure_ascii=False)`` object per line)."""

import json


def append_to_jsonl(data: dict, filename: str, encoding: str = "utf-8") -> None:
    """Append a json payload to the end of a jsonl file."""
    with open(filename, "a", encoding=encoding) as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def load_jsonl(filename: str, encoding: str = "utf-8") -> list[dict]:
    """Load a jsonl file into a list of json objects."""
    with open(filename, encoding=encoding) as f:
        return [json.loads(line) for line in f]


def save_jsonl(data: list[dict], filename: str, encoding: str = "utf-8") -> None:
    """Save a list of json objects to a jsonl file, overwriting it."""
    with open(filename, "w", encoding=encoding) as f:
        for line in data:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")


def remove_duplicates_from_list_of_dicts(data: list[dict], key: str) -> list[dict]:
    """Keep the first dict for each value of ``key``, preserving order."""
    seen = set()
    new_data = []
    for d in data:
        if d[key] not in seen:
            new_data.append(d)
            seen.add(d[key])
    return new_data
