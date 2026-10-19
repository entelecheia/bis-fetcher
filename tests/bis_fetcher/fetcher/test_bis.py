import os

import pytest

from bis_fetcher.fetcher.bis import BisFetcher


@pytest.mark.skipif(
    not os.environ.get("BIS_LIVE_TESTS"), reason="hits bis.org with Chrome; set BIS_LIVE_TESTS=1"
)
def test_bisfetcher():
    b = BisFetcher(max_num_pages=3, overwrite_existing=True)
    b.fetch()


if __name__ == "__main__":
    test_bisfetcher()
