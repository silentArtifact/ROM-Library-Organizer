import sys
from pathlib import Path

# Ensure the project src directory is on sys.path for imports in tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
