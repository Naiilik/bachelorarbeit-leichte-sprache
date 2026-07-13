import json
import os
import statistics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "results")
output_dir = os.path.join(RESULTS_ROOT, "standard_deviation")
os.makedirs(output_dir, exist_ok=True)

input_path = os.path.join(RESULTS_ROOT, "results.json")
output_json = os.path.join(output_dir, "stability.json")
output_plot = os.path.join(output_dir, "model_stability.pdf")
output_plot_top = os.path.join(output_dir, "model_stability_top_bottom.pdf")

with open(input_path, "r") as f:
    results = json.load(f)

models = {}
for entry in results:
    model = entry.get("model", "unknown")
    score = entry.get("GeneralScore")
    if score is None:
        continue
    models.setdefault(model, []).append(score)

stability_results = []
for model, scores in models.items():
    overall_mean = statistics.mean(scores)
    overall_std = statistics.stdev(scores) if len(scores) > 1 else 0.0
    stability_results.append({
        "model": model,
        "overall_general_score_mean": overall_mean,
        "overall_general_score_std": overall_std,
        "value_count": len(scores),
    })

stability_results.sort(key=lambda item: item["overall_general_score_std"])

with open(output_json, "w") as f:
    json.dump(stability_results, f, indent=2)

print(f"Saved stability results to {output_json}")
for rank, item in enumerate(stability_results, start=1):
    print(
        f"{rank:2}. {item['model']} - mean: {item['overall_general_score_mean']:.3f}, "
        f"std: {item['overall_general_score_std']:.3f}, values: {item['value_count']}"
    )

try:
    import matplotlib.pyplot as plt
    import numpy as np

    PALETTE = ["#4285F4", "#10A37F", "#CC785C", "#FF7000", "#7C3AED", "#E63946", "#F4A261", "#2A9D8F"]

    # sorted ascending by std — most stable first; reverse for barh so best appears at top
    labels_all = [item["model"] for item in stability_results]
    std_all = [item["overall_general_score_std"] for item in stability_results]
    colors_all = [PALETTE[i % len(PALETTE)] for i in range(len(labels_all))]

    labels_rev = list(reversed(labels_all))
    std_rev = list(reversed(std_all))
    colors_rev = list(reversed(colors_all))

    # --- Full plot (horizontal) ---
    fig, ax = plt.subplots(figsize=(8, max(5, len(labels_all) * 0.5)))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    y = np.arange(len(labels_rev))
    bars = ax.barh(y, std_rev, 0.6, color=colors_rev, alpha=0.85, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels(labels_rev, fontsize=9, fontweight="bold")
    ax.set_xlabel("Standardabweichung (GeneralScore)", fontsize=11)
    ax.set_title("Modell-Stabilität: Standardabweichung des GeneralScore", fontsize=13, fontweight="bold", pad=14)
    ax.xaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar, value in zip(bars, std_rev):
        ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}", ha="left", va="center", fontsize=8, fontweight="bold")

    plt.subplots_adjust(left=0.22, right=0.93, top=0.93, bottom=0.1)
    fig.savefig(output_plot, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved full plot to {output_plot}")

    # --- Top 5 stabilste / Bottom 5 instabilste ---
    n = min(5, len(stability_results) // 2)
    top5 = stability_results[:n]       # niedrigste std = stabilste
    bottom5 = stability_results[-n:]   # höchste std = instabilste

    tb_items = top5 + bottom5
    tb_labels = [item["model"] for item in tb_items]
    tb_std = [item["overall_general_score_std"] for item in tb_items]
    tb_colors = ["#10A37F"] * n + ["#E63946"] * n

    x = np.arange(len(tb_labels))

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars_tb = ax.bar(x, tb_std, 0.55, color=tb_colors, alpha=0.85, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(tb_labels, fontsize=11, fontweight="bold", rotation=15, ha="right")
    ax.set_ylabel("Standardabweichung (GeneralScore)", fontsize=11)
    ax.set_title(f"Top {n} stabilste & {n} instabilste Modelle", fontsize=14, fontweight="bold", pad=14)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars_tb:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    from matplotlib.patches import Patch
    legend_handles = [
        Patch(facecolor="#10A37F", alpha=0.85, label=f"Top {n} stabilste"),
        Patch(facecolor="#E63946", alpha=0.85, label=f"Top {n} instabilste"),
    ]
    ax.legend(handles=legend_handles, fontsize=10, framealpha=0.7)
    ax.axvline(x=n - 0.5, color="#999", linestyle="--", linewidth=1, zorder=2)

    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.18)
    fig.savefig(output_plot_top, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved top/bottom plot to {output_plot_top}")

except ModuleNotFoundError:
    print("matplotlib ist nicht installiert. Installiere es mit: python -m pip install matplotlib")
