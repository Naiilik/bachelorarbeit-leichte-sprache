import json
from pathlib import Path


def load_results(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sort_combinations_by_score(results: list[dict], descending: bool = True) -> list[dict]:
    return sorted(
        results,
        key=lambda entry: entry.get("GeneralScore", float("-inf")),
        reverse=descending,
    )


def format_entry(entry: dict) -> str:
    return (
        f"Model: {entry.get('model', 'unknown')} | Prompt: {entry.get('Prompt', 'unknown')} | "
        f"Text: {entry.get('Text', 'unknown')} | GS: {entry.get('GeneralScore', 'n/a')} | "
        f"Time: {entry.get('Time', 'n/a')} | StdScore: {entry.get('StdScore', 'n/a')} | "
        f"StdTime: {entry.get('StdTime', 'n/a')}"
    )


def save_sorted_results(results: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main() -> None:
    results_root = Path(__file__).resolve().parent.parent / "results"
    output_dir = results_root / "qualityAnalysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = results_root / "results.json"
    output_path = output_dir / "results_sorted.json"

    results = load_results(input_path)
    sorted_results = sort_combinations_by_score(results, descending=True)
    save_sorted_results(sorted_results, output_path)

    print(f"Sortierte Kombinationen nach GeneralScore in '{output_path}' gespeichert.")
    print(f"Gesamtanzahl Kombinationen: {len(sorted_results)}\n")

    if not sorted_results:
        print("Keine Daten zum Auswerten gefunden.")
        return

    best = sorted_results[0]
    worst = sorted_results[-1]

    print("Beste Kombination (höchster GS):")
    print(format_entry(best))
    print()
    print("Schlechteste Kombination (niedrigster GS):")
    print(format_entry(worst))


if __name__ == "__main__":
    main()
