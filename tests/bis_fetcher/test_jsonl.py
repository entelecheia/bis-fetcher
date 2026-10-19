"""The jsonl helpers keep the previous helpers' output byte for byte."""

from bis_fetcher import jsonl

ROWS = [{"url": "a", "title": "Économie – 経済"}, {"url": "b", "n": 1, "x": None}]
EXPECTED = '{"url": "a", "title": "Économie – 経済"}\n{"url": "b", "n": 1, "x": null}\n'


def test_save_jsonl_writes_utf8_lines_and_overwrites(tmp_path):
    f = tmp_path / "out.jsonl"
    f.write_text("stale\n", encoding="utf-8")
    jsonl.save_jsonl(ROWS, str(f))
    assert f.read_bytes() == EXPECTED.encode("utf-8")


def test_append_to_jsonl_appends_one_line(tmp_path):
    f = tmp_path / "out.jsonl"
    for row in ROWS:
        jsonl.append_to_jsonl(row, str(f))
    assert f.read_bytes() == EXPECTED.encode("utf-8")


def test_load_jsonl_round_trips(tmp_path):
    f = tmp_path / "in.jsonl"
    f.write_bytes(EXPECTED.encode("utf-8"))
    assert jsonl.load_jsonl(str(f)) == ROWS


def test_remove_duplicates_keeps_first_in_order():
    data = [{"url": "a", "v": 1}, {"url": "b"}, {"url": "a", "v": 2}, {"url": "c"}]
    assert jsonl.remove_duplicates_from_list_of_dicts(data, key="url") == [
        {"url": "a", "v": 1},
        {"url": "b"},
        {"url": "c"},
    ]
