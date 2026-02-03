import { readFileSync, writeFileSync } from 'fs';

const content = readFileSync('src/App.vue', 'utf8');

const oldCode = `function onNavPointerDown(e) {
  // 只允许从"把手区域"开始拖动，避免影响按钮点击
  navDragging.value = true
  navPointerId = e.pointerId`;

const newCode = `function onNavPointerDown(e) {
  const target = e.target
  if (target.closest('button') || target.closest('.nav-btn')) {
    return
  }
  e.preventDefault()
  navDragging.value = true
  navPointerId = e.pointerId`;

const newContent = content.replace(oldCode, newCode);

writeFileSync('src/App.vue', newContent, 'utf8');

console.log('Fixed onNavPointerDown function');
