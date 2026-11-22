
"""Export three ScentMatch recommendation examples to Markdown."""

import json
from pathlib import Path

SOURCE = Path("reports/halima_user_examples.json")
OUTPUT = Path("reports/halima_user_examples.md")

LABELS = {
    "Woody": "Woody preferences",
    "Sweet": "Sweet preferences",
    "Limited history": "Limited history (one known perfume)",
}


def main():
    examples = json.loads(SOURCE.read_text(encoding="utf-8"))

    lines = [
        "# Week 3 - Qualitative recommendation examples",
        "",
        "Model: final_nlgcl_notes_rescued_s3.pt",
        "",
        "Three real users selected from the training histories.",
        "These examples illustrate recommendation coherence,",
        "not held-out accuracy or a true zero-history cold-start.",
        "",
    ]

    for example in examples:
        profile = example["profile"]
        history = example["history"]

        lines.extend([
            f"## {LABELS[profile]}",
            "",
            f"User index: {example['user_idx']}",
            f"Known perfumes: {len(history)}",
            "",
            "### History",
            "",
        ])

        for perfume in history:
            notes = ", ".join(perfume["notes"][:6])
            lines.append(f"- {perfume['name']} ({notes})")

        lines.extend([
            "",
            "### Top 3 recommendations",
            "",
            "| Perfume | Score | Model explanation |",
            "|---|---:|---|",
        ])

        for rec in example["recommendations"]:
            name = rec["name"].replace("|", "/")
            explanation = rec["explanation"].replace("|", "/")

            lines.append(
                f"| {name} | {rec['score']:.4f} | {explanation} |"
            )

        lines.append("")

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Report saved: {OUTPUT}")


if __name__ == "__main__":
    main()

