## Python Word Count Example - Using Gutenberg.org

I prepared a small exercise package for a workshop in Utrecht - De Meern. This exercise package was aiming to teach list-dict comprehensions in a fun way. Exercises might be considered as in an intermediate level.

I am combining the source code for that worshop, only to archive the effort of mine.

One can use the source code of mine to replicate the workshop, by excluding the `analyze_books.py` with `./word_counter/` and target the following questions:

1. We have a nested dictionary of book information. Write a function to create a list of tuples, including only the book_name and book_downloads.
2. Write a function to sort book_name and downloads by checking the number of the downloads. (ascending is fine)
3. Write a function to count words in each text (string). (please use simple tokenizer given in the notebook)
4. Write a function with a dictionary that is stating which words are used in the text how many times.
5. Use `download_book_text` to download all the popular books with their own book name. (bonus question)
6. By using the downloaded book texts in the previous step, count the words in each book. (bonus question)
