
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
