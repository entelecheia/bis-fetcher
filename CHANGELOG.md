<!--next-version-placeholder-->

## v0.6.0 (2023-11-24)

### Feature

* **dockerfile:** Add tesseract-ocr and libtesseract-dev to Dockerfile.base ([`b534f5c`](https://github.com/entelecheia/bis-fetcher/commit/b534f5c1cbf7f794ac774e1e88c040e08795e8fe))
* **docker:** Add new env file with project id and other configurations ([`994f2e5`](https://github.com/entelecheia/bis-fetcher/commit/994f2e5fd4e89d18c662394928bf41c147753c1f))

## v0.5.0 (2023-11-11)

### Feature

* **bis_fetcher:** Add author and timestamp to fetched data, add support for fetching pdfs ([`231de01`](https://github.com/entelecheia/bis-fetcher/commit/231de01dd819b6ecb480ec324fb84c13935f84ed))
* **bis_fetcher:** Added use_selenium flag into request function ([`f6a1727`](https://github.com/entelecheia/bis-fetcher/commit/f6a1727f5105d348d900bc4856209291514ffd5b))
* **bis_fetcher:** Use base_url for article links, add use_selenium field and change _config_name_ value to "bis". ([`a9e3655`](https://github.com/entelecheia/bis-fetcher/commit/a9e3655aea5a8e848c55c86263bb77e8455d1f37))
* **bis_fetcher:** Add base_url to BaseFetcher ([`3575281`](https://github.com/entelecheia/bis-fetcher/commit/35752816ee9fcab23112a350be007a47043f7a32))
* **fetcher:** Replace selenium webdriver with chromedriver, introduce locator strategies and Response class in requests ([`b938086`](https://github.com/entelecheia/bis-fetcher/commit/b938086b2b409dcea18760b4e94dc72baaf199c7))
* **fetcher:** Add wait_time parameter and locator capability to ChromeWebDriver ([`369cb21`](https://github.com/entelecheia/bis-fetcher/commit/369cb215badb1041d833835bfc04c813d411e9fc))
* **bis_fetcher:** Add ChromeWebDriver class for fetching HTTP responses using Selenium ([`568c5cc`](https://github.com/entelecheia/bis-fetcher/commit/568c5ccdd64384240a2abc7afd6368e486044cd3))
* **bis_fetcher:** Add request method and driver method ([`22803da`](https://github.com/entelecheia/bis-fetcher/commit/22803dac57910e1fed4d6cc483098190702ac782))

## v0.4.0 (2023-11-10)

### Feature

* **pyproject.toml:** Add selenium dependency ([`6d59443`](https://github.com/entelecheia/bis-fetcher/commit/6d5944376efd010130a5e16189a80d1bc1916f0c))

## v0.3.0 (2023-11-10)

### Feature

* **docker:** Add Dockerfile.app and Dockerfile.base files ([`5912d5c`](https://github.com/entelecheia/bis-fetcher/commit/5912d5cb98e276d2dad49053ae59cacd13783b75))

## v0.2.0 (2023-11-09)

### Feature

* **fetcher:** Implement _next_page_func for handling, add support for start_urls and page_placeholder ([`fe89717`](https://github.com/entelecheia/bis-fetcher/commit/fe897179c55bdd267c7a686d56e1fd6a06e095da))
* **bis_fetcher:** Add BaseFetcher and BisFetcher classes ([`847dc7a`](https://github.com/entelecheia/bis-fetcher/commit/847dc7af220da1329f6e44be830530f3db7e1363))

## v0.1.1 (2023-09-25)

### Fix

* **.copier-config:** Update various configurations ([`8d3c95d`](https://github.com/entelecheia/bis-fetcher/commit/8d3c95d14fb1fe76de2f5c70f81bd95d54d789af))

### Documentation

* **README.md:** Update library description and token in codecov-image link ([`ad1c6aa`](https://github.com/entelecheia/bis-fetcher/commit/ad1c6aa504ca51c4732f2d7e65c7308e097ef90a))
* **book:** Add favicon and google analytics id to config ([`0cf569e`](https://github.com/entelecheia/bis-fetcher/commit/0cf569e9e0cb1b8bc0bde447be5d9299eeff833a))
* **book:** Update description and utility of 'bis-fetcher' library ([`0174a0e`](https://github.com/entelecheia/bis-fetcher/commit/0174a0ee40871b4e3930264af30a32c8a20a0885))

## v0.1.0 (2023-09-25)

### Feature

* Initial version ([`1ef112f`](https://github.com/entelecheia/bis-fetcher/commit/1ef112fb593cfcec73137ea5657683f5e4bf6b0c))
