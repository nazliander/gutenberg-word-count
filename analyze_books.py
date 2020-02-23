from word_counter.gutenberg_books_analyze import GutenbergBooksAnalyze

MAIN_PAGE = "https://www.gutenberg.org"
MOST_POPULAR_PATH = "/ebooks/search/%3Fsort_order%3Ddownloads"

gutenberg_book_cl = GutenbergBooksAnalyze(
    main_page=MAIN_PAGE, most_popular_path=MOST_POPULAR_PATH)

gutenberg_book_cl.download_all_books_as_text()
