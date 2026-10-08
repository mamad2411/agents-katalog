---
name: html-effectiveness-explore
description: 子 skill — 探索与规划。用户在多种实现方案/设计风格之间未决，或方案选定后要写工程版 RFC 时使用。包含三方案对比（compare.html）、视觉设计方向、实现计划（plan.html）三种范式。当父 skill html-effectiveness 路由命中"对比/选型/RFC/计划"类请求时加载。
---

# 01-explore — 探索与规划

> "You're not sure what you want yet. Ask the agent to fan out across several directions and lay them next to each other so you can point at one."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "几种实现方式给我看看 / 哪种更好" | **三方案对比** | `../templates/compare.html` |
| "compare X vs Y vs Z" | 同上 | 同上 |
| "我想要 UI 但说不清风格 / 几个方向给我看" | **视觉设计方向** | 自建（见下） |
| "做一份实现计划 / RFC / 怎么落地" | **实现计划** | `../templates/plan.html` |
| "ship in 2 weeks 怎么排" | 同上 | 同上 |

---

## 范式 1.1 · 三方案对比

**空间形状**：每个方案 = 一个完整代码块 + 一张 Pro/Con 表 + 一行指标（bundle / 可测试性 / SSR / 复用）。三个方案要**并排**才能比较，markdown 只能上下堆。

**最少要素**：
- 至少 2、不超过 4 栏（多了用户记不住）
- 每栏一段最小可运行代码（5-15 行）
- Pro/Con 各 3 条，**具体**（不是 "easy to read"，而是 "Single import reused across filter, command bar, and board search"）
- 一行指标用同一组维度，便于横向比较
- 文末一段 **agent 的推荐**（不要让用户全自己判断）

**HTML 骨架**：

```html
<div class="approaches">
  <article class="approach">
    <header><span class="tag">Approach 1</span><h2>Inline useEffect</h2></header>
    <pre><code>...实际可运行代码...</code></pre>
    <table class="proscons">
      <thead><tr><th>Pro</th><th>Con</th></tr></thead>
      <tbody><tr><td>...</td><td>...</td></tr></tbody>
    </table>
    <footer class="metrics">
      <span>Bundle <b>+0 kb</b></span>
      <span>Test <b>medium</b></span>
      <span>Reuse <b>low</b></span>
      <span>SSR <b>yes</b></span>
    </footer>
  </article>
  <!-- 重复 2-3 次 -->
</div>
<aside class="recommendation"><strong>建议：</strong>...</aside>
```

**关键 CSS**：

```css
.approaches { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.approach { display: flex; flex-direction: column; gap: 16px;
            padding: 20px; border: 1px solid var(--gray-300);
            border-radius: 12px; background: var(--white); }
.approach pre { flex: 1; max-height: 360px; overflow: auto; }
.proscons td:first-child { color: var(--success); }
.proscons td:last-child  { color: var(--danger); }
.metrics { display: flex; gap: 16px; flex-wrap: wrap;
           font-size: 13px; color: var(--gray-700); }
```

**直接可用模板**：[`../../templates/compare.html`](../../templates/compare.html)

---

## 范式 1.2 · 视觉设计方向

**空间形状**：4 张**真实渲染**的卡片（不是描述！）+ 每张一行风格说明 + 顶栏 light/dark 切换。

**典型 4 个方向**（覆盖大多数场景）：
- A — Minimal · 纯字体单一动作
- B — Illustrated · 加一个小 SVG 插画
- C — Playful · 有微动画 / 玩味
- D — Instructional · 把空状态当 onboarding

**关键 CSS / JS**：

```css
.directions { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; }
.directions[data-theme="dark"] { background: var(--slate); color: var(--ivory); }
.render { aspect-ratio: 4/3; padding: 32px; border-radius: 12px;
          background: var(--ivory); display: flex; align-items: center;
          justify-content: center; flex-direction: column; }
```

```js
document.querySelectorAll('.theme-toggle button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.directions').forEach(d => d.dataset.theme = b.dataset.theme);
});
```

无独立模板（按需生成；可参考 `../../templates/compare.html` 的两栏结构改造）。

---

## 范式 1.3 · 实现计划（plan）

**空间形状**：6 块固定区域：
1. **元信息条**：Effort / Surfaces / New tables / Feature flag
2. **Milestones**：4 段时间线（slice 1-4，每段独立可评审）
3. **Data flow**：SVG 框图（实线 = 请求/响应，虚线 = realtime fan-out）
4. **Mockups**：用 HTML 直接渲染的 UI 草图（不要图片占位）
5. **Key code**：1-2 段最容易做错的代码（migration、optimistic mutation）
6. **Risks & mitigations**：表格 (Risk, Sev, Mitigation)
7. **Open questions**：每条带"和谁、何时决定"

**HTML 骨架**：

```html
<header class="meta">
  <h1>Implementation plan — [Feature]</h1>
  <dl class="meta-grid">
    <div><dt>Effort</dt><dd>~2 weeks</dd></div>
    <div><dt>Surfaces touched</dt><dd>3 packages</dd></div>
    <div><dt>New tables</dt><dd>2</dd></div>
    <div><dt>Feature flag</dt><dd><code>flag_v1</code></dd></div>
  </dl>
</header>

<section class="step"><span class="step-no">01</span>
  <h2>Milestones</h2>
  <ol class="timeline">...</ol>
</section>

<section class="step"><span class="step-no">02</span>
  <h2>Data flow</h2>
  <svg viewBox="0 0 800 320">...</svg>
</section>

<!-- 03 Mockups · 04 Key code · 05 Risks · 06 Open questions -->
```

**SVG 数据流要点**：
- 节点 `<rect>` 用 8px 圆角
- 实线（请求路径）用 `--slate`，虚线（fan-out）用 `--clay` + `stroke-dasharray="4 4"`
- 箭头复用 `<defs><marker id="arr">`（见 `../shared/components.html` 第 1 节）

**直接可用模板**：[`../../templates/plan.html`](../../templates/plan.html)

---

## 共同原则

- **不要写一个 winner**，让 3 个方案都看起来可信，再给推荐
- **指标要可比**——别第一栏写 "fast"，第二栏写 "200ms"
- **Pro/Con 各 3 条**——少了不可信，多了读不完
- **真实姓名占位**：`Mira Okafor`, `Devon Park`，不写 `User A`
- **数据流图必须有图例**——实线 vs 虚线的含义写清楚
