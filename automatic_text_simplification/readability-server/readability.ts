import { hyphenate as hyphenate } from "hyphen/de";
import { AlgorithmResult, AnalyseResult } from "./types/readability";

export function fleschReadingEaseDescription(
  ASL: number,
  ASW: number,
): number[] {
  var score = 180 - ASL - 58.5 * ASW;

  var newFRE = score;
  newFRE = newFRE < 0 ? 0 : newFRE;
  newFRE = newFRE > 100 ? 100 : newFRE;
  return [score, newFRE];
}

export function LIX(
  words: number,
  sentences: number,
  longWord: number,
): number[] {
  var score = words / sentences + (longWord * 100) / words;

  var newLIX = score;
  newLIX = newLIX < 20 ? 20 : newLIX;
  newLIX = newLIX > 80 ? 80 : newLIX;
  newLIX = Math.abs(((newLIX - 20) / 60) * 100 - 100);
  return [score, newLIX];
}

export function WS1(MS: number, SL: number, IW: number, ES: number): number[] {
  var score = 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875;

  var newWS1 = score;
  newWS1 = newWS1 < 4 ? 4 : newWS1;
  newWS1 = newWS1 > 15 ? 15 : newWS1;
  newWS1 = Math.abs(((newWS1 - 4) / 9) * 100 - 100);

  return [score, newWS1];
}

export function WS2(MS: number, SL: number, IW: number): number[] {
  var score = 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779;

  var newWS2 = score;
  newWS2 = newWS2 < 4 ? 4 : newWS2;
  newWS2 = newWS2 > 15 ? 15 : newWS2;
  newWS2 = Math.abs(((newWS2 - 4) / 9) * 100 - 100);

  return [score, newWS2];
}

export function WS3(MS: number, SL: number): number[] {
  var score = 0.29663 * MS + 0.1905 * SL - 1.1144;
  var newWS3 = score;
  newWS3 = newWS3 < 4 ? 4 : newWS3;
  newWS3 = newWS3 > 15 ? 15 : newWS3;
  newWS3 = Math.abs(((newWS3 - 4) / 9) * 100 - 100);

  return [score, newWS3];
}

export function WS4(MS: number, SL: number): number[] {
  var score = 0.2744 * MS + 0.2656 * SL - 1.693;
  var newWS4 = score;
  newWS4 = newWS4 < 4 ? 4 : newWS4;
  newWS4 = newWS4 > 15 ? 15 : newWS4;
  newWS4 = Math.abs(((newWS4 - 4) / 9) * 100 - 100);

  return [score, newWS4];
}

export function generalScore(
  ASL: number,
  ASW: number,
  words: number,
  sentences: number,
  MS: number,
  SL: number,
  IW: number,
  ES: number,
  longWord: number,
): number[] {
  var newFRE = fleschReadingEaseDescription(ASL, ASW)[1];

  var newWS1 = WS1(MS, SL, IW, ES)[1];

  var newWS2 = WS2(MS, SL, IW)[1];

  var newWS3 = WS3(MS, SL)[1];

  var newWS4 = WS4(MS, SL)[1];

  var lix = LIX(words, sentences, longWord)[1];

  var newGeneralScore = (newFRE + newWS1 + newWS2 + newWS3 + newWS4 + lix) / 6;
  return [newGeneralScore, newFRE, newWS1, newWS2, newWS3, newWS4, lix];
}

export function scores(results: AnalyseResult | null): AlgorithmResult {
  const empty = {
    words: 0,
    sentences: 0,
    syllableCount: 0,
    ASL: 0,
    ASW: 0,
    SL: 0,
    MS: 0,
    IW: 0,
    ES: 0,
    longWord: 0,
  };

  // Absicherung, falls Analyse-Objekte fehlen oder leer sind
  results = results && results.words ? results : empty;

  // Hilfsfunktion: Gibt true zurück, wenn keine Wörter vorhanden sind
  const isEmpty = (analyse: AnalyseResult) =>
    !analyse.words || analyse.words === 0;

  return {
    fleschReadingEase: isEmpty(results)
      ? [0, 0]
      : [
          fleschReadingEaseDescription(results.ASL, results.ASW)[0],
          fleschReadingEaseDescription(results.ASL, results.ASW)[1],
        ],
    WS1: isEmpty(results)
      ? [0, 0]
      : [
          WS1(results.MS, results.SL, results.IW, results.ES)[0],
          WS1(results.MS, results.SL, results.IW, results.ES)[1],
        ],
    WS2: isEmpty(results)
      ? [0, 0]
      : [
          WS2(results.MS, results.SL, results.IW)[0],
          WS2(results.MS, results.SL, results.IW)[1],
        ],
    WS3: isEmpty(results)
      ? [0, 0]
      : [WS3(results.MS, results.SL)[0], WS3(results.MS, results.SL)[1]],
    WS4: isEmpty(results)
      ? [0, 0]
      : [WS4(results.MS, results.SL)[0], WS4(results.MS, results.SL)[1]],
    LIX: isEmpty(results)
      ? [0, 0]
      : [
          LIX(results.words, results.sentences, results.longWord)[0],
          LIX(results.words, results.sentences, results.longWord)[1],
        ],
    generalScore: isEmpty(results)
      ? [0, 0]
      : [
          generalScore(
            results.ASL,
            results.ASW,
            results.words,
            results.sentences,
            results.MS,
            results.SL,
            results.IW,
            results.ES,
            results.longWord,
          )[0],
          generalScore(
            results.ASL,
            results.ASW,
            results.words,
            results.sentences,
            results.MS,
            results.SL,
            results.IW,
            results.ES,
            results.longWord,
          )[0],
        ],
  };
}

export async function analyse(text: string): Promise<AnalyseResult> {
  if (!text || !text.trim()) {
    return {
      words: 0,
      sentences: 0,
      syllableCount: 0,
      ASL: 0,
      ASW: 0,
      SL: 0,
      MS: 0,
      IW: 0,
      ES: 0,
      longWord: 0,
    };
  }
  const words = text
    .split(/\s+/)
    .map((w) => w.replace(/[^\wäöüÄÖÜß]/g, ""))
    .filter(Boolean);
  const sentences = text
    .split(/[.!?\n\r]+/)
    .map((s) => s.trim())
    .filter(Boolean);
  const result = await hyphenate(text);
  const syllableCount = result.split(/[\u00AD\s]+/g).length;

  let MS = 0,
    IW = 0,
    ES = 0,
    longWord = 0;
  for (let i = 0; i < words.length; i++) {
    const hyphenated = await hyphenate(words[i]);
    if (hyphenated.split(/[\u00AD\s]+/g).length >= 3) MS++;
    if (words[i].length > 6) {
      IW++;
      longWord++;
    }
    if (hyphenated.split(/[\u00AD\s]+/g).length == 1) ES++;
  }

  return {
    words: words.length,
    sentences: sentences.length,
    syllableCount,
    ASL: words.length && sentences.length ? words.length / sentences.length : 0,
    ASW: words.length ? syllableCount / words.length : 0,
    SL: words.length && sentences.length ? words.length / sentences.length : 0,
    MS: words.length ? (MS / words.length) * 100 : 0,
    IW: words.length ? (IW / words.length) * 100 : 0,
    ES: words.length ? (ES / words.length) * 100 : 0,
    longWord,
  };
}
