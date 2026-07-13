<template>
  <div class="container">
    <h1>Verständnisstudie</h1>

    <div class="group-info" v-if="group">Gruppe: {{ group }}</div>

    <div class="audio-card">
      <h2>Text anhören</h2>
      <p v-if="!audioPlayed" class="audio-hint">Bitte hören Sie sich den Text an, bevor Sie die Fragen beantworten.</p>
      <p v-else class="audio-done">Audio wurde abgespielt.</p>
      <div class="button-row">
        <button @click="readText" :disabled="audioPlayed || isPlaying">🔊 Vorlesen</button>
        <button @click="pauseReading" :disabled="!isPlaying">⏸ Pause</button>
      </div>
    </div>

    <template v-if="audioPlayed">
      <div
        v-for="(question, qIndex) in questions"
        :key="qIndex"
        class="question-card"
      >
        <h3>{{ qIndex + 1 }}. {{ question.question }}</h3>

        <label
          v-for="(option, oIndex) in question.options"
          :key="oIndex"
          class="option"
        >
          <input
            type="radio"
            :name="'question-' + qIndex"
            :value="oIndex"
            v-model="answers[qIndex]"
          />
          {{ option }}
        </label>
      </div>

      <button class="submit-button" @click="submit" :disabled="submitted">
        Antworten absenden
      </button>
    </template>

    <div class="result-card" v-if="submitted">
      <h2>Ergebnis: {{ score }} / {{ questions.length }}</h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { questions } from "./questions";

const group = ref<string | null>(null);
const submitted = ref(false);
const score = ref(0);
const answers = ref<(number | undefined)[]>([]);
const audioPlayed = ref(false);
const isPlaying = ref(false);

const audio = ref<HTMLAudioElement | null>(null);

onMounted(async () => {
  const data = await $fetch<{ group: string }>("/api/group");
  group.value = data.group;

  const src = data.group === "A" ? "/audio-a.mp3" : "/audio-b.mp3";
  audio.value = new Audio(src);
  audio.value.onended = () => {
    isPlaying.value = false;
    audioPlayed.value = true;
  };
});

function readText() {
  if (!audio.value || audioPlayed.value) return;
  audio.value.play();
  isPlaying.value = true;
}

function pauseReading() {
  if (!audio.value) return;
  audio.value.pause();
  isPlaying.value = false;
}

async function submit() {
  let correct = 0;
  questions.forEach((question, index) => {
    if (answers.value[index] === question.correct) correct++;
  });

  score.value = correct;
  submitted.value = true;

  await $fetch("/api/result", {
    method: "POST",
    body: {
      group: group.value,
      score: correct,
      answers: answers.value,
      timestamp: Date.now(),
    },
  });
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
  padding: 40px;
  font-family: Arial, sans-serif;
}

.group-info {
  margin-bottom: 20px;
  color: #777;
}

.audio-card,
.question-card,
.result-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #ddd;
}

.audio-hint {
  color: #555;
  margin-bottom: 12px;
}

.audio-done {
  color: #2a9d2a;
  margin-bottom: 12px;
}

.button-row {
  display: flex;
  gap: 10px;
}

button {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.option {
  display: block;
  margin-top: 10px;
}

.submit-button {
  width: 100%;
  font-size: 16px;
  padding: 14px;
}

.result-card {
  text-align: center;
}
</style>
