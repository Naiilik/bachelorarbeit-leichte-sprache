import json
import os
import unicodedata

base_dir = os.path.dirname(os.path.abspath(__file__))
original_path = "input_texts/inputText.json"
improved_path = "quantitative_analysis/results.json"
output_json = "quantitative_analysis/input_texts/improvements/improvement_comparison.json"
output_csv = "quantitative_analysis/input_texts/improvements/improvement_comparison.csv"


def normalize_label(value):
    return unicodedata.normalize("NFC", os.path.splitext(value)[0]).strip()


# Load original input text scores
original_scores = {}
if os.path.exists(original_path):
    with open(original_path, "r", encoding="utf-8") as f:
        original_data = json.load(f)
    for entry in original_data:
        input_file = entry.get("input_file")
        if not input_file:
            continue
        label = normalize_label(input_file)
        response = entry.get("response", {})
        score = None
        time = None
        score_data = response.get("score") if isinstance(response, dict) else None
        if isinstance(score_data, dict):
            score = score_data.get("generalScore")
            if isinstance(score, list) and score:
                score = score[0]
        if isinstance(response, dict):
            time = response.get("time")
        if score is None:
            continue
        original_scores.setdefault(label, []).append({"score": score, "time": time})
else:
    raise FileNotFoundError(f"Original input results not found: {original_path}")

# Load improved text scores
improved_scores = {}
if os.path.exists(improved_path):
    with open(improved_path, "r", encoding="utf-8") as f:
        improved_data = json.load(f)
    for entry in improved_data:
        label = entry.get("Text")
        score = entry.get("GeneralScore")
        time = entry.get("Time")
        if isinstance(score, list) and score:
            score = score[0]
        if label is None or score is None:
            continue
        improved_scores.setdefault(label, []).append({"score": score, "time": time})
else:
    raise FileNotFoundError(f"Improved results not found: {improved_path}")


def aggregate(values):
    if not values:
        return {"mean_score": None}
    scores = [v["score"] for v in values if v["score"] is not None]
    return {
        "mean_score": sum(scores) / len(scores) if scores else None,
    }

comparison = []
for label, original_values in original_scores.items():
    improved_values = improved_scores.get(label, [])
    original_agg = aggregate(original_values)
    improved_agg = aggregate(improved_values)
    comparison.append({
        "text": label,
        "original_mean_score": original_agg["mean_score"],
        "improved_mean_score": improved_agg["mean_score"],
        "score_difference": None if None in (original_agg["mean_score"], improved_agg["mean_score"]) else improved_agg["mean_score"] - original_agg["mean_score"],
    })

comparison.sort(key=lambda item: (item["improved_mean_score"] if item["improved_mean_score"] is not None else -999), reverse=True)

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(comparison, f, indent=2, ensure_ascii=False)

with open(output_csv, "w", encoding="utf-8") as f:
    header = [
        "text",
        "original_mean_score",
        "improved_mean_score",
        "score_difference",
    ]
    f.write(",".join(header) + "\n")
    for row in comparison:
        csv_values = [
            row["text"],
            f"{row['original_mean_score']:.3f}" if row["original_mean_score"] is not None else "",
            f"{row['improved_mean_score']:.3f}" if row["improved_mean_score"] is not None else "",
            f"{row['score_difference']:.3f}" if row["score_difference"] is not None else "",
        ]
        f.write(",".join(csv_values) + "\n")

print(f"Saved comparison JSON to {output_json}")
print(f"Saved comparison CSV to {output_csv}")

try:
    import matplotlib.pyplot as plt
    import numpy as np

    PALETTE = ["#4285F4", "#10A37F", "#CC785C", "#FF7000", "#7C3AED", "#E63946", "#F4A261", "#2A9D8F"]

    labels = [row["text"] for row in comparison]
    original_scores_list = [row["original_mean_score"] or 0 for row in comparison]
    improved_scores_list = [row["improved_mean_score"] or 0 for row in comparison]
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]

    x = np.arange(len(labels))
    bar_width = 0.38

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars_orig = ax.bar(x - bar_width / 2, original_scores_list, bar_width,
                       label="Original", color=colors, alpha=0.45,
                       edgecolor=colors, linewidth=1.2, zorder=3)
    bars_impr = ax.bar(x + bar_width / 2, improved_scores_list, bar_width,
                       label="Verbessert", color=colors, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    ax.set_ylabel("General Score", fontsize=11)
    ax.set_title("Eingabetext-Vergleich: Original vs. Verbessert", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars_orig:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=9, color="#555")
    for bar in bars_impr:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.legend(fontsize=10, framealpha=0.7)
    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    plot_path = os.path.join(base_dir, "improvement_comparison.pdf")
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved comparison plot to {plot_path}")
except ModuleNotFoundError:
    print("matplotlib ist nicht installiert. Installiere es mit: python -m pip install matplotlib")

print("\nComparison results:")
for row in comparison:
    print(
        f"{row['text']}: orig_score={row['original_mean_score']:.3f} | imp_score={row['improved_mean_score']:.3f} | "
        f"diff={row['score_difference']:.3f}"
    )