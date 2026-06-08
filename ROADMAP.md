# Atlas Roadmap

Built in public, one phase at a time. Each phase ships tested code + a `docs/NOTES_<phase>.md`
design note. The daily build routine picks up the next unchecked phase.

> Convention: `[ ]` not started · `[~]` in progress · `[x]` done.

## Foundations
- [x] **Phase 0 — Scaffold.** Packaging, reciprocal-rank-fusion hybrid-retrieval core,
  typed `Tool` + `ToolRegistry`, tests, ruff, CI, Docker skeleton, roadmap.
- [ ] **Phase 1 — Document store + chunking.** Ingest docs, chunk with overlap, stable ids.
- [ ] **Phase 2 — Lexical retriever (BM25).** Keyword retrieval over the chunk store.

## Retrieval
- [ ] **Phase 3 — Dense retriever.** Sentence-embedding index (FAISS) with cosine search.
- [ ] **Phase 4 — Hybrid retriever.** Fuse BM25 + dense via the Phase-0 RRF; configurable weights.
- [ ] **Phase 5 — Reranking.** Cross-encoder rerank of the fused candidates; measure nDCG lift.

## Agent core
- [ ] **Phase 6 — Model client + tracing.** Anthropic (Claude) + mock client; every step emits a span.
- [ ] **Phase 7 — Planner agent.** Decompose a question into a typed tool plan.
- [ ] **Phase 8 — SQL/analytics tool.** Safe, read-only query tool over a sample warehouse.
- [ ] **Phase 9 — Sandboxed code tool.** Restricted Python execution for computed answers.
- [ ] **Phase 10 — Orchestrator + synthesizer.** Run the plan, gather tool outputs, compose a cited answer.

## Delivery
- [ ] **Phase 11 — Streaming FastAPI service.** SSE token streaming + run inspection endpoints.
- [ ] **Phase 12 — Caching.** Cache retrieval + model calls; report cost/tokens per run.
- [ ] **Phase 13 — Evals (via lens-llm-eval).** Groundedness + answer-quality gates wired into CI.

## Hardening & polish
- [ ] **Phase 14 — Observability dashboard.** Trace viewer: plan, tool calls, latencies.
- [ ] **Phase 15 — Guardrails.** Tool-permission policy, output validation, refusal handling.
- [ ] **Phase 16 — Dockerized demo + sample corpus.** One-command end-to-end run.
- [ ] **Phase 17 — Architecture deep-dive + demo GIF.** Recruiter-ready walkthrough.
