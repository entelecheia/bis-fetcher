"""Command line interface for bis_fetcher"""

import argparse

from ._version import __version__

DESCRIPTION = (
    "A Python library that scrapes the BIS website to download and extract "
    "text from central bank speeches."
)


def main(argv: list[str] | None = None) -> None:
    """Main function for the CLI"""
    parser = argparse.ArgumentParser(prog="bis_fetcher", description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    print(f"BIS Fetcher {__version__}: {DESCRIPTION}")


if __name__ == "__main__":
    main()
