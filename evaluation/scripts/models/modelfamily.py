import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

FAMILY_PREFIXES = {
    "Gemini": ("gemini",),
    "GPT":    ("gpt",),
    "Claude": ("claude",),
    "Mistral": ("mistral",),
    "Ollama": ("qwen", "llama", "nous", "gemma", "phi"),
}

FAMILY_COLORS = {
    "Gemini": "#4285F4",
    "GPT":    "#10A37F",
    "Claude": "#CC785C",
    "Mistral": "#FF7000",
    "Ollama": "#7C3AED",
    "Other":  "#9CA3AF",
}

def classify_model(model_name: str) -> str:
    lower = model_name.lower()
    for family, prefixes in FAMILY_PREFIXES.items():
        if any(lower.startswith(p) for p in prefixes):
            return family
    return "Other"

def load_rankings(path: Path) -> list[dict]:
    with open(path) as f:
        return json.load(f)

def group_by_family(rankings: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {family: [] for family in FAMILY_PREFIXES}
    grouped["Other"] = []
    for entry in rankings:
        family = classify_model(entry["model"])
        grouped[family].append(entry)
    return {k: v for k, v in grouped.items() if v}

def build_family_stats(grouped: dict[str, list[dict]]) -> dict:
    stats = {}
    for family, models in grouped.items():
        scores = [m["average_general_score"] for m in models]
        times  = [m["average_time"] for m in models]
        best   = max(models, key=lambda m: m["average_general_score"])
        stats[family] = {
            "model_count": len(models),
            "average_score": round(sum(scores) / len(scores), 4),
            "best_score": round(max(scores), 4),
            "worst_score": round(min(scores), 4),
            "average_time_s": round(sum(times) / len(times), 4),
            "best_model": best["model"],
            "models": sorted(
                [
                    {
                        "model": m["model"],
                        "average_general_score": round(m["average_general_score"], 4),
                        "average_time": round(m["average_time"], 4),
                    }
                    for m in models
                ],
                key=lambda m: m["average_general_score"],
                reverse=True,
            ),
        }
    return stats

def save_json(stats: dict, out_path: Path) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"JSON gespeichert: {out_path}")

def plot_family_chart(stats: dict, out_path: Path) -> None:
    families = list(stats.keys())
    avg_scores = [stats[f]["average_score"] for f in families]
    best_scores = [stats[f]["best_score"] for f in families]
    colors = [FAMILY_COLORS.get(f, FAMILY_COLORS["Other"]) for f in families]

    x = np.arange(len(families))
    bar_width = 0.38

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars_avg = ax.bar(
        x - bar_width / 2, avg_scores, bar_width,
        label="Ø Score", color=colors, alpha=0.85, zorder=3
    )
    bars_best = ax.bar(
        x + bar_width / 2, best_scores, bar_width,
        label="Bester Score", color=colors, alpha=0.45,
        edgecolor=colors, linewidth=1.2, zorder=3
    )

    ax.set_xticks(x)
    ax.set_xticklabels(families, fontsize=12, fontweight="bold")
    ax.set_ylabel("General Score", fontsize=11)
    ax.set_title("Modell-Familien: Durchschnitt & Bester Score", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars_avg:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}",
            ha="center", va="bottom", fontsize=9, fontweight="bold"
        )
    for bar in bars_best:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}",
            ha="center", va="bottom", fontsize=9, color="#555"
        )

    model_counts = [f"n={stats[f]['model_count']}" for f in families]
    for xi, label in zip(x, model_counts):
        ax.text(xi, -0.08, label, ha="center", va="top", fontsize=8.5, color="#666",
                transform=ax.get_xaxis_transform())

    ax.legend(fontsize=10, framealpha=0.7)
    plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Diagramm gespeichert: {out_path}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "results" / "models"
    base.mkdir(parents=True, exist_ok=True)
    rankings = load_rankings(base / "model_ranking.json")
    grouped  = group_by_family(rankings)
    stats    = build_family_stats(grouped)

    save_json(stats, base / "model_family_stats.json")
    plot_family_chart(stats, base / "model_family_chart.pdf")
