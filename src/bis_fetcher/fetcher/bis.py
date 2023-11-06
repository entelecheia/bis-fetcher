import logging
from datetime import datetime
from functools import partial
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from hyfi.main import HyFI

from .base import BaseFetcher

logger = logging.getLogger(__name__)


class BisFetcher(BaseFetcher):
    """
    Fetcher for BIS.
    """

    _config_name_: str = "khmer"
    _config_group_: str = "/fetcher"
    output_dir: str = f"workspace/datasets{_config_group_}/{_config_name_}"

    search_url: str = (
        "https://www.bis.org/cbspeeches/index.htm?m=256&cbspeeches_page={page}"
    )
    search_keywords: List[str] = []

    def fetch_links(self):
        parse_page_func = partial(
            _parse_page_links,
            print_every=self.print_every,
            verbose=self.verbose,
        )
        self._fetch_links(parse_page_func)

    def fetch_articles(self):
        self._fetch_articles(_parse_article_text)


def _parse_page_links(
    page_url: str,
    print_every: int = 10,
    verbose: bool = False,
) -> Optional[List[dict]]:
    """Get the links from the given page."""
    links = []
    try:
        response = requests.get(page_url)
        # Check if page exists (status code 200) or not (status code 404)
        if response.status_code == 404:
            logger.info("Page [%s] does not exist, stopping...", page_url)
            return None
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the section with class 'section-category'
        table = soup.find("table", class_="documentList")

        # Find all articles within the section
        tr = table.find_all("tr")

        for tr_no, tr in enumerate(tr):
            # Extract and print article information
            title = tr.find("div", class_="title").text
            url = tr.find("a")["href"]
            if verbose and tr_no % print_every == 0:
                logger.info("Title: %s", title)
                logger.info("URL: %s", url)
            link = {
                "title": title,
                "url": url,
            }
            links.append(link)
    except Exception as e:
        logger.error("Error while fetching the page url: %s", page_url)
        logger.error(e)
    return links


def _parse_article_text(url: str) -> Optional[dict]:
    """Parse the article text from the given divs."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the div with class 'entry-content'
        entry_content_div = soup.find("div", class_="entry-content")

        # Find the div with class 'entry-meta'
        entry_meta_div = soup.find("div", class_="entry-meta")

        if entry_content_div and entry_meta_div:
            return _extract_text(entry_content_div, entry_meta_div)
    except Exception as e:
        logger.error("Error while scraping the article url: %s", url)
        logger.error(e)
    return None


def _extract_text(entry_content_div, entry_meta_div):
    # Find all p tags within the div and extract the text
    p_tags = entry_content_div.find_all("p")
    article_text = "\n".join(p_tag.text for p_tag in p_tags)

    # Extract the entry categories
    entry_categories = [a_tag.text for a_tag in entry_meta_div.find_all("a", rel="tag")]

    # Extract the entry time and convert it to a datetime object
    entry_time_str = entry_meta_div.find("time", class_="entry-time")["datetime"]
    entry_time = datetime.fromisoformat(entry_time_str)

    return {
        "categories": entry_categories,
        "time": entry_time.isoformat(),  # Convert datetime to string
        "text": article_text,
    }
