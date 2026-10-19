<!--next-version-placeholder-->

## v1.0.0 (2026-10-19)

### Bug Fixes

- Add connect/read timeouts to every HTTP request
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Fail the release build when uv.lock cannot be refreshed
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- Keep articles retryable when the PDF download fails
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Pass the fetcher request_timeout to the Chrome status request
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Pass the URL to download_pdf for direct PDF links
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Refresh uv.lock in the release build; add REVIEW.md
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- Resolve follow-up issues (#81, #82, #83, #87, #90, #91)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Save downloaded PDFs in a pdfs/ subdirectory
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Save downloaded PDFs under the fetcher output directory
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Stop crawl_links after exactly max_num_pages pages
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

### Build System

- Move tooling to uv, hatchling, ruff and PSR v10
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- **deps**: Bump docutils from 0.17.1 to 0.20.1
  ([`df7ebc2`](https://github.com/entelecheia/bis-fetcher/commit/df7ebc20e205ec832f405de37737e5777164bb05))

### Chores

- Drop Codecov (config, upload step, badges)
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- Remove the HyFI dependency ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- Update lint_and_test.yaml
  ([`3b8cfa6`](https://github.com/entelecheia/bis-fetcher/commit/3b8cfa61c550f8105b51307fbec7c2b8c70647f9))

- Update poetry.lock
  ([`f0e2d0d`](https://github.com/entelecheia/bis-fetcher/commit/f0e2d0d9cbbadfc85cfe0d3e86d771146cfbf0a2))

- Update requirements.txt
  ([`8256e2f`](https://github.com/entelecheia/bis-fetcher/commit/8256e2f5a4a6df4c482df17d458360e049cc0813))

- **deps**: Bump actions/setup-python from 4 to 5
  ([`e7d5628`](https://github.com/entelecheia/bis-fetcher/commit/e7d5628adc04594a9ee398a798596ec9b311a2e4))

- **deps**: Bump codecov/codecov-action from 3 to 4
  ([`18e3bc0`](https://github.com/entelecheia/bis-fetcher/commit/18e3bc041051b07f2384c59a3218bb03c3acb931))

- **deps**: Bump codecov/codecov-action from 4 to 5
  ([`8bea0d6`](https://github.com/entelecheia/bis-fetcher/commit/8bea0d6676235282703977d269d7ab386e323f8a))

- **deps**: Bump docker/build-push-action from 5.1.0 to 5.3.0
  ([`c4316a8`](https://github.com/entelecheia/bis-fetcher/commit/c4316a8bf397a72b93d8afd8d2375a64aabce6ec))

- **deps**: Bump docker/build-push-action from 5.3.0 to 6.0.1
  ([`5bcbe80`](https://github.com/entelecheia/bis-fetcher/commit/5bcbe80e71c684f4317011dfbad2269e78b0b9b5))

- **deps**: Bump docker/build-push-action from 6.0.1 to 6.0.2
  ([`608cc7f`](https://github.com/entelecheia/bis-fetcher/commit/608cc7fb164f0cedd1adb850e0c5d8f646ddcfdc))

- **deps**: Bump docker/build-push-action from 6.0.2 to 6.2.0
  ([`8795dca`](https://github.com/entelecheia/bis-fetcher/commit/8795dcabd5e5717deeec781b79fa9026aae65d8b))

- **deps**: Bump docker/build-push-action from 6.2.0 to 6.3.0
  ([`0138ed6`](https://github.com/entelecheia/bis-fetcher/commit/0138ed6f915604ed902b5014e55aa249da0e23c6))

- **deps**: Bump docker/build-push-action from 6.3.0 to 6.4.1
  ([`4894a60`](https://github.com/entelecheia/bis-fetcher/commit/4894a60a700b67fc0d50e3e4edc3484bc1edd968))

- **deps**: Bump docker/build-push-action from 6.4.1 to 6.5.0
  ([`8f81de9`](https://github.com/entelecheia/bis-fetcher/commit/8f81de959f322b9f90317a4fbbb4327406a445e4))

- **deps**: Bump docker/build-push-action from 6.5.0 to 6.6.1
  ([`4ecff99`](https://github.com/entelecheia/bis-fetcher/commit/4ecff9957fa72a79b6b2e2bd36627195efbc725e))

- **deps**: Bump docker/build-push-action from 6.6.1 to 6.7.0
  ([`a292915`](https://github.com/entelecheia/bis-fetcher/commit/a292915dbf6097c2f8f6e92c45a746616fbd064c))

- **deps**: Bump docker/build-push-action from 6.7.0 to 6.9.0
  ([`a66f2e3`](https://github.com/entelecheia/bis-fetcher/commit/a66f2e36e445e9cc2cf8a13e92eb4f55a2c97b00))

- **deps**: Bump docker/build-push-action from 6.9.0 to 6.12.0
  ([`a43879d`](https://github.com/entelecheia/bis-fetcher/commit/a43879d5e7a0d2833ddad1bd5c12d41de60f3513))

- **deps**: Bump docker/login-action from 3.0.0 to 3.1.0
  ([`276b2c3`](https://github.com/entelecheia/bis-fetcher/commit/276b2c3cc8d404b87a83915ae06dcdbdbbbadc54))

- **deps**: Bump docker/login-action from 3.1.0 to 3.2.0
  ([`7a59408`](https://github.com/entelecheia/bis-fetcher/commit/7a5940835dfb6a5b9cbf4edfa8743e17a98463e5))

- **deps**: Bump docker/login-action from 3.2.0 to 3.3.0
  ([`4b1cf15`](https://github.com/entelecheia/bis-fetcher/commit/4b1cf15358bbdf94d150ccf95a97b9be53cd82b5))

- **deps**: Bump docker/metadata-action from 5.0.0 to 5.2.0
  ([`516ba5f`](https://github.com/entelecheia/bis-fetcher/commit/516ba5fe19d49749e6791b39f11c152ab66ae65f))

- **deps**: Bump docker/metadata-action from 5.2.0 to 5.3.0
  ([`13643c6`](https://github.com/entelecheia/bis-fetcher/commit/13643c6b2ede3b72d436ec70866077cbee83862e))

- **deps**: Bump docker/metadata-action from 5.3.0 to 5.4.0
  ([`03b1a76`](https://github.com/entelecheia/bis-fetcher/commit/03b1a766206f99a0e05cd0a3ea6ed08a185da28c))

- **deps**: Bump docker/metadata-action from 5.4.0 to 5.5.0
  ([`4643398`](https://github.com/entelecheia/bis-fetcher/commit/46433987da90abbff25f8023b14fa59afa240b9a))

- **deps**: Bump docker/metadata-action from 5.5.0 to 5.5.1
  ([`05757e5`](https://github.com/entelecheia/bis-fetcher/commit/05757e55358a578efd758fe4cdec189ddf7b8426))

- **deps**: Bump docker/metadata-action from 5.5.1 to 5.6.1
  ([`b55acd2`](https://github.com/entelecheia/bis-fetcher/commit/b55acd2445374807566930d2636d240b084e71df))

- **deps**: Bump peaceiris/actions-gh-pages from 3 to 4
  ([`19185c3`](https://github.com/entelecheia/bis-fetcher/commit/19185c3677dfabfd4d98e5e60636e5f5599638a5))

- **deps**: Bump selenium from 4.16.0 to 4.17.2
  ([`c445be3`](https://github.com/entelecheia/bis-fetcher/commit/c445be37587f7b17a6a5bc360b90babb482d9a21))

- **deps**: Bump selenium from 4.17.2 to 4.21.0
  ([`c963fa4`](https://github.com/entelecheia/bis-fetcher/commit/c963fa4038ac9c9ffc706aa1edd49542ae4730e0))

### Code Style

- Apply ruff fixes and formatting ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

### Continuous Integration

- Always validate PRs beyond the files API limit (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Build the book with uv instead of pip (#85)
  ([#86](https://github.com/entelecheia/bis-fetcher/pull/86),
  [`c3cbba1`](https://github.com/entelecheia/bis-fetcher/commit/c3cbba1698dd1e42510b9fb431c5457f94797723))

- Count renamed paths and avoid grep -q in the docs-only check (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Let workflow_call run the app image deploy
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Make releases retryable and keep ci-ok reported for docs-only PRs (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Pin Docker image workflow actions and fix the always-true if
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Pin the Pages action and serialize book deploys
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Run full validation when the PR files API fails (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- State that only tags from this release workflow can be republished (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

- Validate the tag before a republish (entelecheia/hyfi#479)
  ([#89](https://github.com/entelecheia/bis-fetcher/pull/89),
  [`b298d74`](https://github.com/entelecheia/bis-fetcher/commit/b298d74fcbb28bfc87669c8c148930ed739acb3a))

### Features

- Implement the BisFetcher class
  ([`9bb8fc0`](https://github.com/entelecheia/bis-fetcher/commit/9bb8fc0eabd4d2e0f91ea5459faf3652f43a46e2))

### Refactoring

- Replace HyFI with pydantic and a local jsonl module
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

### Testing

- Cover the argparse CLI in process ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))

- Opt in to live BIS tests only with BIS_LIVE_TESTS=1
  ([#80](https://github.com/entelecheia/bis-fetcher/pull/80),
  [`9d5ec42`](https://github.com/entelecheia/bis-fetcher/commit/9d5ec4262fc1033bae35680bc704c4711f76cf16))


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
