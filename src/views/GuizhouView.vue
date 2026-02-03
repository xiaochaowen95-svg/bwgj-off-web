<template>
  <div class="guizhou-page">
    <section class="guizhou-section">
      <div class="guizhou-head">
        <h2>贵州区域</h2>
        <div class="guizhou-sub">展示贵州区域全部妹妹，可左右切换（不自动轮播）</div>
      </div>

      <div class="guizhou-loading" v-if="loading">正在加载贵州专区信息…</div>
      <div class="guizhou-error" v-else-if="error">{{ error }}</div>

      <template v-else>
        <div v-if="!girls.length" class="guizhou-empty">
          还没有检测到贵州专区数据。请在 public/guizhou/ 放图片/视频，并编辑 public/guizhou/data.json（或兼容 public/mm/guizhou/data.json）。
        </div>

        <div v-else class="guizhou-carousel">
          <button class="gz-btn gz-prev gz-btn-pc" type="button" @click="prevGirl" :disabled="girls.length <= 1" aria-label="上一位">
            <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M14.5 5.5L8.5 12l6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>

          <div class="gz-card" :class="{ selected: selected?.id === currentGirl?.id }">
            <div
              class="gz-img"
              :class="{ clickable: !!currentGirl?.image || !!currentGirl?.video }"
              @click="handleMediaClick"
            >
              <img v-if="currentGirl?.image" :src="currentGirl.image" :alt="currentGirl.name" />
              <video
                v-else-if="currentGirl?.video"
                class="gz-preview-video"
                :src="currentGirl.video"
                :poster="(currentGirl.poster || getPoster(currentGirl.video) || undefined)"
                muted
                playsinline
                preload="metadata"
              ></video>

              <div class="gz-badges">
                <span v-if="selected?.id === currentGirl?.id" class="gz-badge gz-badge-selected">已选</span>
                <span v-else class="gz-badge gz-badge-tip">左右切换</span>
                <span v-if="currentGirl?.video" class="gz-badge gz-badge-video">视频</span>
              </div>

              <button
                v-if="currentGirl?.video"
                type="button"
                class="gz-play"
                @click.stop="playVideo"
                title="播放视频"
              >
                <span class="gz-play-icon" aria-hidden="true">▶</span>
                <span>播放视频</span>
              </button>
            </div>

            <div class="gz-info">
              <div class="gz-title">
                <span class="gz-name">{{ currentGirl.name }}</span>
                <span class="gz-index">{{ currentIndex + 1 }} / {{ girls.length }}</span>
              </div>
              <div class="gz-desc" v-if="currentGirl.desc">{{ currentGirl.desc }}</div>

              <div class="gz-confirm">
                <button type="button" class="gz-confirm-btn" @click="confirmGirl">确定选择</button>
                <button v-if="selected" type="button" class="gz-reset-btn" @click="resetSelection">重新选择</button>
              </div>
            </div>
          </div>

          <button class="gz-btn gz-next gz-btn-pc" type="button" @click="nextGirl" :disabled="girls.length <= 1" aria-label="下一位">
            <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M9.5 5.5l6 6.5-6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>

          <div class="gz-btn-mobile">
            <button class="gz-btn gz-prev" type="button" @click="prevGirl" :disabled="girls.length <= 1" aria-label="上一位">
              <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M14.5 5.5L8.5 12l6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="gz-btn gz-next" type="button" @click="nextGirl" :disabled="girls.length <= 1" aria-label="下一位">
              <svg class="gz-nav-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M9.5 5.5l6 6.5-6 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="selected" class="gz-form">
          <h3>需求表单</h3>

          <div class="gz-form-row">
            <div class="gz-form-label">意向妹妹</div>
            <div class="gz-form-value">{{ selected.name }}</div>
          </div>

          <div class="gz-form-row">
            <label class="gz-form-label" for="gz-mode">客户游玩方式</label>
            <div class="gz-form-control">
              <select id="gz-mode" v-model="playMode" class="gz-select">
                <option value="自带">自带（不需要交定金）</option>
                <option value="外卖">外卖</option>
              </select>
            </div>
          </div>

          <div class="gz-form-row">
            <label class="gz-form-label">游玩时间</label>
            <div class="gz-form-control">
              <div class="gz-datetime-grid">
                <select v-model="month" class="gz-select gz-time-select">
                  <option value="">月份</option>
                  <option v-for="opt in monthOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
                <select v-model="day" class="gz-select gz-time-select" :disabled="!month">
                  <option value="">日期</option>
                  <option v-for="opt in dayOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
                <select v-model="hour" class="gz-select gz-time-select">
                  <option value="">小时</option>
                  <option v-for="opt in hourOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
                <select v-model="minute" class="gz-select gz-time-select">
                  <option value="">分钟</option>
                  <option v-for="opt in minuteOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
              </div>
              <div class="gz-hint" v-if="datetimeText">已选：{{ datetimeText }}</div>
            </div>
          </div>

          <div class="gz-form-row" v-if="playMode === '外卖'">
            <label class="gz-form-label" for="gz-address">游玩地址</label>
            <div class="gz-form-control">
              <input id="gz-address" class="gz-input" type="text" placeholder="请填写具体地址" v-model="address" />
            </div>
          </div>

          <div class="gz-note">提示：我们不会存储任何数据，当前表单关闭信息就将丢失。</div>
          <div class="gz-note strong">特别说明：小河区域不能外出。</div>

          <div class="gz-actions">
            <button type="button" class="gz-copy-btn" :disabled="!canCopy" @click="copyDemand">复制需求信息</button>
          </div>
        </div>

        <div class="gz-price">
          <h3>贵州地区价目表</h3>
          <div class="gz-price-grid">
            <div class="gz-price-item" v-for="p in priceList" :key="p.label">
              <div class="gz-price-label">{{ p.label }}</div>
              <div class="gz-price-value">{{ p.value }}</div>
            </div>
          </div>
        </div>
      </template>

      <transition name="toast">
        <div v-if="toast" class="copy-toast">✔️ {{ toast }}</div>
      </transition>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const emit = defineEmits(['enlarge-image', 'play-video', 'show-toast'])

const girls = ref([])
const loading = ref(false)
const error = ref('')
const currentIndex = ref(0)
const selected = ref(null)

const playMode = ref('自带')
const month = ref('')
const day = ref('')
const hour = ref('')
const minute = ref('')
const address = ref('')
const toast = ref('')

const posterCache = ref({})
const posterPending = new Set()

const priceList = [
  { label: '小圈', value: '1000 / 次；1300 / 2次（无图）' },
  { label: '小中', value: '1500' },
  { label: '中', value: '2000' },
  { label: '中大', value: '2500' },
  { label: '大圈', value: '1800 / 次（不一定有）' },
]

const currentGirl = computed(() => {
  if (!girls.value.length) return null
  return girls.value[Math.min(girls.value.length - 1, Math.max(0, currentIndex.value))] || null
})

const monthOptions = computed(() => {
  return Array.from({ length: 12 }, (_, i) => {
    const m = i + 1
    return { value: String(m).padStart(2, '0'), label: `${m}月` }
  })
})

const dayOptions = computed(() => {
  const m = month.value ? Number(month.value) : 1
  const daysInMonth = new Date(2026, m, 0).getDate()
  return Array.from({ length: daysInMonth }, (_, i) => {
    const d = i + 1
    return { value: String(d).padStart(2, '0'), label: `${d}日` }
  })
})

const hourOptions = computed(() => {
  return Array.from({ length: 24 }, (_, i) => {
    return { value: String(i).padStart(2, '0'), label: `${i}点` }
  })
})

const minuteOptions = computed(() => {
  return Array.from({ length: 60 }, (_, i) => {
    return { value: String(i).padStart(2, '0'), label: `${i}分` }
  })
})

const datetimeText = computed(() => {
  if (!month.value || !day.value || !hour.value || !minute.value) return ''
  const m = Number(month.value)
  const d = Number(day.value)
  const h = Number(hour.value)
  const min = Number(minute.value)
  return `2026年${m}月${d}日 ${String(h).padStart(2, '0')}点${String(min).padStart(2, '0')}分`
})

const canCopy = computed(() => {
  if (!selected.value) return false
  if (!month.value || !day.value || !hour.value || !minute.value) return false
  if (playMode.value === '外卖' && !address.value.trim()) return false
  return true
})

function getPoster(videoUrl) {
  return posterCache.value[videoUrl] || ''
}

async function capturePoster(videoUrl) {
  if (!videoUrl || posterCache.value[videoUrl] || posterPending.has(videoUrl)) return
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
          posterCache.value = { ...posterCache.value, [videoUrl]: dataUrl }
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

async function loadGirls() {
  if (loading.value) return
  loading.value = true
  error.value = ''
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

        if (!image && !video && file) {
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

    girls.value = normalized
    currentIndex.value = 0
  } catch (err) {
    error.value = '贵州专区数据加载失败：请检查 public/guizhou/data.json 或 public/mm/guizhou/data.json 是否存在且 JSON 格式正确。'
    girls.value = []
  } finally {
    loading.value = false
  }
}

function prevGirl() {
  if (!girls.value.length) return
  currentIndex.value = (currentIndex.value - 1 + girls.value.length) % girls.value.length
}

function nextGirl() {
  if (!girls.value.length) return
  currentIndex.value = (currentIndex.value + 1) % girls.value.length
}

function confirmGirl() {
  if (!currentGirl.value) return
  selected.value = currentGirl.value
}

function resetSelection() {
  selected.value = null
  playMode.value = '自带'
  month.value = ''
  day.value = ''
  hour.value = ''
  minute.value = ''
  address.value = ''
}

function handleMediaClick() {
  if (currentGirl.value?.image) {
    emit('enlarge-image', currentGirl.value.image)
  } else if (currentGirl.value?.video) {
    playVideo()
  }
}

function playVideo() {
  if (!currentGirl.value?.video) return
  emit('play-video', currentGirl.value.video, currentGirl.value.poster || getPoster(currentGirl.value.video))
}

function buildDemandText() {
  const lines = []
  lines.push('【贵州专区需求】')
  if (selected.value?.id && selected.value?.name) {
    lines.push(`意向妹妹：${selected.value.id} ${selected.value.name}`)
  } else if (selected.value?.name) {
    lines.push(`意向妹妹：${selected.value.name}`)
  }
  if (playMode.value) lines.push(`游玩方式：${playMode.value}`)
  if (datetimeText.value) lines.push(`游玩时间：${datetimeText.value}`)
  if (playMode.value === '外卖' && address.value) lines.push(`游玩地址：${address.value}`)
  lines.push('备注：小河区域不能外出')
  return lines.join('\n')
}

function copyDemand() {
  const text = buildDemandText()
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast('需求信息已复制！')
    }).catch(() => {
      fallbackCopy(text)
    })
  } else {
    fallbackCopy(text)
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.select()
  try {
    document.execCommand('copy')
    showToast('需求信息已复制！')
  } catch {
    showToast('复制失败，请手动复制')
  }
  document.body.removeChild(textarea)
}

function showToast(msg) {
  toast.value = msg
  setTimeout(() => {
    toast.value = ''
  }, 2000)
}

watch(playMode, (v) => {
  if (v !== '外卖') {
    address.value = ''
  }
})

watch([currentGirl, currentIndex, girls], () => {
  const cur = currentGirl.value
  if (cur?.video && !cur.poster) capturePoster(cur.video)

  const list = girls.value || []
  if (list.length < 2) return
  const i = currentIndex.value
  const next = list[(i + 1) % list.length]
  const prev = list[(i - 1 + list.length) % list.length]
  if (next?.video && !next.poster) capturePoster(next.video)
  if (prev?.video && !prev.poster) capturePoster(prev.video)
})

onMounted(() => {
  loadGirls()
})
</script>

<style scoped>
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

.copy-toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.85);
  color: #fff;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  z-index: 99999;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px);
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

.gz-btn-mobile {
  display: none;
}

@media (max-width: 680px) {
  .guizhou-page {
    padding: 12px 12px 44px;
  }

  .guizhou-section {
    padding: 20px 12px 24px;
  }

  .guizhou-carousel {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .gz-btn-pc {
    display: none;
  }

  .gz-btn-mobile {
    display: flex;
    justify-content: center;
    gap: 16px;
    width: 100%;
  }

  .gz-btn-mobile .gz-btn {
    width: 140px;
    height: 56px;
  }
}
</style>
