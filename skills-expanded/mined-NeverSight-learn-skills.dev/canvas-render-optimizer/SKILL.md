---
name: canvas-render-optimizer
description: "Use when Canvas渲染性能差、帧率低、绘制卡顿、需要优化Canvas性能。触发场景：canvas优化、渲染性能、帧率提升、绘制优化、requestAnimationFrame、离屏渲染、图层合并、性能调试。"
---

# Canvas 渲染优化专家

铁律：先测量，再优化。不做"感觉会更快"的改动，只做"测量证明有效"的优化。

## Inputs / Outputs / Gates / Handoffs

- **Inputs**：当前Canvas代码、性能问题现象、目标帧率
- **Outputs**：优化后的渲染代码、性能对比报告
- **Gates**：优化前后必须测量FPS，无数据不合并
- **Handoffs**：`game-test-automation` → 自动化性能测试

---

## 性能诊断清单

### 1. 测量工具

```javascript
// FPS计数器
let fps = 0, lastTime = performance.now(), frameCount = 0;
function measureFPS() {
  frameCount++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    fps = frameCount;
    frameCount = 0;
    lastTime = now;
    console.log(`FPS: ${fps}`);
  }
}

// 在主循环中调用
function loop() {
  measureFPS();
  // ... 渲染代码
  requestAnimationFrame(loop);
}
```

### 2. 常见瓶颈

| 瓶颈 | 症状 | 解决方案 |
|------|------|---------|
| 过多drawImage | GPU压力大 | 合并精灵图、减少绘制次数 |
| 频繁fillText | 文字渲染慢 | 缓存到离屏Canvas |
| 复杂路径 | stroke/fill慢 | 简化路径、分帧绘制 |
| 大量状态切换 | 上下文切换成本 | 批量绘制同类型对象 |
| 无效重绘 | 全屏重绘 | 脏矩形技术 |

---

## 优化技术

### 1. 离屏渲染（缓存）

```javascript
// 将不动的背景缓存到离屏Canvas
const offscreen = document.createElement('canvas');
const offCtx = offscreen.getContext('2d');

// 一次性绘制背景
function cacheBackground() {
  offscreen.width = canvas.width;
  offscreen.height = canvas.height;
  // 绘制复杂背景
  drawComplexBackground(offCtx);
}

// 主循环中直接复制
function render() {
  ctx.drawImage(offscreen, 0, 0); // 一次操作代替多次绘制
  // ... 绘制动态元素
}
```

### 2. 图层分离

```javascript
// 静态层：地形、墙壁（很少变化）
// 动态层：敌人、子弹（频繁变化）
// UI层：状态栏、按钮（独立更新）

const staticLayer = createLayer();   // 只在建造时重绘
const dynamicLayer = createLayer();  // 每帧重绘
const uiLayer = createLayer();       // 事件驱动重绘
```

### 3. 批量绘制

```javascript
// ❌ 差：每个敌人单独设置样式
enemies.forEach(e => {
  ctx.fillStyle = e.color;
  ctx.beginPath();
  ctx.arc(e.x, e.y, e.r, 0, Math.PI * 2);
  ctx.fill();
});

// ✅ 好：按颜色分组批量绘制
const byColor = groupBy(enemies, 'color');
for (const [color, list] of Object.entries(byColor)) {
  ctx.fillStyle = color;
  ctx.beginPath();
  list.forEach(e => ctx.moveTo(e.x + e.r, e.y) || ctx.arc(e.x, e.y, e.r, 0, Math.PI * 2));
  ctx.fill();
}
```

### 4. 脏矩形

```javascript
// 只重绘发生变化的区域
const dirtyRects = [];

function markDirty(x, y, w, h) {
  dirtyRects.push({x, y, w, h});
}

function renderDirty() {
  dirtyRects.forEach(r => {
    ctx.save();
    ctx.beginPath();
    ctx.rect(r.x, r.y, r.w, r.h);
    ctx.clip();
    // 重绘该区域
    redrawRegion(r);
    ctx.restore();
  });
  dirtyRects.length = 0;
}
```

### 5. 对象池

```javascript
// 避免频繁创建/销毁对象
const bulletPool = [];
const MAX_BULLETS = 100;

function getBullet() {
  return bulletPool.pop() || {x:0, y:0, vx:0, vy:0, active:false};
}

function recycleBullet(b) {
  b.active = false;
  bulletPool.push(b);
}
```

---

## 工作流

- [ ] **第一步：测量基准**
  ```javascript
  console.time('render');
  render();
  console.timeEnd('render');
  ```
  - [ ] 记录初始FPS
  - [ ] 找出最慢的函数

- [ ] **第二步：识别瓶颈**
  - [ ] 使用Chrome DevTools Performance
  - [ ] 检查是否有超过16ms的帧

- [ ] **第三步：应用优化**
  - 按优先级：离屏渲染 > 批量绘制 > 对象池 > 脏矩形

- [ ] **第四步：验证效果**
  - 用户确认门控：**展示优化前后FPS对比，FPS未提升则回滚**

---

## 性能目标

| 场景 | 目标FPS | 可接受 |
|------|---------|--------|
| 少量单位(<50) | 60 | 55+ |
| 中量单位(50-100) | 60 | 45+ |
| 大量单位(100-200) | 45 | 30+ |
| 极限压力(200+) | 30 | 20+ |

---

## 反模式警告

| 反模式 | 问题 | 修复 |
|--------|------|------|
| 每帧new对象 | GC压力大 | 对象池 |
| 每帧设置字体 | 状态切换成本 | 缓存测量结果 |
| 高频调用measureText | 性能杀手 | 预计算文字宽度 |
| 过大的Canvas | 内存/带宽压力 | 分层或缩小 |
| 频繁getImageData | 同步读取阻塞GPU | 避免或用OffscreenCanvas |

---

## 参考资源

- `references/canvas-perf-checklist.md` — 完整性能检查清单
- `references/webgl-migration.md` — WebGL迁移指南（终极优化）
