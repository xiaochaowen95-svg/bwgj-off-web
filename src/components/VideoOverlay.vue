<template>
  <transition name="overlay">
    <div v-if="isVisible" class="video-overlay" @click="close">
      <button type="button" class="close-btn" @click="close" aria-label="关闭">✕</button>
      <div class="video-container" @click.stop>
        <video
          ref="videoEl"
          :src="videoSrc"
          :poster="videoPoster"
          controls
          autoplay
          playsinline
          preload="auto"
        ></video>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  videoSrc: {
    type: String,
    default: ''
  },
  videoPoster: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])

const videoEl = ref(null)
const isVisible = ref(false)

watch(() => props.videoSrc, (newSrc) => {
  isVisible.value = !!newSrc
  if (newSrc && videoEl.value) {
    videoEl.value.load()
  }
})

function close() {
  if (videoEl.value) {
    videoEl.value.pause()
  }
  isVisible.value = false
  emit('close')
}

onUnmounted(() => {
  if (videoEl.value) {
    videoEl.value.pause()
    videoEl.value.removeAttribute('src')
    videoEl.value.load()
  }
})
</script>

<style scoped>
.video-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(10px);
  display: grid;
  place-items: center;
  padding: env(safe-area-inset-top, 20px) env(safe-area-inset-right, 20px) env(safe-area-inset-bottom, 20px) env(safe-area-inset-left, 20px);
  cursor: pointer;
}

.video-container {
  max-width: 95%;
  max-height: 95%;
  width: auto;
  height: auto;
  cursor: default;
}

video {
  display: block;
  max-width: 100%;
  max-height: 85vh;
  width: auto;
  height: auto;
  border-radius: 18px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.75);
  background: rgba(0, 0, 0, 0.55);
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

.overlay-enter-from video,
.overlay-leave-to video {
  transform: scale(0.9);
}
</style>
