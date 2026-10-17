# Book of Mormon Text Analysis

This project parses a plain-text edition of the Book of Mormon and generates
charts showing word frequencies, distinctive vocabulary, and selected themes
across its books.

## Requirements

Python 3 and the following packages are required:

- matplotlib
- numpy
- pandas
- scikit-learn
- wordcloud

Install the dependencies with pip:

```bash
python3 -m pip install -r requirements.txt
```

## Run

To run the full pipeline from the project root:

```bash
python3 src/run_all.py
```

This preprocesses the source text and then generates all charts. To run
individual steps instead, use:

```bash
python3 src/preprocess.py
python3 src/frequencies.py
python3 src/book_frequencies.py
python3 src/tfidf_heatmap.py
python3 src/theme_heatmap.py
```

`preprocess.py` reads `data/bom_raw.txt` and writes the chapter-level dataset
to `data/bom_chapters.csv`. The other scripts read that CSV and write their
charts to `results/`. The generated CSV and PNG charts are intentionally not
included in the repository; run the pipeline to create them locally.

## Scripts and outputs

- `src/preprocess.py` parses the source text into book, chapter, text, and word
  count columns in `data/bom_chapters.csv`.
- `src/frequencies.py` creates `results/word_cloud.png`,
  `results/top_words.png`, `results/top_bigrams.png`, and
  `results/top_trigrams.png`.
- `src/book_frequencies.py` compares selected words across books and creates
  `results/book_frequencies.png`. Edit the word list in the script to analyze
  different words; frequencies are normalized per 1,000 words by default.
- `src/tfidf_heatmap.py` creates `results/tfidf_heatmap.png`, showing the top
  five TF-IDF terms for each book.
- `src/theme_heatmap.py` creates `results/theme_heatmap.png`, comparing
  manually selected theme-word frequencies per 1,000 words.

## Data and interpretation

The source text in `data/bom_raw.txt` is Project Gutenberg eBook #17,
*The Book of Mormon*: https://www.gutenberg.org/ebooks/17. The source file
includes Project Gutenberg's license and usage information. Check the
applicable terms before redistributing the text, and retain the required
notices when sharing it. The generated chapter dataset in
`data/bom_chapters.csv` is derived from that source text, so it is not
automatically covered by the code license either.

The charts reflect the project's processing and analysis choices, not
objective or exhaustive measures of meaning. In particular, the theme
heatmap depends on a manually curated word list, while the TF-IDF and word
frequency results depend on tokenization and stopword choices in the scripts.

## License

The original code and project documentation are licensed under the MIT
License; see [LICENSE](LICENSE). This license does not apply to the
Project Gutenberg source text or automatically extend to datasets or other
materials derived from it. See the source text and its license information
for applicable terms.
