import json
import os
import statistics
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(SCRIPT_DIR, "..", "..", "automatic_text_simplification", "generation", "results", "data.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "results", "results.json")

with open(RESULTS_PATH, "r") as f:
    all_results = json.load(f)

groups = defaultdict(lambda: {"scores": [], "times": []})
for entry in all_results:
    key = (entry["promptTitle"], entry["textTitle"], entry.get("model", "unknown"))
    groups[key]["scores"].append(entry.get("score", {}).get("generalScore", [None])[0])
    groups[key]["times"].append(entry.get("time", 1000))

all_entries = []
for (prompt, text, model), values in groups.items():
    all_entries.append({
        "model" : model,
        "GeneralScore" : statistics.mean(values["scores"]),
        "StdScore" : statistics.stdev(values["scores"]),
        "Time" : statistics.mean(values["times"]),
        "StdTime" : statistics.stdev(values["times"]),
        "Prompt" : prompt,
        "Text" : text
    })

# Speichere alle Einträge in JSON
if not os.path.exists(os.path.dirname(OUTPUT_PATH)):
    os.makedirs(os.path.dirname(OUTPUT_PATH))
with open(OUTPUT_PATH, "w") as f:
    json.dump(all_entries, f, indent=2)

print("Ergebnisse gespeichert in results/results.json")