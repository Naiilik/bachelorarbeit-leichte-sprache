import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR / "scripts"

# Reihenfolge ist relevant: calculateMean.py erzeugt results/results.json,
# von dem alle folgenden Skripte lesen. modelComparison.py muss vor
# Cluster.py und modelfamily.py laufen, da diese model_ranking.json brauchen.
SCRIPTS = [
    SCRIPTS_DIR / "calculateMean.py",
    SCRIPTS_DIR / "qualityAnalysis.py",
    SCRIPTS_DIR / "model_prompt" / "model_prompt.py",
    SCRIPTS_DIR / "model_text" / "modelTextComparison.py",
    SCRIPTS_DIR / "models" / "modelComparison.py",
    SCRIPTS_DIR / "models" / "Cluster.py",
    SCRIPTS_DIR / "models" / "modelfamily.py",
    SCRIPTS_DIR / "input_texts" / "textComparison.py",
    SCRIPTS_DIR / "prompts" / "promptComparison.py",
    SCRIPTS_DIR / "standard_deviation" / "stability.py",
]

for script in SCRIPTS:
    print(f"\n=== {script.relative_to(SCRIPT_DIR)} ===")
    result = subprocess.run([sys.executable, str(script)])
    if result.returncode != 0:
        print(f"\nAbbruch: {script.relative_to(SCRIPT_DIR)} ist mit Fehler beendet worden.")
        sys.exit(result.returncode)

print("\nAlle Skripte erfolgreich ausgeführt. Ergebnisse liegen in results/.")
