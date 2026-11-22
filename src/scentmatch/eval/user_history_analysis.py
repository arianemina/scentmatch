
"""Analyse des utilisateurs selon leur historique d'entraînement.

ScentMatch - Week 3
Contribution : Halima Ghazi
"""

from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/processed")


def segment_users(train: pd.DataFrame) -> pd.DataFrame:
    """Classe les utilisateurs selon leur nombre de parfums distincts."""

    history = (
        train.groupby("user_idx")["item_idx"]
        .nunique()
        .rename("history_size")
        .reset_index()
    )

    def assign_segment(size: int) -> str:
        if size == 1:
            return "1 parfum"
        if size == 2:
            return "2 parfums"
        if 3 <= size <= 5:
            return "3 à 5 parfums"
        return "6 parfums ou plus"

    history["segment"] = history["history_size"].apply(assign_segment)

    return history


def main() -> None:
    train = pd.read_parquet(DATA_DIR / "train.parquet")

    segments = segment_users(train)

    summary = (
        segments.groupby("segment", observed=True)
        .size()
        .rename("users")
        .reset_index()
    )

    summary["percentage"] = (
        summary["users"] / len(segments) * 100
    ).round(2)

    print("\nScentMatch - User History Analysis")
    print(summary.to_string(index=False))

    output = Path("reports/halima_user_segments.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output, index=False)

    print(f"\nRésultats enregistrés : {output}")


if __name__ == "__main__":
    main()
