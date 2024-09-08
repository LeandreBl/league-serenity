<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <footer class="footer">
    <p>
      {{ t('idea-stolen-from') }}:
      <a href="https://www.srenity.online/" target="_blank" rel="noopener">Srenity</a>
    </p>
  </footer>
</template>

<style scoped>
footer {
  position: absolute;
  bottom: 0;
  right: 0;
  padding: 1rem;
  font-size: 0.9rem;
  color: #ffffff;
  background: transparent;
  text-align: right;
}

.footer a {
  color: #ffffff;
  right: 10%;
}

.footer a:hover {
  color: #da60df;
}
</style>
