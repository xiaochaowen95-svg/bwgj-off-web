<template>
  <div class="price-view">
    <section class="price-section">
      <h2>价目表</h2>
      <div class="price-cards">
        <div class="price-card" v-for="item in priceList" :key="item.name">
          <div class="circle">{{ item.name }}</div>
          <div class="price">￥{{ item.price }}</div>
        </div>
      </div>
      <div class="desc">所有妹子成都本地真实上门，酒店/公寓随便约，照片95%+真人，档次越高越真。</div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const priceList = ref([
  { name: '小圈', price: '1000' },
  { name: '小中', price: '1500' },
  { name: '中圈', price: '2000' },
  { name: '中大', price: '2500' },
  { name: '大圈', price: '3500' }
])
</script>

<style scoped>
.price-view {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.price-section {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 215, 0, 0.14);
  border-radius: 18px;
  box-shadow: 0 10px 36px rgba(0, 0, 0, 0.35);
  padding: 18px 18px 26px;
  backdrop-filter: blur(10px);
}

.price-section h2 {
  margin: 0 0 20px;
  font-size: 28px;
  letter-spacing: 1px;
}

.price-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.price-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 24px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.price-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 215, 0, 0.35);
  box-shadow: 0 12px 32px rgba(255, 215, 0, 0.12);
}

.circle {
  font-size: 20px;
  font-weight: 900;
  width: 80px;
  height: 80px;
  border-radius: 999px;
  border: 2px solid rgba(255, 215, 0, 0.55);
  background: linear-gradient(145deg, rgba(255, 215, 0, 0.14) 0%, rgba(255, 165, 0, 0.08) 100%);
  color: rgba(255, 215, 0, 0.98);
  display: grid;
  place-items: center;
  box-shadow: 0 8px 22px rgba(255, 215, 0, 0.18);
}

.price {
  font-size: 26px;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.95);
}

.desc {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.14);
  background: rgba(255, 215, 0, 0.06);
  opacity: 0.95;
  line-height: 1.65;
  text-align: center;
}

@media (max-width: 680px) {
  .price-cards {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }

  .circle {
    width: 64px;
    height: 64px;
    font-size: 16px;
  }

  .price {
    font-size: 22px;
  }
}
</style>
