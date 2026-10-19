"""Offline regression tests for fetcher request handling."""

from pathlib import Path

import requests

from bis_fetcher import jsonl
from bis_fetcher.fetcher.base import crawl_links, scrape_article_text
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
    url = "https://www.bis.org/review/r261019a.pdf"
    article = BisFetcher(output_dir=str(tmp_path))._parse_article_text(url)
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


def test_pdf_is_saved_under_output_dir(monkeypatch, tmp_path):
    pdf = (FIXTURES / "speech.pdf").read_bytes()

    class PdfResponse:
        content = pdf

        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: PdfResponse())
    monkeypatch.chdir(tmp_path)  # no workspace/ here
    out = tmp_path / "out" / "bis"
    fetcher = BisFetcher(output_dir=str(out))
    assert fetcher.download_pdf("https://www.bis.org/review/r261019a.pdf?x=1")
    assert (out / "r261019a.pdf").read_bytes() == pdf
    assert fetcher.download_pdf("https://www.bis.org/review/..") is None
    assert [p.name for p in tmp_path.rglob("*") if p.is_file()] == ["r261019a.pdf"]


def test_failed_pdf_download_is_retried_on_the_next_run(monkeypatch, tmp_path):
    class PdfResponse:
        content = (FIXTURES / "speech.pdf").read_bytes()

        def raise_for_status(self):
            pass

    def timed_out(url, **kwargs):
        raise requests.Timeout("read timed out")

    url = "https://www.bis.org/review/r261019a.pdf"
    links = [{"url": url, "title": "Speech"}]
    saved = tmp_path / "articles.jsonl"
    fetcher = BisFetcher(output_dir=str(tmp_path))

    def run():
        done = [a["url"] for a in jsonl.load_jsonl(str(saved))] if saved.exists() else []
        return scrape_article_text(
            links, fetcher._parse_article_text, article_urls=done, article_filepath=str(saved)
        )

    monkeypatch.setattr(requests, "get", timed_out)
    assert run() == []
    assert not saved.exists()

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: PdfResponse())
    articles = run()
    assert [a["url"] for a in articles] == [url]
    assert articles[0]["text"]


def test_selenium_status_request_uses_fetcher_timeout(monkeypatch):
    timeouts = []

    def stalled_get(url, **kwargs):
        timeouts.append(kwargs.get("timeout"))
        raise requests.Timeout("read timed out")

    monkeypatch.setattr(requests, "get", stalled_get)
    response = BisFetcher(request_timeout=(1.0, 2.0)).request(
        "https://www.bis.org/cbspeeches/index.htm", use_selenium=True
    )
    assert response.status_code == 0
    assert timeouts == [(1.0, 2.0)]
