<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
const { t } = useI18n()
import VideoBackground from '@/components/VideoBackgroundComponent.vue'
import Credits from '@/components/CreditsComponent.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
</script>

<template>
  <LanguageSwitcher />
  <VideoBackground video-src="/backgrounds/sky.mp4">
    <div class="navlink-container">
      <RouterLink to="/splinter-ce-dieu" class="navlink-btn">
        <p>{{ t('find-league-serenity').toUpperCase() }}</p>
      </RouterLink>
    </div>
    <Credits />
  </VideoBackground>
</template>

<style scoped>
.navlink-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.navlink-btn {
  background: #181818;
  color: #fff;
  padding: 1rem 2rem;
  text-decoration: none;
  font-size: 1.2rem;
  transition: background 0.2s;
  display: inline-block;
}

.navlink-btn:hover {
  background: #000;
}

.navlink-btn p {
  margin: 0;
}
</style>
