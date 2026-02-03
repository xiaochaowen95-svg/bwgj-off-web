<template>
  <div class="process-view">
    <section class="process-section">
      <h2>预约流程</h2>
      
      <div class="process-flow">
        <div class="process-step">
          <div class="step-number">1</div>
          <div class="step-icon">💬</div>
          <div class="step-title">确定需求</div>
          <div class="step-content">先跟客服妹妹说清楚<br/>（档次/时间/地点/大概几点玩）</div>
        </div>
        
        <div class="process-connector"></div>
        
        <div class="process-step">
          <div class="step-number">2</div>
          <div class="step-icon">🖼️</div>
          <div class="step-title">发图选人</div>
          <div class="step-content">客服发图<br/>挑选心仪妹妹</div>
        </div>
        
        <div class="process-connector"></div>
        
        <div class="process-step">
          <div class="step-number">3</div>
          <div class="step-icon">🚗</div>
          <div class="step-title">约好上门</div>
          <div class="step-content">选好→定时间地点<br/>妹子准时上门，先看人确认OK再继续</div>
        </div>
        
        <div class="process-connector"></div>
        
        <div class="process-step">
          <div class="step-number">4</div>
          <div class="step-icon">💎</div>
          <div class="step-title">满意付钱</div>
          <div class="step-content">满意付钱<br/>不满意可以退</div>
        </div>
      </div>
      
      <div class="extra">
        <h3>额外福利</h3>
        <div class="benefits-grid">
          <div class="benefit-item">
            <div class="benefit-icon">🏙️</div>
            <div class="benefit-text">三环内上门免车费</div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">🛣️</div>
            <div class="benefit-text">三环外路费实报实销（提前讲好）</div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">🎁</div>
            <div class="benefit-text">每日首单 -100元</div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">💝</div>
            <div class="benefit-text">推荐朋友消费成功返你100元（截图核销）</div>
          </div>
        </div>
        <div class="special">💡 特殊服务说明：三通、SM、无冒等特服需 +500</div>
        <div class="pay">💰 付款说明：无任何定金！见面满意付！预定除外！三环内免费上门，绕城外需实报车费（先付）。首次下单外出都需先付100定金，三环外付车费可免定金，自己开车去妹妹那里不需要定金。</div>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.process-view {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.process-section {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 215, 0, 0.14);
  border-radius: 18px;
  box-shadow: 0 10px 36px rgba(0, 0, 0, 0.35);
  padding: 18px 18px 26px;
  backdrop-filter: blur(10px);
}

.process-section h2 {
  margin: 0 0 20px;
  font-size: 28px;
  letter-spacing: 1px;
}

.process-flow {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
}

.process-step {
  flex: 1;
  max-width: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.25);
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.process-step:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 215, 0, 0.35);
  box-shadow: 0 12px 32px rgba(255, 215, 0, 0.12);
}

.step-number {
  position: absolute;
  top: -12px;
  left: -12px;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 1px solid rgba(255, 215, 0, 0.55);
  background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
  color: #111;
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 14px;
  box-shadow: 0 4px 14px rgba(255, 215, 0, 0.35);
}

.step-icon {
  font-size: 40px;
}

.step-title {
  font-size: 18px;
  font-weight: 900;
}

.step-content {
  text-align: center;
  opacity: 0.9;
  line-height: 1.6;
  font-size: 14px;
}

.process-connector {
  width: 28px;
  height: 2px;
  margin-top: 80px;
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.45), rgba(255, 215, 0, 0.12));
  position: relative;
}

.process-connector::after {
  content: '→';
  position: absolute;
  right: -12px;
  top: -11px;
  font-size: 18px;
  color: rgba(255, 215, 0, 0.85);
}

.extra {
  margin-top: 32px;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.25);
}

.extra h3 {
  margin: 0 0 16px;
  font-size: 22px;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.12);
  background: rgba(255, 215, 0, 0.04);
}

.benefit-icon {
  font-size: 28px;
  min-width: 36px;
  text-align: center;
}

.benefit-text {
  opacity: 0.95;
  line-height: 1.5;
}

.special,
.pay {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 107, 107, 0.25);
  background: rgba(255, 107, 107, 0.08);
  opacity: 0.95;
  line-height: 1.65;
  margin-top: 12px;
}

.pay {
  border-color: rgba(255, 215, 0, 0.25);
  background: rgba(255, 215, 0, 0.08);
}

@media (max-width: 980px) {
  .process-flow {
    flex-direction: column;
    align-items: center;
  }

  .process-step {
    max-width: 100%;
  }

  .process-connector {
    width: 2px;
    height: 28px;
    margin: 0;
    background: linear-gradient(180deg, rgba(255, 215, 0, 0.45), rgba(255, 215, 0, 0.12));
  }

  .process-connector::after {
    content: '↓';
    right: auto;
    top: auto;
    bottom: -14px;
    left: -9px;
  }

  .benefits-grid {
    grid-template-columns: 1fr;
  }
}
</style>
