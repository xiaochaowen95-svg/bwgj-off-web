<template>
  <div class="home-view">
    <section class="intro-section">
      <h1>欢迎光临</h1>
      <div class="intro-subtitle">成都区域优质妹妹展示平台</div>
      <div class="intro-desc">左右滑动查看更多妹妹图片，点击可放大预览 📸</div>
    </section>

    <section class="carousel-section" @wheel="onWheel">
      <div class="carousel-container" :style="carouselStyle">
        <div
          v-for="(item, index) in displayItems"
          :key="index"
          class="carousel-item"
          :class="{ active: index === centerIndex }"
          :style="getItemStyle(index)"
          @click="() => onItemClick(index)"
        >
          <img
            v-if="item.type === 'image'"
            :src="item.src"
            :alt="`图片 ${item.originalIndex + 1}`"
          />
          <video
            v-else-if="item.type === 'video'"
            class="carousel-video"
            :src="item.src"
            :poster="(item.poster || getPoster(item.src) || undefined)"
            muted
            playsinline
            preload="metadata"
          ></video>

          <div class="item-number">{{ item.originalIndex + 1 }}</div>

          <button
            v-if="item.type === 'video' && index === centerIndex"
            type="button"
            class="play-overlay"
            @click.stop="() => playVideo(item.src, item.poster || getPoster(item.src))"
            title="播放视频"
          >
            <span class="play-icon" aria-hidden="true">▶</span>
            <span>播放视频</span>
          </button>
        </div>
      </div>
    </section>

    <div class="carousel-controls">
      <button type="button" class="ctrl-btn" @click="prevItem" aria-label="上一张">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M14.5 5.5L8.5 12l6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <div class="ctrl-indicator">
        {{ currentIndex + 1 }} / {{ totalItems }}
      </div>

      <button type="button" class="ctrl-btn" @click="nextItem" aria-label="下一张">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M9.5 5.5l6 6.5-6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true
  },
  posterCache: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['enlarge-image', 'play-video', 'update-poster'])

const currentIndex = ref(0)
const posterPending = new Set()

const totalItems = computed(() => props.images.length)

const displayItems = computed(() => {
  const total = props.images.length
  if (total === 0) return []

  const getItem = (idx) => {
    const realIdx = ((idx % total) + total) % total
    const img = props.images[realIdx]
    const type = getMediaType(img)
    return {
      src: img,
      type,
      originalIndex: realIdx,
      poster: type === 'video' ? props.posterCache[img] : ''
    }
  }

  const visible = []
  for (let i = -2; i <= 2; i++) {
    visible.push(getItem(currentIndex.value + i))
  }
  return visible
})

const centerIndex = computed(() => 2)

const carouselStyle = computed(() => {
  return {
    perspective: '2400px'
  }
})

function getMediaType(src) {
  const ext = String(src).split('.').pop().toLowerCase()
  return ['mp4', 'webm', 'mov', 'm4v'].includes(ext) ? 'video' : 'image'
}

function getItemStyle(index) {
  const offset = index - centerIndex.value
  const absOffset = Math.abs(offset)

  if (absOffset > 2) {
    return {
      opacity: 0,
      pointerEvents: 'none',
      transform: 'translateX(0) translateZ(-1200px) rotateY(0deg) scale(0.2)'
    }
  }

  const translateX = offset * 500
  const translateZ = -absOffset * 200
  const rotateY = offset * 15
  const scale = 1 - absOffset * 0.15

  return {
    transform: `translateX(${translateX}px) translateZ(${translateZ}px) rotateY(${rotateY}deg) scale(${scale})`,
    opacity: absOffset === 0 ? 1 : 0.8,
    pointerEvents: absOffset <= 1 ? 'auto' : 'none',
    zIndex: absOffset === 0 ? 10 : 10 - absOffset
  }
}

function getPoster(videoUrl) {
  return props.posterCache[videoUrl] || ''
}

async function capturePoster(videoUrl) {
  if (!videoUrl || props.posterCache[videoUrl] || posterPending.has(videoUrl)) return
  posterPending.add(videoUrl)
  try {
    const video = document.createElement('video')
    video.preload = 'metadata'
    video.muted = true
    video.playsInline = true
    video.setAttribute('playsinline', '')
    video.src = videoUrl
    
    await new Promise((resolve, reject) => {
      video.addEventListener('loadeddata', () => {
        try {
          video.currentTime = Math.min(0.12, Math.max(0.01, video.duration ? video.duration * 0.02 : 0.12))
        } catch {}
      }, { once: true })
      
      video.addEventListener('seeked', () => {
        try {
          const w = video.videoWidth || 0
          const h = video.videoHeight || 0
          if (!w || !h) throw new Error('invalid size')
          const canvas = document.createElement('canvas')
          canvas.width = w
          canvas.height = h
          const ctx = canvas.getContext('2d')
          if (!ctx) throw new Error('no context')
          ctx.drawImage(video, 0, 0, w, h)
          const dataUrl = canvas.toDataURL('image/jpeg', 0.82)
          emit('update-poster', videoUrl, dataUrl)
          resolve()
        } catch (e) {
          reject(e)
        } finally {
          video.removeAttribute('src')
          video.load()
        }
      }, { once: true })
      
      video.addEventListener('error', () => reject(new Error('load failed')), { once: true })
      video.load()
    })
  } catch {
    // ignore
  } finally {
    posterPending.delete(videoUrl)
  }
}

function onItemClick(index) {
  const offset = index - centerIndex.value
  if (offset === 0) {
    const item = displayItems.value[index]
    if (item.type === 'image') {
      emit('enlarge-image', item.src)
    } else if (item.type === 'video') {
      playVideo(item.src, item.poster || getPoster(item.src))
    }
  } else if (offset < 0) {
    prevItem()
  } else if (offset > 0) {
    nextItem()
  }
}

function prevItem() {
  const total = props.images.length
  if (total === 0) return
  currentIndex.value = (currentIndex.value - 1 + total) % total
}

function nextItem() {
  const total = props.images.length
  if (total === 0) return
  currentIndex.value = (currentIndex.value + 1) % total
}

function onWheel(e) {
  if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
    if (e.deltaX > 5) nextItem()
    else if (e.deltaX < -5) prevItem()
  }
}

function playVideo(src, poster) {
  emit('play-video', src, poster)
}

watch([currentIndex, () => props.images], () => {
  const current = displayItems.value[centerIndex.value]
  if (current?.type === 'video' && !current.poster) {
    capturePoster(current.src)
  }

  const total = props.images.length
  if (total < 2) return
  const prevIdx = (currentIndex.value - 1 + total) % total
  const nextIdx = (currentIndex.value + 1) % total
  const prevSrc = props.images[prevIdx]
  const nextSrc = props.images[nextIdx]
  if (getMediaType(prevSrc) === 'video' && !props.posterCache[prevSrc]) capturePoster(prevSrc)
  if (getMediaType(nextSrc) === 'video' && !props.posterCache[nextSrc]) capturePoster(nextSrc)
}, { immediate: true })

onMounted(() => {
  const current = displayItems.value[centerIndex.value]
  if (current?.type === 'video') capturePoster(current.src)
})
</script>

<style scoped>
.home-view {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px 60px;
  overflow: visible;
}

.intro-section {
  max-width: 900px;
  margin: 0 auto 40px;
  text-align: center;
  padding: 0 16px;
}

.intro-section h1 {
  margin: 0;
  font-size: 36px;
  letter-spacing: 2px;
}

.intro-subtitle {
  margin-top: 10px;
  font-size: 18px;
  opacity: 0.9;
}

.intro-desc {
  margin-top: 10px;
  font-size: 14px;
  opacity: 0.8;
}

.carousel-section {
  height: 720px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  position: relative;
  margin-bottom: 50px;
  padding: 40px 0;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 30px;
  backdrop-filter: blur(5px);
}

@media (max-width: 680px) {
  .home-view {
    padding: 12px 12px 44px;
    min-height: auto;
  }

  .intro-section {
    margin-bottom: 20px;
  }

  .intro-section h1 {
    font-size: 22px;
  }

  .intro-subtitle {
    font-size: 14px;
  }

  .intro-desc {
    font-size: 12px;
  }

  .carousel-section {
    height: 380px;
    padding: 20px 0;
    margin-bottom: 30px;
  }

  .carousel-item {
    width: 240px;
    height: 340px;
  }

  .carousel-controls {
    gap: 15px;
  }

  .ctrl-btn {
    width: 48px;
    height: 48px;
  }

  .ctrl-btn svg {
    width: 18px;
    height: 18px;
  }

  .ctrl-indicator {
    font-size: 14px;
    padding: 8px 16px;
    min-width: 80px;
  }
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
}

.carousel-item {
  position: absolute;
  width: 450px;
  height: 650px;
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.14);
  box-shadow: 0 18px 55px rgba(0, 0, 0, 0.55);
  transition: all 0.7s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  background: rgba(0, 0, 0, 0.35);
  transform-style: preserve-3d;
}

.carousel-item.active {
  cursor: default;
  border-color: rgba(255, 215, 0, 0.45);
  box-shadow: 0 22px 70px rgba(0, 0, 0, 0.70), 0 0 0 3px rgba(255, 215, 0, 0.22);
}

.carousel-item img,
.carousel-video {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: rgba(0, 0, 0, 0.25);
}

.carousel-video {
  background: rgba(0, 0, 0, 0.45);
}

.item-number {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(0, 0, 0, 0.45);
  color: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 900;
  backdrop-filter: blur(10px);
  pointer-events: none;
}

.play-overlay {
  position: absolute;
  right: 14px;
  bottom: 14px;
  border: 1px solid rgba(255, 215, 0, 0.22);
  background: linear-gradient(145deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0.18) 100%);
  color: rgba(255, 255, 255, 0.94);
  padding: 12px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 900;
  backdrop-filter: blur(10px);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.play-icon {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  color: rgba(255, 215, 0, 0.98);
  background: rgba(255, 215, 0, 0.12);
  border: 1px solid rgba(255, 215, 0, 0.25);
}

.play-overlay:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 215, 0, 0.35);
  box-shadow: 0 14px 26px rgba(0, 0, 0, 0.55);
}

.carousel-controls {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.ctrl-btn {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  border: 1px solid rgba(255, 215, 0, 0.32);
  background:
    radial-gradient(circle at 30% 25%, rgba(255, 255, 255, 0.18), transparent 45%),
    linear-gradient(145deg, rgba(255, 215, 0, 0.18) 0%, rgba(255, 165, 0, 0.10) 45%, rgba(0, 0, 0, 0.30) 100%);
  color: rgba(255, 215, 0, 0.98);
  display: grid;
  place-items: center;
  padding: 0;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  box-shadow:
    0 14px 34px rgba(0, 0, 0, 0.55),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.ctrl-btn svg {
  width: 26px;
  height: 26px;
  filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.55));
}

.ctrl-btn:hover {
  transform: translateY(-2px) scale(1.04);
  border-color: rgba(255, 215, 0, 0.55);
  box-shadow:
    0 18px 44px rgba(0, 0, 0, 0.65),
    0 0 0 4px rgba(255, 215, 0, 0.10),
    inset 0 1px 0 rgba(255, 255, 255, 0.20);
}

.ctrl-indicator {
  font-size: 16px;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.85);
  padding: 10px 20px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(10px);
  min-width: 100px;
  text-align: center;
}

@media (max-width: 768px) {
  .intro-section h1 {
    font-size: 28px;
  }

  .carousel-section {
    height: 480px;
  }

  .carousel-item {
    width: 300px;
    height: 420px;
  }

  .ctrl-btn {
    width: 52px;
    height: 52px;
  }

  .ctrl-btn svg {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .intro-section h1 {
    font-size: 24px;
  }

  .carousel-section {
    height: 400px;
  }

  .carousel-item {
    width: 260px;
    height: 360px;
  }
}
</style>
