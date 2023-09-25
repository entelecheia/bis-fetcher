# BIS Fetcher

[![pypi-image]][pypi-url]
[![version-image]][release-url]
[![release-date-image]][release-url]
[![license-image]][license-url]
[![jupyter-book-image]][docs-url]
[![codecov][codecov-image]][codecov-url]

<!-- Links: -->
[hyperfast python template]: https://github.com/entelecheia/hyperfast-python-template

[codecov-image]: https://codecov.io/gh/entelecheia/bis-fetcher/branch/main/graph/badge.svg?token=NfDlYO8LNh
[codecov-url]: https://codecov.io/gh/entelecheia/bis-fetcher
[pypi-image]: https://img.shields.io/pypi/v/bis-fetcher
[license-image]: https://img.shields.io/github/license/entelecheia/bis-fetcher
[license-url]: https://github.com/entelecheia/bis-fetcher/blob/main/LICENSE
[version-image]: https://img.shields.io/github/v/release/entelecheia/bis-fetcher?sort=semver
[release-date-image]: https://img.shields.io/github/release-date/entelecheia/bis-fetcher
[release-url]: https://github.com/entelecheia/bis-fetcher/releases
[jupyter-book-image]: https://jupyterbook.org/en/stable/_images/badge.svg

[repo-url]: https://github.com/entelecheia/bis-fetcher
[pypi-url]: https://pypi.org/project/bis-fetcher
[docs-url]: https://entelecheia.github.io/bis-fetcher
[changelog]: https://github.com/entelecheia/bis-fetcher/blob/main/CHANGELOG.md
[contributing guidelines]: https://github.com/entelecheia/bis-fetcher/blob/main/CONTRIBUTING.md
<!-- Links: -->

A Python library that scrapes the BIS website to download and extract text from central bank speeches.

- Documentation: [https://entelecheia.github.io/bis-fetcher][docs-url]
- GitHub: [https://github.com/entelecheia/bis-fetcher][repo-url]
- PyPI: [https://pypi.org/project/bis-fetcher][pypi-url]

`bis-fetcher` is a Python library that programmatically scrapes the website of the Bank for International Settlements (BIS) to download PDF files of all available central bank speeches. It then extracts the text from these PDFs.

The library allows easy access to a comprehensive dataset of central bank speeches over time. Researchers can use this data to perform quantitative analysis of central bank communication and track changes in tone, topics, and sentiment.

The BIS hosts speeches by governors and other senior officials from central banks around the world. However, scraping the website manually is tedious. bis-fetcher automates the entire workflow from crawling the site to text extraction.

It provides a simple API to get a list of available speeches, download the PDFs, and extract text. The text can be further processed or fed into models for analysis.

## Changelog

See the [CHANGELOG] for more information.

## Contributing

Contributions are welcome! Please see the [contributing guidelines] for more information.

## License

This project is released under the [MIT License][license-url].

## Table of Contents

```{tableofcontents}
```
