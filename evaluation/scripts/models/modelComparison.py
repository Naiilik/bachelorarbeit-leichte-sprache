import json
import os
import statistics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "results")
OUTPUT_DIR = os.path.join(RESULTS_ROOT, "models")
os.makedirs(OUTPUT_DIR, exist_ok=True)

input_path = os.path.join(RESULTS_ROOT, "results.json")
output_json = os.path.join(OUTPUT_DIR, "model_ranking.json")
output_plot = os.path.join(OUTPUT_DIR, "model_ranking.pdf")

with open(input_path, "r") as f:
    results = json.load(f)

scores_by_model = {}
times_by_model = {}
for entry in results:
    model = entry.get("model", "unknown")
    score = entry.get("GeneralScore")
    time = entry.get("Time") or entry.get("time")
    if score is None:
        continue
    scores_by_model.setdefault(model, []).append(score)
    if time is not None:
        times_by_model.setdefault(model, []).append(time)

ranked = []
for model, scores in scores_by_model.items():
    avg_score = statistics.mean(scores)
    avg_time = statistics.mean(times_by_model.get(model, [0])) if times_by_model.get(model) else None
    ratio = avg_time / avg_score if avg_time is not None and avg_score != 0 else None
    ranked.append({
        "model": model,
        "average_general_score": avg_score,
        "average_time": avg_time,
        "time_per_general_score": ratio,
        "count": len(scores),
        "scores": scores,
    })

ranked.sort(key=lambda item: item["average_general_score"], reverse=True)

with open(output_json, "w") as f:
    json.dump(ranked, f, indent=2)

print(f"Saved ranking JSON to {output_json}")
print("Model ranking by average GeneralScore:")
for rank, item in enumerate(ranked, start=1):
    time_str = f", avg time = {item['average_time']:.3f}" if item["average_time"] is not None else ""
    print(f"{rank:2}. {item['model']}: {item['average_general_score']:.3f} ({item['count']} entries){time_str}")

try:
    import matplotlib.pyplot as plt

    models = [item["model"] for item in ranked]
    averages = [item["average_general_score"] for item in ranked]
    avg_times = [item["average_time"] or 0 for item in ranked]
    ratios = [item["time_per_general_score"] or 0 for item in ranked]

    models_reversed = list(reversed(models))
    averages_reversed = list(reversed(averages))
    plt.figure(figsize=(8, max(5, len(models) * 0.5)))
    bars = plt.barh(models_reversed, averages_reversed, color="#4C72B0")
    plt.xlabel("Average GeneralScore")
    plt.title("Model Comparison by Average GeneralScore")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    for bar, value in zip(bars, averages_reversed):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", ha="left", va="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150)
    print(f"Saved plot to {output_plot}")

    # Plot sorted by time / score ratio
    sorted_by_ratio = sorted(ranked, key=lambda item: item["time_per_general_score"] or float("inf"))
    models_ratio = [item["model"] for item in sorted_by_ratio]
    ratio_values = [item["time_per_general_score"] or 0 for item in sorted_by_ratio]

    plt.figure(figsize=(8, max(5, len(models_ratio) * 0.5)))
    bars = plt.barh(models_ratio, ratio_values, color="#55A868")
    plt.xlabel("Time / GeneralScore")
    plt.title("Model Comparison by Time per GeneralScore")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    for bar, value in zip(bars, ratio_values):
        plt.text(bar.get_width() + 0.0005, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", ha="left", va="center", fontsize=8)
    plt.tight_layout()
    ratio_plot = os.path.join(OUTPUT_DIR, "model_time_score_ratio.pdf")
    plt.savefig(ratio_plot, dpi=150)
    print(f"Saved ratio plot to {ratio_plot}")

    # Scatter plot: average time vs average GeneralScore
    plotted_items = [item for item in ranked if item["average_time"] is not None]
    scatter_x = [item["average_time"] for item in plotted_items]
    scatter_y = [item["average_general_score"] for item in plotted_items]
    scatter_labels = [item["model"] for item in plotted_items]

    plt.figure(figsize=(10, 6))
    plt.scatter(scatter_x, scatter_y, color="#C44E52", s=80)
    for x, y, label in zip(scatter_x, scatter_y, scatter_labels):
        plt.text(x, y, label, fontsize=8, ha="left", va="bottom")
    plt.xlabel("Average Time")
    plt.ylabel("Average GeneralScore")
    plt.title("Model Time vs GeneralScore")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    time_score_plot = os.path.join(OUTPUT_DIR, "model_time_vs_score.pdf")
    plt.savefig(time_score_plot, dpi=150)
    print(f"Saved time vs score plot to {time_score_plot}")
except ModuleNotFoundError:
    print("matplotlib ist nicht installiert. Installiere es mit: python -m pip install matplotlib")
