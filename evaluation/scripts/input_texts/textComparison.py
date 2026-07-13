import json
import os
import statistics

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "results")
OUTPUT_DIR = os.path.join(RESULTS_ROOT, "input_texts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

input_path = os.path.join(RESULTS_ROOT, "results.json")
output_json = os.path.join(OUTPUT_DIR, "text_comparison.json")
output_plot_score = os.path.join(OUTPUT_DIR, "text_average_score.pdf")
output_plot_time = os.path.join(OUTPUT_DIR, "text_average_time.pdf")

with open(input_path, "r") as f:
    results = json.load(f)

text_data = {}
for entry in results:
    text_label = entry.get("Text", "unknown")
    score = entry.get("GeneralScore")
    time = entry.get("Time")
    if score is None:
        continue
    text_data.setdefault(text_label, {"scores": [], "times": []})
    text_data[text_label]["scores"].append(score)
    if time is not None:
        text_data[text_label]["times"].append(time)

text_summary = []
for text_label, values in text_data.items():
    scores = values["scores"]
    times = values["times"]
    avg_score = statistics.mean(scores)
    avg_time = statistics.mean(times) if times else None
    summary = {
        "text": text_label,
        "average_general_score": avg_score,
        "best_score": max(scores),
        "average_time": avg_time,
        "min_time": min(times) if times else None,
        "count": len(scores),
        "score_std": statistics.pstdev(scores) if len(scores) > 1 else 0,
    }
    text_summary.append(summary)

text_summary.sort(key=lambda item: item["average_general_score"], reverse=True)

with open(output_json, "w") as f:
    json.dump(text_summary, f, indent=2)

print(f"Saved text comparison JSON to {output_json}")
for rank, item in enumerate(text_summary, start=1):
    time_str = f", avg time = {item['average_time']:.3f}" if item["average_time"] is not None else ""
    print(f"{rank:2}. {item['text']}: score = {item['average_general_score']:.3f} ({item['count']} entries){time_str}")

try:
    labels = [item["text"] for item in text_summary]
    avg_scores = [item["average_general_score"] for item in text_summary]
    best_scores = [item["best_score"] for item in text_summary]
    avg_times = [item["average_time"] or 0 for item in text_summary]
    min_times = [item["min_time"] or 0 for item in text_summary]
    counts = [f"n={item['count']}" for item in text_summary]

    x = np.arange(len(labels))
    COLOR_SCORE = "#4C72B0"
    COLOR_TIME = "#55A868"

    # --- Score plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars = ax.bar(x, avg_scores, 0.55, color=COLOR_SCORE, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    ax.set_ylabel("General Score", fontsize=11)
    ax.set_title("Eingabetext-Vergleich: Durchschnittlicher Score", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    for xi, label in zip(x, counts):
        ax.text(xi, -0.08, label, ha="center", va="top", fontsize=8.5, color="#666",
                transform=ax.get_xaxis_transform())

    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    fig.savefig(output_plot_score, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved score plot to {output_plot_score}")

    # --- Time plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars_t = ax.bar(x, avg_times, 0.55, color=COLOR_TIME, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    ax.set_ylabel("Zeit (s)", fontsize=11)
    ax.set_title("Eingabetext-Vergleich: Durchschnittliche Zeit", fontsize=14, fontweight="bold", pad=14)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars_t:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    for xi, label in zip(x, counts):
        ax.text(xi, -0.08, label, ha="center", va="top", fontsize=8.5, color="#666",
                transform=ax.get_xaxis_transform())

    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    fig.savefig(output_plot_time, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved time plot to {output_plot_time}")

except ModuleNotFoundError:
    print("matplotlib ist nicht installiert. Installiere es mit: python -m pip install matplotlib")
