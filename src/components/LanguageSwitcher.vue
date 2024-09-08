<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

function toggleLang() {
  locale.value = locale.value === 'en' ? 'fr' : 'en'
}
</script>

<template>
  <button class="lang-toggle" @click="toggleLang">
    {{ locale === 'en' ? '🇫🇷' : '🇬🇧' }}
  </button>
</template>

<style scoped>
.lang-toggle {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9rem;
  backdrop-filter: blur(6px);
  transition: background 0.2s;
}

.lang-toggle:hover {
  background: rgba(0, 0, 0, 0.8);
}
</style>
