import pytest
from bis_fetcher.fetcher.chromedriver import ChromeWebDriver

# Constants for tests
VALID_URL = "https://www.python.org"
INVALID_URL = "https://invalid-url"


@pytest.mark.skip(reason="Need to skip this test in CI/CD")
def test_chromedriver_valid_url():
    driver = ChromeWebDriver(url=VALID_URL)
    print(driver.status_code, driver.title)
    assert driver.url == VALID_URL
    assert driver.status_code == 200
    assert driver.text != ""
    assert driver.title != ""


@pytest.mark.skip(reason="Need to skip this test in CI/CD")
def test_chromedriver_invalid_url():
    driver = ChromeWebDriver(url=INVALID_URL)
    assert driver.url == INVALID_URL
    assert driver.status_code == 0
    assert driver.text == ""
    assert driver.title == ""


if __name__ == "__main__":
    test_chromedriver_valid_url()
    test_chromedriver_invalid_url()
