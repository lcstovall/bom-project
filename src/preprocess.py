import re
from pathlib import Path
import pandas as pd

# Input / Output
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "bom_raw.txt"
OUTPUT_FILE = PROJECT_ROOT / "data" / "bom_chapters.csv"

# Regular expressions

# Matches (Books):
# THE FIRST BOOK OF NEPHI HIS REIGN AND MINISTRY (1 Nephi)
# THE SECOND BOOK OF NEPHI
# THE BOOK OF ENOS
# THIRD BOOK OF NEPHI
# FOURTH NEPHI
# THE WORDS OF MORMON
book_pattern = re.compile(
    r"^(THE\s+)?((FIRST|SECOND|THIRD)\s+BOOK\s+OF\s+.+|FOURTH\s+NEPHI|THE\s+BOOK\s+OF\s+.+|THE\s+WORDS\s+OF\s+MORMON)",
    re.IGNORECASE,
)

# Matches (Chapters):
# 1 Nephi Chapter 1
# Alma Chapter 32
# Moroni Chapter 10
chapter_pattern = re.compile(
    r"^(.+?)\s+Chapter\s+(\d+)\s*$",
    re.IGNORECASE,
)

# Matches (Verses):
# 1:1
# 32:17
verse_pattern = re.compile(r"^\d+:\d+\s*")

# Read file
text = INPUT_FILE.read_text(encoding="utf-8")
lines = [line.strip() for line in text.splitlines()]

# Remove Gutenberg header
start = None

for i, line in enumerate(lines):
    if line.startswith("THE FIRST BOOK OF NEPHI"):
        start = i
        break

if start is None:
    raise RuntimeError("Couldn't find start of Book of Mormon.")

lines = lines[start:]

# Remove Gutenberg footer
end = len(lines)

for i, line in enumerate(lines):
    if line.startswith("*** END OF THE PROJECT GUTENBERG"):
        end = i
        break

lines = lines[:end]

# Parse chapters
records = []
current_book = None
current_chapter = None
current_text = []

for line in lines:

    if not line:
        continue

    # Detect book headings
    if book_pattern.match(line):

        # Save previous chapter
        if current_book is not None and current_chapter is not None:
            text = " ".join(current_text)
            text = re.sub(r"\s+", " ", text).strip()

            records.append(
                {
                    "book": current_book,
                    "chapter": current_chapter,
                    "text": text,
                    "word_count": len(text.split()),
                }
            )

        # Normalize book names
        if "(1 Nephi)" in line:
            current_book = "1 Nephi"
        elif "SECOND BOOK OF NEPHI" in line.upper():
            current_book = "2 Nephi"
        elif "THIRD BOOK OF NEPHI" in line.upper():
            current_book = "3 Nephi"
        elif "FOURTH NEPHI" in line.upper():
            current_book = "4 Nephi"
        elif "BOOK OF JACOB" in line.upper():
            current_book = "Jacob"
        elif "BOOK OF ENOS" in line.upper():
            current_book = "Enos"
        elif "BOOK OF JAROM" in line.upper():
            current_book = "Jarom"
        elif "BOOK OF OMNI" in line.upper():
            current_book = "Omni"
        elif "WORDS OF MORMON" in line.upper():
            current_book = "Words of Mormon"
        elif "BOOK OF MOSIAH" in line.upper():
            current_book = "Mosiah"
        elif "BOOK OF ALMA" in line.upper():
            current_book = "Alma"
        elif "BOOK OF HELAMAN" in line.upper():
            current_book = "Helaman"
        elif line.upper().startswith("THE BOOK OF MORMON"):
            current_book = "Mormon"
        elif "BOOK OF ETHER" in line.upper():
            current_book = "Ether"
        elif "BOOK OF MORONI" in line.upper():
            current_book = "Moroni"

        current_chapter = None
        current_text = []
        continue

    # Detect chapter headings
    m = chapter_pattern.match(line)

    if m:

        if current_book is not None and current_chapter is not None:
            text = " ".join(current_text)
            text = re.sub(r"\s+", " ", text).strip()

            records.append(
                {
                    "book": current_book,
                    "chapter": current_chapter,
                    "text": text,
                    "word_count": len(text.split()),
                }
            )

        current_book = m.group(1)
        current_chapter = int(m.group(2))
        current_text = []
        continue

    # Single-chapter books
    if current_book is not None and current_chapter is None:
        if verse_pattern.match(line):
            current_chapter = 1

    # Remove verse number
    line = verse_pattern.sub("", line)

    if current_chapter is not None:
        current_text.append(line)

# Save final chapter
if current_book is not None:

    text = " ".join(current_text)
    text = re.sub(r"\s+", " ", text).strip()

    records.append(
        {
            "book": current_book,
            "chapter": current_chapter,
            "text": text,
            "word_count": len(text.split()),
        }
    )

# Create dataframe
df = pd.DataFrame(records)

# Save
df.to_csv(OUTPUT_FILE, index=False)