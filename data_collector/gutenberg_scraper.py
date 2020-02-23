
import os
from pathlib import Path
import json
import requests
import re
from bs4 import BeautifulSoup


from data_collector.scraping_utils import (
    get_book_link_from_html,
    get_book_name_from_html,
    get_book_author_from_html,
    get_book_downloads_from_html,
    get_book_image_from_html)
from data_collector.custom_logger import set_logger


LOGGER = set_logger("data_collector")
CACHED_DATA_PATH = os.path.join(
    os.fspath(Path(__file__).parents[0]),
    "cached_data",
    "popular_books.json")


def request_page_content(page_url):
    '''Requests (GET) a page content.'''
    page = requests.get(page_url)
    assert page.status_code == 200, "Request is not successful"
    return page.content


def get_book_link_list_from_page_content(page_content):
    '''Finds all the book list tags in a given page content.

    Args:
        page_content (bytes): This is the requested page content with
        requests package.

    Returns:
        list of book_list tags
    '''
    soup_object = BeautifulSoup(page_content, features="lxml")
    return soup_object.findAll("li", {"class": "booklink"})


def get_book_contents_dict(book_html):
    '''Creates a book contents dictionary for each book
    html tag listed in the page.

    Args:
        book_html (bs4.element.Tag): The html tag for book

    Returns:
        book_dict (dict): Book dictionary with name, author
        link, download count and image information.
    '''

    book_dict = {"book_name": None,
                 "book_author": None,
                 "book_link": None,
                 "book_downloads": None,
                 "book_image": None}

    book_dict["book_link"] = get_book_link_from_html(book_html)
    book_dict["book_name"] = get_book_name_from_html(book_html)
    book_dict["book_author"] = get_book_author_from_html(book_html)
    book_dict["book_downloads"] = get_book_downloads_from_html(book_html)
    book_dict["book_image"] = get_book_image_from_html(book_html)

    return book_dict


def create_main_dict_for_popular_books(popular_book_page):
    '''Cretaes a main dictionary made of the popular books listed
    in the Gutenberg popular books webpage.

    Args:
        popular_book_page (str): Popular books webpage string value.

    Retruns:
        dict of book contents, including name, author, download count,
        image (if exists) and link.
    '''
    try:
        gutenberg_content = request_page_content(popular_book_page)
        book_list = get_book_link_list_from_page_content(gutenberg_content)
        return {f"b_{idx}": get_book_contents_dict(book)
                for idx, book in enumerate(book_list)}
    except Exception as e:
        LOGGER.info(f"{e}: cannot reach the website...")
        LOGGER.info(f"Trying to use the cached dataset...")
        with open(CACHED_DATA_PATH) as cached_data:
            return json.load(cached_data)


def get_book_text_link(book_link_str):
    '''Given a book link as string finds the book text link as path only.

    Book link must be given with a homepage concated. As an example:
    "https://www.gutenberg.org/ebooks/46" or
    "https://www.gutenberg.org/ebooks/102"

    Args:
        book_link_str (str): Book link as string.

    Returns:
        book_text_link (str): The link path containing the
        book itself as a text file.

    Example:
        >>> get_book_text_link("https://www.gutenberg.org/ebooks/46")
        "/files/46/46-0.txt"
    '''
    try:
        book_page = book_link_str
        book_page_content = request_page_content(book_page)
        soup_object = BeautifulSoup(book_page_content, features="lxml")
        return soup_object.find(
            "a", {"type": re.compile(r"text/plain")})["href"]
    except Exception:
        LOGGER.info(
                f"Cannot get the book text in:\n{book_link_str}")
        return None
