"""Offline regression tests for fetcher request handling."""

from pathlib import Path

import pytest
import requests

from bis_fetcher import jsonl
from bis_fetcher.fetcher import bis
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
    assert (out / "pdfs" / "r261019a.pdf").read_bytes() == pdf
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
    with pytest.raises(requests.Timeout):
        BisFetcher(request_timeout=(1.0, 2.0)).request(
            "https://www.bis.org/cbspeeches/index.htm", use_selenium=True
        )
    assert timeouts == [(1.0, 2.0)]


def test_pdf_named_like_a_record_file_does_not_overwrite_it(monkeypatch, tmp_path):
    class PdfResponse:
        content = (FIXTURES / "speech.pdf").read_bytes()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: PdfResponse())
    records = tmp_path / "articles.jsonl"
    records.write_text('{"url": "https://www.bis.org/review/r1.htm"}\n')
    BisFetcher(output_dir=str(tmp_path)).download_pdf("https://www.bis.org/x/articles.jsonl")
    assert records.read_text() == '{"url": "https://www.bis.org/review/r1.htm"}\n'


class _PdfResponse:
    content = (FIXTURES / "speech.pdf").read_bytes()

    def raise_for_status(self):
        pass


def test_pdf_without_text_layer_falls_back_to_ocr(monkeypatch, tmp_path):
    class NoTextPage:
        def extract_text(self):
            return ""

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: _PdfResponse())
    monkeypatch.setattr(bis, "PdfReader", lambda f: type("R", (), {"pages": [NoTextPage()]})())
    fetcher = BisFetcher(output_dir=str(tmp_path))
    url = "https://www.bis.org/review/r261019a.pdf"

    # The real OCR path returns one string per page.
    monkeypatch.setattr(bis, "convert_from_path", lambda path: ["page1", "page2"])
    monkeypatch.setattr(fetcher, "Deskew", lambda image: image)
    monkeypatch.setattr(fetcher, "extract_text_from_image", lambda image: f"ocr {image}")
    assert fetcher.download_pdf(url) == ["ocr page1", "ocr page2"]

    # OCR finds nothing either: a failure, so the article is retried later.
    monkeypatch.setattr(fetcher, "extract_text_from_image", lambda image: "  ")
    assert fetcher.download_pdf(url) is None
    assert fetcher._parse_article_text(url) is None


def test_direct_pdf_link_with_query_string_is_downloaded(monkeypatch, tmp_path):
    requested = []

    def get(url, **kwargs):
        requested.append(url)
        return _PdfResponse()

    monkeypatch.setattr(requests, "get", get)
    url = "https://www.bis.org/review/r261019a.PDF?download=1"
    article = BisFetcher(output_dir=str(tmp_path))._parse_article_text(url)
    assert article is not None and article["pdf_url"] == url and article["text"]
    assert requested == [url]  # fetched once as a PDF, not parsed as HTML first


def test_timed_out_listing_page_is_reported_not_empty(monkeypatch, caplog):
    def stalled_get(url, **kwargs):
        raise requests.Timeout("read timed out")

    monkeypatch.setattr(requests, "get", stalled_get)
    fetcher = BisFetcher(request_timeout=(1.0, 2.0))
    with pytest.raises(bis.PageFetchError):
        fetcher._parse_page_links("https://www.bis.org/cbspeeches/index.htm?cbspeeches_page=2")

    pages = {"p1": [{"url": "a"}]}

    def parse_page(page_url):
        if page_url in pages:
            return pages[page_url]
        return fetcher._parse_page_links(page_url)

    links = crawl_links(
        "p{page}",
        parse_page_func=parse_page,
        next_page_func=lambda start, current, page: start.format(page=page),
        max_num_pages=5,
    )
    assert [link["url"] for link in links] == ["a"]  # page 1 kept, crawl stopped at page 2
    assert "Failed to fetch page p2" in caplog.text


def test_missing_listing_page_ends_the_crawl_without_a_browser(monkeypatch):
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: type("R", (), {"status_code": 404})()
    )
    # Chrome is never started for an error page, so this runs without a browser.
    assert BisFetcher()._parse_page_links("https://www.bis.org/cbspeeches/index.htm") is None


@pytest.mark.parametrize("status", [403, 429, 500, 503])
def test_http_error_listing_page_is_reported_not_empty(monkeypatch, status):
    # Review of #96: only 404 stopped the crawl; other errors were parsed as empty pages.
    monkeypatch.setattr(requests, "get", lambda url, **kw: type("R", (), {"status_code": status})())
    with pytest.raises(bis.PageFetchError, match=str(status)):
        BisFetcher()._parse_page_links("https://www.bis.org/cbspeeches/index.htm")


def test_articles_saved_blank_before_are_retried_and_replaced(tmp_path):
    # Review of #96: rows saved with empty text by older versions were skipped forever.
    fetcher = BisFetcher(output_dir=str(tmp_path))
    fetcher._articles = [
        {"url": "a", "text": "kept"},
        {"url": "b", "text": ""},
        {"url": "c", "text": ["", " "]},
    ]
    assert fetcher._done_article_urls() == ["a"]
    fetcher.save_articles([{"url": "b", "text": "ocr"}])
    assert fetcher._articles == [
        {"url": "a", "text": "kept"},
        {"url": "c", "text": ["", " "]},
        {"url": "b", "text": "ocr"},
    ]


def test_article_limit_counts_fetches_not_skipped_links():
    # Review of #96: the limit counted link positions, so done links used it up.
    links = [{"url": f"u{i}", "title": "t"} for i in range(5)]
    fetched = []

    def parse(url):
        fetched.append(url)
        return {"text": "x"}

    done = ["u0", "u1", "u2"]
    articles = scrape_article_text(links, parse, article_urls=done, max_num_articles=1)
    assert fetched == ["u3"] and [a["url"] for a in articles] == ["u3"]
