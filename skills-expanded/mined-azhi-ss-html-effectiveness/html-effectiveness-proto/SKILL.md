---
name: html-effectiveness-proto
description: 子 skill — 原型与可点击流。当用户要决定一个 transition 的 duration/easing（动画沙盒，animation.html）或要"走一遍"4-6 屏交互流验证手感时使用。包含动画沙盒和可点击流两种范式。当父 skill 路由命中"动画/原型/手感/clickable flow"类请求时加载。
---

# 04-proto — 原型

> "Motion and interaction can't be described, only felt. A throwaway page with the real easing curve or the real click-through tells you in five seconds what a paragraph of prose never could."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "试一下这个 transition / easing / 时长合适吗" | **动画沙盒** | `../../templates/animation.html` |
| "spring vs cubic-bezier 哪个手感对" | 同上 | 同上 |
| "想感受一下这个 flow / 4 屏的 onboarding" | **可点击流** | 自建（见下） |

---

## 范式 4.1 · 动画沙盒

**空间形状**：动画在中央 + 滑块控制 duration / easing + Play 按钮。用户调到对了为止。

**HTML 骨架**：

```html
<div class="stage">
  <div class="ball"></div>
</div>
<div class="controls">
  <label>Duration
    <input type="range" id="dur" min="100" max="2000" value="600" step="50">
    <output>600ms</output>
  </label>
  <label>Easing
    <select id="ease">
      <option>cubic-bezier(.4, 0, .2, 1)</option>
      <option>cubic-bezier(.34, 1.56, .64, 1)</option>
      <option>cubic-bezier(.68, -0.55, .27, 1.55)</option>
      <option>linear</option>
      <option>ease-in-out</option>
    </select>
  </label>
  <button id="play" class="btn primary">Play</button>
  <button id="copy" class="btn ghost">Copy CSS</button>
</div>
```

**关键 JS**：

```js
const ball = document.querySelector('.ball');
const dur = document.querySelector('#dur');
const ease = document.querySelector('#ease');
const out = dur.parentElement.querySelector('output');

dur.oninput = () => { out.textContent = dur.value + 'ms'; };

document.querySelector('#play').onclick = () => {
  ball.style.transition = `transform ${dur.value}ms ${ease.value}`;
  const at = ball.style.transform === 'translateX(400px)' ? '0' : '400px';
  ball.style.transform = `translateX(${at})`;
};

document.querySelector('#copy').onclick = async (e) => {
  await navigator.clipboard.writeText(`transition: transform ${dur.value}ms ${ease.value};`);
  e.target.textContent = 'Copied ✓';
  setTimeout(() => e.target.textContent = 'Copy CSS', 1500);
};
```

```css
.stage { position: relative; height: 120px; padding: 40px;
         background: var(--gray-100); border-radius: var(--r-md);
         margin-bottom: var(--sp-5); }
.ball { width: 40px; height: 40px; border-radius: 50%;
        background: var(--clay); }
```

**导出闭环**：永远带 "Copy CSS" 按钮，让用户调好后**直接拿走**最终的 transition 字符串。

**直接可用模板**：[`../../templates/animation.html`](../../templates/animation.html) — 含 duration / distance slider、8 种常用 easing 下拉、loop 模式、5 个一键 preset（Material / iOS spring / Snappy / Bouncy / Gentle）、live CSS 输出、Copy CSS 按钮。

---

## 范式 4.2 · 可点击流

**空间形状**：4-6 屏的关键路径，每屏一个 `<section>`，按钮跳到下一屏。**用 `:target` 而不是 JS** 路由——更简洁。

**HTML 骨架**：

```html
<section id="screen-1" class="screen">
  <h1>Welcome to Acme</h1>
  <p>Get organized in three steps.</p>
  <a href="#screen-2" class="btn primary">Get started →</a>
</section>

<section id="screen-2" class="screen">
  <h1>Create your first project</h1>
  <input placeholder="Project name" />
  <a href="#screen-3" class="btn primary">Continue →</a>
  <a href="#screen-1" class="btn ghost">← Back</a>
</section>

<section id="screen-3" class="screen">...</section>
<section id="screen-4" class="screen">
  <h1>You're all set 🎉</h1>
  <a href="#screen-1" class="btn ghost">Start over</a>
</section>
```

**关键 CSS**（`:target` 路由）：

```css
.screen { display: none; min-height: 100vh; padding: 60px 80px;
          flex-direction: column; gap: 24px;
          align-items: center; justify-content: center; }
.screen:target { display: flex; }

/* 默认显示第一屏 */
#screen-1 { display: flex; }
/* 当任何 :target 命中时隐藏 #screen-1 */
.screen:target ~ #screen-1 { display: none; }
/* 简单粗暴的版本：用 JS 也行，但 :target 零脚本 */
```

或者用 `<a>` + JS 切换 `display`：

```js
window.addEventListener('hashchange', () => {
  document.querySelectorAll('.screen').forEach(s =>
    s.style.display = ('#' + s.id) === location.hash ? 'flex' : 'none'
  );
  if (!location.hash) document.querySelector('#screen-1').style.display = 'flex';
});
```

无独立模板。

---

## 共同原则

- **真实可点的按钮 + 真实视觉**——不要"placeholder UI"，要看起来像产品的下一版
- **动画沙盒一定要有 Copy CSS 出口**——用户调好的参数能直接落到代码里
- **Flow 屏数 ≤ 6**——多了用户走不完
- **Flow 必须有"返回上一屏"**——让用户来回比较
