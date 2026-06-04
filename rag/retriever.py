from dataclasses import dataclass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from rag.config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K


@dataclass
class RetrievedChunk:
    content: str
    source: str
    page: int | None


_retriever = None
_rag_available = False


def index_exists() -> bool:
    return CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir())


def _load_vectorstore() -> Chroma | None:
    if not index_exists():
        return None

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


def get_retriever():
    global _retriever, _rag_available

    if _retriever is not None:
        return _retriever, _rag_available

    vectorstore = _load_vectorstore()
    if vectorstore is None:
        _retriever = None
        _rag_available = False
        return _retriever, _rag_available

    _retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    _rag_available = True
    return _retriever, _rag_available


def retrieve_context(query: str) -> tuple[str, list[RetrievedChunk]]:
    retriever, rag_available = get_retriever()

    if not rag_available or retriever is None:
        return "", []

    docs = retriever.invoke(query)
    if not docs:
        return "", []

    chunks: list[RetrievedChunk] = []
    sections: list[str] = []

    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        page_label = f", page {page + 1}" if isinstance(page, int) else ""
        chunks.append(
            RetrievedChunk(
                content=doc.page_content.strip(),
                source=source,
                page=page + 1 if isinstance(page, int) else None,
            )
        )
        sections.append(
            f"[Excerpt {index} — {source}{page_label}]\n{doc.page_content.strip()}"
        )

    context = "\n\n".join(sections)
    return context, chunks


def format_rag_system_addendum(context: str) -> str:
    if not context:
        return ""

    return f"""
### Retrieved Knowledge Base Excerpts

Use the excerpts below for factual mental-health guidance when they are relevant to the user's message.
Prefer this information over general knowledge for coping strategies, definitions, and educational content.
If the excerpts do not cover the question, respond with empathy using your general guidance while staying in scope.
Do not contradict the crisis and safety rules above.

{context}
"""
