from data_collector.custom_logger import set_logger


LOGGER = set_logger("scraper_logger")


def get_book_link_from_html(book_html):
    try:
        return book_html.find("a")["href"]
    except KeyError:
        LOGGER.info(
                f"Cannot get the book link in:\n{book_html}")
        return None


def get_book_name_from_html(book_html):
    try:
        return book_html.find("span", {"class": "title"}).text
    except AttributeError:
        LOGGER.info(
                f"Cannot get the book name in:\n{book_html}")
        return None


def get_book_author_from_html(book_html):
    try:
        return book_html.find("span", {"class": "subtitle"}).text
    except AttributeError:
        book_name = get_book_name_from_html(book_html)
        LOGGER.info(
                "Cannot get the book author in: "
                f"{book_name}")
        return None


def get_book_downloads_from_html(book_html):
    try:
        return book_html.find("span", {"class": "extra"}).text
    except AttributeError:
        LOGGER.info(
                f"Cannot get the downloads in:\n{book_html}")
        return None


def get_book_image_from_html(book_html):
    try:
        return book_html.find("img")["src"]
    except TypeError:
        book_name = get_book_name_from_html(book_html)
        LOGGER.info(
                "Cannot get the image in: "
                f"{book_name}")
        return None
