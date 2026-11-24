<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import quotes from '../quotes.ts'
import { shuffleArray } from '@/shuffle.ts'
import Affirmation from '@/components/AffirmationComponent.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { useI18n } from 'vue-i18n'

const { locale, t } = useI18n()

const ambianceSound = new Audio('/sounds/dreamy.mp3')
ambianceSound.loop = true
ambianceSound.volume = 0.3

// Browsers block sound until the user interacts with the page: coming from
// the home page, its click allows it; on a direct load, a click to start.
const started = ref(false)
const start = () =>
  ambianceSound.play().then(
    () => (started.value = true),
    // blocked: wait for the click; any other error (no file): go on mute
    (e) => (started.value = e.name !== 'NotAllowedError'),
  )
onMounted(start)
onUnmounted(() => ambianceSound.pause())

const quotesList = shuffleArray(quotes)
const videoFiles = Object.keys(import.meta.glob('../../public/backgrounds/*.mp4', { eager: true }))

const index = ref(quotesList.length - 1)
const currentItem = computed(() => quotesList[index.value])

const selectedVideo = ref(videoFiles[Math.floor(Math.random() * videoFiles.length)])

const next = () => {
  setTimeout(() => {
    index.value = (index.value + 1) % quotesList.length
    selectedVideo.value = videoFiles[Math.floor(Math.random() * videoFiles.length)]
  }, 3000)
}
</script>

<template>
  <LanguageSwitcher />
  <div v-if="!started" class="start" @click="start">
    <p>{{ t('click-to-start').toUpperCase() }}</p>
  </div>
  <Affirmation
    v-else
    :video-src="selectedVideo.replace('../../public', '')"
    :text="currentItem.languages[locale]"
    :audio-src="`/sounds/${currentItem.soundpaths[locale]}`"
    :next="next"
    :key="index"
    :language="locale"
  />
</template>

<style scoped>
.start {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
}
</style>
