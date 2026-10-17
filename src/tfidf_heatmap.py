from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "bom_chapters.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(INPUT_FILE)

# Book order
BOOKS = [
    "1 Nephi",
    "2 Nephi",
    "Jacob",
    "Enos",
    "Jarom",
    "Omni",
    "Words of Mormon",
    "Mosiah",
    "Alma",
    "Helaman",
    "3 Nephi",
    "4 Nephi",
    "Mormon",
    "Ether",
    "Moroni",
]

# Combine chapters into books
documents = []

for book in BOOKS:
    text = " ".join(df[df["book"] == book]["text"])
    documents.append(text)

# TF-IDF
CUSTOM_STOPWORDS = {
    "ye",
    "yea",
    "behold",
    "unto",
    "therefore",
    "wherefore",
    "pass",
    "came",
    "thy",
    "hath",
    "thou",
    "said",
    "say",
    "somewhat",
    "year",
    "verily",
    "thee",
    "enos",
    "jarom",
    "mosiah",
    "benjamin",
    "alma",
    "limhi",
    "ammon",
    "moroni",
    "jared",
    "coriantumr",
    "shiz",
    "abinadi",
    "amalickiah",
    "mormon",
    "shule",
    "akish",
    "lib",
    "ether",
    "amos",
    "amaleki",
    "amulek",
    "chemish",
    "abinadom",
    "amaron"
}

stopwords = ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS)

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words=list(stopwords),
    max_df=0.8,
)

X = vectorizer.fit_transform(documents)

feature_names = np.array(vectorizer.get_feature_names_out())

# Find top words for each book
TOP_N = 5
heatmap = np.zeros((len(BOOKS), TOP_N))
labels = []

for i in range(len(BOOKS)):
    row = X[i].toarray().ravel()
    top = np.argsort(row)[-TOP_N:][::-1]
    heatmap[i] = row[top]
    labels.append(feature_names[top])

# Plot
fig, ax = plt.subplots(figsize=(9, 8))

im = ax.imshow(
    heatmap,
    cmap="YlOrRd",
    aspect="auto",
)

# x-axis
ax.set_xticks(np.arange(TOP_N))
ax.set_xticklabels(
    [f"Top {i+1}" for i in range(TOP_N)]
)

# y-axis
ax.set_yticks(np.arange(len(BOOKS)))
ax.set_yticklabels(BOOKS)

# Put the words inside each cell
for i in range(len(BOOKS)):
    for j in range(TOP_N):

        ax.text(
            j,
            i,
            labels[i][j],
            ha="center",
            va="center",
            fontsize=8,
            color="black",
        )

cbar = plt.colorbar(im)
cbar.set_label("TF-IDF Score")

plt.title("Most Distinctive Words by Book")
plt.tight_layout()
plt.savefig(
    RESULTS_DIR / "tfidf_heatmap.png",
    dpi=300,
)