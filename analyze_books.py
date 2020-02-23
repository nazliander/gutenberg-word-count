import json
import os

from word_counter.gutenberg_books_analyze import GutenbergBooksAnalyze
from analysis_results.analysis_schema import schema

MAIN_PAGE = "https://www.gutenberg.org"
MOST_POPULAR_PATH = "/ebooks/search/%3Fsort_order%3Ddownloads"

if __name__ == "__main__":
    gutenberg_book_cl = GutenbergBooksAnalyze(
        main_page=MAIN_PAGE, most_popular_path=MOST_POPULAR_PATH)

    if len(gutenberg_book_cl.popular_books_dict) > len(
            os.listdir("./downloaded_books/")):
        gutenberg_book_cl.download_all_books_as_text()

    words_per_book = gutenberg_book_cl.count_words_per_book()

    def create_schema_json(schema, list_of_tuples):
        def map_tuples_to_schema(schema, tup):
            return {k: t for k, t in zip(schema.keys(), tup)}
        return [map_tuples_to_schema(schema, info) for info in list_of_tuples]

    with open('./analysis_results/analysis.json', 'w') as f:
        json.dump(create_schema_json(schema, words_per_book), f)
