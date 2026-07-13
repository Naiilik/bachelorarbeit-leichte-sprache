import json
import os
import statistics

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "results")
OUTPUT_DIR = os.path.join(RESULTS_ROOT, "prompts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

input_path = os.path.join(RESULTS_ROOT, "results.json")
output_json = os.path.join(OUTPUT_DIR, "prompt_comparison.json")
output_plot_score = os.path.join(OUTPUT_DIR, "prompt_average_score.pdf")
output_plot_time = os.path.join(OUTPUT_DIR, "prompt_average_time.pdf")

with open(input_path, "r") as f:
    results = json.load(f)

prompt_data = {}
for entry in results:
    prompt = entry.get("Prompt", "unknown")
    score = entry.get("GeneralScore")
    time = entry.get("Time")
    if score is None:
        continue
    prompt_data.setdefault(prompt, {"scores": [], "times": []})
    prompt_data[prompt]["scores"].append(score)
    if time is not None:
        prompt_data[prompt]["times"].append(time)

prompt_summary = []
for prompt, values in prompt_data.items():
    scores = values["scores"]
    times = values["times"]
    avg_score = statistics.mean(scores)
    avg_time = statistics.mean(times) if times else None
    summary = {
        "prompt": prompt,
        "average_general_score": avg_score,
        "best_score": max(scores),
        "average_time": avg_time,
        "min_time": min(times) if times else None,
        "count": len(scores),
        "score_std": statistics.pstdev(scores) if len(scores) > 1 else 0,
    }
    prompt_summary.append(summary)

prompt_summary.sort(key=lambda item: item["average_general_score"], reverse=True)

with open(output_json, "w") as f:
    json.dump(prompt_summary, f, indent=2)

print(f"Saved prompt comparison JSON to {output_json}")
for rank, item in enumerate(prompt_summary, start=1):
    time_str = f", avg time = {item['average_time']:.3f}" if item["average_time"] is not None else ""
    print(f"{rank:2}. {item['prompt']}: score = {item['average_general_score']:.3f} ({item['count']} entries){time_str}")

try:
    labels = [item["prompt"] for item in prompt_summary]
    avg_scores = [item["average_general_score"] for item in prompt_summary]
    best_scores = [item["best_score"] for item in prompt_summary]
    avg_times = [item["average_time"] or 0 for item in prompt_summary]
    min_times = [item["min_time"] or 0 for item in prompt_summary]

    PALETTE = ["#4285F4", "#10A37F", "#CC785C", "#FF7000", "#7C3AED", "#E63946", "#F4A261", "#2A9D8F"]
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]

    x = np.arange(len(labels))

    # --- Score plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars = ax.bar(x, avg_scores, 0.55, color=colors, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    ax.set_ylabel("General Score", fontsize=11)
    ax.set_title("Prompt-Vergleich", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    fig.savefig(output_plot_score, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved score plot to {output_plot_score}")

    # --- Time plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars_t = ax.bar(x, avg_times, 0.55, color=colors, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    ax.set_ylabel("Zeit (s)", fontsize=11)
    ax.set_title("Prompt-Vergleich", fontsize=14, fontweight="bold", pad=14)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars_t:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.legend(fontsize=10, framealpha=0.7)
    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    fig.savefig(output_plot_time, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved time plot to {output_plot_time}")

except ModuleNotFoundError:
    print("matplotlib ist nicht installiert. Installiere es mit: python -m pip install matplotlib")
