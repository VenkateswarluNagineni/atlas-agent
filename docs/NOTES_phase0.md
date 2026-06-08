# Phase 0 — Scaffold (design notes)

## What landed
- `retrieval.py`: **Reciprocal Rank Fusion** (RRF) — the core that lets Atlas combine a
  lexical (BM25) and a dense (vector) retriever into one ranking using only ranks, not
  incomparable scores. `k=60` is the constant from the original RRF paper.
- `tools.py`: a typed `Tool` (pydantic `args_schema` + callable) and a `ToolRegistry`
  with duplicate/unknown guards. Tools validate their arguments before running.
- Unit tests for both (RRF consensus behaviour; tool validation + registry guards).
- ruff + pytest CI green from commit one.

## Decisions & trade-offs
- **RRF over score-weighting.** BM25 scores and cosine similarities aren't on the same
  scale; naively summing them is meaningless. RRF needs only the rank order, so it fuses
  heterogeneous retrievers robustly — and it's a one-liner to reason about.
- **Typed tools from day zero.** The thing that turns "an agent" into a debuggable
  *system* is typed, validated tool calls + a registry. Building this first means every
  later agent step is inspectable and testable.
- **Mock-first model client (phase 6).** A deterministic mock client lets the whole
  orchestrator be tested in CI without API keys or network.
- **Evals are not optional.** Phase 13 wires answer quality into CI via the companion
  `lens-llm-eval` project — agents that aren't evaluated can't be trusted in production.

## Next
Phase 1: a document store with overlap chunking and stable ids, then the BM25 lexical
retriever in Phase 2 — the first real input to the RRF core.
