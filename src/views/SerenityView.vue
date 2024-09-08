<script setup lang="ts">
import { ref, computed } from 'vue'
import quotes from '../quotes.ts'
import { shuffleArray } from '@/shuffle.ts'
import Affirmation from '@/components/AffirmationComponent.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const ambianceSound = new Audio('/sounds/dreamy.mp3')
ambianceSound.loop = true
ambianceSound.volume = 0.3
ambianceSound.play()

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
  <Affirmation
    :video-src="selectedVideo.replace('../../public', '')"
    :text="currentItem.languages[locale]"
    :audio-src="`/sounds/${currentItem.soundpaths[locale]}`"
    :next="next"
    :key="index"
    :language="locale"
  />
</template>

<style scoped></style>
