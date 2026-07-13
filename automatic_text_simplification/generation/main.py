import requests
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")
DATA_PATH = os.path.join(SCRIPT_DIR, "results", "data.json")

# Production URL des n8n Workflows 
URL = "http://localhost:5678/webhook/45fa5a94-e74e-4e3b-9c27-135adc541655"



#----------------------------------------------------------------------#
#                           HIER BEARBEITEN
#----------------------------------------------------------------------#
#-----------#
temperatur = "0.6"  # Temperatur pro Modell
runs = 3            # Anzahl der Wiederholungen pro Kombination
#-----------#

# Kombination auswählen
# Leer lassen -> Schleife iteriert über alle Einträge innerhalb des JSON
# Einfügen -> Es wird für die Kategorie nur der Eintrag beachtet
# Hinweis: Beim Einfügen eines Modells werden die LLM-Familien ignoriert,
# zu denen das Modell nicht gehört
SELECTED_PROMPTS = []   # z. B. ["Komplex"]
SELECTED_TEXTS = []     # z. B. ["Alltagstext"]
SELECTED_LLMS = []      # z. B. ["Claude"]
SELECTED_MODELS = []    # z. B. ["claude-opus-4-20250514"]
#-----------#
#----------------------------------------------------------------------#



with open(os.path.join(CONFIG_DIR, "prompts.json"), encoding="utf-8") as f:
    prompts_data = json.load(f)
with open(os.path.join(CONFIG_DIR, "text.json"), encoding="utf-8") as f:
    texts_data = json.load(f)
with open(os.path.join(CONFIG_DIR, "models.json"), encoding="utf-8") as f:
    models_data = json.load(f)


def gefiltert(alle, auswahl):
    if not auswahl:
        return list(alle)
    return [x for x in alle if x in auswahl]


def lade_ergebnisse():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        return []
    with open(DATA_PATH) as f:
        return json.load(f)


def speichere_ergebnisse(ergebnisse):
    with open(DATA_PATH, "w") as f:
        json.dump(ergebnisse, f, indent=2)


ergebnisse = lade_ergebnisse()

for prompt_key in gefiltert(prompts_data.keys(), SELECTED_PROMPTS):
    promptTitle = prompt_key
    prompt = prompts_data[prompt_key]
    for text_key in gefiltert(texts_data.keys(), SELECTED_TEXTS):
        inputTextTitle = text_key
        inputText = texts_data[text_key]
        for llm in gefiltert(models_data.keys(), SELECTED_LLMS):
            for model in gefiltert(models_data[llm], SELECTED_MODELS):
                for run in range(runs):
                    print(f"{llm}/{model} | {prompt_key} | {text_key} | Lauf {run + 1}")
                    try:
                        response = requests.post(URL, json={
                            "text": inputText,
                            "textTitle": inputTextTitle,
                            "model": model,
                            "prompt": prompt,
                            "promptTitle": promptTitle,
                            "LLM": llm,
                            "temperatur": temperatur,
                        }, timeout=120)
                        response.raise_for_status()
                        ergebnisse.append(response.json())
                        speichere_ergebnisse(ergebnisse)
                    except requests.RequestException as e:
                        print(f"Fehler bei {llm}/{model} ({prompt_key}, {text_key}): {e}")