"""Offline regression tests for fetcher request handling."""

import requests

from bis_fetcher.fetcher.bis import BisFetcher


def test_timeout_skips_article_instead_of_failing(monkeypatch):
    timeouts = []

    def stalled_get(url, **kwargs):
        # A stalled server: without a timeout the real call would hang forever.
        timeouts.append(kwargs.get("timeout"))
        raise requests.Timeout("read timed out")

    monkeypatch.setattr(requests, "get", stalled_get)
    fetcher = BisFetcher(request_timeout=(1.0, 2.0))
    assert fetcher._parse_article_text("https://www.bis.org/review/r261019a.htm") is None
    assert fetcher.download_pdf("https://www.bis.org/review/r261019a.pdf") is None
    assert timeouts == [(1.0, 2.0), (1.0, 2.0)]
