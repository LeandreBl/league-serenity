<script setup lang="ts">
defineProps<{
  videoSrc: string
  text: string
  audioSrc: string
  next: () => void
}>()

import VideoBackground from '@/components/VideoBackgroundComponent.vue'
import Credits from '@/components/CreditsComponent.vue'
import { onMounted, ref } from 'vue'

const audioRef = ref<HTMLAudioElement | null>(null)

onMounted(() => {
  if (audioRef.value) {
    audioRef.value.load()
    audioRef.value.oncanplay = () => {
      setTimeout(() => {
        audioRef.value?.play().catch((err) => {
          console.warn('Audio play() failed:', err)
        })
      }, 1000)
    }
  }
})
</script>

<template>
  <VideoBackground :video-src="videoSrc">
    <div class="container bottom-text fade-in">
      <div class="affirmation-text">{{ text }}</div>
      <audio ref="audioRef" :src="audioSrc" type="audio/wav" @ended="next" />
    </div>
    <Credits />
  </VideoBackground>
</template>

<style scoped>
.affirmation-text {
  font-size: 2em;
  color: #ffffff;
  text-shadow:
    0 0 4px #000,
    0 0 8px #000,
    0 0 40px #988702;
  z-index: 100;
  animation: fadeInAnimation ease 4s;
  animation-iteration-count: 1;
  animation-fill-mode: none;
  animation-iteration-count: 1;
  line-height: 1.1;
  font-weight: 600;
}

.bottom-text {
  position: absolute;
  bottom: 15%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  width: 100%;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 3s ease forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>
