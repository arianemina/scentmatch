
"""Tests de l'analyse des performances par historique utilisateur."""

import pandas as pd

from scentmatch.eval.user_history_analysis import segment_users
from scentmatch.eval.metrics import recall_at_k


def test_segment_users():
    train = pd.DataFrame({
        "user_idx": [0, 1, 1, 2, 2, 2],
        "item_idx": [10, 20, 21, 30, 31, 32],
    })

    result = segment_users(train).set_index("user_idx")

    assert result.loc[0, "segment"] == "1 parfum"
    assert result.loc[1, "segment"] == "2 parfums"
    assert result.loc[2, "segment"] == "3 à 5 parfums"


def test_recall_at_20():
    ranked = [10, 20, 30, 40]
    relevant = {20, 50}

    result = recall_at_k(ranked, relevant, 20)

    assert result == 0.5


def test_full_report_segment_recall(monkeypatch, tmp_path):
    """Verify Recall@20 for each user-history segment."""

    import numpy as np
    import pandas as pd
    import pytest

    from scentmatch.eval import evaluate
    from scentmatch.eval.harness import EvalData

    train = pd.DataFrame({
        "user_idx": [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3],
        "item_idx": [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5],
    })

    val = pd.DataFrame({
        "user_idx": [0, 1, 2, 3],
        "item_idx": [6, 7, 8, 9],
    })

    data = EvalData(4, 10, train, val, val.copy())

    segments = pd.DataFrame({
        "user_idx": [0, 1, 2, 3],
        "segment": ["1", "2", "3-5", "6+"],
    })

    segments.to_parquet(tmp_path / "user_segments.parquet")

    rankings = {
        0: [6, 7, 8, 9],
        1: [6, 7, 8, 9],
        2: [6, 7, 8, 9],
        3: [6, 7, 8, 9],
    }

    monkeypatch.setattr(
        evaluate,
        "rank_scores",
        lambda score_fn, data, split: rankings,
    )

    monkeypatch.setattr(
        evaluate,
        "personalisation",
        lambda rankings: 0.0,
    )

    monkeypatch.setattr(
        evaluate,
        "tail_share",
        lambda rankings, popularity: 0.0,
    )

    result = evaluate.full_report(
        name="Test model",
        score_fn=lambda users: np.zeros((len(users), 10)),
        data=data,
        split="val",
        proc=tmp_path,
        feedback=None,
    )

    assert result["Recall@20[1]"] == pytest.approx(1.0)
    assert result["Recall@20[2]"] == pytest.approx(1.0)
    assert result["Recall@20[3-5]"] == pytest.approx(1.0)
    assert result["Recall@20[6+]"] == pytest.approx(1.0)


def test_segment_recall_different_results(monkeypatch, tmp_path):
    """Verify that each segment gets its own Recall@20."""

    import numpy as np
    import pandas as pd
    import pytest

    from scentmatch.eval import evaluate
    from scentmatch.eval.harness import EvalData

    train = pd.DataFrame({
        "user_idx": [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3],
        "item_idx": [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5],
    })

    val = pd.DataFrame({
        "user_idx": [0, 1, 2, 3],
        "item_idx": [6, 7, 8, 9],
    })

    data = EvalData(4, 11, train, val, val.copy())

    segments = pd.DataFrame({
        "user_idx": [0, 1, 2, 3],
        "segment": ["1", "2", "3-5", "6+"],
    })
    segments.to_parquet(tmp_path / "user_segments.parquet")

    rankings = {
        0: [6, 7, 8, 9],    # Hit
        1: [6, 8, 9, 10],   # Miss
        2: [6, 7, 8, 9],    # Hit
        3: [6, 7, 8, 10],   # Miss
    }

    monkeypatch.setattr(
        evaluate, "rank_scores",
        lambda score_fn, data, split: rankings,
    )
    monkeypatch.setattr(
        evaluate, "personalisation",
        lambda rankings: 0.0,
    )
    monkeypatch.setattr(
        evaluate, "tail_share",
        lambda rankings, popularity: 0.0,
    )

    result = evaluate.full_report(
        name="Test model",
        score_fn=lambda users: np.zeros((len(users), 11)),
        data=data,
        split="val",
        proc=tmp_path,
        feedback=None,
    )

    assert result["Recall@20[1]"] == pytest.approx(1.0)
    assert result["Recall@20[2]"] == pytest.approx(0.0)
    assert result["Recall@20[3-5]"] == pytest.approx(1.0)
    assert result["Recall@20[6+]"] == pytest.approx(0.0)


def test_empty_segment(monkeypatch, tmp_path):
    """Verify metrics return None for empty segments."""

    import numpy as np
    import pandas as pd

    from scentmatch.eval import evaluate
    from scentmatch.eval.harness import EvalData

    train = pd.DataFrame({
        "user_idx": [0, 1, 1],
        "item_idx": [0, 0, 1],
    })

    val = pd.DataFrame({
        "user_idx": [0, 1],
        "item_idx": [2, 3],
    })

    data = EvalData(2, 5, train, val, val.copy())

    segments = pd.DataFrame({
        "user_idx": [0, 1],
        "segment": ["1", "2"],
    })
    segments.to_parquet(tmp_path / "user_segments.parquet")

    rankings = {
        0: [2, 3, 4],
        1: [2, 3, 4],
    }

    monkeypatch.setattr(
        evaluate,
        "rank_scores",
        lambda score_fn, data, split: rankings,
    )
    monkeypatch.setattr(
        evaluate,
        "personalisation",
        lambda rankings: 0.0,
    )
    monkeypatch.setattr(
        evaluate,
        "tail_share",
        lambda rankings, popularity: 0.0,
    )

    result = evaluate.full_report(
        name="Test model",
        score_fn=lambda users: np.zeros((len(users), 5)),
        data=data,
        split="val",
        proc=tmp_path,
        feedback=None,
    )

    assert result["Recall@20[3-5]"] is None
    assert result["Recall@20[6+]"] is None
    assert result["NDCG@10[3-5]"] is None
    assert result["NDCG@10[6+]"] is None
