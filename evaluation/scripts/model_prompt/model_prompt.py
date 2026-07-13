import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "results")
OUTPUT_DIR = os.path.join(RESULTS_ROOT, "model_prompt")
os.makedirs(OUTPUT_DIR, exist_ok=True)

input_path = os.path.join(RESULTS_ROOT, "results.json")
output_json = os.path.join(OUTPUT_DIR, "model_prompt_matrix.json")

with open(input_path, "r") as f:
    results = json.load(f)

models = []
prompts = []
cell_values = {}

for entry in results:
    model = entry.get("model", "unknown")
    prompt = entry.get("Prompt", "unknown")
    score = entry.get("GeneralScore")
    if score is None:
        continue
    if model not in models:
        models.append(model)
    if prompt not in prompts:
        prompts.append(prompt)
    cell_values.setdefault((model, prompt), []).append(score)

# Build matrix of average scores
matrix = []
for model in models:
    row = []
    for prompt in prompts:
        values = cell_values.get((model, prompt), [])
        row.append(sum(values) / len(values) if values else None)
    matrix.append(row)

# Sort models by average GeneralScore across prompts
model_rows = []
for model, row in zip(models, matrix):
    valid_values = [value for value in row if value is not None]
    avg_score = sum(valid_values) / len(valid_values) if valid_values else 0
    model_rows.append((model, row, avg_score))

model_rows.sort(key=lambda item: item[2], reverse=True)
models, matrix, _ = zip(*model_rows)
models = list(models)
matrix = list(matrix)

output_data = {
    "models": models,
    "prompts": prompts,
    "matrix": matrix,
}

with open(output_json, "w") as f:
    json.dump(output_data, f, indent=2)

csv_path = os.path.join(OUTPUT_DIR, "model_prompt_matrix.csv")
with open(csv_path, "w") as f:
    header = ["model"] + prompts
    f.write(",".join(header) + "\n")
    for model, row in zip(models, matrix):
        row_values = [f"{value:.2f}" if value is not None else "" for value in row]
        f.write(model + "," + ",".join(row_values) + "\n")

print(f"Saved model/prompt matrix to {output_json}")
print(f"Saved table CSV to {csv_path}")

# Print simple table
col_widths = [max(len(str(item)), 7) for item in header]
for j, prompt in enumerate(prompts, start=1):
    col_widths[j] = max(col_widths[j], len(prompt))
for i, model in enumerate(models):
    col_widths[0] = max(col_widths[0], len(model))

row_format = " | ".join(f"{{:<{w}}}" for w in col_widths)
print(row_format.format(*header))
print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
for model, row in zip(models, matrix):
    row_values = [f"{value:.2f}" if value is not None else "" for value in row]
    print(row_format.format(model, *row_values))

# --- Analysis ---

# Best and worst model per prompt
per_prompt = {}
for j, prompt in enumerate(prompts):
    col = [(models[i], matrix[i][j]) for i in range(len(models)) if matrix[i][j] is not None]
    col.sort(key=lambda x: x[1], reverse=True)
    per_prompt[prompt] = {
        "best_model":  col[0][0],  "best_score":  round(col[0][1], 3),
        "worst_model": col[-1][0], "worst_score": round(col[-1][1], 3),
    }

# Spread per model across prompts (max - min of row)
model_spread = []
for model, row in zip(models, matrix):
    valid = [v for v in row if v is not None]
    if not valid:
        continue
    spread = max(valid) - min(valid)
    model_spread.append({
        "model": model,
        "spread": round(spread, 3),
        "max_score": round(max(valid), 3),
        "min_score": round(min(valid), 3),
    })
model_spread.sort(key=lambda x: x["spread"])

analysis = {
    "best_worst_per_prompt": per_prompt,
    "most_consistent_model": model_spread[0],
    "most_variable_model":   model_spread[-1],
    "spread_ranking": model_spread,
}

analysis_path = os.path.join(OUTPUT_DIR, "model_prompt_analysis.json")
with open(analysis_path, "w") as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)
print(f"\nSaved analysis to {analysis_path}")

print("\n--- Bestes & schlechtestes Modell pro Prompt ---")
for prompt, data in per_prompt.items():
    print(f"  {prompt}: Bestes={data['best_model']} ({data['best_score']:.1f})  |  Schlechtestes={data['worst_model']} ({data['worst_score']:.1f})")

print("\n--- Konsistenz über Prompts (Spread = max - min) ---")
print(f"  Geringster Abstand: {model_spread[0]['model']}  (spread={model_spread[0]['spread']:.3f})")
print(f"  Größter Abstand:    {model_spread[-1]['model']}  (spread={model_spread[-1]['spread']:.3f})")
