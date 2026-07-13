import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

base = Path(__file__).resolve().parents[2] / "results" / "models"
base.mkdir(parents=True, exist_ok=True)
output_plot = base / "model_cluster.pdf"

with open(base / "model_ranking.json") as f:
    ranking = json.load(f)

scores = np.array([item["average_general_score"] for item in ranking])

# 2-cluster split at the largest gap between consecutive scores
sorted_idx = np.argsort(scores)
sorted_scores = scores[sorted_idx]
gaps = np.diff(sorted_scores)
split_pos = int(np.argmax(gaps))

cluster_labels = np.zeros(len(scores), dtype=int)
for rank, orig_idx in enumerate(sorted_idx):
    cluster_labels[orig_idx] = 0 if rank <= split_pos else 1

mean_per_cluster = {c: scores[cluster_labels == c].mean() for c in (0, 1)}
high_cluster = max(mean_per_cluster, key=mean_per_cluster.get)
color_map = {high_cluster: "#10A37F", 1 - high_cluster: "#E63946"}
dot_colors = [color_map[c] for c in cluster_labels]

fig, ax = plt.subplots(figsize=(8, 1.8))
fig.patch.set_facecolor("#F9FAFB")
ax.set_facecolor("#F9FAFB")

ax.scatter(scores, np.zeros(len(scores)),
           c=dot_colors, s=60, alpha=0.85, zorder=3, linewidths=0)

ax.set_xlabel("Ø General Score", fontsize=11)
ax.set_title("Modell Cluster", fontsize=13, fontweight="bold", pad=10)
ax.xaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
ax.set_axisbelow(True)
ax.set_yticks([])
ax.spines[["top", "right", "left"]].set_visible(False)

legend_handles = [
    Patch(facecolor="#10A37F", alpha=0.85, label="Cluster: hoher GS"),
    Patch(facecolor="#E63946", alpha=0.85, label="Cluster: niedriger GS"),
]
ax.legend(handles=legend_handles, fontsize=9, framealpha=0.7,
          loc="upper left", bbox_to_anchor=(0.0, -0.45), ncol=1)

plt.subplots_adjust(left=0.05, right=0.97, top=0.82, bottom=0.45)
fig.savefig(output_plot, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved cluster plot to {output_plot}")

gap_left  = sorted_scores[split_pos]
gap_right = sorted_scores[split_pos + 1]
print(f"Split-Gap: {gap_left:.1f} → {gap_right:.1f}  (Δ {gap_right - gap_left:.1f})")
print(f"Cluster hoch:     {(cluster_labels == high_cluster).sum()} Modelle, Ø {mean_per_cluster[high_cluster]:.1f}")
print(f"Cluster niedrig:  {(cluster_labels == 1 - high_cluster).sum()} Modelle, Ø {mean_per_cluster[1 - high_cluster]:.1f}")
