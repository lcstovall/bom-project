from pathlib import Path
import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "bom_chapters.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Read data
df = pd.read_csv(INPUT_FILE)

# Tokenization
def tokenize(text):
    """Convert text to lowercase words."""
    return re.findall(r"[a-z']+", text.lower())

# Filter stopwords
bom_stopwords = {
    "unto",
    "shall",
    "ye",
    "yea",
    "behold",
    "therefore",
    "wherefore",
    "thereof",
    "therein",
    "thereon",
    "thou",
    "thee",
    "thy",
    "hath",
    "did",
    "saith",
    "came",
    "pass",
    "according",
    "forth",
    "man",
    "men",
    "said",
    "concerning",
    "say",
    "began",
    "things",
    "judges",
    "year",
    "years",
    "reign",
}

stopwords = set(ENGLISH_STOP_WORDS)
stopwords |= bom_stopwords

# Build corpus
corpus = " ".join(df["text"])
tokens = tokenize(corpus)
tokens = [word for word in tokens if word not in stopwords]

# Word frequencies
word_counts = Counter(tokens)

# Word Cloud
wc = WordCloud(
    width=1600,
    height=800,
    background_color="white",
    colormap="viridis",
    max_words=150,
    relative_scaling=0.5,
)

wc.generate_from_frequencies(word_counts)

plt.figure(figsize=(15, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Book of Mormon Word Cloud")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "word_cloud.png", dpi=300)

# Top 25 words
top_words = word_counts.most_common(25)
words = [w for w, _ in top_words]
counts = [c for _, c in top_words]
plt.figure(figsize=(12, 5))
plt.bar(words, counts)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Frequency")
plt.title("Top 25 Most Frequent Words in the Book of Mormon")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "top_words.png", dpi=300)

# N-gram helper
def make_ngrams(tokens, n):
    return zip(*(tokens[i:] for i in range(n)))

# Bigrams
bigram_counts = Counter(make_ngrams(tokens, 2))
top_bigrams = bigram_counts.most_common(20)
labels = [" ".join(bg) for bg, _ in top_bigrams]
counts = [c for _, c in top_bigrams]
plt.figure(figsize=(14, 5))
plt.bar(labels, counts)
plt.xticks(rotation=60, ha="right")
plt.ylabel("Frequency")
plt.title("Top 20 Bigrams")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "top_bigrams.png", dpi=300)

# Trigrams
trigram_counts = Counter(make_ngrams(tokens, 3))
top_trigrams = trigram_counts.most_common(20)
labels = [" ".join(tg) for tg, _ in top_trigrams]
counts = [c for _, c in top_trigrams]
plt.figure(figsize=(14, 5))
plt.bar(labels, counts)
plt.xticks(rotation=60, ha="right")
plt.ylabel("Frequency")
plt.title("Top 20 Trigrams")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "top_trigrams.png", dpi=300)