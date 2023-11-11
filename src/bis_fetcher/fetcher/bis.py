import logging
from datetime import datetime
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup

from .base import BaseFetcher, By

logger = logging.getLogger(__name__)


class BisFetcher(BaseFetcher):
    """
    Fetcher for BIS.
    """

    _config_name_: str = "bis"
    _config_group_: str = "/fetcher"
    output_dir: str = f"workspace/datasets{_config_group_}/{_config_name_}"
    use_selenium: bool = True

    base_url: str = "https://www.bis.org"
    search_url: str = (
        "https://www.bis.org/cbspeeches/index.htm?m=256&cbspeeches_page={page}"
    )
    search_keywords: List[str] = []

    link_locator: Tuple[str, str] = (
        By.CSS_SELECTOR,
        "#cbspeeches_list > div > table > tbody > tr:nth-child(10) > td:nth-child(2) > div > div.title",
    )
    link_container_name: str = "table"
    link_container_attrs: dict = {"class": "documentList"}
    link_find_all_name: str = "tr"
    link_find_all_attrs: dict = {}
    lint_article_name: str = "div"
    lint_article_attrs: dict = {"class": "title"}

    def _parse_page_links(
        self,
        page_url: str,
        print_every: int = 10,
        verbose: bool = False,
    ) -> Optional[List[dict]]:
        """Get the links from the given page."""
        links = []
        try:
            response = self.request(
                page_url,
                locator=self.link_locator,
            )
            # Check if page exists (status code 200) or not (status code 404)
            if response.status_code == 404:
                logger.info("Page [%s] does not exist, stopping...", page_url)
                return None
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the section with class 'section-category'
            section = soup.find(
                self.link_container_name, attrs=self.link_container_attrs
            )

            # Find all articles within the section
            articles = section.find_all(
                self.link_find_all_name, attrs=self.link_find_all_attrs
            )

            for article_no, article in enumerate(articles):
                # Extract and print article information
                title_div = article.find(
                    self.lint_article_name, attrs=self.lint_article_attrs
                )
                if title_div is None:
                    logger.info("No title found for article %s", article_no)
                    continue
                title = title_div.text
                url = self.base_url + article.find("a")["href"]
                if verbose and article_no % print_every == 0:
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

    def _parse_article_text(self, url: str) -> Optional[dict]:
        """Parse the article text from the given divs."""
        try:
            response = self.request(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the div with class 'entry-content'
            entry_content_div = soup.find("div", class_="entry-content")

            # Find the div with class 'entry-meta'
            entry_meta_div = soup.find("div", class_="entry-meta")

            if entry_content_div and entry_meta_div:
                return self._extract_text(entry_content_div, entry_meta_div)
        except Exception as e:
            logger.error("Error while scraping the article url: %s", url)
            logger.error(e)
        return None

    def _extract_text(self, entry_content_div, entry_meta_div):
        # Find all p tags within the div and extract the text
        p_tags = entry_content_div.find_all("p")
        article_text = "\n".join(p_tag.text for p_tag in p_tags)

        # Extract the entry categories
        entry_categories = [
            a_tag.text for a_tag in entry_meta_div.find_all("a", rel="tag")
        ]

        # Extract the entry time and convert it to a datetime object
        entry_time_str = entry_meta_div.find("time", class_="entry-time")["datetime"]
        entry_time = datetime.fromisoformat(entry_time_str)

        return {
            "categories": entry_categories,
            "time": entry_time.isoformat(),  # Convert datetime to string
            "text": article_text,
        }
