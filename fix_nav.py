import sys

with open('src/App.vue', 'r', encoding='utf-8-sig', errors='ignore') as f:
    content = f.read()

old_code = '''function onNavPointerDown(e) {
  // 只允许从"把手区域"开始拖动，避免影响按钮点击
  navDragging.value = true
  navPointerId = e.pointerId'''

new_code = '''function onNavPointerDown(e) {
  const target = e.target
  if (target.closest('button') || target.closest('.nav-btn')) {
    return
  }
  e.preventDefault()
  navDragging.value = true
  navPointerId = e.pointerId'''

content = content.replace(old_code, new_code)

with open('src/App.vue', 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Fixed onNavPointerDown function")
