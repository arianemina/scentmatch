
"""Comparaison des performances par historique utilisateur - ScentMatch."""

import json
from pathlib import Path

import pandas as pd

INPUT = Path("reports/halima_comparison_validation.json")
OUTPUT = Path("reports/halima_comparison_table.csv")

SEGMENTS = ["1", "2", "3-5", "6+"]


def main():
    results = json.loads(INPUT.read_text(encoding="utf-8"))

    popular = next(
        r for r in results if r["ranker"] == "Most-popular"
    )

    model = next(
        r for r in results
        if r["ranker"] == "final_nlgcl_notes_rescued_s3"
    )

    rows = []

    for segment in SEGMENTS:
        baseline = popular[f"Recall@20[{segment}]"]
        nlgcl = model[f"Recall@20[{segment}]"]

        rows.append({
            "Historique": segment,
            "Recall@20 Most Popular": baseline,
            "Recall@20 NLGCL": nlgcl,
            "Gain absolu": nlgcl - baseline,
            "Gain relatif (%)": (
                (nlgcl / baseline - 1) * 100
                if baseline > 0 else None
            ),
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT, index=False)

    print("\nComparaison des performances par segment")
    print(df.round(4).to_string(index=False))
    print(f"\nTableau enregistré : {OUTPUT}")


if __name__ == "__main__":
    main()
