<template>
  <nav
    class="top-nav"
    :class="{ collapsed: isCollapsed, dragging: isDragging }"
    :style="{ transform: `translateY(${offsetY}px)` }"
    @pointerdown="onPointerDown"
    @touchstart.passive="onTouchStart"
  >
    <button
      type="button"
      class="nav-collapse-btn"
      :title="isCollapsed ? '展开菜单' : '收起菜单'"
      @click.stop="toggle"
      aria-label="Toggle navigation"
    >
      <span>{{ isCollapsed ? '►' : '◄' }}</span>
    </button>

    <div class="nav-handle">
      <div class="nav-handle-icon" aria-hidden="true">≡</div>
    </div>

    <button
      type="button"
      class="nav-link"
      :class="{ active: currentView === 'home' }"
      @click="$emit('navigate', 'home')"
    >
      <span class="link-icon">🏠</span>
      <span class="link-label">首页</span>
    </button>

    <button
      type="button"
      class="nav-link"
      :class="{ active: currentView === 'process' }"
      @click="$emit('navigate', 'process')"
    >
      <span class="link-icon">📋</span>
      <span class="link-label">流程</span>
    </button>

    <button
      type="button"
      class="nav-link"
      :class="{ active: currentView === 'price' }"
      @click="$emit('navigate', 'price')"
    >
      <span class="link-icon">💰</span>
      <span class="link-label">价格</span>
    </button>

    <button
      type="button"
      class="nav-link"
      :class="{ active: currentView === 'guizhou' }"
      @click="$emit('navigate', 'guizhou')"
    >
      <span class="link-icon">🌸</span>
      <span class="link-label">贵州</span>
    </button>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  currentView: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['navigate'])

const isCollapsed = ref(false)
const offsetY = ref(0)
const isDragging = ref(false)

let dragStartY = 0
let dragStartOffsetY = 0

function toggle() {
  isCollapsed.value = !isCollapsed.value
}

function clampOffset(y) {
  const navHeight = 50 + 44 * 5
  const viewportHeight = window.innerHeight
  const minY = 0
  const maxY = Math.max(0, viewportHeight - navHeight)
  return Math.max(minY, Math.min(maxY, y))
}

function onPointerDown(e) {
  if (e.target.closest('button')) return
  
  isDragging.value = true
  dragStartY = e.clientY
  dragStartOffsetY = offsetY.value

  const onPointerMove = (moveEvent) => {
    const dy = moveEvent.clientY - dragStartY
    offsetY.value = clampOffset(dragStartOffsetY + dy)
  }

  const onPointerUp = () => {
    isDragging.value = false
    window.removeEventListener('pointermove', onPointerMove)
    window.removeEventListener('pointerup', onPointerUp)
  }

  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', onPointerUp)
}

function onTouchStart(e) {
  if (e.target.closest('button')) return
  if (!e.touches || e.touches.length !== 1) return
  
  isDragging.value = true
  dragStartY = e.touches[0].clientY
  dragStartOffsetY = offsetY.value

  const onTouchMove = (moveEvent) => {
    if (!moveEvent.touches || moveEvent.touches.length !== 1) return
    const dy = moveEvent.touches[0].clientY - dragStartY
    offsetY.value = clampOffset(dragStartOffsetY + dy)
  }

  const onTouchEnd = () => {
    isDragging.value = false
    window.removeEventListener('touchmove', onTouchMove)
    window.removeEventListener('touchend', onTouchEnd)
  }

  window.addEventListener('touchmove', onTouchMove)
  window.addEventListener('touchend', onTouchEnd)
}

onMounted(() => {
  const saved = localStorage.getItem('navCollapsed')
  if (saved === 'true') isCollapsed.value = true
})

onUnmounted(() => {
  localStorage.setItem('navCollapsed', isCollapsed.value ? 'true' : 'false')
})
</script>

<style scoped>
.top-nav {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 20px 0 0 20px;
  padding: 12px 8px;
  backdrop-filter: blur(14px);
  box-shadow: -8px 6px 28px rgba(0, 0, 0, 0.42);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  cursor: grab;
}

.top-nav.dragging {
  cursor: grabbing;
}

.top-nav.collapsed {
  transform: translateX(-52px);
}

.top-nav.collapsed .link-label {
  opacity: 0;
  pointer-events: none;
}

.nav-collapse-btn {
  all: unset;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0;
  font-size: 18px;
  font-weight: 900;
  cursor: pointer;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.75);
  transition: all 0.2s ease;
}

.nav-collapse-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 215, 0, 0.35);
  color: rgba(255, 215, 0, 0.98);
  transform: scale(1.05);
}

.nav-handle {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 38px;
  margin: 4px 0;
  opacity: 0.6;
  cursor: grab;
  user-select: none;
}

.top-nav.dragging .nav-handle {
  cursor: grabbing;
  opacity: 1;
}

.nav-handle-icon {
  font-size: 20px;
  font-weight: 900;
  pointer-events: none;
}

.nav-link {
  all: unset;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.85);
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 15px;
  font-weight: 800;
  white-space: nowrap;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 215, 0, 0.35);
  color: rgba(255, 215, 0, 0.98);
  transform: translateX(-2px);
}

.nav-link.active {
  background: linear-gradient(145deg, rgba(255, 215, 0, 0.14) 0%, rgba(255, 165, 0, 0.08) 100%);
  border-color: rgba(255, 215, 0, 0.45);
  color: rgba(255, 215, 0, 0.98);
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.12);
}

.link-icon {
  font-size: 18px;
  display: inline-block;
  min-width: 22px;
  text-align: center;
}

.link-label {
  transition: opacity 0.3s ease;
}

@media (max-width: 768px) {
  .top-nav {
    top: auto;
    bottom: 80px;
    right: 12px;
    border-radius: 20px;
    transform: translateY(0);
  }

  .top-nav.collapsed {
    transform: translateX(-52px);
  }

  .nav-handle {
    display: none;
  }
}
</style>
