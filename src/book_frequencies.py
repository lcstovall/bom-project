from pathlib import Path
import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Load data
PROJECT_ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT_ROOT / "data" / "bom_chapters.csv")
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Tokenizer
def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())

# Plot function
def plot_words(words, normalize=True):
    """
    Plot the frequency of several words across the books
    of the Book of Mormon.

    Parameters
    ----------
    words : list[str]
        List of words to plot.

    normalize : bool
        If True, plot occurrences per 1000 words.
        Otherwise plot raw counts.
    """
    books = list(df["book"].unique())
    plt.figure(figsize=(13, 6))
    for word in words:
        frequencies = []
        for book in books:
            text = " ".join(df[df["book"] == book]["text"])
            tokens = tokenize(text)
            counts = Counter(tokens)
            if normalize:
                value = counts[word.lower()] / len(tokens) * 1000
            else:
                value = counts[word.lower()]
            frequencies.append(value)

        plt.plot(
            books,
            frequencies,
            marker="o",
            linewidth=2,
            label=word,
        )

    plt.xticks(rotation=45, ha="right")

    if normalize:
        plt.ylabel("Occurrences per 1000 words")
    else:
        plt.ylabel("Occurrences")

    plt.title("Word Frequency by Book")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "book_frequencies.png", dpi=300)

plot_words([
    "faith",
    "christ",
    "god",
    "lord",
    "repent",
    "people",
])