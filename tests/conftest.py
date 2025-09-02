# tests/conftest.py
from pathlib import Path
import sys

# Add the project root (the folder that contains 'app') to sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
