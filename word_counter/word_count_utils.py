

def simple_tokenizer(text):
    import re
    word_regex = re.compile(r"(\w+)")
    return re.findall(word_regex, text.lower())


def sort_ascending_the_download_counts_per_book(popular_books_dict):
    necessary_info = [
        (main_dict["book_name"], main_dict["book_downloads"])
        for book_index, main_dict in popular_books_dict.items()]

    return sorted([(int(download.split(" ")[0]), book_name)
                   for book_name, download in necessary_info])


def word_count(text):
    return len(simple_tokenizer(text))


def word_count_with_dict(text):
    words = simple_tokenizer(text)
    word_count = {}
    for w in words:
        word_count[w] = word_count.get(w, 0) + 1
    return word_count
