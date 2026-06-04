from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "mental_health_guides"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4


def find_guides_directory() -> Path:
    """Locate the mental health PDF guides folder (name may have leading spaces)."""
    for child in PROJECT_ROOT.iterdir():
        if child.is_dir() and "mental health chatbot guides" in child.name.lower():
            return child
    raise FileNotFoundError(
        "Could not find a folder named 'Mental Health Chatbot guides' in the project root."
    )
