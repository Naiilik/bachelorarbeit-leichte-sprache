export interface Question {
  question: string;
  options: string[];
  correct: number; // Index der richtigen Antwort
}

// -------------------------------------------------------
// Hier Fragen hinzufügen oder entfernen:
// -------------------------------------------------------
export const questions: Question[] = [
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
  {
    question: "Wer begutachtet privat versicherte Menschen?",
    options: [
      "Der Medizinische Dienst.",
      "Der Sozialmedizinische Dienst.",
      "Medicproof.",
      "Die Pflegekasse.",
    ],
    correct: 2,
  },
  {
    question:
      "Ein 20-jähriger Erwachsener soll begutachtet werden. Darf die Begutachtung am Telefon stattfinden?",
    options: [
      "Nein, nur Videotelefonie ist erlaubt, kein normales Telefonat.",
      "Ja, aber nur wenn eine Unterstützungsperson anwesend ist.",
      "Ja, wenn die Person zustimmt.",
      "Nein, das ist nur bei Jugendlichen zwischen 14 und 18 möglich.",
    ],
    correct: 2,
  },
  {
    question:
      "Ein 12-jähriges Kind soll begutachtet werden. Darf die Begutachtung am Telefon stattfinden?",
    options: [
      "Nein.",
      "Ja.",
      "Nur wenn das Kind zu Hause ist.",
      "Nur mit Zustimmung der Eltern.",
    ],
    correct: 0,
  },
  {
    question:
      "Eine Person stellt zum ersten Mal einen Antrag auf Pflege. Darf die Begutachtung am Telefon stattfinden?",
    options: [
      "Ja.",
      "Nur bei Kindern.",
      "Nur bei privat Versicherten.",
      "Nein.",
    ],
    correct: 3,
  },
  {
    question:
      "Ein 16-Jähriger soll telefonisch begutachtet werden. Welche zusätzliche Voraussetzung gilt?",
    options: [
      "Ein Arzt muss anwesend sein.",
      "Die Pflegekasse muss zustimmen.",
      "Eine Unterstützungsperson muss helfen.",
      "Die Eltern müssen den Pflegegrad bestimmen.",
    ],
    correct: 2,
  },
  {
    question: "Welche Aussage trifft zu?",
    options: [
      "Wer den festgestellten Pflegegrad ablehnt, kann nicht telefonisch begutachtet werden.",
      "Gutachter dürfen ohne Anmeldung erscheinen.",
      "Privatversicherte werden immer vom Medizinischen Dienst begutachtet.",
      "Kinder unter 14 Jahren dürfen telefonisch begutachtet werden.",
    ],
    correct: 0,
  },
  {
    question: "Wo findet die Begutachtung normalerweise statt?",
    options: [
      "Im Krankenhaus.",
      "In der Wohnung oder Pflegeeinrichtung.",
      "In der Pflegekasse.",
      "In einer Arztpraxis.",
    ],
    correct: 1,
  },
];
