"""Offline run of the BIS fetch pipeline against saved fixtures.

``fixtures/expected/*`` was produced by commit 8ba4e28 (the code before the
dependency rewrite) running ``run_sample`` below, so this test pins the jsonl output.
Network, Selenium and multiprocessing are replaced in-process.
"""

import multiprocessing.dummy
from pathlib import Path

import pytest
import requests

from bis_fetcher.fetcher import base
from bis_fetcher.fetcher.bis import BisFetcher

FIXTURES = Path(__file__).parent.parent / "fixtures"
OUTPUT_FILES = ["links.jsonl", "links.jsonl.tmp", "articles.jsonl", "articles.jsonl.tmp"]

LISTING = """<html><body><div id="cbspeeches_list"><div>
<table class="documentList"><tbody>
<tr><td class="item_date">
  19 Oct 2026
</td><td><div><div class="title"><a href="/review/r261019a.htm">Monetary policy and price stability</a></div>
<a class="authorlnk dashed" href="#"> Jane Governor </a></div></td></tr>
<tr><td class="item_date">18 Oct 2026</td><td><div><div class="title"><a href="/review/r261018b.htm">Banque de France – stabilité financière</a></div></div></td></tr>
<tr><td>row without a title</td></tr>
</tbody></table></div></div></body></html>"""

PAGES = {
    "https://www.bis.org/cbspeeches/index.htm?m=256&cbspeeches_page=1": LISTING,
    "https://www.bis.org/review/r261019a.htm": (
        '<html><body><div class="pdftxt">'
        '<a class="pdftitle_link" href="/review/r261019a.pdf">PDF</a></div></body></html>'
    ),
    "https://www.bis.org/review/r261018b.htm": "<html><body><p>No PDF here</p></body></html>",
}


class _PdfResponse:
    content = (FIXTURES / "speech.pdf").read_bytes()

    def raise_for_status(self):
        pass


def _fake_request(self, url, **kwargs):
    if url not in PAGES:
        return base.Response(text="", status_code=404)
    return base.Response(text=PAGES[url], status_code=200)


def run_sample(workdir: Path) -> Path:
    """Fetch twice into ``workdir/out``; the second run re-scrapes existing articles."""
    out = workdir / "out"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(BisFetcher, "request", _fake_request)
        mp.setattr(requests, "get", lambda url, **kwargs: _PdfResponse())
        mp.setattr(base.mp, "Pool", multiprocessing.dummy.Pool)
        mp.chdir(workdir)
        (workdir / "workspace").mkdir(exist_ok=True)  # download_pdf writes here
        for overwrite in (False, True):
            BisFetcher(
                output_dir=str(out),
                max_num_pages=1,
                num_workers=1,
                overwrite_existing=overwrite,
            ).fetch()
    return out


def test_fetch_output_matches_pre_removal_output(tmp_path):
    out = run_sample(tmp_path)
    for name in OUTPUT_FILES:
        assert (out / name).read_bytes() == (FIXTURES / "expected" / name).read_bytes(), name


def test_fetcher_accepts_extra_fields():
    assert BisFetcher(unknown_option=1).unknown_option == 1
