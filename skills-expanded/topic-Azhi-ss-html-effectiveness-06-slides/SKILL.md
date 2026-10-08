---
name: html-effectiveness-slides
description: 子 skill — 键盘控制幻灯片。当用户要"上去就能讲"的会议幻灯片、不想用 Keynote/PPT/Google Slides、希望单 HTML 文件左右键翻页时使用。当父 skill 路由命中"幻灯片/slide deck/做几张 slides/讲几页"类请求时加载。
---

# 06-slides — 键盘控制幻灯片

> "A handful of `<section>` tags and twenty lines of JS is a slide deck. Point the agent at a Slack thread or a design doc and get something you can arrow-key through in a meeting — no Keynote, no export step."

## 何时用

| 用户说 | 该走这里吗 |
|-------|-----------|
| "做几张 slides 给团队讲讲" | ✓ |
| "把这份 RFC 讲一下，slide 形式" | ✓ |
| "上台分享 5 页内容" | ✓ |
| "做一份幻灯片用键盘翻" | ✓ |
| "做一份正式 deck 给 board / 投资人" | ✗ 走专业工具 (Keynote)，HTML deck 太朴素 |
| "做一份 PDF" | ✗ 不是这个 skill 的范畴 |

---

## 标准结构（6 张以内最好）

| # | 类型 | 干什么 |
|---|------|--------|
| 1 | Title | 一句标题 + 一句副标题（讲什么、要做什么决定） |
| 2 | "Three things shipped" | 3 列等宽卡片，并行展示 |
| 3 | In progress | 工作流 + 完成度百分比 |
| 4 | Metrics | 大数字 + delta（2-4 个） |
| 5 | Decision needed | 决定的问题 + 两个 options |
| 6 | Next & closer | 下周计划 + "Questions →" |

> **3-7 张是甜区**。≤ 2 张走 markdown，≥ 8 张观众睡着。

---

## 键盘交互（必备）

| 键 | 行为 |
|----|------|
| `→` `Space` `PageDown` | 下一张 |
| `←` `PageUp` | 上一张 |
| `.` `Home` | 回到第一张 |
| `f` | 全屏切换 |

底部右下角显示 `n / total` 页码，左下角显示 keyboard hint。

---

## 关键 JS（直接复用）

```js
const slides = document.querySelectorAll('.slide');
const pager = document.querySelector('.pager');
let i = 0;

function show(n) {
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, k) => s.classList.toggle('active', k === i));
  pager.textContent = (i + 1) + ' / ' + slides.length;
}

window.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
    e.preventDefault(); show(i + 1);
  }
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
    e.preventDefault(); show(i - 1);
  }
  if (e.key === '.' || e.key === 'Home') show(0);
  if (e.key === 'f') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});
show(0);
```

---

## 关键 CSS

```css
.deck { width: 100vw; height: 100vh; overflow: hidden; }
.slide { display: none; min-height: 100vh; padding: 80px 100px;
         flex-direction: column; gap: 24px; }
.slide.active { display: flex; }

.slide h1 { font-size: 56px; font-weight: 500; line-height: 1.1;
            letter-spacing: -0.015em; max-width: 14ch; }
.slide h2 { font-size: 36px; font-weight: 500; line-height: 1.2; }
.slide p  { font-size: 22px; line-height: 1.55; color: var(--gray-700);
            max-width: 60ch; }

.pager { position: fixed; bottom: 24px; right: 32px;
         color: var(--gray-500); font-family: var(--font-mono);
         font-size: 14px; user-select: none; }
.help { position: fixed; bottom: 24px; left: 32px;
        color: var(--gray-500); font-size: 13px; }
```

---

## 直接可用模板

[`../../templates/slides.html`](../../templates/slides.html) — 6 张完整模板，含：
- Title slide
- "Three things shipped" 三栏并排
- "Carrying into next week" 进度卡
- Metrics 大数字
- Decision needed + 两个 option 卡片
- Next & closer

**修改方式**：直接打开模板，把 `[占位]` 文字换成真实内容，保持张数 ≤ 6。

---

## 共同原则

- **每张只讲一件事**——拥挤的 slide 是 LLM 写 deck 最常犯的错
- **字号至少 22px**——演示距离屏幕远，小字看不清
- **数字要大**——KPI 卡片 `font-size: 72px` 不算夸张
- **永远显示页码**——观众需要知道还剩几页
- **`f` 切全屏**——上台前按一下，移除浏览器 chrome
