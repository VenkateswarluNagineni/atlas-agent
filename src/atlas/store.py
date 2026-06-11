"""Document store with overlapping chunking.

Retrieval quality starts at chunking: too-large chunks dilute relevance, too-small ones
lose context, and no overlap drops facts that straddle a boundary. This module splits
documents into fixed-size, overlapping word windows with stable, deterministic ids so the
same document always yields the same chunk ids (re-indexing is idempotent).
"""

from __future__ import annotations

from collections.abc import Iterator

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """A contiguous slice of a document."""

    id: str
    doc_id: str
    index: int = Field(description="0-based position of this chunk within its document")
    text: str
    start_word: int
    end_word: int = Field(description="Exclusive end word offset")

    @property
    def n_words(self) -> int:
        return self.end_word - self.start_word


def chunk_document(
    doc_id: str, text: str, *, chunk_size: int = 200, overlap: int = 40
) -> list[Chunk]:
    """Split ``text`` into overlapping word windows.

    Consecutive chunks share ``overlap`` words so context that crosses a boundary is not
    lost. Chunk ids are ``"{doc_id}#{index:04d}"`` — stable across runs, so re-indexing the
    same document overwrites rather than duplicates.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be in [0, chunk_size)")

    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[Chunk] = []
    index = 0
    for start in range(0, len(words), step):
        end = min(start + chunk_size, len(words))
        chunks.append(
            Chunk(
                id=f"{doc_id}#{index:04d}",
                doc_id=doc_id,
                index=index,
                text=" ".join(words[start:end]),
                start_word=start,
                end_word=end,
            )
        )
        index += 1
        if end == len(words):
            break  # last window reached the end; don't emit trailing duplicates
    return chunks


class DocumentStore:
    """In-memory store of chunks, indexed by chunk id and by document."""

    def __init__(self, *, chunk_size: int = 200, overlap: int = 40) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        self._chunks: dict[str, Chunk] = {}
        self._by_doc: dict[str, list[str]] = {}

    def add_document(self, doc_id: str, text: str) -> list[Chunk]:
        """Chunk and store a document, replacing any previously stored version of it."""
        # Drop stale chunks so re-adding an edited doc doesn't leave orphans behind.
        for old_id in self._by_doc.get(doc_id, []):
            self._chunks.pop(old_id, None)

        chunks = chunk_document(
            doc_id, text, chunk_size=self.chunk_size, overlap=self.overlap
        )
        for chunk in chunks:
            self._chunks[chunk.id] = chunk
        self._by_doc[doc_id] = [c.id for c in chunks]
        return chunks

    def get_chunk(self, chunk_id: str) -> Chunk:
        return self._chunks[chunk_id]

    def chunks_for(self, doc_id: str) -> list[Chunk]:
        return [self._chunks[cid] for cid in self._by_doc.get(doc_id, [])]

    def __len__(self) -> int:
        return len(self._chunks)

    def __iter__(self) -> Iterator[Chunk]:
        return iter(self._chunks.values())
