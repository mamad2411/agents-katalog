---
name: html-effectiveness-research
description: 子 skill — 研究与学习。当用户问"X 在这个 repo 里怎么工作"（特性解释器，含 TL;DR/折叠步骤/tab 代码/FAQ）或要解释抽象概念（concept.html，含交互式可视化）时使用。当父 skill 路由命中"解释/explain/教我/这是什么/learn"类请求时加载。
---

# 07-research — 研究与学习

> "An explainer with collapsible sections, tabbed code samples and a glossary in the margin reads very differently from the same words dumped linearly. The agent can build the scaffolding that makes a new topic navigable."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "rate limit 在这个 repo 里怎么工作" | **特性解释器** | 自建（见下） |
| "auth flow 是什么样的" | **特性解释器** | 同上 |
| "讲讲一致性哈希 / Raft / token bucket" | **概念解释器** | `../../templates/concept.html` |
| "这是什么 / 我怎么理解 X" | 看深度 — markdown 一段或概念解释器 | — |

> **特性解释器** = 在**这个 repo 里**的具体实现（用户已在仓库内）
> **概念解释器** = **抽象概念**（与具体仓库无关，要交互式可视化）

---

## 范式 7.1 · 特性解释器

**空间形状**：4 段
1. **TL;DR 框** — 一段话讲完核心机制 + 性能数字
2. **请求路径编号步骤** — 1/2/3/4，每步可折叠看代码
3. **配置 Tab 切换** — yaml / route.ts / response 三 tab 切换
4. **FAQ** — `<details>` 列表

**HTML 骨架**：

```html
<aside class="tldr">
  <strong>TL;DR</strong>
  <p>The whole path is ~40 lines and adds about 0.4 ms p50 to every request.</p>
</aside>

<h2>The request path, step by step</h2>
<ol class="steps">
  <li>
    <span class="num">1</span>
    <h3>Identify the caller <code>middleware/ratelimit.ts:21</code></h3>
    <p>The middleware reduces the request to a <code>bucketKey</code>...</p>
    <details><summary>show source</summary>
      <pre><code>...</code></pre>
    </details>
  </li>
  <!-- 步骤 2-4 -->
</ol>

<h2>Configuring a limit on your route</h2>
<div class="tabs" role="tablist">
  <button role="tab" data-tab="yaml" class="active">limits.yaml</button>
  <button role="tab" data-tab="route">route.ts</button>
  <button role="tab" data-tab="resp">response</button>
</div>
<div class="tab-panels">
  <pre data-panel="yaml" class="active"><code>...</code></pre>
  <pre data-panel="route" hidden><code>...</code></pre>
  <pre data-panel="resp" hidden><code>...</code></pre>
</div>

<h2>FAQ</h2>
<details>
  <summary>How do I exempt internal traffic?</summary>
  <p>Set <code>x-acme-internal: 1</code> from the caller; the middleware checks it against mTLS peer name.</p>
</details>
```

**关键 JS**（tab 切换）：

```js
document.querySelectorAll('[role="tab"]').forEach(b => b.onclick = () => {
  document.querySelectorAll('[role="tab"]').forEach(x => x.classList.remove('active'));
  b.classList.add('active');
  document.querySelectorAll('[data-panel]').forEach(p => {
    p.hidden = p.dataset.panel !== b.dataset.tab;
    p.classList.toggle('active', !p.hidden);
  });
});
```

参见 `../shared/components.html` 第 7 节"Tab strip"。

无独立模板（按 feature 形态而异）。

---

## 范式 7.2 · 概念解释器

**空间形状**：4 段
1. **Hero 段** — 一段散文，建立直觉（"You have K keys spread across N servers..."）
2. **交互式可视化** — SVG/canvas，可加节点 / 删节点 / 看 key 移动
3. **对比表** — naive 方法 vs 这个方法（4-5 个维度并排）
4. **Where you'll meet it** — 实战场景列举

**例：一致性哈希环**

```html
<div class="viz">
  <svg viewBox="-150 -150 300 300">
    <circle r="120" fill="none" stroke="var(--gray-300)" />
    <g id="ring-arcs"><!-- 节点 arcs 由 JS 渲染 --></g>
    <g id="ring-nodes"><!-- 节点圆点 --></g>
    <g id="ring-keys"><!-- key 小点 --></g>
  </svg>
  <div class="ring-controls">
    <div class="stat"><span>nodes</span><output id="n-count">4</output></div>
    <div class="stat"><span>keys</span><output id="k-count">32</output></div>
    <div class="stat"><span>moved on last change</span><output id="moved">—</output></div>
    <button id="add" class="btn primary">+ Add node</button>
    <button id="rm" class="btn ghost">− Remove a node</button>
    <button id="reset" class="btn ghost">Reset</button>
  </div>
</div>
```

完整可工作的环可视化代码见 [`../../templates/concept.html`](../../templates/concept.html)（含 hash → angle 函数、arc 计算、key 重分布跟踪）。

**复用要点**：
- 把 `concept.html` 复制一份
- 替换 SVG 部分为新概念的可视化（state machine / Bloom filter / Raft 等）
- 替换控件按钮为该概念的 actions
- 替换对比表为该概念 vs naive 方法

---

## 共同原则

- **永远开头一段散文建立直觉**——直接给定义就失败了
- **可视化必须真的能操作**——按钮没用 = 静态图 = 失败
- **永远展示"naive vs concept"对比表**——读者需要知道为什么不能用更简单的
- **"Where you'll meet it" 列举要具体**——名字真实系统（Dynamo/Cassandra/Envoy），别写"various distributed systems"
