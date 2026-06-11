import pytest

from atlas.store import Chunk, DocumentStore, chunk_document


def _text(n: int) -> str:
    return " ".join(f"w{i}" for i in range(n))


def test_chunking_covers_all_words_with_overlap():
    chunks = chunk_document("d1", _text(100), chunk_size=40, overlap=10)
    # step = 30 -> windows start at 0, 30, 60 (60+40 reaches the end) -> 3 chunks
    assert [c.index for c in chunks] == [0, 1, 2]
    assert chunks[0].text.split()[-1] == "w39"
    # consecutive chunks share `overlap` words
    assert chunks[0].text.split()[-10:] == chunks[1].text.split()[:10]
    # last chunk reaches the final word
    assert chunks[-1].text.split()[-1] == "w99"


def test_no_overlap_partitions_exactly():
    chunks = chunk_document("d", _text(60), chunk_size=20, overlap=0)
    assert len(chunks) == 3
    joined = " ".join(c.text for c in chunks)
    assert joined == _text(60)


def test_chunk_ids_are_stable_and_deterministic():
    a = chunk_document("doc", _text(50), chunk_size=20, overlap=5)
    b = chunk_document("doc", _text(50), chunk_size=20, overlap=5)
    assert [c.id for c in a] == [c.id for c in b]
    assert a[0].id == "doc#0000"
    assert a[1].id == "doc#0001"


def test_empty_text_yields_no_chunks():
    assert chunk_document("d", "   ") == []


def test_invalid_overlap_rejected():
    with pytest.raises(ValueError):
        chunk_document("d", _text(10), chunk_size=10, overlap=10)
    with pytest.raises(ValueError):
        chunk_document("d", _text(10), chunk_size=0)


def test_store_add_get_and_reindex():
    store = DocumentStore(chunk_size=10, overlap=2)
    store.add_document("d1", _text(30))
    first_count = len(store)
    assert first_count > 0
    assert store.chunks_for("d1")[0].id == "d1#0000"

    # Re-adding a shorter version replaces, not appends.
    store.add_document("d1", _text(5))
    assert len(store) == 1
    assert all(isinstance(c, Chunk) for c in store)


def test_n_words_property():
    chunk = chunk_document("d", _text(25), chunk_size=10, overlap=0)[0]
    assert chunk.n_words == 10
