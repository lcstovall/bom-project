from pathlib import Path
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "bom_chapters.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(INPUT_FILE)

# Books (scriptural order)
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

# Theme words
THEMES = {
    "Jesus Christ": [
        "christ",
        "jesus",
        "messiah",
        "lamb",
        "shepherd",
        "redeemer",
        "mediator",
    ],

    "God the Father": [
        "god",
        "father",
        "almighty",
        "creator",
    ],

    "The Holy Spirit": [
        "spirit",
        "ghost",
        "comforter",
    ],

    "Faith": [
        "faith",
        "faithful",
        "believe",
        "believed",
        "believeth",
        "believing",
        "belief",
        "trust",
        "trusted",
        "trusting",
    ],

    "Repentance": [
        "repent",
        "repented",
        "repenteth",
        "repenting",
        "repentance",
        "confess",
        "confessed",
    ],

    "Love": [
        "love",
        "loveth",
        "loved",
        "loving",
        "charity",
        "grace",
        "gracious",
        "mercy",
        "mercies",
        "merciful",
        "compassion",
    ],

    "Salvation": [
        "save",
        "saved",
        "salvation",
        "deliver",
        "delivered",
        "deliverance",
        "redeem",
        "redeemed",
        "redemption",
        "atonement",
        "reconcile",
        "reconciled",
        "ransom",
    ],

    "Justice": [
        "justice",
        "just",
        "justify",
        "justified",
        "judgment",
        "judge",
        "judged",
    ],

    "Prayer": [
        "pray",
        "prayed",
        "prayer",
        "praying",
        "prayers",
        "cry",
        "cried",
        "criest",
        "call",
        "called",
        "calling",
    ],

}

# Tokenizer
def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())

# Compute normalized frequencies
heatmap = np.zeros((len(BOOKS), len(THEMES)))

for i, book in enumerate(BOOKS):

    text = " ".join(df[df["book"] == book]["text"])
    tokens = tokenize(text)
    counts = Counter(tokens)
    total_words = len(tokens)
    for j, (theme, words) in enumerate(THEMES.items()):
        total = sum(counts[word] for word in words)
        heatmap[i, j] = total / total_words * 1000

# Plot
fig, ax = plt.subplots(figsize=(12, 8))

im = ax.imshow(
    heatmap,
    cmap="YlGnBu",
    aspect="auto",
)

# Axis labels
ax.set_xticks(np.arange(len(THEMES)))
ax.set_xticklabels(THEMES.keys(), rotation=45, ha="right")
ax.set_yticks(np.arange(len(BOOKS)))
ax.set_yticklabels(BOOKS)

# Annotate cells
for i in range(len(BOOKS)):
    for j in range(len(THEMES)):
        ax.text(
            j,
            i,
            f"{heatmap[i, j]:.1f}",
            ha="center",
            va="center",
            fontsize=8,
            color="black",
        )

cbar = plt.colorbar(im)
cbar.set_label("Occurrences per 1,000 Words")

plt.title("Doctrinal Theme Word Frequencies by Book")
plt.tight_layout()
plt.savefig(
    RESULTS_DIR / "theme_heatmap.png",
    dpi=300,
)