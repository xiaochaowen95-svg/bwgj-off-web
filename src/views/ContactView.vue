<template>
  <div class="contact-view">
    <section class="contact-section">
      <h2>联系客服</h2>
      <div style="font-size:2em;color:#FFD700;margin-bottom:24px;">👇 联系方式在这里 👇</div>
      
      <div class="safex-highlight">
        <div class="safex-badge">⭐推荐首选⭐</div>
        <div class="safex-title">🔥 SafeX客服（强烈推荐）🔥</div>
        <a href="https://sfw.vc/waiwei91" target="_blank" class="safex-link">https://sfw.vc/waiwei91</a>
        <button class="copy-btn" @click="copy('https://sfw.vc/waiwei91', 'SafeX链接')">📋 复制链接</button>
        <div class="safex-desc">安全私密 · 响应快速 · 服务专业</div>
      </div>
      
      <div class="contact-divider">其他联系方式</div>
      
      <div class="contact-block">
        <div class="contact-item">
          <span>客服QQ：2388570976</span>
          <button class="copy-btn-small" @click="copy('2388570976', 'QQ号')">复制</button>
        </div>
        <div class="contact-item">
          <span>Telegram客服：</span>
          <a href="http://t.me/waiwei923_bot" target="_blank" class="inline-link">t.me/waiwei923_bot</a>
          <button class="copy-btn-small" @click="copy('waiwei923_bot', 'TG用户名')">复制</button>
        </div>
        <div class="contact-item">
          <span>妹子相册：</span>
          <a href="http://1261554.apps3.mui139.pics/" target="_blank" class="inline-link">http://1261554.apps3.mui139.pics/</a>
          <button class="copy-btn-small" @click="copy('http://1261554.apps3.mui139.pics/', '相册链接')">复制</button>
          <span style="margin-left: 10px;">密码：888</span>
          <button class="copy-btn-small" @click="copy('888', '密码')">复制</button>
        </div>
        <div class="contact-note">如需人工推荐或有疑问，直接联系客服！</div>
      </div>
    </section>
    
    <transition name="toast">
      <div v-if="toast" class="copy-toast">✔️ {{ toast }}</div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const toast = ref('')

function copy(text, label) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(`${label}已复制！`)
    }).catch(() => {
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
    showToast(`${label}已复制！`)
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
</script>

<style scoped>
.contact-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.contact-section {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 215, 0, 0.14);
  border-radius: 18px;
  box-shadow: 0 10px 36px rgba(0, 0, 0, 0.35);
  padding: 18px 18px 26px;
  backdrop-filter: blur(10px);
}

.contact-section h2 {
  margin: 0 0 20px;
  font-size: 28px;
  letter-spacing: 1px;
  text-align: center;
}

.safex-highlight {
  margin: 24px 0;
  padding: 26px 24px;
  border-radius: 18px;
  border: 2px solid rgba(255, 215, 0, 0.55);
  background: linear-gradient(145deg, rgba(255, 215, 0, 0.14) 0%, rgba(255, 165, 0, 0.08) 100%);
  text-align: center;
  box-shadow: 0 12px 38px rgba(255, 215, 0, 0.22);
  position: relative;
  overflow: hidden;
}

.safex-highlight::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: radial-gradient(circle at 20% 20%, rgba(255, 215, 0, 0.18), transparent 55%),
    radial-gradient(circle at 80% 30%, rgba(255, 107, 107, 0.10), transparent 60%);
  pointer-events: none;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.safex-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 999px;
  background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
  color: #111;
  font-weight: 900;
  font-size: 14px;
  margin-bottom: 12px;
  box-shadow: 0 6px 18px rgba(255, 215, 0, 0.35);
}

.safex-title {
  font-size: 24px;
  font-weight: 900;
  margin-bottom: 14px;
  color: rgba(255, 215, 0, 0.98);
}

.safex-link {
  display: block;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 16px;
  word-break: break-all;
  text-decoration: underline;
}

.safex-link:hover {
  color: rgba(255, 215, 0, 0.98);
}

.copy-btn {
  border: none;
  cursor: pointer;
  padding: 14px 24px;
  border-radius: 999px;
  font-weight: 900;
  font-size: 16px;
  background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
  color: #111;
  box-shadow: 0 10px 22px rgba(255, 215, 0, 0.22);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 28px rgba(255, 215, 0, 0.28);
}

.safex-desc {
  margin-top: 14px;
  font-size: 14px;
  opacity: 0.9;
}

.contact-divider {
  margin: 32px 0 20px;
  text-align: center;
  font-size: 18px;
  font-weight: 900;
  opacity: 0.75;
  position: relative;
}

.contact-divider::before,
.contact-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
}

.contact-divider::before {
  left: 0;
}

.contact-divider::after {
  right: 0;
}

.contact-block {
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.25);
}

.contact-item {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 14px 0;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.12);
  line-height: 1.6;
}

.contact-item:last-of-type {
  border-bottom: none;
}

.inline-link {
  color: rgba(255, 215, 0, 0.95);
  text-decoration: underline;
}

.inline-link:hover {
  color: rgba(255, 215, 0, 1);
}

.copy-btn-small {
  border: 1px solid rgba(255, 215, 0, 0.35);
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 800;
  font-size: 13px;
  background: rgba(255, 215, 0, 0.12);
  color: rgba(255, 215, 0, 0.98);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.copy-btn-small:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 215, 0, 0.55);
  box-shadow: 0 6px 14px rgba(255, 215, 0, 0.18);
}

.contact-note {
  margin-top: 16px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid rgba(255, 107, 107, 0.25);
  background: rgba(255, 107, 107, 0.08);
  opacity: 0.95;
  line-height: 1.6;
  text-align: center;
}

.copy-toast {
  position: fixed;
  top: 80px;
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

@media (max-width: 680px) {
  .contact-view {
    padding: 14px 12px 44px;
  }

  .contact-section {
    padding: 14px 12px 18px;
  }

  .safex-title {
    font-size: 20px;
  }

  .contact-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
