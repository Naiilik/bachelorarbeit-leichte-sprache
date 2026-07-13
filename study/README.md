# Studienapplikation

## Voraussetzungen

- Node.js

## Setup

1. Abhängigkeiten installieren

```bash
npm install
```

2. Entwicklungsserver starten

```bash
npm run dev
```

3. Production

```bash
npm run build
```

## Verwenden

Die Webapp kann direkt über den Entwicklungsserver getestet werden. Allerdings muss hierfür eine Datenbank angelegt werden, welche die Ergebnisse speichert.
Alternativ kann die Webapp auch selbst gehostet werden. Für die Arbeit wurde hierfür Cloudflare verwendet.

## Datenbank

Es wird eine Cloudflare D1 Datenbank benötigt. Hierin müssen sich zwei Tabellen befinden:

**Tabelle `results`**

- `id`
- `participant_id`
- `group_name`
- `score`
- `answers`
- `created_at`

**Tabelle `assignment_counter`**

- `group_name`
- `count`

Die Datenbank muss dem Projekt als Binding mit dem Namen `DB` zugewiesen werden,
da der Code über `env.DB` darauf zugreift.

## Lokales Testen

Für lokale Tests wird keine echte Cloudflare-Datenbank benötigt. Die Datenbankzugriffe
werden automatisch lokal emuliert (SQLite-Datei unter `.wrangler/state/v3`).

1. Lokale Datenbank mit dem Schema befüllen:

```bash
npx wrangler d1 execute DB --local --file=./schema.sql
```

2. Entwicklungsserver starten:

```bash
npm run dev
```

Die Testdaten bleiben lokal und haben keinen Einfluss auf die produktive Datenbank.

## Anpassen

Um die verwendete Audiodatei auszutauschen, muss lediglich die Audio Datei im Ordner `public` ausgetauscht werden. Die Fragen, sowie Antwortmöglichkeiten werden unter `app/questions.ts`gespeichert.

```typeScript
{
    question:
      "Warum spricht der Gutachter auch mit Angehörigen oder Betreuern?",
    options: [
      "Damit sie einen Termin vereinbaren können.",
      "Damit der Gutachter erfährt, wie viel Pflege die Person bisher erhalten hat.",
      "Damit der Gutachter besser einschätzen kann, wie selbstständig die Person ist.",
      "Damit die Angehörigen bestätigen, dass die Begutachtung stattfinden darf.",
    ],
    correct: 2,
  },
```

Hierbei gibt `question` die Frage an, `options` die Antwortmöglichkeiten und `correct` den Index der korrekten Antwort.

## Erweitern

Um eine neue Gruppe hinzuzufügen, muss unter `app/groups.ts` ein weiterer Gruppenname zur Liste hinzugefügt werden.

```typeScript
// -------------------------------------------------------
// Hier Gruppen hinzufügen oder entfernen.
// Für jede Gruppe muss eine Audiodatei public/audio-[name].mp3 existieren.
// -------------------------------------------------------
export const groups = ["A", "B"];
```

Desweiteren muss dann dem namen entsprechend, eine neue Audiodatei in den `public` Ordner hinzugefügt werden, welche folgendem Namensschema folgt: audio-[name].mp3

Um eine weitere Frage hinzuzufügen, muss lediglich ein weiterer Eintrag in `app/questions.ts` erstellt werden welcher dem Frageschema folgt, welches im Kapitel _Anpassen_ beschrieben wurde.
