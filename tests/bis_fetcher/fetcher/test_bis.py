from bis_fetcher.fetcher.bis import BisFetcher


def test_bisfetcher():
    b = BisFetcher(max_num_pages=3, overwrite_existing= True)
    b.fetch()


if __name__ == "__main__":
    test_bisfetcher()
