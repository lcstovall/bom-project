from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = [
    "preprocess.py",
    "frequencies.py",
    "book_frequencies.py",
    "tfidf_heatmap.py",
    "theme_heatmap.py",
]

for script in SCRIPTS:
    print(f"Running {script}...", flush=True)
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "src" / script)],
        cwd=PROJECT_ROOT,
        check=True,
    )

print(f"All outputs generated in {PROJECT_ROOT / 'results'}")
