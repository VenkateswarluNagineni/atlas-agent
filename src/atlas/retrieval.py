"""Hybrid-retrieval fusion.

Reciprocal Rank Fusion (RRF) combines several ranked result lists (e.g. lexical BM25 +
dense vector search) into one ranking without needing comparable scores — only ranks.
This is the core of Atlas's hybrid retriever; the BM25 and dense backends plug in later.
"""

from __future__ import annotations

from collections.abc import Sequence


def reciprocal_rank_fusion(rankings: Sequence[Sequence[str]], k: int = 60) -> list[str]:
    """Fuse multiple ranked lists of document ids into one ranking.

    Each document scores ``sum(1 / (k + rank))`` across the lists it appears in (rank is
    0-based). ``k`` damps the influence of top ranks (60 is the value from the original
    Cormack et al. RRF paper). Returns doc ids sorted by fused score, descending.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)


def reciprocal_rank_fusion_scored(
    rankings: Sequence[Sequence[str]], k: int = 60
) -> list[tuple[str, float]]:
    """Like :func:`reciprocal_rank_fusion` but returns ``(doc_id, fused_score)`` pairs."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
