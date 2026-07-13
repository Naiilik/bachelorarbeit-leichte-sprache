/**
 * Result type for text analysis. Contains various metrics used in readability calculations.
 */
export type AnalyseResult = {
  words: number;
  sentences: number;
  syllableCount: number;
  ASL: number; // Average Sentence Length
  ASW: number; // Average Syllables per Word
  SL: number; // Sentence Length
  MS: number; // Mean Syllables
  IW: number; // Difficult Words
  ES: number; // Easy Sentences
  longWord: number;
};

/**
 * Result type for readability algorithms. Each property is a tuple where the first element is the score
 * and the second element is the corresponding grade level.
 */
export type AlgorithmResult = {
  fleschReadingEase: [number, number]; // 180 - ASL - 58.5 * ASW
  WS1: [number, number]; // 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875
  WS2: [number, number]; // 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779
  WS3: [number, number]; // 0.29663 * MS + 0.1905 * SL - 1.1144
  WS4: [number, number]; // 0.2744 * MS + 0.2656 * SL - 1.6932
  LIX: [number, number];
  generalScore: [number, number]; // Average of all above scores
};
