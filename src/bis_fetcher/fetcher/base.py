"""Base Fetcher"""
import logging
import multiprocessing as mp
import time
from functools import partial
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import requests
from hyfi.composer import BaseModel
from hyfi.main import HyFI

from .chromedriver import ChromeWebDriver

logger = logging.getLogger(__name__)


class Response(BaseModel):
    text: str = ""
    status_code: int = 0


class By:
    """Set of supported locator strategies."""

    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


class BaseFetcher(BaseModel):
    """
    Base Fetcher
    """

    _config_name_: str = "base"
    _config_group_: str = "/fetcher"

    article_filename: str = "articles.jsonl"
    base_url: str = ""
    delay_between_requests: float = 0.0
    key_field: str = "url"
    keyword_placeholder: str = "{keyword}"
    link_filename: str = "links.jsonl"
    max_num_articles: Optional[int] = 30
    max_num_pages: Optional[int] = 2
    num_workers: int = 1
    output_dir: str = f"workspace/datasets{_config_group_}/{_config_name_}"
    overwrite_existing: bool = False
    page_placeholder: str = "{page}"
    print_every: int = 10
    search_keywords: List[str] = []
    search_url: str = ""
    start_page: Optional[int] = 1
    start_urls: List[str] = []
    verbose: bool = True

    _links: List[dict] = []
    _articles: List[dict] = []
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def __call__(self):
        self.fetch()

    def fetch(self):
        self.fetch_links()
        self.fetch_articles()

    def request(
        self,
        url: str,
        use_selenium: bool = False,
        wait_time: int = 10,
        locator: Optional[Tuple[str, str]] = None,
        params: dict = None,
        **kwargs,
    ) -> Response:
        """Sends a GET request.

        Args:
            url (str): URL for the request
            params (dict, optional): Dictionary, list of tuples or bytes to send
                in the query string for the Request. Defaults to None.
            **kwargs: Optional arguments that `request` takes.

        Returns:
            Response object containing response text and status code
        """
        if use_selenium:
            driver = ChromeWebDriver().get(
                url,
                wait_time=wait_time,
                locator=locator,
            )
            return Response(text=driver.text, status_code=driver.status_code)
        res = requests.get(url, params=params, headers=self._headers, **kwargs)
        return Response(text=res.text, status_code=res.status_code)

    @property
    def start_urls_encoded(self):
        if self.start_urls:
            return self.start_urls
        if self.keyword_placeholder in self.search_url:
            # Generate start URLs by replacing keyword placeholder with encoded keywords
            start_urls = [
                self.search_url.replace(
                    self.keyword_placeholder, self.encode_keyword(keyword)
                )
                for keyword in self.search_keywords
            ]
        else:
            start_urls = [self.search_url]
        return start_urls

    def encode_keyword(self, keyword: str):
        return keyword.replace(" ", "+")

    @property
    def links(self):
        return self._links or self._load_links()

    @property
    def articles(self):
        return self._articles or self._load_articles()

    @property
    def link_filepath(self) -> str:
        _path = Path(self.output_dir) / self.link_filename
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path.absolute())

    @property
    def article_filepath(self) -> str:
        _path = Path(self.output_dir) / self.article_filename
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path.absolute())

    @property
    def link_filepath_tmp(self) -> str:
        _path = Path(self.output_dir) / f"{self.link_filename}.tmp"
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path)

    @property
    def article_filepath_tmp(self) -> str:
        _path = Path(self.output_dir) / f"{self.article_filename}.tmp"
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def _load_links(self) -> List[dict]:
        if Path(self.link_filepath).exists():
            self._links = HyFI.load_jsonl(self.link_filepath)
        return self._links

    def _load_articles(self) -> List[dict]:
        if Path(self.article_filepath).exists():
            self._articles = HyFI.load_jsonl(self.article_filepath)
        return self._articles

    def fetch_links(self):
        parse_page_func = partial(
            self._parse_page_links,
            print_every=self.print_every,
            verbose=self.verbose,
        )

        next_page_func = partial(
            self._next_page_func,
            page_placeholder=self.page_placeholder,
        )

        self._fetch_links(parse_page_func, next_page_func)

    def fetch_articles(self):
        parse_article_text = partial(self._parse_article_text)

        self._fetch_articles(parse_article_text)

    def _fetch_links(self, parse_page_func: Callable, next_page_func: Callable):
        num_workers = min(self.num_workers, len(self.search_keywords))
        num_workers = max(num_workers, 1)
        link_urls = [link["url"] for link in self.links]
        fetch_links_func = partial(
            crawl_links,
            parse_page_func=parse_page_func,
            next_page_func=next_page_func,
            start_page=self.start_page,
            max_num_pages=self.max_num_pages,
            link_urls=link_urls,
            link_filepath=self.link_filepath_tmp,
            delay_between_requests=self.delay_between_requests,
        )
        if links := self._fetch_links_mp(
            num_workers,
            fetch_links_func,
        ):
            self.save_links(links)
        else:
            logger.info("No more links found")

    def save_links(self, links: List[dict]):
        self._links.extend(links)
        original_len = len(self._links)
        self._links = HyFI.remove_duplicates_from_list_of_dicts(
            self._links, key=self.key_field
        )
        logger.info(
            "Removed %s duplicate links from %s links",
            original_len - len(self._links),
            original_len,
        )
        HyFI.save_jsonl(self._links, self.link_filepath)
        logger.info("Saved %s links to %s", len(self._links), self.link_filepath)

    def _fetch_links_mp(
        self,
        num_workers: int,
        batch_func: Callable,
    ) -> List[dict]:
        with mp.Pool(num_workers) as pool:
            results = pool.map(batch_func, self.start_urls_encoded)
        links = []
        for result in results:
            links.extend(result)
        return links

    def _fetch_articles(self, parse_article_func: Callable):
        num_workers = min(self.num_workers, len(self.links))
        article_urls = [article["url"] for article in self.articles]
        fetch_articles_func = partial(
            scrape_article_text,
            parse_article_func=parse_article_func,
            article_urls=article_urls,
            overwrite_existing=self.overwrite_existing,
            article_filepath=self.article_filepath_tmp,
            max_num_articles=self.max_num_articles,
            delay_between_requests=self.delay_between_requests,
            print_every=self.print_every,
            verbose=self.verbose,
        )
        if articles := self._fetch_articles_mp(num_workers, fetch_articles_func):
            self.save_articles(articles)
        else:
            logger.info("No more articles found")

    def save_articles(self, articles: List[dict]):
        self._articles.extend(articles)
        original_len = len(self._articles)
        self._articles = HyFI.remove_duplicates_from_list_of_dicts(
            self._articles, key=self.key_field
        )
        logger.info(
            "Removed %s duplicate articles from %s articles",
            original_len - len(self._articles),
            original_len,
        )
        HyFI.save_jsonl(self._articles, self.article_filepath)
        logger.info(
            "Saved %s articles to %s",
            len(self._articles),
            self.article_filepath,
        )

    def _fetch_articles_mp(
        self,
        num_workers: int,
        batch_func: Callable,
    ) -> List[dict]:
        articles = []
        if len(self.links) < 1:
            return articles
        batch_size = len(self.links) // num_workers
        batches = [
            self.links[i : i + batch_size]
            for i in range(0, len(self.links), batch_size)
        ]
        with mp.Pool(num_workers) as pool:
            results = pool.map(batch_func, batches)
        for result in results:
            articles.extend(result)
        return articles

    def _next_page_func(
        self,
        start_url: str,
        current_url: Optional[str],
        page: int,
        page_placeholder: Optional[str],
    ) -> Optional[str]:
        if page_placeholder and page_placeholder in start_url:
            # Return next page url by replacing placeholder with page number
            page_url = start_url.replace(page_placeholder, str(page))
        elif current_url is None:
            page_url = start_url
        else:
            # TODO: implement your next page logic to return None if no more pages
            raise NotImplementedError("Next page logic not implemented in base class")
        logger.info("Page url: %s", page_url)
        return page_url

    def _parse_page_links(
        self,
        page_url: str,
        print_every: int = 10,
        verbose: bool = False,
    ) -> Optional[List[dict]]:
        """Get the links from the given page."""

        # TODO: Parse the page and extract all links
        raise NotImplementedError("Parsing links is not implemented in base class")

    def _parse_article_text(self, url: str) -> dict:
        # TODO: Scrape the article page and extract the text
        raise NotImplementedError(
            "Parsing article text is not implemented in base class"
        )


def crawl_links(
    start_url: str,
    parse_page_func: Callable,
    next_page_func: Callable,
    start_page: int = 1,
    max_num_pages: Optional[int] = 2,
    link_urls: Optional[List[str]] = None,
    link_filepath: Optional[str] = None,
    delay_between_requests: float = 0.0,
) -> List[dict]:
    """Crawl links for article links with the given keyword.

    Args:
        keyword (str): Keyword to search for.
        search_url (str, optional): URL to search for the keyword. Defaults to "https://www.khmertimeskh.com/page/{page}/?s={keyword}".
        links (List[dict], optional): List of links to append to. Defaults to None.
        max_num_pages (Optional[int], optional): Maximum number of pages to crawl. Defaults to 2.
        link_filepath (Optional[str], optional): Filepath to save the links to. Defaults to None.
        print_every (int, optional): Print progress every n pages. Defaults to 10.
        verbose (bool, optional): Print progress. Defaults to False.

    Returns:
        List[dict]: List of links.
    """

    page = start_page
    page_cnt = 0
    page_url = None
    links = []
    link_urls = link_urls or []
    logger.info("Fetching links for url: %s", start_url)
    while True:
        # get next page url
        page_url = next_page_func(start_url, page_url, page)
        # Parse page
        page_links = parse_page_func(page_url)

        # Check if page_links is None
        if page_links is None:
            logger.info("No more links found, stopping...")
            break

        for link in page_links:
            if link["url"] not in link_urls:
                link["page_url"] = page_url
                link["page"] = page
                links.append(link)
                link_urls.append(link["url"])
                if link_filepath:
                    HyFI.append_to_jsonl(link, link_filepath)
            else:
                logger.info(
                    "Link %s already exists, skipping...",
                    link["url"],
                )

        page += 1
        page_cnt += 1

        if max_num_pages and page_cnt > max_num_pages:
            logger.info("Reached max number of pages, stopping...")
            break
        # Delay between requests
        if delay_between_requests > 0:
            logger.info("Sleeping for %s seconds...", delay_between_requests)
            time.sleep(delay_between_requests)

    logger.info("Finished fetching links for url: %s", start_url)
    logger.info("Total links fetched: %s", len(links))
    return links


def scrape_article_text(
    links: List[dict],
    parse_article_func: Callable,
    article_urls: Optional[List[dict]] = None,
    overwrite_existing: bool = False,
    max_num_articles: Optional[int] = 10,
    article_filepath: Optional[str] = None,
    delay_between_requests: float = 0.0,
    print_every: int = 10,
    verbose: bool = False,
) -> List[dict]:
    """Scrape the article text from the given links.

    Args:
        links (List[dict]): List of links to scrape.
        articles (Optional[List[dict]], optional): List of articles to append to. Defaults to None.
        overwrite_existing (bool, optional): Overwrite existing articles. Defaults to False.
        max_num_articles (Optional[int], optional): Maximum number of articles to scrape. Defaults to 10.
        article_filepath (Optional[str], optional): Filepath to save the articles to. Defaults to None.
        print_every (int, optional): Print progress every n articles. Defaults to 10.
        verbose (bool, optional): Print progress. Defaults to False.

    Returns:
        List[dict]: List of articles.
    """
    articles = []
    article_urls = article_urls or []
    for i, link in enumerate(links):
        if max_num_articles is not None and i >= max_num_articles:
            logger.info("Reached max number of articles, stopping...")
            break

        url = link["url"]
        title = link["title"]
        if url in article_urls and not overwrite_existing:
            logger.info("Article [%s](%s) already exists, skipping...", title, url)
            continue

        # Parse article
        _article = parse_article_func(url)
        if _article is None:
            logger.info(
                "Article [%s](%s) does not exist, skipping...",
                title,
                url,
            )
            continue
        article = link.copy()
        article.update(_article)
        articles.append(article)
        article_urls.append(url)
        if article_filepath:
            HyFI.append_to_jsonl(article, article_filepath)
        if (verbose and (i + 1) % print_every == 0) or delay_between_requests > 0:
            logger.info("Article [%s](%s) scraped", title, url)

        # Delay between requests
        if delay_between_requests > 0 and i < len(links) - 1:
            logger.info("Sleeping for %s seconds...", delay_between_requests)
            time.sleep(delay_between_requests)

    logger.info("Finished scraping articles")
    logger.info("Total articles scraped: %s", len(articles))
    return articles
