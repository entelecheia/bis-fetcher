import logging
from typing import Optional, Tuple

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class ChromeWebDriver:
    """
    ChromeWebDriver class to fetch the HTTP response for a given URL

    Implementation of the Selenium Chrome WebDriver
    with HTTP Response data included via the ChromeDriver performance logging capability
    https://sites.google.com/a/chromium.org/chromedriver/logging/performance-log
    The ChromeWebDriver response attribute(s) contain a dict with information about the response
    {
        "connectionId": [Integer],
        "connectionReused": [Boolean],
        "encodedDataLength": [Integer],
        "fromDiskCache": [Boolean],
        "fromServiceWorker": [Boolean],
        "headers": [dict], # HTTP Headers as a dict
        "headersText": [String], # HTTP Headers as text
        "mimeType": [String],
        "protocol": [String],
        "remoteIPAddress": [String],
        "remotePort": [Integer],
        "requestHeaders": [dict],
        "requestHeadersText": [String],
        "securityDetails": [dict], # TLS/SSL related information
        "securityState": [String],
        "status": [Integer], # HTTP Status Code of the Response
        "statusText": [String],
        "timing": [dict],
        "url": [String]
    }
    """

    autoclose: bool = True
    options: Options = None
    status_code: int = 0
    text: str = ""
    title: str = ""
    url: str
    wait_time: int = 10

    _driver: Optional[webdriver.Chrome] = None

    def __init__(
        self,
        url: Optional[str] = None,
        headless: bool = True,
        no_sandbox: bool = True,
        disable_dev_shm_usage: bool = True,
        autoclose: bool = True,
        wait_time: int = 10,
    ):
        """
        Initializes a ChromeWebDriver instance.

        Args:
            url (Optional[str]): URL to fetch. Defaults to None.
            headless (bool): Whether to run the ChromeWebDriver in headless mode. Defaults to True.
            no_sandbox (bool): Whether to disable the Chrome sandbox. Defaults to True.
            disable_dev_shm_usage (bool): Whether to disable the /dev/shm usage. Defaults to True.
            autoclose (bool): Whether to automatically close the ChromeWebDriver instance. Defaults to True.
            wait_time (int): The maximum time to wait for the page to load, in seconds. Defaults to 1.
        """
        self.url = url  # URL to fetch
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        if no_sandbox:
            self.options.add_argument("--no-sandbox")
        if disable_dev_shm_usage:
            self.options.add_argument("--disable-dev-shm-usage")
        self.autoclose = autoclose
        self.wait_time = wait_time

        self._driver = None
        self.text = ""
        self.title = ""
        self.status_code = 0
        if url is not None:
            self.get(url)

    @property
    def driver(self):
        """
        Property that returns the ChromeWebDriver instance.

        Returns:
            ChromeWebDriver: The ChromeWebDriver instance.
        """
        if self._driver is None or self._driver.session_id is None:
            self._driver = webdriver.Chrome(options=self.options)
        return self._driver

    def get(
        self,
        url: str,
        wait_time: Optional[int] = None,
        locator: Optional[Tuple[str, str]] = None,
    ) -> "ChromeWebDriver":
        """
        Fetches the HTTP response for the given URL using the ChromeWebDriver.

        This method sets the URL to fetch and attempts to fetch the response.
        If an error occurs during the fetch, it logs the error and closes the ChromeWebDriver instance.

        Args:
            url (str): The URL to fetch.
            wait_time (int, optional): The maximum time to wait for the page to load, in seconds. Defaults to 10.
            wait_for_element_id (str, optional): The ID of the element to wait for. Defaults to None.

        Returns:
            ChromeWebDriver: The ChromeWebDriver instance.
        """
        self.url = url  # set the URL to fetch
        wait_time = wait_time or self.wait_time
        try:
            self._get(
                url,
                wait_time,
                locator=locator,
            )
        except Exception as e:
            logger.error("Error while fetching the url: %s", url)
            logger.error(e)
            self.close()
        return self

    def _get(
        self,
        url: str,
        wait_time: int = 10,
        locator: Optional[Tuple[str, str]] = None,
    ):
        self.status_code = requests.get(url).status_code  # get the HTTP status code
        self.driver.get(url)  # get the requested URL
        self.driver.refresh()
        if wait_time > 0 and locator is not None:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
        self.title = self.driver.title
        self.text = self.driver.page_source
        if self.autoclose:
            self.close()

    def close(self):
        """
        Closes the ChromeWebDriver instance.

        This method closes the ChromeWebDriver instance by closing the current window
        and quitting the driver, releasing all associated resources.
        """
        if self._driver is not None:
            self._driver.close()
