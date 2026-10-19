"""Offline regression tests for fetcher request handling."""

from pathlib import Path

import requests

from bis_fetcher.fetcher.base import crawl_links
from bis_fetcher.fetcher.bis import BisFetcher

FIXTURES = Path(__file__).parent.parent / "fixtures"


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


def test_direct_pdf_link_is_downloaded(monkeypatch, tmp_path):
    class PdfResponse:
        content = (FIXTURES / "speech.pdf").read_bytes()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: PdfResponse())
    monkeypatch.chdir(tmp_path)
    (tmp_path / "workspace").mkdir()  # download_pdf writes here
    url = "https://www.bis.org/review/r261019a.pdf"
    article = BisFetcher()._parse_article_text(url)
    assert article is not None
    assert article["pdf_url"] == url
    assert article["text"]


def test_max_num_pages_visits_exactly_n_pages():
    visited = []

    def parse_page(page_url):
        visited.append(page_url)
        return [{"url": f"{page_url}#a"}]

    links = crawl_links(
        "listing?page={page}",
        parse_page_func=parse_page,
        next_page_func=lambda start, current, page: start.format(page=page),
        max_num_pages=2,
    )
    assert visited == ["listing?page=1", "listing?page=2"]
    assert len(links) == 2
