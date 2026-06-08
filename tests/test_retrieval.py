from atlas.retrieval import reciprocal_rank_fusion, reciprocal_rank_fusion_scored


def test_rrf_rewards_agreement_across_lists():
    lexical = ["a", "b", "c"]
    dense = ["b", "a", "d"]
    fused = reciprocal_rank_fusion([lexical, dense])
    # "b" is rank 1 then 0, "a" is rank 0 then 1 -> tie, but both beat c/d.
    assert set(fused[:2]) == {"a", "b"}
    assert fused.index("a") < fused.index("c")


def test_rrf_consensus_top_wins():
    # A doc ranked first in both lists should win outright.
    fused = reciprocal_rank_fusion([["x", "y"], ["x", "z"]])
    assert fused[0] == "x"


def test_scored_variant_is_descending():
    scored = reciprocal_rank_fusion_scored([["x", "y"], ["x", "z"]])
    scores = [s for _, s in scored]
    assert scores == sorted(scores, reverse=True)
