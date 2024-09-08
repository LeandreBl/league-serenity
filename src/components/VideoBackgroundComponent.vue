<script setup lang="ts">
defineProps<{
  videoSrc: string
}>()
</script>

<template>
  <div class="video-background fade-in">
    <video autoplay muted loop playsinline>
      <source :src="videoSrc" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    <div class="overlay">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.video-background {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.video-background video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  transform: translate(-50%, -50%);
  object-fit: cover;
  z-index: 0;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 3s ease-in-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.overlay {
  z-index: 1;
}
</style>
