import os

from word_counter.word_count_utils import (
    word_count)

from data_collector.gutenberg_scraper import (
    request_page_content, create_main_dict_for_popular_books,
    get_book_text_link)

from data_collector.custom_logger import set_logger


LOGGER = set_logger("analyze_logger")


class GutenbergBooksAnalyze:
    def __init__(self, main_page, most_popular_path):
        self.main_page = main_page
        self.most_popular_path = (self.main_page + most_popular_path)
        self.popular_books_dict = create_main_dict_for_popular_books(
            self.most_popular_path)
        self.book_path = "./downloaded_books/"

    def download_book_text(self, book_link_str, path_name):
        book_text_link_path = get_book_text_link(book_link_str)
        requested_book_text = request_page_content(
            self.main_page + book_text_link_path)
        requested_book_text_decoded = requested_book_text.decode("utf")
        with open(f"./downloaded_books/{path_name}.txt", "w") as f:
            f.write(requested_book_text_decoded)

    def download_all_books_as_text(self):
        book_info_link_list = [
            (book_info["book_name"], self.main_page + book_info["book_link"])
            for book_info in self.popular_books_dict.values()]
        for book_name, book_info_link in book_info_link_list:
            try:
                self.download_book_text(book_info_link, book_name)
                LOGGER.info(
                    f"We are done with {book_info_link}.")
            except Exception as e:
                LOGGER.error(
                    f"Error in {book_info_link}: {e}")
                pass

    def count_words_per_book(self):
        books_info_list = [tuple(x.values())
                           for x in self.popular_books_dict.values()]
        book_list_available = os.listdir(self.book_path)
        # This is an extra check if the book is available as .txt file.
        books_info_list_filtered = [info for info in books_info_list
                                    if info[0] + ".txt" in book_list_available]
        # We do the operation only on the available books...
        book_info_list_updated = []
        for book_info in books_info_list_filtered:
            book_name = book_info[0]
            with open(self.book_path + book_name + ".txt", "r") as opened_book:
                opened_book_text = opened_book.read()
            book_info_record = (*book_info, word_count(opened_book_text))
            book_info_list_updated.append(book_info_record)
        return book_info_list_updated
