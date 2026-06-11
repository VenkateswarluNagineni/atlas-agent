# Phase 1 — Document store + chunking (design notes)

## What landed
- `store.py`:
  - `chunk_document(doc_id, text, chunk_size, overlap)` — splits text into fixed-size,
    **overlapping** word windows with stable ids `"{doc_id}#{index:04d}"`.
  - `Chunk` model (id, doc_id, index, text, word offsets, `n_words`).
  - `DocumentStore` — in-memory, indexed by chunk id and by document; `add_document`
    replaces a doc's old chunks instead of duplicating them.
- 7 tests covering overlap correctness, exact partitioning at overlap=0, id stability,
  empty input, invalid params, and store re-indexing.

## Decisions & trade-offs
- **Overlap is the whole point.** A fact that straddles a chunk boundary is invisible to a
  retriever unless adjacent chunks share text. Consecutive windows share `overlap` words; a
  test pins that `chunk[0]`'s last 10 words equal `chunk[1]`'s first 10.
- **Word-based windows, not characters.** Word windows keep tokens intact and map more
  naturally to embedding context limits than raw character counts. Trade-off: not exact
  token counts — a tokenizer-aware splitter can slot in later behind the same signature.
- **Deterministic ids = idempotent indexing.** Ids derive from `doc_id` + position, so
  re-indexing the same document overwrites its chunks rather than creating duplicates. This
  is what lets the store be rebuilt safely on every ingest.
- **Replace-on-readd in the store.** `add_document` first drops the doc's previous chunk ids,
  so editing a document and re-adding it never leaves orphaned chunks in the index.
- **In-memory now, pluggable later.** Phase 1 keeps the store in a dict; the BM25 (phase 2),
  dense/FAISS (phase 3), and hybrid (phase 4) retrievers will consume these chunks without
  caring where they're stored.

## Next
Phase 2: the BM25 lexical retriever over these chunks — the first real ranking that feeds
the reciprocal-rank-fusion core built in Phase 0.
