---
name: "arch-viewer-browser-check"
description: "在浏览器中验收 Architecture Viewer 六张视图的 mermaid 渲染质量（分层带颜色、节点形状、虚线边、解析错误）。每次视图收口、视觉契约变更或成片修改后调用。"
---

# Architecture Viewer 浏览器渲染验收

对 `architecture_visualized.html` 中六张视图（block / c4-context / c4-container / c4-component / class / deployment）做渲染级验收。用于视图视觉收口后验证「图本身无解析错误 + 视觉契约实际生效」。

## 何时调用

- 任一张视图成片修改后
- 视觉契约（classDef 色板、子图结构、节点形状规范）变更后
- 闸门（`check`）通过但怀疑浏览器渲染有差异时

## 前置条件

- 本地查看器已在 `http://127.0.0.1:8135/architecture_visualized.html` 运行（`node lib/cli.js serve` 或等价）
- 目标仓库的 `architecture_viewer/*.md` 已是最新成片

## 验收流程

### 1. 切 Tab 并等待渲染

页面提供全局函数 `switchTab('<view>')`，视图名：`block` / `c4-context` / `c4-container` / `c4-component` / `class` / `deployment`。

```js
switchTab('deployment');
await sleep(1500);
const panel = document.getElementById('tab-deployment');
const svgs = panel.querySelectorAll('svg');
// 期望 2 个 svg（子图1 全景 + 子图2 特写）
```

**陷阱**：切 Tab 是懒渲染，第二个 mermaid 块偶发不渲染（PRE 内无 svg、无报错）。若 `svgs.length < 2`，手动补渲染：

```js
for (const el of [...panel.querySelectorAll('.mermaid')].filter(e => !e.querySelector('svg'))) {
  const { svg } = await mermaid.render('mm-' + Date.now(), el.textContent);
  el.innerHTML = svg;
}
```

### 2. 解析错误检查

```js
const bodyErr = /Syntax error in text|Parse error/.test(document.body.textContent);
const perBlock = [...panel.querySelectorAll('.mermaid')].map(el =>
  /Syntax error|error/i.test(el.textContent) ? el.textContent.slice(0, 150) : null
);
```

无 `Syntax error` 才算通过；mermaid 解析失败会把错误文本留在 PRE 里。

### 3. 分层 subgraph 颜色验收

视觉契约色板：
- actor `#eceff1`
- api `#ede7f6`
- storage `#e0f7fa`
- ops `#c8e6c9`

```js
const fills = [...svg.querySelectorAll('.node rect, .node polygon, .node .label-container')]
  .map(el => getComputedStyle(el).fill);
// 或直接查 .subgraph 的 rect
const subgraphFills = [...svg.querySelectorAll('.subgraph rect')]
  .map(el => getComputedStyle(el).fill);
```

判定：实际渲染出的 `fill` 集合包含契约色板中本视图应出现的颜色。classDiagram 不适用（用 `style` 指令而非 classDef）。

### 4. 节点形状验收

- 外部演员（用户/开发者）→ stadium 形状（圆角胶囊）：节点 path/rect 圆角半径 ≈ 高度/2
- 内部组件 → 矩形卡片
- 数据库 → 圆柱（`[(...)]` 语法，渲染为带上下弧的形状）

```js
const nodeCount = svg.querySelectorAll('.node').length;
// stadium 节点可通过 <path> 的 d 属性含大量弧线判断，或直接数 .node 下是否为 path 而非 rect
const stadiumCount = [...svg.querySelectorAll('.node')].filter(n => n.querySelector('path')).length;
```

### 5. 虚线边验收（关键陷阱）

**Mermaid 用 CSS 类表达虚线，不是内联样式。** 只查 `path.getAttribute('style')` 会得到 0，属误报。

正确判定：

```js
const edges = [...svg.querySelectorAll('.flowchart-link')].map(p => ({
  cssDash: getComputedStyle(p).strokeDasharray,     // 虚线非 '0px'
  cls: p.getAttribute('class') || ''                 // 含 edge-pattern-dotted
}));
const dashedCount = edges.filter(e =>
  /edge-pattern-dotted/.test(e.cls) || (e.cssDash && e.cssDash !== '0px')
).length;
```

判定：ops → 运行时 / 部署 → 入口 的边必须为虚线（`edge-pattern-dotted`），业务调用链为实线。

### 6. 边标签验收

中文动作标签 <= 8 字。检查 `.edgeLabel` 文本：

```js
const labels = [...svg.querySelectorAll('.edgeLabels .edgeLabel')].map(l => l.textContent.trim());
```

判定：标签非空、无英文残留（除技术名词）、无 `uses`/`calls` 等 UML 味词汇。

### 7. 路径标签验收

内部节点的 `<small>` 应是真实仓库路径，外部演员用 `(外部)`。此步闸门 `check --filled` 已覆盖，浏览器侧只确认 `<small>` 文本实际渲染出来（不被截断）。

## 报告模板

按下列条目输出，每条 ✅/❌ + 实测值：

| 条目 | 实测 |
|---|---|
| 子图1/2 渲染数 | N/2 |
| 解析错误 | 无 / 有（贴出） |
| 色板 | 实际 fill 集合 vs 契约 |
| 节点数 / stadium 数 | N / M |
| 虚线边数 | N（edge-pattern-dotted） |
| 边标签 | 列出前 5 个 |

## 不适用范围

- class-diagram：方法签名必须在 class 箱体里，不适用 stadium/分层卡片契约，只验配色 + note 路径渲染。
- c4-context：C4 语义限制只画角色→系统→外部，节点少是正常的，不判「密度不足」。

## 已知页面行为

- `switchTab()` 是全局函数，直接调用即可。
- 首次加载只渲染当前 Tab 的 mermaid，切 Tab 才触发懒渲染。
- `mermaid.render(id, src)` 可手动补渲染未显示的块。
