<script setup>
import { ref, onMounted } from 'vue'
import HelloWorld from './components/HelloWorld.vue'
import mmImages from './mmImages.js'

const priceSection = ref(null)
const processSection = ref(null)
const contactSection = ref(null)

const particles = ref([])

onMounted(() => {
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
})

function scrollTo(section) {
  if (section && section.value) {
    section.value.scrollIntoView({ behavior: 'smooth' })
  }
}

const priceList = [
  { name: '小圈', price: 1300 },
  { name: '小中', price: 1700 },
  { name: '中圈', price: 2000 },
  { name: '中大', price: 2500 },
  { name: '大圈', price: 3000 },
]
</script>

<template>
  <div>
    <!-- 粒子背景 -->
    <div class="particles-bg">
      <div v-for="particle in particles" :key="particle.id" class="particle" :style="{ left: particle.left + '%', top: particle.top + '%', animationDelay: particle.delay + 's', animationDuration: particle.duration + 's' }"></div>
    </div>

    <nav class="top-nav">
      <button @click="scrollTo(priceSection)">价目表</button>
      <button @click="scrollTo(processSection)">预约流程</button>
      <button @click="scrollTo(contactSection)">联系客服</button>
    </nav>

    <h1>妹子图片展示（前6张）</h1>
    <div class="img-list">
      <div v-for="(img, idx) in mmImages.slice(0, 6)" :key="img" class="img-card">
        <img :src="img" :alt="`妹子图片${idx+1}`" />
        <div class="img-path">{{ img }}</div>
      </div>
    </div>

    <!-- 价目表区块 -->
    <section ref="priceSection" class="price-section">
      <h2>价目表</h2>
      <div class="price-cards">
        <div class="price-card" v-for="item in priceList" :key="item.name">
          <div class="circle">{{ item.name }}</div>
          <div class="price">￥{{ item.price }}</div>
        </div>
      </div>
      <div class="desc">所有妹子成都本地真实上门，酒店/公寓随便约，照片95%+真人，档次越高越顶</div>
      <ul class="notice">
        <li>⚠️ 妹妹上门后，请先核对人和照片是否一致，如差距较大请及时告知客服，千万不要先付款！</li>
        <li>⚠️ 90分钟两次为您定好的妹妹，中途不能换人（做了一次后不能更换）。</li>
        <li>⚠️ 有无纹身等特殊要求请提前说明。</li>
      </ul>
    </section>

    <!-- 预约流程区块 -->
    <section ref="processSection" class="process-section">
      <h2>预约流程</h2>
      <ol class="steps">
        <li>确定需求，先跟客服妹妹说清楚（档次/时间/地点/大概几点玩）</li>
        <li>客服发图选人</li>
        <li>约好时间 & 见面，选好→定时间地点→妹子准时上门，先看人确认OK再继续</li>
        <li>满意付钱，不满意可换/退</li>
      </ol>
      <div class="extra">
        <h3>额外福利</h3>
        <ul>
          <li>🏙️ 三环内上门免车费</li>
          <li>🛣️ 三环外路费实报实销（提前讲好）</li>
          <li>🎁 每日首单 -100元</li>
          <li>🎁 推荐朋友消费成功返你100元（截图核销）</li>
        </ul>
        <div class="special">💡 特殊服务说明：三通、SM、无冒等特服需 +500</div>
        <div class="pay">💰 付款说明：无任何定金！见面满意付！预定除外！三环内免费上门，绕城外需实报车费（先付）。首次下单外出都需先付100定金，三环外付车费可免定金，自己开车去妹妹那里不需要定金。</div>
      </div>
    </section>

    <!-- 联系客服区块 -->
    <section ref="contactSection" class="contact-section">
      <h2>联系客服</h2>
      <div class="contact-block">
        <div>Telegram频道：<a href="https://t.me/+y4ehd5vU9LM3Y2Q1" target="_blank">https://t.me/+y4ehd5vU9LM3Y2Q1</a></div>
        <div>妹子相册：<a href="http://1261554.apps3.mui139.pics/" target="_blank">http://1261554.apps3.mui139.pics/</a> 密码：888</div>
        <div>如需人工推荐或有疑问，直接TG联系或留言！</div>
      </div>
    </section>

    <HelloWorld msg="Vite + Vue" />
  </div>
</template>

<style scoped>
.top-nav {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-bottom: 32px;
  background: #181818;
  padding: 18px 0 10px 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px #0003;
  position: sticky;
  top: 0;
  z-index: 10;
}
.top-nav button {
  background: #FFD700;
  color: #222;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  font-weight: bold;
  padding: 8px 24px;
  cursor: pointer;
  transition: background 0.2s;
}
.top-nav button:hover {
  background: #ffe066;
}
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
  border-radius: 8px 8px 0 0;
}
.img-path {
  color: #FFD700;
  font-size: 14px;
  padding: 4px 8px 8px 8px;
  word-break: break-all;
}
.price-section, .process-section, .contact-section {
  margin: 48px auto 0 auto;
  padding: 32px;
  background: #222;
  border-radius: 16px;
  color: #FFD700;
  max-width: 700px;
  box-shadow: 0 4px 24px #0005;
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
  margin-top: 12px;
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
</style>
