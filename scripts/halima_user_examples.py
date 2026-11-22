
"""ScentMatch Week 3 - Real user recommendation examples."""

import json
from collections import Counter
from pathlib import Path

import pandas as pd

from scentmatch.train.predict import Catalogue, ModelRecommender


PROCESSED = Path("data/processed")
CHECKPOINT = Path("checkpoints/final_nlgcl_notes_rescued_s3.pt")
OUTPUT = Path("reports/halima_user_examples.json")

WOODY_NOTES = {"oud", "sandalwood", "cedar", "cedarwood", "vetiver"}
SWEET_NOTES = {"vanilla", "caramel", "praline", "tonka bean", "honey"}


def perfume_info(cat, item_idx):
    item_idx = int(item_idx)

    return {
        "name": cat.short_titles[item_idx],
        "notes": sorted(
            cat.note_names[n]
            for n in cat.notes_of(item_idx)
        ),
    }


def user_notes(cat, history):
    notes = Counter()

    for item in history:
        notes.update(
            cat.note_names[n].lower()
            for n in cat.notes_of(int(item))
        )

    return notes



def select_user(cat, target_notes, selected):
    candidates = []

    for user_idx, history in cat.train_items.items():
        if user_idx in selected or not (3 <= len(history) <= 10):
            continue

        notes = user_notes(cat, history)
        match = sum(notes[n] for n in target_notes)

        if match >= 2:
            candidates.append((match, int(user_idx)))

    if not candidates:
        raise ValueError("No matching user found")

    return max(candidates)[1]



def main():
    cat = Catalogue(PROCESSED)
    model = ModelRecommender(cat, CHECKPOINT, PROCESSED)

    users = pd.read_parquet(PROCESSED / "users.parquet")
    id_map = dict(zip(users["user_idx"], users["user_id"]))

    selected = set()

    woody = select_user(cat, WOODY_NOTES, selected)
    selected.add(woody)

    sweet = select_user(cat, SWEET_NOTES, selected)
    selected.add(sweet)

    cold_candidates = [
        int(u) for u, history in cat.train_items.items()
        if len(set(history)) == 1 and u not in selected
    ]

    if not cold_candidates:
        raise ValueError("No short-history user found")

    cold = cold_candidates[0]

    profiles = {
        "Woody": woody,
        "Sweet": sweet,
        "Limited history": cold,
    }

    results = []

    for label, user_idx in profiles.items():
        history = cat.train_items[user_idx]
        recs = model.recommend_user(
            str(id_map[user_idx]), k=3
        )

        results.append({
            "profile": label,
            "user_idx": user_idx,
            "history": [
                perfume_info(cat, i)
                for i in history
            ],
            "recommendations": [
                {
                    **perfume_info(cat, r.item_idx),
                    "score": r.score,
                    "explanation": r.explanation,
                }
                for r in recs
            ],
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Examples saved to {OUTPUT}")

    for result in results:
        print(
            result["profile"],
            "| history:",
            len(result["history"]),
            "| recommendations:",
            len(result["recommendations"]),
        )


if __name__ == "__main__":
    main()
