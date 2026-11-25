---
name: super-dev-seeai
description: Activate the Super Dev SEEAI competition mode inside Codex CLI.
when_to_use: Use when the user says /super-dev-seeai, super-dev-seeai:, or super-dev-seeai： followed by a requirement. Activate the fast competition delivery mode.
version: 2.4.0
---
# Super Dev SEEAI - 赛事极速版 (Codex)

## 关键约束提醒（每次操作前必读）

以下规则在整个开发过程中始终有效，不得以任何理由违反：

1. **图标系统**: 功能图标只能来自 Lucide / Heroicons / Tabler 图标库。绝对禁止使用 emoji 表情 作为功能图标、装饰图标或临时占位。如果你发现自己即将输出包含 emoji 的 UI 代码，停下来，改用图标库组件。

2. **AI 模板化禁令**: 禁止紫/粉渐变主色调、禁止 emoji 图标、禁止无信息层级的卡片墙、禁止默认系统字体直出。

3. **代码即交付**: 不允许“先用 emoji 顶上后面再换”。图标库必须在第一行 UI 代码前就锁定。

4. **自检规则**: 在向用户展示任何 UI 代码或预览前，必须自检源码中不存在任何 emoji 字符（Unicode range U+2600-U+27BF, U+1F300-U+1FAFF）。发现后先替换为正式图标库再继续。

## Direct Activation Rule（强制）

- If this skill is invoked, Super Dev SEEAI competition mode is already active.
- Do not spend a turn explaining the skill or deciding whether to enter the workflow.
- Treat this as a distinct fast-delivery contract optimized for time-boxed competition work.
- Keep quality, but compress the path aggressively after Spec.


## 触发方式（强制）

- Treat `super-dev-seeai: <需求描述>` and `super-dev-seeai：<需求描述>` as the AGENTS-driven natural-language SEEAI entry.
- Treat `$super-dev-seeai` as the explicit Codex CLI Skill entry for the competition mode.
- In Codex App/Desktop, selecting `/super-dev-seeai` from the slash Skill list is the official app entry.
- Do not route SEEAI requests back to ordinary chat or to the full standard Super Dev contract.


## Runtime Contract（强制）

- Super Dev SEEAI is still Super Dev governance, but with a competition-fast contract.
- The host remains responsible for model execution, tools, search, terminal, and edits.
- Use Codex native web/search/edit/terminal capabilities for research, building, and validation.
- Keep local `super-dev` CLI for governance artifacts only when it materially helps the fast path.
- The mode is designed for 30-minute showcase builds such as a polished landing page, mini-game, or focused demo tool.
- Default decision rule: protect one demo path first, one wow point second, and only then add extra engineering depth.


## 首轮响应契约（强制）

- 首次触发时第一轮回复必须说明：Super Dev SEEAI 赛事模式已激活，当前阶段是 `research`。
- 先快速理解需求，再做极短顺位思考：作品类型、评委 wow 点、必须完成项、主动放弃项。
- 如果用户需求模糊，最多只补 1 个关键问题；能合理假设时直接给出假设并推进，不展开长澄清。
- 先完成 fast research，再写 compact research / PRD / architecture / UIUX。
- 文档确认后创建 compact Spec，然后直接进入 full-stack sprint。
- 不要在 SEEAI 模式里重新切回标准 Super Dev 的 preview confirm / 长质量闭环。
- 若会落盘 workflow state，必须把 `flow_variant = seeai` 一起写入。


## 首轮输出模板（强制）

SEEAI 首轮回复不要展开成长讨论。优先用极短结构锁定范围，然后立即进入 research：

- `作品类型`：官网类 / 小游戏类 / 工具类，三选一。
- `评委 wow 点`：本次成品最值得被记住的一个亮点。
- `P0 主路径`：半小时内必须真正跑通的一条演示路径。
- `主动放弃项`：本轮明确不做的部分，避免范围失控。
- `关键假设`：只有在用户没说清时才写，最多 1 到 2 条。

如果需求不缺关键信息，就不要反问。直接按这个模板给出判断，然后开始 fast research 和 compact 文档。

## 比赛短文档模板（强制）

SEEAI 的文档必须真实落盘到 `output/*`，但只保留比赛需要的信息：

- `research.md`：题目理解、目标观众、参考风格、评委 wow 点、风险与主动放弃项。
- `prd.md`：作品目标、P0 主路径、P1 wow 点、P2 可选项、非目标。
- `architecture.md`：页面/玩法主循环、技术栈、数据流、是否需要最小后端、降级方案。
- `uiux.md`：视觉关键词、主 KV、页面骨架、关键交互、动效重点、设计 token。
- `spec`：只保留一个 sprint 清单，按 `P0 -> P1 -> polish` 排序。

### 推荐标题骨架
- `research.md`：`# 题目理解` `# 参考风格` `# Wow 点` `# 主动放弃项`
- `prd.md`：`# 作品目标` `# P0 主路径` `# P1 Wow 点` `# P2 可选项` `# 非目标`
- `architecture.md`：`# 主循环` `# 技术栈` `# 数据流` `# 最小后端` `# 降级方案`
- `uiux.md`：`# 视觉方向` `# 首屏/主界面` `# 关键交互` `# 动效重点` `# 设计 Token`
- `spec`：`# Sprint Checklist` 下只列 `P0`、`P1`、`Polish`

不要把文档写成长方案、长竞品分析或完整工程规划。文档存在的目的，是帮你更快做出更像成品的作品。

## 技术栈快速决策矩阵（核心）

收到题目后，根据作品类型**立刻**选择技术栈。不纠结，不混搭。

### 决策树

```
题目类型？
|-- 小游戏 / 互动动画
|   |-- 纯2D休闲 -> HTML Canvas + Vanilla JS（零依赖，开箱即用）
|   |-- 复杂2D游戏 -> Phaser.js（场景管理、物理引擎、精灵动画一体化）
|   `-- 3D/沉浸感 -> Three.js + React Three Fiber（如果用React）
|
|-- 官网 / 展示页 / 落地页
|   |-- 纯静态展示 -> HTML + Tailwind CDN + GSAP/Framer Motion
|   |-- 需要路由/多页 -> React + Vite + Tailwind + Framer Motion
|   `-- 需要SSR/SEO -> Next.js + Tailwind + Framer Motion
|
|-- 工具 / 应用
|   |-- 纯前端工具 -> React + Vite + Tailwind + Zustand
|   |-- 需要后端API -> React前端 + Express/Fastify后端
|   `-- 实时协作 -> React + Socket.io / WebSocket
|
`-- 数据看板 / 可视化
    |-- 简单图表 -> React + Recharts / Chart.js
    |-- 复杂交互 -> React + D3.js
    `-- 实时数据 -> React + ECharts + WebSocket
```

### 赛事推荐组合（已验证能30分钟内交付）

| 组合 | 适用场景 | CDN快速启动 | 需要构建 |
|------|---------|------------|---------|
| **HTML+Tailwind CDN+GSAP** | 展示页/官网 | 是 | 否 |
| **React+Vite+Tailwind+Framer** | 工具/应用/多页 | 否 | 是 |
| **HTML Canvas+Vanilla JS** | 2D小游戏/互动 | 是 | 否 |
| **Phaser.js** | 复杂2D游戏 | 是 | 否 |
| **Three.js** | 3D展示/沉浸 | 是 | 否 |

**赛事铁律**: 能用 CDN 零构建的优先用 CDN，省掉构建和配置时间。


## 小游戏开发模板库（核心）

### 模板1: HTML Canvas 游戏骨架
适用于所有 2D 休闲游戏（贪吃蛇、打砖块、弹球、飞机大战等）。
骨架包含：Canvas 初始化、游戏主循环、HUD、菜单/结束 Overlay、localStorage 最高分。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GAME_TITLE</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0a0a0a; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: 'Inter', sans-serif; }
    #gameContainer { position: relative; }
    canvas { display: block; border-radius: 12px; box-shadow: 0 0 40px rgba(59,130,246,0.3); }
    #hud { position: absolute; top: 0; left: 0; right: 0; padding: 16px 24px; display: flex; justify-content: space-between; color: #fff; font-size: 14px; font-weight: 600; pointer-events: none; z-index: 10; }
    #overlay { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.8); border-radius: 12px; z-index: 20; transition: opacity 0.3s; }
    #overlay.hidden { opacity: 0; pointer-events: none; }
    #overlay h1 { color: #fff; font-size: 36px; margin-bottom: 8px; }
    #overlay p { color: #94a3b8; margin-bottom: 24px; }
    #overlay button { padding: 12px 32px; border: none; border-radius: 8px; background: #3b82f6; color: #fff; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.15s, background 0.15s; }
    #overlay button:hover { transform: scale(1.05); background: #2563eb; }
    .score-display { background: rgba(255,255,255,0.1); padding: 6px 16px; border-radius: 20px; backdrop-filter: blur(8px); }
  </style>
</head>
<body>
  <div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
    <div id="hud">
      <div class="score-display">Score: <span id="score">0</span></div>
      <div class="score-display">Level: <span id="level">1</span></div>
      <div class="score-display">Best: <span id="best">0</span></div>
    </div>
    <div id="overlay">
      <h1>GAME_TITLE</h1>
      <p>游戏描述</p>
      <button id="startBtn">Start Game</button>
    </div>
  </div>
  <script>
    const CONFIG = { width: 800, height: 600, bgColor: '#0a0a0a', accentColor: '#3b82f6', fps: 60 };
    const STATE = { MENU: 0, PLAYING: 1, PAUSED: 2, OVER: 3 };
    let gameState = STATE.MENU, score = 0, level = 1;
    let bestScore = parseInt(localStorage.getItem('game_best') || '0');
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = CONFIG.width; canvas.height = CONFIG.height;
    const keys = {};
    document.addEventListener('keydown', e => { keys[e.key] = true; e.preventDefault(); });
    document.addEventListener('keyup', e => { keys[e.key] = false; });
    let lastTime = 0;
    function gameLoop(timestamp) {
      const dt = (timestamp - lastTime) / 1000; lastTime = timestamp;
      ctx.fillStyle = CONFIG.bgColor;
      ctx.fillRect(0, 0, CONFIG.width, CONFIG.height);
      if (gameState === STATE.PLAYING) { update(dt); draw(); }
      requestAnimationFrame(gameLoop);
    }
    function update(dt) { /* game logic */ }
    function draw() { /* render */ }
    function addScore(pts) {
      score += pts;
      document.getElementById('score').textContent = score;
      if (score > bestScore) {
        bestScore = score; localStorage.setItem('game_best', bestScore);
        document.getElementById('best').textContent = bestScore;
      }
    }
    function startGame() {
      score = 0; level = 1; gameState = STATE.PLAYING;
      document.getElementById('overlay').classList.add('hidden');
    }
    function gameOver() {
      gameState = STATE.OVER;
      const o = document.getElementById('overlay');
      o.classList.remove('hidden');
      o.querySelector('h1').textContent = 'Game Over';
      o.querySelector('p').textContent = 'Final Score: ' + score;
      o.querySelector('button').textContent = 'Play Again';
    }
    document.getElementById('startBtn').addEventListener('click', startGame);
    document.getElementById('best').textContent = bestScore;
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
```

### 模板2: 碰撞检测工具箱

```javascript
// 矩形碰撞
function rectCollision(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}
// 圆形碰撞
function circleCollision(a, b) {
  const dx = a.x - b.x, dy = a.y - b.y;
  return dx*dx + dy*dy < (a.r + b.r) * (a.r + b.r);
}
// 粒子效果
class Particle {
  constructor(x, y, color) {
    this.x=x; this.y=y; this.vx=(Math.random()-0.5)*8; this.vy=(Math.random()-0.5)*8;
    this.life=1; this.decay=0.02+Math.random()*0.03; this.size=2+Math.random()*4; this.color=color;
  }
  update() { this.x+=this.vx; this.y+=this.vy; this.life-=this.decay; this.vy+=0.1; }
  draw(ctx) {
    ctx.globalAlpha=this.life; ctx.fillStyle=this.color;
    ctx.fillRect(this.x-this.size/2, this.y-this.size/2, this.size, this.size);
    ctx.globalAlpha=1;
  }
  get dead() { return this.life <= 0; }
}
```

### 模板3: 常见游戏模式速查

| 游戏类型 | 核心循环 | 关键对象 | 反馈重点 |
|---------|---------|---------|---------|
| 贪吃蛇 | 移动->吃食->变长->碰撞检测 | 蛇身数组、食物坐标 | 吃到食物闪烁、蛇身渐变色 |
| 打砖块 | 发球->挡板->砖块碰撞 | 挡板、球、砖块网格 | 砖块破碎粒子、连击特效 |
| 飞机大战 | 移动->射击->躲避->Boss | 玩家飞机、敌机数组、子弹数组 | 爆炸粒子、屏幕震动 |
| 消除游戏 | 选择->匹配->消除->下落 | 网格数组、选中状态、动画队列 | 消除爆炸、连锁得分飞字 |
| 跑酷 | 跳跃->障碍->加速->距离 | 角色、障碍物队列、地面 | 跳跃拉伸、落地压缩、速度线 |

### 模板4: 游戏HUD/UI组件

```javascript
// 屏幕震动
function screenShake(intensity=5, duration=200) {
  const c = document.getElementById('gameContainer');
  const start = Date.now();
  function shake() {
    const elapsed = Date.now() - start;
    if (elapsed < duration) {
      const f = 1 - elapsed/duration;
      c.style.transform = `translate(${(Math.random()-0.5)*intensity*f}px,${(Math.random()-0.5)*intensity*f}px)`;
      requestAnimationFrame(shake);
    } else { c.style.transform = ''; }
  }
  shake();
}
// 得分飞字
function floatingText(x, y, text, color='#fbbf24') {
  const el = document.createElement('div');
  el.textContent = text;
  Object.assign(el.style, { position:'absolute', left:x+'px', top:y+'px', color, fontSize:'20px', fontWeight:'bold', pointerEvents:'none', transition:'all 0.8s ease-out', zIndex:'30' });
  document.getElementById('gameContainer').appendChild(el);
  requestAnimationFrame(() => { el.style.top=(y-60)+'px'; el.style.opacity='0'; });
  setTimeout(() => el.remove(), 800);
}
```

### 游戏开发铁律
- 核心玩法循环必须完整：开始->游玩->结束->再来一次
- 反馈感 > 真实物理：夸张的视觉反馈比物理精确更重要
- 操作延迟 < 50ms：任何卡顿都会毁掉游戏体验
- 分数/进度必须实时可见


## 精美页面模板库（核心）

### 设计Token预设（6套赛事验证主题）

#### 主题A: 暗夜科技（适合科技/AI/数据类）
```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #111827;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --accent: #3b82f6;
  --accent-glow: rgba(59,130,246,0.4);
  --gradient-hero: linear-gradient(135deg, #0a0a0f 0%, #1e1b4b 50%, #0a0a0f 100%);
  --card-bg: rgba(17,24,39,0.8);
  --card-border: rgba(59,130,246,0.15);
}
```

#### 主题B: 日出暖橙（适合教育/社交/正能量）
```css
:root {
  --bg-primary: #fffbf5; --bg-secondary: #fef3e2;
  --text-primary: #1c1917; --text-secondary: #78716c;
  --accent: #f97316; --accent-glow: rgba(249,115,22,0.3);
  --gradient-hero: linear-gradient(135deg, #fffbf5 0%, #fed7aa 100%);
  --card-bg: rgba(255,251,245,0.9); --card-border: rgba(249,115,22,0.15);
}
```

#### 主题C: 翡翠绿意（适合环保/健康/生活）
```css
:root {
  --bg-primary: #f0fdf4; --bg-secondary: #dcfce7;
  --text-primary: #14532d; --text-secondary: #4d7c0f;
  --accent: #16a34a; --accent-glow: rgba(22,163,74,0.3);
  --gradient-hero: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
  --card-bg: rgba(240,253,244,0.9); --card-border: rgba(22,163,74,0.15);
}
```

#### 主题D: 极简黑白（适合工具/效率/专业）
```css
:root {
  --bg-primary: #fafafa; --bg-secondary: #f4f4f5;
  --text-primary: #18181b; --text-secondary: #71717a;
  --accent: #18181b; --accent-glow: rgba(24,24,27,0.1);
  --gradient-hero: linear-gradient(180deg, #fafafa 0%, #e4e4e7 100%);
  --card-bg: #ffffff; --card-border: rgba(24,24,27,0.08);
}
```

#### 主题E: 深海蓝绿（适合海洋/探索/游戏）
```css
:root {
  --bg-primary: #042f2e; --bg-secondary: #134e4a;
  --text-primary: #ccfbf1; --text-secondary: #5eead4;
  --accent: #14b8a6; --accent-glow: rgba(20,184,166,0.4);
  --gradient-hero: linear-gradient(135deg, #042f2e 0%, #0f766e 50%, #042f2e 100%);
  --card-bg: rgba(19,78,74,0.6); --card-border: rgba(20,184,166,0.2);
}
```

#### 主题F: 赛博朋克（适合潮流/音乐/创意）
```css
:root {
  --bg-primary: #0c0015; --bg-secondary: #1a002e;
  --text-primary: #f0e6ff; --text-secondary: #c084fc;
  --accent: #e879f9; --accent-secondary: #06ffa5;
  --accent-glow: rgba(232,121,249,0.4);
  --gradient-hero: linear-gradient(135deg, #0c0015 0%, #2d1b69 50%, #0c0015 100%);
  --card-bg: rgba(26,0,46,0.8); --card-border: rgba(232,121,249,0.2);
}
```

**禁止使用**: 紫粉渐变、默认蓝色模板感配色。

### 动效预设工具箱

```javascript
// 1. 滚动渐入（Intersection Observer）
function setupScrollReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('revealed'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}
// CSS: .reveal { opacity:0; transform:translateY(30px); transition:all 0.6s cubic-bezier(0.16,1,0.3,1); }
// .reveal.revealed { opacity:1; transform:translateY(0); }

// 2. 数字滚动动画
function animateNumber(el, target, duration=1500) {
  const start = parseInt(el.textContent)||0; const t0 = performance.now();
  function update(now) {
    const p = Math.min((now-t0)/duration, 1);
    const eased = 1 - Math.pow(1-p, 3);
    el.textContent = Math.round(start + (target-start)*eased).toLocaleString();
    if(p<1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// 3. 鼠标跟随光晕
function setupCursorGlow(container) {
  const glow = document.createElement('div');
  Object.assign(glow.style, { position:'absolute', width:'400px', height:'400px',
    borderRadius:'50%', pointerEvents:'none',
    background:'radial-gradient(circle, var(--accent-glow) 0%, transparent 70%)',
    transform:'translate(-50%,-50%)', zIndex:'0', opacity:'0.6' });
  container.style.position = 'relative';
  container.appendChild(glow);
  container.addEventListener('mousemove', e => {
    const r = container.getBoundingClientRect();
    glow.style.left = (e.clientX-r.left)+'px';
    glow.style.top = (e.clientY-r.top)+'px';
  });
}

// 4. 打字机效果
function typeWriter(el, text, speed=60) {
  let i = 0; el.textContent = '';
  function type() { if(i<text.length) { el.textContent += text.charAt(i++); setTimeout(type, speed); } }
  type();
}

// 5. 卡片3D倾斜
function setupTiltCard(card, intensity=15) {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX-r.left)/r.width - 0.5;
    const y = (e.clientY-r.top)/r.height - 0.5;
    card.style.transform = `perspective(800px) rotateY(${x*intensity}deg) rotateX(${-y*intensity}deg) scale(1.02)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
}
```

### Hero区域模板（3种高转化布局）

#### Hero A: 大标题+CTA+背景动画（通用）
```html
<section style="min-height:100vh;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;background:var(--bg-primary)">
  <div style="position:absolute;inset:0;opacity:0.5;background:var(--gradient-hero)"></div>
  <div style="position:relative;z-index:10;text-align:center;max-width:800px;padding:0 24px">
    <div style="display:inline-block;padding:6px 16px;border-radius:20px;background:var(--accent);color:#fff;font-size:13px;font-weight:600;margin-bottom:24px">Tagline</div>
    <h1 style="font-size:clamp(36px,6vw,72px);font-weight:800;color:var(--text-primary);line-height:1.1;margin-bottom:16px">主标题 <span style="color:var(--accent)">关键词高亮</span></h1>
    <p style="font-size:18px;color:var(--text-secondary);margin-bottom:32px;max-width:600px;margin-left:auto;margin-right:auto">副标题</p>
    <div style="display:flex;gap:12px;justify-content:center">
      <a href="#cta" style="padding:14px 32px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600">Primary CTA</a>
    </div>
  </div>
</section>
```

#### Hero B: 左文右图（产品/工具类）
```html
<section style="min-height:100vh;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:48px;padding:80px 48px;background:var(--bg-primary)">
  <div>
    <h1 style="font-size:48px;font-weight:800;color:var(--text-primary)">标题</h1>
    <p style="font-size:18px;color:var(--text-secondary);margin-bottom:24px">描述</p>
    <button style="padding:12px 28px;border-radius:8px;background:var(--accent);color:#fff;border:none;font-weight:600;cursor:pointer">Get Started</button>
  </div>
  <div style="aspect-ratio:4/3;border-radius:16px;background:var(--card-bg);border:1px solid var(--card-border)"></div>
</section>
```

#### Hero C: 全屏动态背景+居中标题（展示类）
```html
<section style="height:100vh;display:flex;align-items:center;justify-content:center;position:relative">
  <div style="position:absolute;inset:0;background:var(--gradient-hero);z-index:1"></div>
  <div style="position:relative;z-index:10;text-align:center;color:#fff">
    <h1 style="font-size:clamp(40px,8vw,80px);font-weight:900;text-shadow:0 2px 20px rgba(0,0,0,0.3)">主标题</h1>
    <p style="font-size:20px;max-width:600px;margin:16px auto 0;opacity:0.85">副标题</p>
  </div>
</section>
```

### 页面开发铁律
- 首屏3秒内传达核心价值，不允许普通模板感
- 至少一个让人记住的动效瞬间（鼠标跟随/数字滚动/粒子背景）
- 所有颜色使用 CSS 变量，不硬编码 hex
- 移动端至少可用，桌面端完美


## 赛事文档模板库（核心）

比赛不只看代码，**文档和演示决定最终名次**。以下模板在 Spec 确认后立即生成。

### 模板1: 参赛项目 README

```markdown
# PROJECT_NAME

> 一句话描述项目核心价值（评委3秒内能理解）

## 项目亮点
- 亮点1（技术实现/设计/创新）
- 亮点2
- 亮点3

## 技术栈

| 层级 | 技术 | 选型理由 |
|------|------|----------|
| 前端 | XXX | 快速/美观/生态 |
| 后端 | XXX（如无则写"纯前端"） | 必要性 |
| 数据 | XXX | 轻量/够用 |
| 部署 | XXX | 一键/零配置 |

## 快速开始
```bash
npm install && npm run dev
```

## 功能演示路径
1. 打开首页 -> 看到XXX
2. 点击XXX -> 触发XXX
3. 完成XXX -> 看到结果
```

### 模板2: 技术亮点文档

```markdown
## 1. 创新点：XXX
**问题**: 为什么要做这个
**方案**: 具体怎么实现的
**效果**: 数据/截图/对比

## 2. 技术难点突破：XXX
**挑战**: 遇到什么问题
**解决**: 怎么解决的
**收获**: 学到了什么
```

### 模板3: 演示脚本（30秒版 + 2分钟版）

```markdown
## 30秒电梯演讲
大家好，我们是TEAM_NAME。我们做了PROJECT_NAME。
它解决的核心问题是【痛点】。我们的方案是【一句话方案】。
最大的亮点是【wow点】。谢谢！

## 2分钟完整演示
### 开场（15秒）：我们注意到一个问题... 切到首页展示痛点场景
### 核心演示（60秒）：按功能顺序走一条完整主路径
### 亮点展示（30秒）：展示技术亮点/创新设计
### 总结（15秒）：一句话总结核心价值 + 未来展望

## 演示注意
- 准备备用演示路径（主路径出问题时的Plan B）
- 数据预填充，不要现场输入
- 不依赖网络，本地运行
```

### 模板4: 答辩准备卡

```markdown
## 必答题
1. 技术方案为什么这样选？ -> 性能/生态/时间权衡
2. 再给一周时间优先做什么？ -> 核心体验/用户反馈
3. 最大的技术挑战？ -> 具体问题+解决方案
4. 和竞品相比核心差异？ -> 创新点+用户价值
5. 用户体验有什么特别设计？ -> 细节+数据支撑

## 加分回答（主动提及）
- 我们不只做了功能，还关注了XXX细节
- 我们在有限时间内做了降级方案确保演示稳定

## 减分避免
- 不要说"时间不够所以没做完"
- 不要说"这个功能比较简单"
- 不要说"AI帮我们写的"（改说"我们利用AI辅助提升了开发效率"）
```

### 赛事文档铁律
- 文档必须落盘到 output/* 和项目根目录 README.md
- 技术亮点不能空泛，必须有具体的方案描述
- 演示脚本必须提前演练一遍，确保路径完整无断点
- 答辩回答不要说"时间不够"或"AI写的"


## 作品类型决策模板

进入 SEEAI 后，优先先判断当前更像哪一类题，再决定研究和实现重心：

- 官网类：优先主视觉、品牌故事、信息层级、首屏转化、滚动节奏与演示动效。
  默认技术栈：React/Vite 或 Next.js + Tailwind + Framer Motion。
  默认 sprint：先做 Hero 与主叙事，再做亮点区和 CTA，最后统一动效与滚动节奏。
- 小游戏类：优先核心玩法循环、反馈感、记分/胜负、开始到再次游玩的完整闭环。
  默认技术栈：HTML Canvas + Vanilla JS；更复杂时再上 Phaser。
  默认 sprint：先做可玩的主循环，再补积分/胜负反馈，最后加音效、特效和复玩钩子。
- 工具类：优先一个高价值主流程、输入输出清晰、演示结果直观、无需复杂配置。
  默认技术栈：React + Vite + Tailwind + 本地状态；必要时补最小 Express/Fastify 后端。
  默认 sprint：先打通输入到结果的主流程，再补结果页质感，最后加分享/导出等演示加分项。

如果需求跨多类，默认选最容易形成强演示效果的那一类做主轴，其余只做辅助。

## 题型识别提示

在首轮判断时，优先用需求关键词快速归类，不要犹豫太久：

- 如果需求强调品牌、产品发布、活动宣传、首屏、官网、落地页，默认按官网类处理。
- 如果需求强调玩法、得分、胜负、闯关、点击反馈、复玩，默认按小游戏类处理。
- 如果需求强调生成、分析、查询、表单、输入输出、结果页、效率提升，默认按工具类处理。
- 如果用户同时提到官网 + 交互玩法，先判断评审更容易记住哪一面，把那一面作为主轴。


## 比赛质量底线

即使在半小时里，也必须守住这些底线：

- 首屏或第一轮交互必须让人一眼看懂主题，不允许普通模板感。
- 至少有一个清晰 wow 点：视觉、玩法、结果页、数据动效、讲解桥段任选其一。
- 主路径必须真实可演示，不能全是占位按钮或空数据。
- 文案不能是通用 AI 空话，标题、卖点、CTA、结果文案要贴题。
- 时间不够时，优先删功能，不要删完成度。


## 赛事专用能力

### 评委视角优化
- 每个作品必须有一个2分钟能讲完的完整演示故事线
- 标题/首屏/Hero区域在3秒内传达核心价值
- 结果页/完成页让评委有完成感，而不是半成品感
- 动效不在于多，在于有1-2个让人记住的瞬间

### 降级策略
- 后端来不及 -> 用 localStorage / mock API，但要标注demo数据
- 多页面来不及 -> 做好单页的完整体验，胜过5个半成品页面
- 复杂交互来不及 -> 简化流程，但保留核心闭环
- 响应式来不及 -> 保证桌面端完美，移动端可用

### 演示准备
- 准备一段30秒的口头介绍：这是什么 + 给谁用 + 核心价值 + wow点
- 准备一条完整的主流程演示路径（从开始到结束无断点）
- 准备一个备选路径（如果主路径出了问题）
- 确保首屏截图就能当宣传图用


## Required behavior

1. First reply: say Super Dev SEEAI mode is active and the current phase is `research`.
2. Use a strict timebox: 0-4 min research, 4-8 min compact docs, 8-10 min confirmation, 10-12 min compact Spec, 12-27 min build sprint, 27-30 min polish/handoff.
3. Run a fast research pass and write `output/*-research.md` as a real file.
4. Draft compact `output/*-prd.md`, `output/*-architecture.md`, and `output/*-uiux.md` in the same session and save them as real files.
5. Scope the work in P0/P1/P2 order: P0 demo path, P1 wow point, P2 only-if-time-allows extras.
6. Stop after the three compact core documents and wait for explicit confirmation.
7. Only after confirmation, create a compact Spec / tasks breakdown.
8. After Spec, move directly into an integrated full-stack build sprint: frontend first, backend if needed, then final polish.
9. If backend or integration work threatens the schedule, degrade to mock data, local state, or a simulated high-fidelity demo path instead of missing the showcase.
10. Do not require a separate preview confirmation gate in SEEAI mode.
11. End with a concise demo summary, key亮点, and how to present the result quickly.
12. When writing or refreshing `.super-dev/workflow-state.json`, persist `flow_variant = seeai` so resume/continue stays in SEEAI mode.


## 会话连续性契约（强制）

- 若存在 `.super-dev/SESSION_BRIEF.md`，每次继续前必须先读取。
- 用户在 SEEAI 模式里说"改一下 / 再炫一点 / 补个功能 / 继续做"等，属于当前比赛流程内动作。
- 文档确认前，任何修改都先落在 compact research / PRD / architecture / UIUX 上。
- Spec 之后，任何修改默认回到当前 full-stack sprint，不额外拆出新的长门禁。


## 实现闭环契约（强制）

- 每轮修改后先做最小 diff review 再汇报完成。
- 运行 build / type-check / test / runtime smoke。
- 新增代码必须接入真实调用链；未接入则删除，禁止留 unused code。
- 新增日志/告警/埋点必须验证会在真实路径触发。

## Never do this

- Never skip research, the three compact core documents, or Spec entirely.
- Never expand SEEAI mode back into the full standard Super Dev long chain unless the user explicitly asks to switch modes.
- Never stop after frontend to wait for a separate preview gate in SEEAI mode.
- Never sacrifice baseline polish and demoability just to move fast.


## Super Dev SEEAI Flow Contract

- SUPER_DEV_SEEAI_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>build_fullstack>polish>handoff
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: omitted
- QUALITY_STYLE: speed_with_showcase_quality
