from bis_fetcher.fetcher.bis import BisFetcher


def test_bisfetcher():
    b = BisFetcher(start_page=1)
    b.fetch()


if __name__ == "__main__":
    test_bisfetcher()
