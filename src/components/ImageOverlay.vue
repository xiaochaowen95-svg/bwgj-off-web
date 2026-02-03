<template>
  <transition name="overlay">
    <div v-if="isVisible" class="overlay" @click="close">
      <button type="button" class="close-btn" @click="close" aria-label="关闭">✕</button>
      <img :src="imageSrc" alt="放大预览" @click.stop />
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  imageSrc: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])

const isVisible = ref(false)

watch(() => props.imageSrc, (newSrc) => {
  isVisible.value = !!newSrc
})

function close() {
  isVisible.value = false
  emit('close')
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(0, 0, 0, 0.90);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
  padding: env(safe-area-inset-top, 20px) env(safe-area-inset-right, 20px) env(safe-area-inset-bottom, 20px) env(safe-area-inset-left, 20px);
  cursor: pointer;
}

.overlay img {
  max-width: 95%;
  max-height: 95%;
  object-fit: contain;
  border-radius: 18px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.75);
  cursor: default;
}

.close-btn {
  position: fixed;
  top: env(safe-area-inset-top, 24px);
  right: env(safe-area-inset-right, 24px);
  width: 48px;
  height: 48px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.45);
  color: rgba(255, 255, 255, 0.95);
  font-size: 24px;
  font-weight: 900;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  display: grid;
  place-items: center;
  z-index: 10001;
}

.close-btn:hover {
  transform: scale(1.08);
  border-color: rgba(255, 107, 107, 0.55);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.55);
}

.overlay-enter-active,
.overlay-leave-active {
  transition: all 0.3s ease;
}

.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.overlay-enter-from img,
.overlay-leave-to img {
  transform: scale(0.9);
}
</style>
