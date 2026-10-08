---
name: html-effectiveness-design
description: 子 skill — 设计系统与组件展示。当用户要从 repo 提取 design tokens 做团队 reference、或要把一个组件的所有 variant 平铺在一张 contact sheet 上 review 时使用。包含设计系统参考（design-tokens.html）和组件变体陈列两种范式。当父 skill 路由命中"设计系统/design tokens/组件变体/展示组件库"类请求时加载。
---

# 03-design — 设计系统与组件

> "HTML is the medium your design system ships in, so it's the natural format for talking about it. Tokens become swatches, components become contact sheets."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "把我们的 design tokens 整理成一份 reference" | **设计系统参考** | `../../templates/design-tokens.html` |
| "review 一下我们用了哪些颜色 / 字号" | 同上 | 同上 |
| "show me all variants of Card / Button" | **组件变体陈列** | 自建（见下） |

---

## 范式 3.1 · 设计系统参考

**空间形状**：4 个区域 + 底部组件展示行。每个 token 必须**可见**：
- 颜色 → 色块 + hex + 变量名
- 字号 → 真实渲染的"Plan the week ahead"字样
- 间距 → 真实宽度的横条
- 圆角/阴影 → 真实渲染的卡片

**HTML 骨架**：

```html
<section class="tokens-color">
  <h2>Color · Primary</h2>
  <div class="palette">
    <div class="swatch" style="background:#D97757">
      <span class="hex">#D97757</span><span class="var">--clay</span>
    </div>
    <div class="swatch" style="background:#141413;color:#FAF9F5">
      <span class="hex">#141413</span><span class="var">--slate</span>
    </div>
    <!-- ivory / oat -->
  </div>
</section>

<section class="tokens-type">
  <h2>Typography</h2>
  <div class="scale">
    <div>
      <p style="font-size:48px;line-height:1.1;font-weight:500">Plan the week ahead</p>
      <small>Display 48 / 1.1 / 500</small>
    </div>
    <!-- Heading 1, Heading 2, Body, Small, Caption -->
  </div>
</section>

<section class="tokens-space">
  <h2>Spacing</h2>
  <div class="space-scale">
    <div><span class="bar" style="width:4px"></span>4 <code>--sp-1</code></div>
    <div><span class="bar" style="width:8px"></span>8 <code>--sp-2</code></div>
    <!-- 12, 16, 24, 32, 48, 64 -->
  </div>
</section>
```

**关键 CSS**：

```css
.palette { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.swatch { aspect-ratio: 1; padding: 16px; border-radius: 12px;
          color: white; display: flex; flex-direction: column;
          justify-content: flex-end; gap: 4px; font-size: 12px; }
.swatch .hex { font-family: var(--font-mono); }
.swatch .var { opacity: 0.7; }

.space-scale > div { display: flex; align-items: center; gap: 12px;
                      padding: 8px 0; }
.space-scale .bar { display: inline-block; height: 16px;
                     background: var(--clay); border-radius: 2px; }
```

**直接可用模板**：[`../../templates/design-tokens.html`](../../templates/design-tokens.html) — 含 4+4+4 配色 swatches、6 级字号 scale、8 级间距、4 级圆角、3 级阴影、核心组件展示行 + light/dark 切换。**修改方式**：把 hex 值、变量名前缀、字号 / 间距数字换成项目自己的 tokens 即可。

---

## 范式 3.2 · 组件变体陈列

**空间形状**：3×N 网格，每格一个变体。标签 A/B/C/D 在卡片左上，"best for: ..." 在底部。可加 prop slider（padding / radius / shadow）让 reviewer 实时调。

**典型变体集合**（以 Card 为例）：
- A · Flat · best for dense lists on tinted backgrounds
- B · Outlined · best for default content cards on ivory
- C · Elevated · best for draggable items, popovers
- D · Accent stripe · best for pinned or priority items
- E · Inset · best for nested cards inside white panels
- F · Horizontal · best for compact row lists, sidebars

**HTML 骨架**：

```html
<header class="bar">
  <span>Card variants</span>
  <div class="controls">
    <label>Padding <input type="range" id="pad" min="8" max="40" value="20">
      <output>20px</output></label>
    <label><input type="checkbox" id="shadow" checked> Shadow</label>
  </div>
</header>

<div class="grid">
  <figure class="variant">
    <span class="tag">A · Flat</span>
    <div class="card flat">[实际渲染的卡片]</div>
    <figcaption>best for: dense lists on tinted backgrounds</figcaption>
  </figure>
  <!-- B / C / D / E / F -->
</div>
```

**关键 JS**（slider 影响所有变体）：

```js
const padSlider = document.querySelector('#pad');
const padOut = padSlider.parentElement.querySelector('output');
padSlider.oninput = () => {
  document.documentElement.style.setProperty('--card-pad', padSlider.value + 'px');
  padOut.textContent = padSlider.value + 'px';
};
document.querySelector('#shadow').onchange = (e) => {
  document.documentElement.style.setProperty(
    '--card-shadow', e.target.checked ? 'var(--shadow-md)' : 'none'
  );
};
```

```css
.card { padding: var(--card-pad, 20px); box-shadow: var(--card-shadow, none); }
```

无独立模板。

---

## 共同原则

- **token 永远显示具体值**——不要光写 `--clay`，要同时显示 `#D97757`
- **组件变体永远 6 个左右**——多了 review 不动
- **每个 variant 必须有 "best for"** ——不光说什么样子，说什么时候用
- **slider 不是装饰**——必须真的影响渲染，而且**所有变体同时变**
