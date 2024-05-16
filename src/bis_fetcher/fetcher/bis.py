import logging
import fitz
from PIL import Image
import pytesseract
from datetime import datetime
from typing import List, Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
from io import BytesIO
import requests
from .base import BaseFetcher, By
import pdfplumber
import numpy as np
import cv2
import pandas as pd

logger = logging.getLogger(__name__)


class BisFetcher(BaseFetcher):
    """
    Fetcher for BIS.
    """

    _config_name_: str = "bis"
    _config_group_: str = "/fetcher"
    output_dir: str = f"workspace/datasets{_config_group_}/{_config_name_}"

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
                use_selenium=True,
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

                date_ = article.find("td", class_="item_date")
                item_date = date_.text.strip() if date_ else ""
                author_ = article.find("a", class_="authorlnk dashed")
                author = author_.text.strip() if author_ else ""

                if verbose and article_no % print_every == 0:
                    logger.info("Title: %s", title)
                    logger.info("URL: %s", url)
                link = {
                    "title": title,
                    "author": author,
                    "timestamp": item_date,
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
            if url.endswith(".pdf"):
                text = self.download_pdf()
                return {
                    "pdf_url": url,
                    "text": text,
                }

            response = self.request(url)
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_div = soup.find("div", class_="pdftxt")
            pdf = pdf_div.find("a", class_="pdftitle_link")["href"]
            pdf_url = self.base_url + pdf
            text = self.download_pdf(pdf_url)

            return {
                "pdf_url": pdf_url,
                "text": text
            }

        except Exception as e:
            logger.error("Error while scraping the article url: %s", url)
            logger.error(e)
        return None

    def download_pdf(self, url: str):

        try:
            response = requests.get(url, allow_redirects=True, stream=True)
            response.raise_for_status()
            filename = url.split("/")[-1]
            with open(f"workspace/{filename}", 'wb') as f:
                f.write(response.content)

            pdf_reader = PdfReader(BytesIO(response.content))
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            page_texts = ['/i255', '/0', '/1', '/2']
            if any(page_text in text for page_text in page_texts):
                text = self.extract_text_from_image_pdf(filename)
            else:
                return text
            return text

        except Exception as e:
            logger.error(
                "Error while downloading or extracting text from PDF: %s", url)
            logger.error(e)
            return None

    def extract_text_from_image_pdf(self, pdf_filename):
        
        pdf_file = "workspace/%s" % (pdf_filename)
        pages = convert_from_path(pdf_file)
        extracted_text = []

        for page in pages:
        # Step 2: Preprocess the image (deskew)
            preprocessed_image = self.Deskew(np.array(page))

        # Step 3: Extract text using OCR
            text = self.extract_text_from_image(preprocessed_image)
            extracted_text.append(text)
        return extracted_text
    
    def Deskew (self, image ): 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
    
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated
    
    def extract_text_from_image(self, image):
        text = pytesseract.image_to_string(image)
        return text
    
    def process_page(self, page):
        try:
            # Transfer image of pdf_file into array
            page_arr = np.array(page)
            # Transfer into grayscale
            page_arr_gray = cv2.cvtColor(page_arr, cv2.COLOR_BGR2GRAY)
            # Deskew the page
            page_deskew = self.Deskew(page_arr_gray)
            # Cal confidence value
            #page_conf = get_conf(page_deskew)
            # Extract string
            d = pytesseract.image_to_data(page_deskew, output_type=pytesseract.Output.DICT)
            d_df = pd.DataFrame.from_dict(d)
            # Get block number
            block_num = int(d_df.loc[d_df['level'] == 2, 'block_num'].max())
            # Drop header and footer by index
            header_index = d_df[d_df['block_num'] == 1].index.values
            footer_index = d_df[d_df['block_num'] == block_num].index.values
            # Combine text in dataframe, excluding header and footer regions
            text = ' '.join(d_df.loc[(d_df['level'] == 5) & (~d_df.index.isin(header_index) & ~d_df.index.isin(footer_index)), 'text'].values)
            return  text
    
        except Exception as e:
            # If can't extract then give some notes into df
            if hasattr(e, 'message'):
                return -1, e.message
            else:
                return -1, str(e)