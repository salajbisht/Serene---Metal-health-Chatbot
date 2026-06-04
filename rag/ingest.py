from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    find_guides_directory,
)


def load_pdf_documents(guides_dir: Path) -> list:
    documents = []
    pdf_paths = sorted(guides_dir.glob("*.pdf"))

    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found in {guides_dir}")

    for pdf_path in pdf_paths:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata["source"] = pdf_path.name
        documents.extend(pages)

    return documents


def build_vector_index(guides_dir: Path | None = None, chroma_dir: Path | None = None) -> Chroma:
    guides_dir = guides_dir or find_guides_directory()
    chroma_dir = chroma_dir or CHROMA_DIR

    print(f"Loading PDFs from: {guides_dir}")
    documents = load_pdf_documents(guides_dir)
    print(f"Loaded {len(documents)} pages from {len(list(guides_dir.glob('*.pdf')))} PDFs")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if chroma_dir.exists():
        import shutil

        shutil.rmtree(chroma_dir)

    chroma_dir.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(chroma_dir),
    )

    print(f"Vector index saved to: {chroma_dir}")
    return vectorstore
