"""Build the RAG vector index from mental health guide PDFs."""

from rag.ingest import build_vector_index


def main() -> None:
    build_vector_index()
    print("RAG index build complete.")


if __name__ == "__main__":
    main()
