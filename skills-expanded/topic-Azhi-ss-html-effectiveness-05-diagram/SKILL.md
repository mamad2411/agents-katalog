---
name: html-effectiveness-diagram
description: 子 skill — 插画与图表。当用户要博客/文档配图（SVG 插图集）、流程图、状态机、deploy pipeline（flowchart.html）时使用。所有图都用内联 SVG，不引外部库（mermaid/d3/excalidraw）。当父 skill 路由命中"图/diagram/flowchart/state machine/pipeline 可视化"类请求时加载。
---

# 05-diagram — 插画与图表

> "Inline SVG gives the agent a real pen. Ask for the figures for a post or a flowchart of a process and get vector art you can tweak by hand or paste straight into the final document."

## 何时用

| 用户说 | 用哪个范式 | 模板 |
|-------|-----------|------|
| "画一下我们的 deploy pipeline" | **流程图** | `../../templates/flowchart.html` |
| "状态机长什么样" | 同上 | 同上 |
| "request flow / data flow 怎么走" | 同上（或参考 [`01-explore`](../01-explore/SKILL.md) 的 plan 数据流） | — |
| "给这篇博客配几张图" | **SVG 插图集** | 自建（见下） |

> **不要用 mermaid / d3 / excalidraw**。直接写 inline SVG——更可控、零依赖、可手改。

---

## 范式 5.1 · SVG 插图集

**空间形状**：一个文档要的所有图都画在一页。每个 `<svg>` 单独一块——读者**右键-检查-复制 outerHTML** 就能拿到一张图。

**HTML 骨架**：

```html
<article class="figure">
  <h3>Figure 1 · Token bucket</h3>
  <svg viewBox="0 0 240 160" width="240" height="160">
    <!-- 用基本图元：rect, circle, path, text -->
    <rect x="60" y="40" width="120" height="80" rx="8"
          fill="var(--ivory)" stroke="var(--slate)" stroke-width="2"/>
    <!-- tokens as small circles -->
    <circle cx="80"  cy="100" r="6" fill="var(--clay)"/>
    <circle cx="100" cy="100" r="6" fill="var(--clay)"/>
    <circle cx="120" cy="100" r="6" fill="var(--clay)"/>
    <!-- inflow -->
    <path d="M 120 10 L 120 38" stroke="var(--success)" fill="none"
          stroke-width="2" marker-end="url(#arr-down)"/>
    <text x="130" y="25" font-size="11">refill rate/sec</text>
  </svg>
  <p class="caption">A bucket holds at most <code>burst</code> tokens; refills at <code>rate</code>/sec.</p>
</article>

<article class="figure">
  <h3>Figure 2 · LRU cache eviction</h3>
  <svg viewBox="0 0 320 100">...</svg>
  <p class="caption">...</p>
</article>
```

**SVG 坐标手算法**（不要让 LLM 蒙数字）：
- viewBox 用整除值：`0 0 240 160`、`0 0 800 400`
- 节点对齐 20px 网格
- 文本居中：`text-anchor="middle" dominant-baseline="middle"`
- 配色用 `var(--clay)` 等 baseline 变量（如果 SVG 不在 base.css 同页则改成 hex）

无独立模板（按图不同而异）。

---

## 范式 5.2 · 流程图

**空间形状**：节点（盒子）+ 边（箭头）+ 状态颜色（pass/fail）+ 节点可点击展开"这步运行什么"。

**典型场景**：deploy pipeline、状态机、决策树。

**HTML 骨架**：

```html
<svg viewBox="0 0 800 400" class="flowchart">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- 节点 -->
  <g class="node process" data-detail="ci-detail" tabindex="0">
    <rect x="20" y="40" width="140" height="60" rx="8"/>
    <text x="90" y="68" text-anchor="middle">CI · lint+typecheck</text>
    <text x="90" y="86" text-anchor="middle" class="sub">~2 min · ci.yml</text>
  </g>

  <g class="node decision">
    <polygon points="240,40 320,70 240,100 160,70" />
    <text x="240" y="74" text-anchor="middle">tests pass?</text>
  </g>

  <g class="node terminal success">
    <rect x="500" y="40" width="140" height="60" rx="30"/>
    <text x="570" y="74" text-anchor="middle">✓ Deploy complete</text>
  </g>

  <!-- 边：成功路径（实线） -->
  <path d="M 160 70 L 200 70" class="edge success" marker-end="url(#arr)"/>
  <path d="M 320 70 L 500 70" class="edge success" marker-end="url(#arr)"/>

  <!-- 边：失败路径（虚线） -->
  <path d="M 240 100 L 240 200 L 500 200" class="edge fail"
        stroke-dasharray="6 4" marker-end="url(#arr)"/>

  <!-- 图例 -->
  <g class="legend" transform="translate(20, 360)">
    <text font-size="11" fill="var(--gray-700)">Solid = pass · Dashed = fail</text>
  </g>
</svg>

<!-- 节点详情面板（点击节点弹出） -->
<aside id="ci-detail" hidden>
  <h4>CI · lint + typecheck</h4>
  <p>~2 min · <code>.github/workflows/ci.yml</code>. Runs <code>eslint</code> + <code>tsc --noEmit</code>.</p>
</aside>
```

**关键 CSS**：

```css
.flowchart .node rect, .flowchart .node polygon {
  fill: var(--white); stroke: var(--gray-300); stroke-width: 1.5;
}
.flowchart .node.terminal.success rect { fill: rgba(120,140,93,0.15); stroke: var(--success); }
.flowchart .node text { font-size: 12px; font-family: var(--font-sans); fill: var(--slate); }
.flowchart .node text.sub { font-size: 10px; fill: var(--gray-500); }
.flowchart .node[tabindex] { cursor: pointer; }
.flowchart .node:focus rect { stroke: var(--clay); stroke-width: 2; outline: none; }

.flowchart .edge { fill: none; stroke: var(--slate); stroke-width: 1.5; }
.flowchart .edge.fail { stroke: var(--danger); }
```

**关键 JS**（节点点击展开详情）：

```js
document.querySelectorAll('.node[data-detail]').forEach(n => {
  n.onclick = () => {
    const id = n.dataset.detail;
    document.querySelectorAll('aside[id]').forEach(a => a.hidden = a.id !== id);
  };
});
```

**直接可用模板**：[`../../templates/flowchart.html`](../../templates/flowchart.html) — 11 节点的 deploy pipeline 骨架，含 process / decision / terminal 三种节点形状、success（实线）/ fail（虚线）双路径、键盘可达的节点点击展开详情面板、内嵌的节点详情 JSON。**修改方式**：替换 SVG 节点的 transform 坐标和文本、调整 path d 走线、把 `<script type="application/json">` 里的 detail data 换成你的 pipeline 内容。

---

## 共同原则

- **永远用 inline SVG，不要外链 lib**——agent 应该会用 `<rect>` `<path>` `<text>`
- **失败路径必须视觉上区分**——通常用 `stroke-dasharray="6 4"` + `--danger` 颜色
- **图例必须显示**——读者第一眼看不懂图就放弃了
- **节点可点击是奢侈但有用**——用户能查"这步在做什么"
- **节点形状有语义**：长方形 = process，菱形 = decision，圆角胶囊 = terminal，圆形 = state
