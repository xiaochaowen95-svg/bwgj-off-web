<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import mmImages from './mmImages.js'
import ImageOverlay from './components/ImageOverlay.vue'
import VideoOverlay from './components/VideoOverlay.vue'
import HomeView from './views/HomeView.vue'
import ProcessView from './views/ProcessView.vue'
import PriceView from './views/PriceView.vue'
import GuizhouView from './views/GuizhouView.vue'
import ContactView from './views/ContactView.vue'

const currentView = ref('home')
const enlargeImgSrc = ref('')
const playVideoSrc = ref('')
const playVideoPoster = ref('')
const posterCache = ref({})

const particles = ref([])

const particleCount = 50
for (let i = 0; i < particleCount; i++) {
  particles.value.push({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 10,
    duration: 10 + Math.random() * 20
  })
}

function getViewFromHash() {
  if (typeof window === 'undefined') return 'home'
  const raw = (window.location.hash || '').replace(/^#/, '')
  const path = raw || '/'

  if (path === '/' || path === '') return 'home'
  if (path === '/price') return 'price'
  if (path === '/process') return 'process'
  if (path === '/contact') return 'contact'
  if (path === '/guizhou') return 'guizhou'
  return 'home'
}

function setHashByView(view) {
  if (typeof window === 'undefined') return
  const viewToHash = {
    home: '/',
    price: '/price',
    process: '/process',
    contact: '/contact',
    guizhou: '/guizhou'
  }
  const nextHash = viewToHash[view] || '/'
  const currentHash = (window.location.hash || '').replace(/^#/, '') || '/'
  if (currentHash !== nextHash) {
    window.location.hash = nextHash
  }
}

function syncViewFromHash() {
  const nextView = getViewFromHash()
  if (currentView.value !== nextView) currentView.value = nextView
  if (typeof window !== 'undefined') window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
}

function navigate(view) {
  currentView.value = view
  setHashByView(view)
  if (typeof window !== 'undefined') window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
}

function handleEnlargeImage(src) {
  enlargeImgSrc.value = src
}

function closeImageOverlay() {
  enlargeImgSrc.value = ''
}

function handlePlayVideo(src, poster) {
  playVideoSrc.value = src
  playVideoPoster.value = poster || ''
}

function closeVideoOverlay() {
  playVideoSrc.value = ''
  playVideoPoster.value = ''
}

function handleUpdatePoster(videoUrl, dataUrl) {
  posterCache.value = { ...posterCache.value, [videoUrl]: dataUrl }
}

onMounted(() => {
  syncViewFromHash()
  window.addEventListener('hashchange', syncViewFromHash)
})

onUnmounted(() => {
  window.removeEventListener('hashchange', syncViewFromHash)
})
</script>

<template>
  <div class="app-root">
    <div class="logo-bg"></div>

    <div class="particles-bg">
      <div v-for="particle in particles" :key="particle.id" class="particle" :style="{ left: particle.left + '%', top: particle.top + '%', animationDelay: particle.delay + 's', animationDuration: particle.duration + 's' }"></div>
    </div>

    <nav class="top-nav">
      <div class="nav-logo-container" @click="navigate('home')" title="点击返回首页">
        <img src="https://cdn.jsdelivr.net/gh/xiaochaowen95-svg/bwgj-img/bwgj.jpg" alt="霸王搞姬 logo" class="nav-logo" />
      </div>
      <button type="button" class="nav-btn" :class="{ active: currentView === 'home' }" @click="navigate('home')">
        <span class="btn-icon">🏠</span>
        <span class="btn-text">首页</span>
      </button>
      <button type="button" class="nav-btn" :class="{ active: currentView === 'process' }" @click="navigate('process')">
        <span class="btn-icon">📋</span>
        <span class="btn-text">预约流程</span>
      </button>
      <button type="button" class="nav-btn" :class="{ active: currentView === 'price' }" @click="navigate('price')">
        <span class="btn-icon">💰</span>
        <span class="btn-text">价目表</span>
      </button>
      <button type="button" class="nav-btn" :class="{ active: currentView === 'guizhou' }" @click="navigate('guizhou')">
        <span class="btn-icon">🌸</span>
        <span class="btn-text">贵州专区</span>
      </button>
      <button type="button" class="nav-btn" :class="{ active: currentView === 'contact' }" @click="navigate('contact')">
        <span class="btn-icon">📞</span>
        <span class="btn-text">联系客服</span>
      </button>
    </nav>

    <main class="app-content">
      <HomeView
        v-if="currentView === 'home'"
        :images="mmImages"
        :poster-cache="posterCache"
        @enlarge-image="handleEnlargeImage"
        @play-video="handlePlayVideo"
        @update-poster="handleUpdatePoster"
      />

      <ProcessView v-else-if="currentView === 'process'" />

      <PriceView v-else-if="currentView === 'price'" />

      <GuizhouView
        v-else-if="currentView === 'guizhou'"
        @enlarge-image="handleEnlargeImage"
        @play-video="handlePlayVideo"
      />

      <ContactView v-else-if="currentView === 'contact'" />
    </main>

    <ImageOverlay
      :image-src="enlargeImgSrc"
      @close="closeImageOverlay"
    />

    <VideoOverlay
      :video-src="playVideoSrc"
      :video-poster="playVideoPoster"
      @close="closeVideoOverlay"
    />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 50%, #16213e 100%);
  background-attachment: fixed;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

#app {
  width: 100%;
  min-height: 100vh;
  position: relative;
  margin: 0;
  padding: 0;
}

.app-root {
  width: 100%;
  min-height: 100vh;
  position: relative;
  padding-top: 0;
  display: flex;
  flex-direction: column;
}

.app-content {
  position: relative;
  z-index: 2;
  flex: 1;
  padding-top: 12px;
  padding-bottom: 24px;
}

button, input, select, textarea {
  font-family: inherit;
}

button {
  -webkit-tap-highlight-color: transparent;
  outline: none;
}

a {
  color: inherit;
  text-decoration: none;
}

.top-nav {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, rgba(24, 24, 24, 0.95) 0%, rgba(40, 40, 40, 0.95) 100%);
  padding: 24px 48px;
  border-radius: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: sticky;
  top: env(safe-area-inset-top, 0px);
  z-index: 3000;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.top-nav::-webkit-scrollbar {
  display: none;
}

.nav-logo-container {
  cursor: pointer;
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
  margin-right: 8px;
}

.nav-logo-container:hover {
  transform: scale(1.08);
}

.nav-logo-container:active {
  transform: scale(0.95);
}

.nav-logo {
  height: 45px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
}

.nav-logo-container:hover .nav-logo {
  box-shadow: 0 4px 16px rgba(255, 215, 0, 0.5);
}

.nav-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
  color: #1a1a1a;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: bold;
  padding: 16px 32px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
  min-width: 140px;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.nav-btn:hover::before {
  left: 100%;
}

.nav-btn:hover {
  transform: translateY(-4px) scale(1.08);
  box-shadow: 0 12px 35px rgba(255, 215, 0, 0.5), 0 0 20px rgba(255, 215, 0, 0.3);
  background: linear-gradient(145deg, #FFE55C 0%, #FFB84D 100%);
}

.nav-btn:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

.nav-btn.active {
  background: linear-gradient(145deg, #FF6B6B 0%, #FF8E53 100%);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4), inset 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  animation: iconFloat 2s ease-in-out infinite;
}

.btn-text {
  font-size: 15px;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.logo-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('https://cdn.jsdelivr.net/gh/xiaochaowen95-svg/bwgj-img/bwgj.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.08;
  z-index: 0;
  pointer-events: none;
}

.particles-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #FFD700;
  border-radius: 50%;
  opacity: 0.7;
  animation: float 20s infinite linear;
}

@keyframes float {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.7;
  }
  90% {
    opacity: 0.7;
  }
  100% {
    transform: translateY(-100vh) rotate(360deg);
    opacity: 0;
  }
}

@media (max-width: 980px) {
  .top-nav {
    gap: 20px;
    padding: 20px 24px;
  }
  
  .nav-btn {
    min-width: 110px;
    padding: 14px 24px;
  }
  
  .btn-icon {
    font-size: 24px;
  }
  
  .btn-text {
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .app-content {
    padding-top: 8px;
    padding-bottom: 20px;
  }

  .top-nav {
    flex-direction: row;
    flex-wrap: nowrap;
    gap: 6px;
    padding: 8px 6px;
    position: sticky;
    top: env(safe-area-inset-top, 0px);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .nav-logo-container {
    margin-right: 4px;
    flex-shrink: 0;
  }

  .nav-logo {
    height: 32px;
  }
  
  .nav-btn {
    flex: 0 0 auto;
    min-width: auto;
    padding: 8px 10px;
    gap: 2px;
    border-radius: 10px;
  }
  
  .btn-icon {
    font-size: 16px;
  }
  
  .btn-text {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .top-nav {
    gap: 4px;
    padding: 6px 4px;
  }

  .nav-logo {
    height: 28px;
  }

  .nav-btn {
    padding: 6px 8px;
    border-radius: 8px;
  }

  .btn-icon {
    font-size: 14px;
  }

  .btn-text {
    font-size: 9px;
  }
}
</style>
