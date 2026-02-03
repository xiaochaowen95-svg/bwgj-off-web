<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import mmImages from './mmImages.js'

const currentView = ref('home')

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
    home: '/'
    , price: '/price'
    , process: '/process'
    , contact: '/contact'
    , guizhou: '/guizhou'
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
}

function showView(view) {
  currentView.value = view
  setHashByView(view)
}

// 贵州专区数据（从 public/mm/guizhou/data.json 加载?const guizhouGirls = ref([])
const guizhouLoading = ref(false)
const guizhouError = ref('')
const guizhouIndex = ref(0)
const guizhouHovering = ref(false)
const guizhouSelected = ref(null)

const guizhouPlayMode = ref('自带')
const guizhouDatetime = ref('')
const guizhouAddress = ref('')

// 日期时间分拆选择（年份固?026?const guizhouMonth = ref('')
const guizhouDay = ref('')
const guizhouHour = ref('')
const guizhouMinute = ref('')

const guizhouMonthOptions = computed(() => {
  return Array.from({ length: 12 }, (_, i) => {
    const m = i + 1
    return { value: String(m).padStart(2, '0'), label: `${m}月` }
  })
})

const guizhouDayOptions = computed(() => {
  const month = guizhouMonth.value ? Number(guizhouMonth.value) : 1
  const year = 2026
  const daysInMonth = new Date(year, month, 0).getDate()
  return Array.from({ length: daysInMonth }, (_, i) => {
    const d = i + 1
    return { value: String(d).padStart(2, '0'), label: `${d}日` }
  })
})

const guizhouHourOptions = computed(() => {
  return Array.from({ length: 24 }, (_, i) => {
    return { value: String(i).padStart(2, '0'), label: `${i}点` }
  })
})

const guizhouMinuteOptions = computed(() => {
  return Array.from({ length: 60 }, (_, i) => {
    return { value: String(i).padStart(2, '0'), label: `${i}分` }
  })
})

const guizhouPriceList = [
  { label: '小圈', value: '1000 / 次；1300 / 2次（无图? },
  { label: '小中', value: '1500' },
  { label: '?, value: '2000' },
  { label: '中大', value: '2500' },
  { label: '大圈', value: '1800 / 次（不一定有? },
]

const guizhouCurrentGirl = computed(() => {
  const list = guizhouGirls.value || []
  if (!list.length) return null
  const idx = Math.min(list.length - 1, Math.max(0, guizhouIndex.value))
  return list[idx] || null
})

// 视频首帧 poster（用于没有图片的纯视频素材）
const guizhouPosterCache = ref({})
const guizhouPosterPending = new Set()

function getGuizhouPoster(videoUrl) {
  if (!videoUrl) return ''
  return guizhouPosterCache.value[videoUrl] || ''
}

function capturePosterFromVideo(videoUrl) {
  return new Promise((resolve, reject) => {
    try {
      const video = document.createElement('video')
      video.preload = 'auto'
      video.muted = true
      video.playsInline = true
      video.src = videoUrl

      const cleanup = () => {
        video.removeAttribute('src')
        video.load()
      }

      const onError = () => {
        cleanup()
        reject(new Error('video load failed'))
      }

      const onLoadedData = () => {
        // 某些浏览?currentTime=0 可能拿不到画面，往后跳一?        try {
          video.currentTime = Math.min(0.12, Math.max(0.01, video.duration ? video.duration * 0.02 : 0.12))
        } catch {
          // ignore
        }
      }

      const onSeeked = () => {
        try {
          const w = video.videoWidth || 0
          const h = video.videoHeight || 0
          if (!w || !h) throw new Error('invalid video size')
          const canvas = document.createElement('canvas')
          canvas.width = w
          canvas.height = h
          const ctx = canvas.getContext('2d')
          if (!ctx) throw new Error('no canvas context')
          ctx.drawImage(video, 0, 0, w, h)
          const dataUrl = canvas.toDataURL('image/jpeg', 0.82)
          cleanup()
          resolve(dataUrl)
        } catch (e) {
          cleanup()
          reject(e)
        }
      }

      video.addEventListener('error', onError, { once: true })
      video.addEventListener('loadeddata', onLoadedData, { once: true })
      video.addEventListener('seeked', onSeeked, { once: true })

      // iOS/Safari 有时不会触发 loadeddata，主动触发加?      video.load()
    } catch (e) {
      reject(e)
    }
  })
}

async function ensureGuizhouPoster(videoUrl) {
  if (!videoUrl) return
  if (guizhouPosterCache.value[videoUrl]) return
  if (guizhouPosterPending.has(videoUrl)) return
  guizhouPosterPending.add(videoUrl)
  try {
    const poster = await capturePosterFromVideo(videoUrl)
    if (poster) {
      guizhouPosterCache.value = {
        ...guizhouPosterCache.value,
        [videoUrl]: poster,
      }
    }
  } catch {
    // 捕获失败就保持空，让 video 自己显示默认画面
  } finally {
    guizhouPosterPending.delete(videoUrl)
  }
}

function formatDatetimeCN(datetimeLocalValue) {
  if (!datetimeLocalValue) return ''
  // datetime-local 格式一般为 "YYYY-MM-DDTHH:mm"
  const [datePart, timePart] = datetimeLocalValue.split('T')
  if (!datePart || !timePart) return datetimeLocalValue
  const [y, m, d] = datePart.split('-').map(n => Number(n))
  const [hh, mm] = timePart.split(':').map(n => Number(n))
  if (!y || !m || !d || Number.isNaN(hh) || Number.isNaN(mm)) return datetimeLocalValue
  return `${y}?{m}?{d}?${String(hh).padStart(2, '0')}?{String(mm).padStart(2, '0')}分`
}

const guizhouDatetimeText = computed(() => formatDatetimeCN(guizhouDatetime.value))

function buildGuizhouDemandText() {
  const girl = guizhouSelected.value
  const lines = []
  lines.push('【贵州专区需求�?)
  if (girl?.id && girl?.name) {
    lines.push(`意向妹妹?{girl.id} ${girl.name}`)
  } else if (girl?.name) {
    lines.push(`意向妹妹?{girl.name}`)
  }
  if (guizhouPlayMode.value) lines.push(`游玩方式?{guizhouPlayMode.value}`)
  if (guizhouDatetimeText.value) lines.push(`游玩时间?{guizhouDatetimeText.value}`)
  if (guizhouPlayMode.value === '外卖' && guizhouAddress.value) lines.push(`游玩地址?{guizhouAddress.value}`)
  lines.push('备注：小河区域不能外?)
  return lines.join('\n')
}

const guizhouCanCopy = computed(() => {
  if (!guizhouSelected.value) return false
  if (!guizhouDatetime.value) return false
  if (guizhouPlayMode.value === '外卖' && !guizhouAddress.value.trim()) return false
  return true
})

function copyGuizhouDemand() {
  copyToClipboard(buildGuizhouDemandText(), '需求信?)
}

async function loadGuizhouGirls() {
  if (guizhouLoading.value) return
  guizhouLoading.value = true
  guizhouError.value = ''
  try {
    const candidates = [
      { url: `/guizhou/data.json?t=${Date.now()}`, basePath: '/guizhou' },
      { url: `/mm/guizhou/data.json?t=${Date.now()}`, basePath: '/mm/guizhou' },
    ]

    let data = null
    let basePath = '/guizhou'
    let lastErr = null
    for (const c of candidates) {
      try {
        const res = await fetch(c.url, { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        data = await res.json()
        basePath = c.basePath
        lastErr = null
        break
      } catch (e) {
        lastErr = e
      }
    }
    if (!data) throw lastErr || new Error('No data')

    const rawGirls = Array.isArray(data?.girls) ? data.girls : []
    const normalized = rawGirls
      .map((g, idx) => {
        const imageFile = g?.imageFile || g?.image || ''
        const videoFile = g?.videoFile || g?.video || ''
        const posterFile = g?.posterFile || ''
        const file = g?.mediaFile || g?.file || ''

        const toUrl = (p) => {
          if (!p) return ''
          if (p.startsWith('/')) return p
          return `${basePath}/${p}`
        }

        const ext = (p) => (String(p).split('.').pop() || '').toLowerCase()
        const isVideo = (p) => ['mp4', 'webm', 'mov', 'm4v'].includes(ext(p))

        let image = ''
        let video = ''

        if (imageFile) image = toUrl(imageFile)
        if (videoFile) video = toUrl(videoFile)

        // 兼容只给了一?file 的情?        if (!image && !video && file) {
          if (isVideo(file)) {
            video = toUrl(file)
          } else {
            image = toUrl(file)
          }
        }

        const poster = posterFile ? toUrl(posterFile) : ''

        const bestNameSource = g?.name || imageFile || videoFile || file
        const fallbackName = bestNameSource
          ? String(bestNameSource).split('/').pop().split('.').slice(0, -1).join('.')
          : `妹妹${idx + 1}`

        return {
          id: g?.id || String(idx + 1),
          name: g?.name || fallbackName,
          desc: g?.desc || g?.intro || '',
          image,
          video,
          poster: poster || image,
        }
      })
      .filter(g => g.image || g.video)

    guizhouGirls.value = normalized
    guizhouIndex.value = 0
  } catch (err) {
    guizhouError.value = '贵州专区数据加载失败：请检?public/guizhou/data.json ?public/mm/guizhou/data.json 是否存在?JSON 格式正确?
    guizhouGirls.value = []
  } finally {
    guizhouLoading.value = false
  }
}

function guizhouPrev() {
  const list = guizhouGirls.value || []
  if (!list.length) return
  guizhouIndex.value = (guizhouIndex.value - 1 + list.length) % list.length
}

function guizhouNext() {
  const list = guizhouGirls.value || []
  if (!list.length) return
  guizhouIndex.value = (guizhouIndex.value + 1) % list.length
}

function confirmGuizhouGirl() {
  if (!guizhouCurrentGirl.value) return
  guizhouSelected.value = guizhouCurrentGirl.value
}

function resetGuizhouSelection() {
  guizhouSelected.value = null
  guizhouPlayMode.value = '自带'
  guizhouDatetime.value = ''
  guizhouMonth.value = ''
  guizhouDay.value = ''
  guizhouHour.value = ''
  guizhouMinute.value = ''
  guizhouAddress.value = ''
}

watch(guizhouPlayMode, (v) => {
  if (v !== '外卖') {
    guizhouAddress.value = ''
  }
})

// 同步分拆的日期时间选择?guizhouDatetime
watch([guizhouMonth, guizhouDay, guizhouHour, guizhouMinute], () => {
  const m = guizhouMonth.value
  const d = guizhouDay.value
  const h = guizhouHour.value
  const min = guizhouMinute.value
  
  if (m && d && h && min) {
    guizhouDatetime.value = `2026-${m}-${d}T${h}:${min}`
  } else {
    guizhouDatetime.value = ''
  }
})

watch([guizhouCurrentGirl, guizhouIndex, guizhouGirls], () => {
  const cur = guizhouCurrentGirl.value
  if (cur?.video && !cur.poster) ensureGuizhouPoster(cur.video)

  // 预取相邻两张，切换更顺滑
  const list = guizhouGirls.value || []
  if (list.length < 2) return
  const i = guizhouIndex.value
  const next = list[(i + 1) % list.length]
  const prev = list[(i - 1 + list.length) % list.length]
  if (next?.video && !next.poster) ensureGuizhouPoster(next.video)
  if (prev?.video && !prev.poster) ensureGuizhouPoster(prev.video)
})

// 移动端侧边导航：收起/展开 + 可拖?const navRef = ref(null)
const isNavCollapsed = ref(false)
const navOffsetY = ref(-180)
const navDragging = ref(false)
const isMobileNav = ref(false)
let navDragStartY = 0
let navDragStartOffset = 0
let navPointerId = null
let navMediaQuery = null
let navMediaQueryHandler = null

function toggleNavCollapsed() {
  isNavCollapsed.value = !isNavCollapsed.value
}

function clampNavOffset(nextOffset) {
  const el = navRef.value
  if (!el || typeof window === 'undefined') return nextOffset
  const rect = el.getBoundingClientRect()
  const margin = 10
  const half = rect.height / 2
  const minCenterY = half + margin
  const maxCenterY = window.innerHeight - half - margin
  const desiredCenterY = window.innerHeight / 2 + nextOffset
  const clampedCenterY = Math.min(maxCenterY, Math.max(minCenterY, desiredCenterY))
  return clampedCenterY - window.innerHeight / 2
}

function syncIsMobileNav() {
  if (typeof window === 'undefined') return
  isMobileNav.value = window.matchMedia('(max-width: 768px)').matches
}

function clampNavIntoView() {
  syncIsMobileNav()
  if (!isMobileNav.value) return
  navOffsetY.value = clampNavOffset(navOffsetY.value)
}

// iOS/部分安卓浏览?pointer 事件不稳定：提供 touch 兜底
function onNavTouchStart(e) {
  const target = e.target
  if (target.closest('button') || target.closest('.nav-btn')) {
    return
  }
  const t = e.touches && e.touches[0]
  if (!t) return
  e.preventDefault()
  navDragging.value = true
  navDragStartY = t.clientY
  navDragStartOffset = navOffsetY.value
}

function onNavTouchMove(e) {
  if (!navDragging.value) return
  const t = e.touches && e.touches[0]
  if (!t) return
  const deltaY = t.clientY - navDragStartY
  navOffsetY.value = clampNavOffset(navDragStartOffset + deltaY)
}

function onNavTouchEnd() {
  navDragging.value = false
}

function onNavPointerDown(e) {
  // 只允许从“把手区域”开始拖动，避免影响按钮点击
  navDragging.value = true
  navPointerId = e.pointerId
  navDragStartY = e.clientY
  navDragStartOffset = navOffsetY.value

  try {
    e.currentTarget.setPointerCapture(e.pointerId)
  } catch {
    // ignore
  }
}

function onNavPointerMove(e) {
  if (!navDragging.value || navPointerId !== e.pointerId) return
  const deltaY = e.clientY - navDragStartY
  navOffsetY.value = clampNavOffset(navDragStartOffset + deltaY)
}

function onNavPointerUp(e) {
  if (navPointerId !== e.pointerId) return
  navDragging.value = false
  navPointerId = null
}

const particles = ref([])

// 生成粒子
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

// 将图片和视频配对
const girlsList = computed(() => {
  const girls = []
  const imageMap = {}
  
  // 先将文件按名字分?  mmImages.forEach(path => {
    const fileName = path.split('/').pop()
    const baseName = fileName.split('_')[0] // 例如 girl001
    const type = fileName.split('_')[1].split('.')[0] // 1 ?2
    
    if (!imageMap[baseName]) {
      imageMap[baseName] = {}
    }
    
    if (type === '1') {
      imageMap[baseName].image = path
    } else if (type === '2') {
      imageMap[baseName].video = path
    }
  })
  
  // 转换为数?  Object.keys(imageMap).forEach(key => {
    if (imageMap[key].image && imageMap[key].video) {
      girls.push({
        id: key,
        image: imageMap[key].image,
        video: imageMap[key].video
      })
    }
  })
  
  return girls
})

// 轮播相关
const currentIndex = ref(0)
const isHovering = ref(false)
let carouselTimer = null

// 自动轮播
function startCarousel() {
  if (carouselTimer) return
  carouselTimer = setInterval(() => {
    if (!isHovering.value && girlsList.value.length > 0) {
      currentIndex.value = (currentIndex.value + 1) % girlsList.value.length
    }
  }, 15000)
}

function stopCarousel() {
  if (carouselTimer) {
    clearInterval(carouselTimer)
    carouselTimer = null
  }
}

onMounted(() => {
  // 支持 URL 直达?#/guizhou 等）
  syncViewFromHash()
  if (typeof window !== 'undefined') {
    window.addEventListener('hashchange', syncViewFromHash)
  }

  startCarousel()

  // 初始化：确保侧边栏在可视区域?  nextTick(() => {
    clampNavIntoView()
  })

  if (typeof window !== 'undefined') {
    window.addEventListener('resize', clampNavIntoView, { passive: true })
    window.addEventListener('orientationchange', clampNavIntoView, { passive: true })

    navMediaQuery = window.matchMedia('(max-width: 768px)')
    navMediaQueryHandler = () => clampNavIntoView()
    if (navMediaQuery.addEventListener) {
      navMediaQuery.addEventListener('change', navMediaQueryHandler)
    } else if (navMediaQuery.addListener) {
      navMediaQuery.addListener(navMediaQueryHandler)
    }
  }
})

onUnmounted(() => {
  stopCarousel()

  if (typeof window !== 'undefined') {
    window.removeEventListener('hashchange', syncViewFromHash)
  }

  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', clampNavIntoView)
    window.removeEventListener('orientationchange', clampNavIntoView)

    if (navMediaQuery && navMediaQueryHandler) {
      if (navMediaQuery.removeEventListener) {
        navMediaQuery.removeEventListener('change', navMediaQueryHandler)
      } else if (navMediaQuery.removeListener) {
        navMediaQuery.removeListener(navMediaQueryHandler)
      }
    }
  }
})

watch(currentView, (v) => {
  // 进入贵州专区时加载数据（避免首页首次加载?fetch?  if (v === 'guizhou' && !guizhouGirls.value.length && !guizhouLoading.value) {
    loadGuizhouGirls()
  }

  // 切换页面时关闭弹?  enlargedImage.value = null
  if (activeVideo.value) {
    closeVideo()
  }
})

// 图片放大查看
const enlargedImage = ref(null)

// 点击图片后播放视频（不预展示视频?const activeVideo = ref(null)
const activeVideoPoster = ref(null)

function enlargeImage(imageSrc) {
  enlargedImage.value = imageSrc
}

function closeEnlargedImage() {
  enlargedImage.value = null
}

function openVideo(videoSrc, posterSrc) {
  activeVideo.value = videoSrc
  activeVideoPoster.value = posterSrc || null
  stopCarousel()
}

function closeVideo() {
  activeVideo.value = null
  activeVideoPoster.value = null
  startCarousel()
}

// 手动切换轮播
function prevSlide() {
  currentIndex.value = (currentIndex.value - 1 + girlsList.value.length) % girlsList.value.length
}

function nextSlide() {
  currentIndex.value = (currentIndex.value + 1) % girlsList.value.length
}

// 计算卡片?D变换
function getCardTransform(index) {
  const diff = index - currentIndex.value
  const total = girlsList.value.length
  
  // 标准化差值到 -total/2 ?+total/2
  let normalizedDiff = diff
  if (diff > total / 2) normalizedDiff = diff - total
  if (diff < -total / 2) normalizedDiff = diff + total
  
  const center = 'translate(-50%, -50%)'
  if (normalizedDiff === 0) {
    // 当前项：正中央，无偏?    return `${center} translateX(0) translateZ(0) scale(1)`
  } else if (normalizedDiff === 1) {
    // 下一项：右侧
    return `${center} translateX(360px) translateZ(-260px) scale(0.78) rotateY(-18deg)`
  } else if (normalizedDiff === -1) {
    // 上一项：左侧
    return `${center} translateX(-360px) translateZ(-260px) scale(0.78) rotateY(18deg)`
  } else {
    // 其他项：隐藏
    return `${center} translateX(0) translateZ(-520px) scale(0.55)`
  }
}

function getCardOpacity(index) {
  const diff = Math.abs(index - currentIndex.value)
  const total = girlsList.value.length
  const normalizedDiff = Math.min(diff, total - diff)
  
  if (normalizedDiff === 0) return 1
  if (normalizedDiff === 1) return 0.7
  return 0
}

const priceList = [
  { name: '小圈', price: 1300 },
  { name: '小中', price: 1700 },
  { name: '中圈', price: 2000 },
  { name: '中大', price: 2500 },
  { name: '大圈', price: 3000 },
]

// 复制功能
const copyToast = ref('')

function copyToClipboard(text, label) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text)
      .then(() => {
        showCopyToast(`${label}已复制！`)
      })
      .catch(() => {
        fallbackCopy(text, label)
      })
  } else {
    fallbackCopy(text, label)
  }
}

function fallbackCopy(text, label) {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.select()
  try {
    document.execCommand('copy')
    showCopyToast(`${label}已复制！`)
  } catch (err) {
    showCopyToast('复制失败，请手动复制')
  }
  document.body.removeChild(textarea)
}

function showCopyToast(message) {
  copyToast.value = message
  setTimeout(() => {
    copyToast.value = ''
  }, 2000)
}
</script>

<template>
  <div class="app-root">
    <!-- logo 背景 -->
    <div class="logo-bg"></div>

    <!-- 粒子背景 -->
    <div class="particles-bg">
      <div v-for="particle in particles" :key="particle.id" class="particle" :style="{ left: particle.left + '%', top: particle.top + '%', animationDelay: particle.delay + 's', animationDuration: particle.duration + 's' }"></div>
    </div>

    <nav
      ref="navRef"
      class="top-nav"
      :class="{ collapsed: isNavCollapsed, dragging: navDragging }"
      :style="isMobileNav ? { transform: `translateY(-50%) translateY(${navOffsetY}px)` } : undefined"
      @pointerdown="onNavPointerDown"
      @pointermove="onNavPointerMove"
      @pointerup="onNavPointerUp"
      @pointercancel="onNavPointerUp"
      @touchstart="onNavTouchStart"
      @touchmove="onNavTouchMove"
      @touchend="onNavTouchEnd"
      @touchcancel="onNavTouchEnd"
    >
      <div class="nav-handle" title="按住拖动 / 点击收起展开">
        <button type="button" class="nav-toggle" @click.stop="toggleNavCollapsed" :aria-label="isNavCollapsed ? '展开导航' : '收起导航'">
          <svg v-if="isNavCollapsed" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div
          class="nav-grip"
          aria-hidden="true"
        ></div>
      </div>

      <button type="button" @click="showView('home')" class="nav-btn" :class="{active: currentView === 'home'}">
        <span class="btn-icon">🏠</span>
        <span class="btn-text">首页</span>
      </button>
      <button type="button" @click="showView('guizhou')" class="nav-btn" :class="{active: currentView === 'guizhou'}">
        <span class="btn-icon">🏞?/span>
        <span class="btn-text">贵州专区</span>
      </button>
      <button type="button" @click="showView('price')" class="nav-btn" :class="{active: currentView === 'price'}">
        <span class="btn-icon">💰</span>
        <span class="btn-text">价目?/span>
      </button>
      <button type="button" @click="showView('process')" class="nav-btn" :class="{active: currentView === 'process'}">
        <span class="btn-icon">📋</span>
        <span class="btn-text">预约流程</span>
      </button>
      <button type="button" @click="showView('contact')" class="nav-btn" :class="{active: currentView === 'contact'}">
        <span class="btn-icon">💬</span>
        <span class="btn-text">联系客服</span>
      </button>
    </nav>

    <!-- 网页 logo -->
    <div class="logo-container" @click="showView('home')" title="点击返回首页">
      <img src="https://cdn.jsdelivr.net/gh/xiaochaowen95-svg/bwgj-img/bwgj.jpg" alt="霸王搞姬 logo" class="page-logo" />
    </div>

    <!-- 首页内容 -->
    <div v-if="currentView === 'home'" class="home-content">
      <div class="carousel-container" @mouseenter="isHovering = true" @mouseleave="isHovering = false">
        <div class="carousel-wrapper">
          <div 
            v-for="(girl, index) in girlsList" 
            :key="girl.id" 
            class="girl-card"
            :class="{
              'active': index === currentIndex,
              'prev': index === (currentIndex - 1 + girlsList.length) % girlsList.length,
              'next': index === (currentIndex + 1) % girlsList.length
            }"
            :style="{
              transform: getCardTransform(index),
              opacity: getCardOpacity(index),
              zIndex: index === currentIndex ? 10 : 1
            }"
          >
            <div class="girl-image" @click="openVideo(girl.video, girl.image)">
              <img :src="girl.image" :alt="girl.id" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- 轮播切换按钮 -->
      <div class="carousel-controls">
        <button class="carousel-btn prev-btn" @click="prevSlide">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        
        <button class="carousel-btn next-btn" @click="nextSlide">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <div class="home-cta">
        <button type="button" class="home-cta-btn" @click="showView('guizhou')">
          进入贵州专区 ?        </button>
        <div class="home-cta-sub">支持直达链接?#/guizhou</div>
      </div>
    </div>

    <!-- 图片放大查看遮罩 -->
    <div v-if="enlargedImage" class="image-overlay" @click="closeEnlargedImage">
      <img :src="enlargedImage" alt="放大查看" @click.stop />
      <button class="close-btn" @click="closeEnlargedImage">?/button>
    </div>

    <!-- 视频播放遮罩（点击图片后播放?-->
    <div v-if="activeVideo" class="video-overlay" @click="closeVideo">
      <video
        class="overlay-video"
        :src="activeVideo"
        :poster="activeVideoPoster || undefined"
        controls
        autoplay
        playsinline
        preload="metadata"
        @click.stop
      >
        您的浏览器不支持视频播放
      </video>
      <button class="close-btn" @click="closeVideo">?/button>
    </div>

    <!-- 贵州专区页面 -->
    <div v-else-if="currentView === 'guizhou'" class="guizhou-page">
      <section class="guizhou-section">
        <div class="guizhou-head">
          <h2>贵州区域</h2>
          <div class="guizhou-sub">展示贵州区域全部妹妹，可左右切换（不自动轮播?/div>
        </div>

        <div class="guizhou-loading" v-if="guizhouLoading">正在加载贵州专区信息?/div>
        <div class="guizhou-error" v-else-if="guizhouError">{{ guizhouError }}</div>

        <template v-else>
          <div v-if="!guizhouGirls.length" class="guizhou-empty">
            还没有检测到贵州专区数据。请?public/guizhou/ 放图?视频，并编辑 public/guizhou/data.json（或兼容 public/mm/guizhou/data.json）�?          </div>

          <div v-else class="guizhou-carousel" @mouseenter="guizhouHovering = true" @mouseleave="guizhouHovering = false">
            <button class="gz-btn gz-prev" type="button" @click="guizhouPrev" :disabled="guizhouGirls.length <= 1" aria-label="上一?>
              <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M14.5 5.5L8.5 12l6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>

            <div class="gz-card" :class="{ selected: guizhouSelected?.id === guizhouCurrentGirl?.id }">
              <div
                class="gz-img"
                :class="{ clickable: !!guizhouCurrentGirl?.image || !!guizhouCurrentGirl?.video }"
                @click="guizhouCurrentGirl?.image ? enlargeImage(guizhouCurrentGirl.image) : (guizhouCurrentGirl?.video ? openVideo(guizhouCurrentGirl.video, guizhouCurrentGirl.poster || getGuizhouPoster(guizhouCurrentGirl.video)) : null)"
              >
                <img v-if="guizhouCurrentGirl?.image" :src="guizhouCurrentGirl.image" :alt="guizhouCurrentGirl.name" />
                <video
                  v-else-if="guizhouCurrentGirl?.video"
                  class="gz-preview-video"
                  :src="guizhouCurrentGirl.video"
                  :poster="(guizhouCurrentGirl.poster || getGuizhouPoster(guizhouCurrentGirl.video) || undefined)"
                  muted
                  playsinline
                  preload="metadata"
                ></video>

                <div class="gz-badges">
                  <span v-if="guizhouSelected?.id === guizhouCurrentGirl?.id" class="gz-badge gz-badge-selected">已�?/span>
                  <span v-else class="gz-badge gz-badge-tip">左右切换</span>
                  <span v-if="guizhouCurrentGirl?.video" class="gz-badge gz-badge-video">视频</span>
                </div>

                <button
                  v-if="guizhouCurrentGirl?.video"
                  type="button"
                  class="gz-play"
                  @click.stop="openVideo(guizhouCurrentGirl.video, guizhouCurrentGirl.poster || getGuizhouPoster(guizhouCurrentGirl.video))"
                  title="播放视频"
                >
                  <span class="gz-play-icon" aria-hidden="true">?/span>
                  <span>播放视频</span>
                </button>
              </div>

              <div class="gz-info">
                <div class="gz-title">
                  <span class="gz-name">{{ guizhouCurrentGirl.name }}</span>
                  <span class="gz-index">{{ guizhouIndex + 1 }} / {{ guizhouGirls.length }}</span>
                </div>
                <div class="gz-desc" v-if="guizhouCurrentGirl.desc">{{ guizhouCurrentGirl.desc }}</div>

                <div class="gz-confirm">
                  <button
                    type="button"
                    class="gz-confirm-btn"
                    @click="confirmGuizhouGirl"
                  >
                    确定选择
                  </button>
                  <button
                    v-if="guizhouSelected"
                    type="button"
                    class="gz-reset-btn"
                    @click="resetGuizhouSelection"
                  >
                    重新选择
                  </button>
                </div>
              </div>
            </div>

            <button class="gz-btn gz-next" type="button" @click="guizhouNext" :disabled="guizhouGirls.length <= 1" aria-label="下一?>
              <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M9.5 5.5l6 6.5-6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>

          <div v-if="guizhouSelected" class="gz-form">
            <h3>需求表?/h3>

            <div class="gz-form-row">
              <div class="gz-form-label">意向妹妹</div>
              <div class="gz-form-value">{{ guizhouSelected.name }}</div>
            </div>

            <div class="gz-form-row">
              <label class="gz-form-label" for="gz-mode">客户游玩方式</label>
              <div class="gz-form-control">
                <select id="gz-mode" v-model="guizhouPlayMode" class="gz-select">
                  <option value="自带">自带（不需要交定金?/option>
                  <option value="外卖">外卖</option>
                </select>
              </div>
            </div>

            <div class="gz-form-row">
              <label class="gz-form-label">游玩时间</label>
              <div class="gz-form-control">
                <div class="gz-datetime-grid">
                  <select v-model="guizhouMonth" class="gz-select gz-time-select">
                    <option value="">月份</option>
                    <option v-for="opt in guizhouMonthOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                  </select>
                  <select v-model="guizhouDay" class="gz-select gz-time-select" :disabled="!guizhouMonth">
                    <option value="">日期</option>
                    <option v-for="opt in guizhouDayOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                  </select>
                  <select v-model="guizhouHour" class="gz-select gz-time-select">
                    <option value="">小时</option>
                    <option v-for="opt in guizhouHourOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                  </select>
                  <select v-model="guizhouMinute" class="gz-select gz-time-select">
                    <option value="">分钟</option>
                    <option v-for="opt in guizhouMinuteOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                  </select>
                </div>
                <div class="gz-hint" v-if="guizhouDatetimeText">已选：{{ guizhouDatetimeText }}</div>
              </div>
            </div>

            <div class="gz-form-row" v-if="guizhouPlayMode === '外卖'">
              <label class="gz-form-label" for="gz-address">游玩地址</label>
              <div class="gz-form-control">
                <input id="gz-address" class="gz-input" type="text" placeholder="请填写具体地址" v-model="guizhouAddress" />
              </div>
            </div>

            <div class="gz-note">提示：我们不会存储任何数据，当前表单关闭信息就将丢失?/div>
            <div class="gz-note strong">特别说明：小河区域不能外出�?/div>

            <div class="gz-actions">
              <button
                type="button"
                class="gz-copy-btn"
                :disabled="!guizhouCanCopy"
                @click="copyGuizhouDemand"
              >
                复制需求信?              </button>
            </div>
          </div>

          <div class="gz-price">
            <h3>贵州地区价目?/h3>
            <div class="gz-price-grid">
              <div class="gz-price-item" v-for="p in guizhouPriceList" :key="p.label">
                <div class="gz-price-label">{{ p.label }}</div>
                <div class="gz-price-value">{{ p.value }}</div>
              </div>
            </div>
          </div>
        </template>

        <transition name="toast">
          <div v-if="copyToast" class="copy-toast">✔️ {{ copyToast }}</div>
        </transition>
      </section>
    </div>

    <!-- 价目表页?-->
    <div v-else-if="currentView === 'price'">
      <section class="price-section">
        <h2>价目?/h2>
        <div class="price-cards">
          <div class="price-card" v-for="item in priceList" :key="item.name">
            <div class="circle">{{ item.name }}</div>
            <div class="price">￥{{ item.price }}</div>
          </div>
        </div>
        <div class="desc">所有妹子成都本地真实上门，酒店/公寓随便约，照片95%+真人，档次越高越?/div>
      </section>
    </div>

    <!-- 预约流程页面 -->
    <div v-else-if="currentView === 'process'">
      <section class="process-section">
        <h2>预约流程</h2>
        
        <!-- 流程步骤卡片 -->
        <div class="process-flow">
          <div class="process-step">
            <div class="step-number">1</div>
            <div class="step-icon">💬</div>
            <div class="step-title">确定需?/div>
            <div class="step-content">先跟客服妹妹说清?br/>（档?时间/地点/大概几点玩）</div>
          </div>
          
          <div class="process-connector"></div>
          
          <div class="process-step">
            <div class="step-number">2</div>
            <div class="step-icon">🖼?/div>
            <div class="step-title">发图选人</div>
            <div class="step-content">客服发图<br/>挑选心仪妹?/div>
          </div>
          
          <div class="process-connector"></div>
          
          <div class="process-step">
            <div class="step-number">3</div>
            <div class="step-icon">?/div>
            <div class="step-title">约好上门</div>
            <div class="step-content">选好→定时间地点<br/>妹子准时上门，先看人确认OK再继?/div>
          </div>
          
          <div class="process-connector"></div>
          
          <div class="process-step">
            <div class="step-number">4</div>
            <div class="step-icon">💎</div>
            <div class="step-title">满意付钱</div>
            <div class="step-content">满意付钱<br/>不满意可?退</div>
          </div>
        </div>
        
        <div class="extra">
          <h3>额外福利</h3>
          <div class="benefits-grid">
            <div class="benefit-item">
              <div class="benefit-icon">🏙?/div>
              <div class="benefit-text">三环内上门免车费</div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon">🛣?/div>
              <div class="benefit-text">三环外路费实报实销（提前讲好）</div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon">🎁</div>
              <div class="benefit-text">每日首单 -100?/div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon">🎁</div>
              <div class="benefit-text">推荐朋友消费成功返你100元（截图核销?/div>
            </div>
          </div>
          <div class="special">💡 特殊服务说明：三通、SM、无冒等特服需 +500</div>
          <div class="pay">💰 付款说明：无任何定金！见面满意付！预定除外！三环内免费上门，绕城外需实报车费（先付）。首次下单外出都需先付100定金，三环外付车费可免定金，自己开车去妹妹那里不需要定金�?/div>
        </div>
      </section>
    </div>

    <!-- 联系客服页面 -->
    <div v-else-if="currentView === 'contact'">
      <section class="contact-section">
        <h2>联系客服</h2>
        <div style="font-size:2em;color:#FFD700;margin-bottom:24px;">👇 联系方式在这?👇</div>
        
        <!-- SafeX 特别推荐区域 -->
        <div class="safex-highlight">
          <div class="safex-badge">?推荐首�??/div>
          <div class="safex-title">🔥 SafeX客服（强烈推荐）🔥</div>
          <a href="https://sfw.vc/waiwei91" target="_blank" class="safex-link">https://sfw.vc/waiwei91</a>
          <button class="copy-btn" @click="copyToClipboard('https://sfw.vc/waiwei91', 'SafeX链接')">📋 复制链接</button>
          <div class="safex-desc">安全私密 · 响应快�?· 服务专业</div>
        </div>
        
        <div class="contact-divider">其他联系方式</div>
        
        <div class="contact-block">
          <div class="contact-item">
            <span>客服QQ?388570976</span>
            <button class="copy-btn-small" @click="copyToClipboard('2388570976', 'QQ?)">复制</button>
          </div>
          <div class="contact-item">
            <span>Telegram客服?/span>
            <a href="http://t.me/waiwei923_bot" target="_blank" class="inline-link">t.me/waiwei923_bot</a>
            <button class="copy-btn-small" @click="copyToClipboard('waiwei923_bot', 'TG用户?)">复制</button>
          </div>
          <div class="contact-item">
            <span>妹子相册?/span>
            <a href="http://1261554.apps3.mui139.pics/" target="_blank" class="inline-link">http://1261554.apps3.mui139.pics/</a>
            <button class="copy-btn-small" @click="copyToClipboard('http://1261554.apps3.mui139.pics/', '相册链接')">复制</button>
            <span style="margin-left: 10px;">密码?88</span>
            <button class="copy-btn-small" @click="copyToClipboard('888', '密码')">复制</button>
          </div>
          <div class="contact-note">如需人工推荐或有疑问，直接联系客服！</div>
        </div>
      </section>
      
      <!-- 复制提示 -->
      <transition name="toast">
        <div v-if="copyToast" class="copy-toast">✔️ {{ copyToast }}</div>
      </transition>
    </div>

    <!-- 已移?HelloWorld 组件，避免页面内容被占据 -->
  </div>
</template>

<style scoped>
.app-root {
  --nav-height: 128px;
  padding-top: calc(var(--nav-height) + env(safe-area-inset-top));
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
  position: fixed;
  top: env(safe-area-inset-top);
  left: 0;
  right: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 215, 0, 0.2);
  transform: none;
}

.nav-handle {
  display: none;
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

.home-cta {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.home-cta-btn {
  border: none;
  cursor: pointer;
  padding: 14px 22px;
  border-radius: 14px;
  font-weight: 800;
  font-size: 16px;
  color: #121212;
  background: linear-gradient(145deg, #FF6B6B 0%, #FF8E53 100%);
  box-shadow: 0 10px 24px rgba(255, 107, 107, 0.28);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.home-cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(255, 107, 107, 0.35);
}

.home-cta-sub {
  font-size: 13px;
  opacity: 0.8;
}

.guizhou-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.guizhou-section {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 215, 0, 0.14);
  border-radius: 18px;
  box-shadow: 0 10px 36px rgba(0, 0, 0, 0.35);
  padding: 18px 18px 26px;
  backdrop-filter: blur(10px);
}

.guizhou-head h2 {
  margin: 0;
  font-size: 28px;
  letter-spacing: 1px;
}

.guizhou-sub {
  margin-top: 6px;
  opacity: 0.8;
  font-size: 14px;
}

.guizhou-loading,
.guizhou-error,
.guizhou-empty {
  margin-top: 18px;
  padding: 14px 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.06);
}

.guizhou-error {
  border: 1px solid rgba(255, 107, 107, 0.35);
  color: rgba(255, 210, 210, 0.95);
}

.guizhou-carousel {
  margin-top: 18px;
  display: grid;
  grid-template-columns: 70px 1fr 70px;
  gap: 14px;
  align-items: center;
}

.gz-btn {
  height: 70px;
  width: 70px;
  border-radius: 999px;
  border: 1px solid rgba(255, 215, 0, 0.32);
  background:
    radial-gradient(circle at 30% 25%, rgba(255, 255, 255, 0.18), transparent 45%),
    linear-gradient(145deg, rgba(255, 215, 0, 0.18) 0%, rgba(255, 165, 0, 0.10) 45%, rgba(0, 0, 0, 0.30) 100%);
  color: rgba(255, 215, 0, 0.98);
  display: grid;
  place-items: center;
  padding: 0;
  line-height: 0;
  -webkit-tap-highlight-color: transparent;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease, border-color 0.18s ease;
  box-shadow:
    0 14px 34px rgba(0, 0, 0, 0.55),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.gz-nav-icon {
  width: 22px;
  height: 22px;
  display: block;
  margin: 0;
  padding: 0;
  pointer-events: none;
  filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.55));
}

.gz-btn:hover {
  transform: translateY(-2px) scale(1.02);
  border-color: rgba(255, 215, 0, 0.55);
  box-shadow:
    0 18px 44px rgba(0, 0, 0, 0.65),
    0 0 0 4px rgba(255, 215, 0, 0.10),
    inset 0 1px 0 rgba(255, 255, 255, 0.20);
}

.gz-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.gz-card {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 16px;
  padding: 14px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
}

.gz-card.selected {
  border-color: rgba(255, 215, 0, 0.55);
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.25), 0 16px 45px rgba(255, 215, 0, 0.12);
}

.gz-card.selected::after {
  content: '';
  position: absolute;
  inset: -2px;
  background: radial-gradient(circle at 20% 20%, rgba(255, 215, 0, 0.22), transparent 55%),
    radial-gradient(circle at 80% 30%, rgba(255, 107, 107, 0.14), transparent 60%);
  pointer-events: none;
}

.gz-img {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
  cursor: default;
  background: rgba(0, 0, 0, 0.25);
  position: relative;
}

.gz-img.clickable {
  cursor: pointer;
}

.gz-img img {
  display: block;
  width: 100%;
  height: 420px;
  object-fit: cover;
}

.gz-preview-video {
  display: block;
  width: 100%;
  height: 420px;
  object-fit: cover;
  background: rgba(0, 0, 0, 0.45);
}

.gz-badges {
  position: absolute;
  left: 12px;
  top: 12px;
  display: flex;
  gap: 8px;
  align-items: center;
  pointer-events: none;
}

.gz-badge {
  font-size: 12px;
  font-weight: 900;
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
  color: rgba(255, 255, 255, 0.92);
}

.gz-badge-selected {
  border-color: rgba(255, 215, 0, 0.45);
  background: rgba(255, 215, 0, 0.14);
  color: rgba(255, 215, 0, 0.98);
}

.gz-badge-video {
  border-color: rgba(255, 107, 107, 0.40);
  background: rgba(255, 107, 107, 0.12);
}

.gz-video-placeholder {
  height: 420px;
  display: grid;
  place-content: center;
  gap: 10px;
  background:
    radial-gradient(circle at 20% 20%, rgba(255, 215, 0, 0.18), transparent 55%),
    radial-gradient(circle at 80% 30%, rgba(255, 107, 107, 0.12), transparent 60%),
    rgba(0, 0, 0, 0.18);
  color: rgba(255, 255, 255, 0.9);
}

.gz-video-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  display: grid;
  place-content: center;
  font-size: 26px;
  font-weight: 900;
  color: rgba(255, 215, 0, 0.95);
  border: 1px solid rgba(255, 215, 0, 0.25);
  background: rgba(0, 0, 0, 0.25);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.45);
}

.gz-video-text {
  font-size: 13px;
  opacity: 0.85;
  text-align: center;
}

.gz-play {
  position: absolute;
  right: 12px;
  bottom: 12px;
  border: 1px solid rgba(255, 215, 0, 0.22);
  background: linear-gradient(145deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0.18) 100%);
  color: rgba(255, 255, 255, 0.94);
  padding: 10px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 900;
  backdrop-filter: blur(10px);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.gz-play-icon {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  color: rgba(255, 215, 0, 0.98);
  background: rgba(255, 215, 0, 0.12);
  border: 1px solid rgba(255, 215, 0, 0.25);
}

.gz-play:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 215, 0, 0.35);
  box-shadow: 0 14px 26px rgba(0, 0, 0, 0.55);
}

.gz-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.gz-title {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
}

.gz-name {
  font-size: 22px;
  font-weight: 900;
}

.gz-index {
  opacity: 0.7;
  font-size: 13px;
}

.gz-desc {
  margin-top: 2px;
  opacity: 0.9;
  line-height: 1.6;
  font-size: 14px;
}

.gz-confirm {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.gz-confirm-btn {
  border: none;
  cursor: pointer;
  padding: 12px 16px;
  border-radius: 14px;
  font-weight: 900;
  background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
  color: #111;
  box-shadow: 0 10px 22px rgba(255, 215, 0, 0.22);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.gz-confirm-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(255, 215, 0, 0.28);
}

.gz-reset-btn {
  border: 1px solid rgba(255, 255, 255, 0.18);
  cursor: pointer;
  padding: 12px 16px;
  border-radius: 14px;
  font-weight: 800;
  background: rgba(0, 0, 0, 0.25);
  color: rgba(255, 255, 255, 0.9);
}

.gz-form {
  margin-top: 18px;
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(0, 0, 0, 0.25);
}

.gz-form h3 {
  margin: 0 0 12px;
  font-size: 20px;
}

.gz-form-row {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.12);
  align-items: center;
}

.gz-form-row > * {
  min-width: 0;
}

.gz-form-row:last-child {
  border-bottom: none;
}

.gz-form-label {
  opacity: 0.85;
  font-weight: 800;
  line-height: 1.25;
}

.gz-form-value {
  font-weight: 900;
}

.gz-form-control {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.gz-input,
.gz-select {
  width: 100%;
  max-width: 100%;
  min-width: 0;
  height: 46px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(0, 0, 0, 0.24);
  color: rgba(255, 255, 255, 0.92);
  outline: none;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
  transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
  box-sizing: border-box;
}

input.gz-input[type="datetime-local"] {
  min-width: 0;
}

.gz-datetime-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.gz-time-select {
  height: 46px;
  font-size: 14px;
}

.gz-time-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.gz-input:focus,
.gz-select:focus {
  border-color: rgba(255, 215, 0, 0.55);
  box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.10);
}

.gz-select {
  appearance: none;
  background-image:
    linear-gradient(45deg, transparent 50%, rgba(255, 215, 0, 0.85) 50%),
    linear-gradient(135deg, rgba(255, 215, 0, 0.85) 50%, transparent 50%),
    linear-gradient(to right, rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0.14));
  background-position:
    calc(100% - 18px) 18px,
    calc(100% - 12px) 18px,
    calc(100% - 40px) 50%;
  background-size: 6px 6px, 6px 6px, 1px 22px;
  background-repeat: no-repeat;
  padding-right: 52px;
}

.gz-hint {
  font-size: 13px;
  opacity: 0.8;
}

.gz-note {
  margin-top: 10px;
  font-size: 13px;
  opacity: 0.85;
}

.gz-note.strong {
  opacity: 0.95;
  color: rgba(255, 215, 0, 0.95);
  font-weight: 900;
}

.gz-actions {
  margin-top: 14px;
  display: flex;
  justify-content: flex-end;
}

.gz-copy-btn {
  border: none;
  cursor: pointer;
  padding: 12px 16px;
  border-radius: 14px;
  font-weight: 900;
  background: linear-gradient(145deg, #FF6B6B 0%, #FF8E53 100%);
  color: #111;
  box-shadow: 0 10px 22px rgba(255, 107, 107, 0.22);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.gz-copy-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(255, 107, 107, 0.28);
}

.gz-copy-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.gz-price {
  margin-top: 18px;
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(0, 0, 0, 0.25);
}

.gz-price h3 {
  margin: 0 0 12px;
  font-size: 20px;
}

.gz-price-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.gz-price-item {
  padding: 12px;
  border-radius: 14px;
  border: 1px solid rgba(255, 215, 0, 0.14);
  background: rgba(255, 215, 0, 0.06);
}

.gz-price-label {
  font-weight: 900;
}

.gz-price-value {
  opacity: 0.9;
  margin-top: 6px;
  line-height: 1.5;
}

@media (max-width: 980px) {
  .guizhou-carousel {
    grid-template-columns: 54px 1fr 54px;
  }
  .gz-btn {
    width: 54px;
    height: 54px;
    border-radius: 999px;
  }
  .gz-card {
    grid-template-columns: 1fr;
  }
  .gz-img img {
    height: 360px;
  }

  .gz-preview-video {
    height: 360px;
  }

  .gz-video-placeholder {
    height: 360px;
  }
  .gz-form-row {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .gz-form-label {
    padding-top: 2px;
  }

  .gz-datetime-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .gz-actions {
    justify-content: stretch;
  }

  .gz-copy-btn {
    width: 100%;
  }
}

@media (max-width: 680px) {
  .guizhou-page {
    padding: 14px 12px 44px;
  }

  .guizhou-section {
    padding: 14px 12px 18px;
  }

  .guizhou-carousel {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .gz-btn {
    width: 56px;
    height: 56px;
    justify-self: center;
  }
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

/* 3D轮播容器样式 */
.home-content {
  max-width: 100%;
  margin: 40px auto;
  padding: 20px;
  min-height: 700px;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 650px;
  perspective: 2000px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.girl-card {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 520px;
  height: 620px;
  display: flex;
  gap: 0;
  background: transparent;
  border-radius: 16px;
  padding: 0;
  box-shadow: 0 10px 35px rgba(0,0,0,0.35);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
}

.girl-card.active {
  box-shadow: 0 12px 48px rgba(255, 215, 0, 0.3);
}

.girl-image {
  flex: 1;
  min-width: 0;
  cursor: pointer;
}

.girl-image img {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  display: block;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.girl-image:hover img {
  transform: scale(1.05);
}

.girl-video {
  flex: 1;
  min-width: 0;
}

.girl-video video {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  display: block;
  background: #000;
  object-fit: cover;
}

/* 图片放大遮罩 */
.image-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: pointer;
}

/* 视频播放遮罩 */
.video-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.overlay-video {
  max-width: 95vw;
  max-height: 85vh;
  border-radius: 12px;
  background: #000;
  box-shadow: 0 12px 48px rgba(0,0,0,0.6);
}

.image-overlay img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 0 50px rgba(255, 215, 0, 0.5);
}

.close-btn {
  position: absolute;
  top: calc(env(safe-area-inset-top) + 16px);
  right: calc(env(safe-area-inset-right) + 16px);
  background: #FFD700;
  color: #222;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  display: grid;
  place-items: center;
  line-height: 1;
  box-shadow: 0 12px 30px rgba(0,0,0,0.55);
  z-index: 10000;
}

.close-btn:hover {
  transform: scale(1.1);
  background: #ffe066;
}

/* 轮播切换按钮容器 */
.carousel-controls {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 30px;
}

/* 轮播切换按钮样式 - 扁平风格 */
.carousel-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 50px;
  background: rgba(255, 215, 0, 0.8);
  border: none;
  border-radius: 8px;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-btn:hover {
  background: rgba(255, 215, 0, 1);
  transform: scale(1.05);
}

.carousel-btn svg {
  width: 28px;
  height: 28px;
}

/* 旧的列表样式（保留备用） */
.girls-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 20px;
}

/* 旧的图片列表样式（保留作为备用） */
.img-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}
.img-card {
  width: 180px;
  background: #181818;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px #0003;
  margin-bottom: 8px;
}
.img-card img {
  width: 100%;
  display: block;
  border-radius: 8px;
}
.price-section, .process-section, .contact-section {
  margin: 80px auto 0 auto;
  padding: 48px 32px;
  background: #222;
  border-radius: 16px;
  color: #FFD700;
  max-width: 700px;
  box-shadow: 0 4px 24px #0005;
  min-height: 60vh;
}
.price-section h2, .process-section h2, .contact-section h2 {
  font-size: 2em;
  color: #FFD700;
  margin-bottom: 24px;
  text-align: center;
}
.price-cards {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}
.price-card {
  background: #111;
  border-radius: 12px;
  flex: 1;
  padding: 18px 0 10px 0;
  text-align: center;
  box-shadow: 0 2px 8px #0003;
  margin: 0 2px;
}
.circle {
  width: 48px;
  height: 48px;
  background: #FFD700;
  color: #222;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  font-weight: bold;
  margin: 0 auto 8px auto;
}
.price {
  font-size: 1.5em;
  color: #FFD700;
  font-weight: bold;
}
.desc {
  color: #fff;
  margin: 18px 0 10px 0;
  text-align: center;
}

/* 流程卡片样式 */
.process-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin: 40px auto;
  max-width: 1400px;
}

.process-step {
  background: linear-gradient(145deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.1) 100%);
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 16px;
  padding: 24px 20px;
  text-align: center;
  min-width: 200px;
  max-width: 240px;
  flex: 1;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
  position: relative;
}

.process-step:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.4);
  border-color: rgba(255, 215, 0, 0.6);
}

.step-number {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #FF6B6B 0%, #FFD700 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8em;
  font-weight: bold;
  color: #fff;
  box-shadow: 0 4px 20px rgba(255, 107, 107, 0.6), 0 0 30px rgba(255, 215, 0, 0.4);
  animation: numberPulse 2s ease-in-out infinite;
  z-index: 10;
  border: 3px solid #1a1a1a;
}

@keyframes numberPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(255, 107, 107, 0.6), 0 0 30px rgba(255, 215, 0, 0.4);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 6px 30px rgba(255, 107, 107, 0.8), 0 0 50px rgba(255, 215, 0, 0.6);
  }
}

.step-icon {
  font-size: 3em;
  margin-bottom: 12px;
  filter: drop-shadow(0 2px 8px rgba(255, 215, 0, 0.3));
}

.step-title {
  font-size: 1.3em;
  font-weight: bold;
  color: #FFD700;
  margin-bottom: 12px;
  letter-spacing: 1px;
}

.step-content {
  color: #fff;
  font-size: 1em;
  line-height: 1.6;
}

.process-connector {
  flex-shrink: 0;
  width: 60px;
  height: 2px;
  background: transparent;
  border-top: 3px dashed rgba(255, 215, 0, 0.6);
  position: relative;
  animation: dashMove 20s linear infinite;
}

@keyframes dashMove {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 100px 0;
  }
}

/* 福利网格布局 */
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin: 20px 0;
}

.benefit-item {
  background: rgba(255, 215, 0, 0.08);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.benefit-item:hover {
  background: rgba(255, 215, 0, 0.15);
  transform: translateX(5px);
  border-color: rgba(255, 215, 0, 0.4);
}

.benefit-icon {
  font-size: 2em;
  flex-shrink: 0;
}

.benefit-text {
  color: #fff;
  font-size: 1em;
  line-height: 1.4;
}

.steps {
  color: #fff;
  padding-left: 20px;
  margin-bottom: 0;
}
.steps li {
  margin-bottom: 8px;
  font-size: 1.1em;
}
.contact-block {
  color: #fff;
  font-size: 1.1em;
  text-align: center;
  margin-top: 20px;
}

.contact-item {
  margin: 12px 0;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.inline-link {
  color: #FFD700;
  text-decoration: none;
  transition: color 0.3s ease;
}

.inline-link:hover {
  color: #FFA500;
  text-decoration: underline;
}

.copy-btn {
  margin-top: 12px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #1a1a1a;
  border: none;
  border-radius: 10px;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
  background: linear-gradient(135deg, #FFE55C 0%, #FFB84D 100%);
}

.copy-btn:active {
  transform: translateY(0);
}

.copy-btn-small {
  padding: 6px 16px;
  background: rgba(255, 215, 0, 0.2);
  color: #FFD700;
  border: 1px solid rgba(255, 215, 0, 0.4);
  border-radius: 6px;
  font-size: 0.9em;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.copy-btn-small:hover {
  background: rgba(255, 215, 0, 0.3);
  border-color: rgba(255, 215, 0, 0.6);
  transform: scale(1.05);
}

.copy-btn-small:active {
  transform: scale(0.98);
}

.copy-toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 20px 40px;
  border-radius: 12px;
  font-size: 1.3em;
  font-weight: bold;
  box-shadow: 0 8px 32px rgba(76, 175, 80, 0.5);
  z-index: 10000;
  animation: toastPop 0.3s ease;
}

@keyframes toastPop {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.5);
}

.contact-note {
  margin-top: 20px;
  color: #FFD700;
  font-size: 1.05em;
}

/* SafeX 高亮样式 */
.safex-highlight {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 142, 83, 0.2) 100%);
  border: 3px solid #FF6B6B;
  border-radius: 20px;
  padding: 32px 24px;
  margin: 30px auto;
  max-width: 600px;
  box-shadow: 0 8px 32px rgba(255, 107, 107, 0.4), 0 0 60px rgba(255, 107, 107, 0.2);
  animation: safexPulse 2s ease-in-out infinite;
  position: relative;
}

.safex-highlight::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #FF6B6B, #FFD700, #FF8E53, #FF6B6B);
  border-radius: 20px;
  z-index: -1;
  opacity: 0.3;
  filter: blur(10px);
  animation: safexGlow 3s linear infinite;
}

@keyframes safexPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 8px 32px rgba(255, 107, 107, 0.4), 0 0 60px rgba(255, 107, 107, 0.2);
  }
  50% {
    transform: scale(1.02);
    box-shadow: 0 12px 48px rgba(255, 107, 107, 0.6), 0 0 80px rgba(255, 107, 107, 0.3);
  }
}

@keyframes safexGlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.safex-badge {
  display: inline-block;
  background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
  color: white;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 16px;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
  letter-spacing: 1px;
}

.safex-title {
  font-size: 2em;
  font-weight: bold;
  color: #FF6B6B;
  margin: 16px 0;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.6), 0 0 40px rgba(255, 107, 107, 0.3);
  letter-spacing: 2px;
}

.safex-link {
  display: inline-block;
  font-size: 1.4em;
  color: #FFD700;
  background: rgba(255, 215, 0, 0.1);
  padding: 16px 32px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: bold;
  margin: 16px 0;
  transition: all 0.3s ease;
  border: 2px solid #FFD700;
}

.safex-link:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: scale(1.05);
  box-shadow: 0 8px 24px rgba(255, 215, 0, 0.4);
}

.safex-desc {
  font-size: 1.15em;
  color: #fff;
  margin-top: 16px;
  letter-spacing: 2px;
}

.contact-divider {
  color: #888;
  font-size: 1.2em;
  margin: 40px 0 20px 0;
  text-align: center;
  position: relative;
}

.contact-divider::before,
.contact-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: linear-gradient(to right, transparent, #888, transparent);
}

.contact-divider::before {
  left: 0;
}

.contact-divider::after {
  right: 0;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

/* 网页 logo 样式 */
.logo-container {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-container:hover {
  transform: scale(1.05);
}

.logo-container:active {
  transform: scale(0.98);
}

.page-logo {
  height: 120px;
  display: block;
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.logo-container:hover .page-logo {
  box-shadow: 0 8px 24px rgba(255, 215, 0, 0.4);
}

/* 粒子背景样式 */
.particles-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
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

/* 移动端适配 */
@media (max-width: 768px) {
  .app-root {
    --nav-height: 0px;
    padding-top: env(safe-area-inset-top);
    padding-left: 0;
    font-size: 13.5px;
  }

  .page-logo {
    height: 64px;
  }

  .logo-container {
    margin-top: 6px;
  }
  
  .top-nav {
    flex-direction: column;
    flex-wrap: nowrap;
    gap: 8px;
    padding: 10px 8px;
    width: 88px;
    left: 10px;
    right: auto;
    top: calc(50% + env(safe-area-inset-top));
    transform: translateY(-50%);
    border-radius: 16px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.5);
    transition: width 0.25s ease, padding 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
    z-index: 2000;
    cursor: grab;
    touch-action: none;
  }

  .top-nav.dragging {
    box-shadow: 0 10px 34px rgba(0,0,0,0.65);
    cursor: grabbing;
  }

  .nav-handle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    width: 100%;
    padding: 7px 6px;
    margin-bottom: 2px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.10) 0%, rgba(255, 165, 0, 0.06) 100%);
    border: 1px solid rgba(255, 215, 0, 0.26);
    cursor: inherit;
    touch-action: none;
    user-select: none;
    position: relative;
    z-index: 1;
    pointer-events: none;
  }

  .top-nav.dragging .nav-handle {
    cursor: inherit;
  }

  .nav-toggle {
    width: 34px;
    height: 30px;
    border-radius: 12px;
    border: 1px solid rgba(255, 215, 0, 0.35);
    background: rgba(255, 215, 0, 0.12);
    color: #FFD700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s ease, background 0.2s ease, border-color 0.2s ease;
    pointer-events: auto;
  }

  .nav-toggle svg {
    width: 18px;
    height: 18px;
  }

  .nav-toggle:active {
    transform: scale(0.96);
  }

  .nav-grip {
    flex: 1;
    min-height: 30px;
    height: 30px;
    border-radius: 10px;
    cursor: inherit;
    touch-action: none;
    background:
      radial-gradient(circle at 20% 50%, rgba(255,215,0,0.65) 2px, transparent 3px) 0 0/10px 10px,
      radial-gradient(circle at 20% 50%, rgba(255,215,0,0.65) 2px, transparent 3px) 5px 5px/10px 10px;
    opacity: 0.55;
    position: relative;
    pointer-events: none;
  }


  
  .nav-btn {
    min-width: 0;
    width: 100%;
    padding: 9px 6px;
    font-size: 12.5px;
    border-radius: 14px;
    box-shadow: none;
    pointer-events: auto;
    cursor: pointer;
  }
  
  .btn-icon {
    font-size: 22px;
  }
  
  .btn-text {
    font-size: 11.5px;
  }

  .top-nav.collapsed {
    width: 64px;
    padding: 10px 8px;
    transform: translateY(-50%) translateX(-52px);
  }

  .top-nav.collapsed .btn-text {
    display: none;
  }

  .top-nav.collapsed .nav-btn {
    padding: 10px 6px;
  }

  .top-nav.collapsed .btn-icon {
    font-size: 24px;
  }

  .top-nav.collapsed .nav-handle {
    padding: 8px 6px;
  }
  
  .home-content {
    min-height: 620px;
    margin: 14px auto;
    padding: 10px;
  }
  
  .carousel-container {
    height: 60vh;
    min-height: 420px;
    max-height: 540px;
    perspective: 1500px;
    margin-bottom: 10px;
  }
  
  .girl-card {
    width: 90vw;
    max-width: 500px;
    height: 68vh;
    max-height: 560px;
  }
  
  .girl-image {
    height: 100%;
  }

  .girl-image img {
    object-fit: contain;
    background: transparent;
  }

  .girl-image:hover img {
    transform: none;
  }
  
  .carousel-btn {
    width: 70px;
    height: 48px;
  }
  
  .carousel-btn svg {
    width: 26px;
    height: 26px;
  }
  
  .carousel-controls {
    gap: 26px;
    margin-top: 14px;
    padding-bottom: 10px;
  }
  
  .price-section, .process-section, .contact-section {
    padding: 24px 16px;
    min-height: auto;
  }
  
  .process-flow {
    flex-direction: column;
    gap: 15px;
    margin: 20px auto;
  }
  
  .process-step {
    max-width: 90%;
    min-width: 280px;
  }
  
  .step-number {
    width: 45px;
    height: 45px;
    font-size: 1.5em;
    top: -12px;
    right: -12px;
  }
  
  .process-connector {
    width: 2px;
    height: 30px;
    border-top: none;
    border-left: 3px dashed rgba(255, 215, 0, 0.6);
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .benefit-item {
    padding: 12px;
  }
  
  .price-cards {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .price-card {
    min-width: calc(50% - 8px);
  }
  
  .contact-block {
    font-size: 0.95em;
  }
  
  .contact-item {
    padding: 8px;
    font-size: 0.9em;
    word-break: break-all;
  }
  
  .safex-highlight {
    padding: 24px 16px;
    margin: 20px 10px;
    max-width: 95%;
  }
  
  .safex-title {
    font-size: 1.5em;
    letter-spacing: 1px;
  }
  
  .safex-link {
    font-size: 1.1em;
    padding: 12px 20px;
    word-break: break-all;
  }
  
  .safex-desc {
    font-size: 1em;
    letter-spacing: 1px;
  }
  
  .safex-badge {
    font-size: 0.95em;
    padding: 6px 18px;
  }
  
  .contact-divider {
    font-size: 1em;
    margin: 30px 0 15px 0;
  }
  
  .contact-note {
    font-size: 0.95em;
  }
  
  .image-overlay img {
    max-width: 95%;
    max-height: 85%;
  }
}

@media (max-width: 480px) {
  .app-root {
    --nav-height: 0px;
    padding-top: env(safe-area-inset-top);
    padding-left: 84px;
    font-size: 12.8px;
  }

  .page-logo {
    height: 52px;
  }
  
  .top-nav {
    width: 82px;
    left: 8px;
    padding: 10px 8px;
    gap: 8px;
    top: calc(50% + env(safe-area-inset-top));
    transform: translateY(-50%);
    z-index: 2000;
    cursor: grab;
  }
  
  .nav-btn {
    padding: 9px 6px;
    border-radius: 12px;
  }
  
  .btn-icon {
    font-size: 20px;
  }
  
  .btn-text {
    font-size: 12px;
  }
  
  .home-content {
    min-height: 580px;
  }
  
  .carousel-container {
    height: 480px;
    margin-bottom: 15px;
  }
  
  .girl-card {
    height: 66vh;
    max-height: 520px;
    padding: 0;
    gap: 0;
  }
  
  .girl-image {
    height: 100%;
  }

  .girl-image img {
    object-fit: contain;
    background: transparent;
  }

  .girl-image:hover img {
    transform: none;
  }
  
  .carousel-btn {
    width: 60px;
    height: 42px;
  }
  
  .carousel-btn svg {
    width: 22px;
    height: 22px;
  }
  
  .carousel-controls {
    gap: 25px;
    margin-top: 20px;
    padding-bottom: 15px;
  }
  
  .price-card {
    min-width: 100%;
  }
  
  .process-step {
    min-width: 260px;
    padding: 20px 16px;
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1.3em;
    top: -10px;
    right: -10px;
  }
  
  .step-icon {
    font-size: 2.5em;
  }
  
  .step-title {
    font-size: 1.15em;
  }
  
  .step-content {
    font-size: 0.9em;
  }
  
  .process-connector {
    height: 25px;
  }
  
  .benefit-item {
    padding: 10px;
  }
  
  .benefit-icon {
    font-size: 1.6em;
  }
  
  .benefit-text {
    font-size: 0.9em;
  }
  
  .contact-block {
    font-size: 0.85em;
  }
  
  .contact-item {
    padding: 6px;
    margin: 10px 0;
  }
  
  .safex-highlight {
    padding: 20px 12px;
    margin: 15px 5px;
  }
  
  .safex-title {
    font-size: 1.3em;
    letter-spacing: 0.5px;
  }
  
  .safex-link {
    font-size: 0.95em;
    padding: 10px 16px;
  }
  
  .safex-desc {
    font-size: 0.9em;
    letter-spacing: 0.5px;
  }
  
  .safex-badge {
    font-size: 0.85em;
    padding: 5px 15px;
  }
  
  .contact-divider {
    font-size: 0.9em;
    margin: 25px 0 12px 0;
  }
  
  .contact-divider::before,
  .contact-divider::after {
    width: 20%;
  }
  
  .contact-note {
    font-size: 0.85em;
    margin-top: 15px;
  }
}

/* logo 背景样式 */
.logo-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('https://cdn.jsdelivr.net/gh/xiaochaowen95-svg/bwgj-img/bwgj.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.1;
  z-index: -2;
  pointer-events: none;
}
</style>
