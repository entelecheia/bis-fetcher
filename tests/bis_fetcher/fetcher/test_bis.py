from bis_fetcher.fetcher.bis import BisFetcher


def test_bisfetcher():
    b = BisFetcher(num_workers=1)
    b.fetch()


if __name__ == '__main__':
    test_bisfetcher()