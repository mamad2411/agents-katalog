---
name: arch-diagram-html
description: Generate dark-themed standalone HTML architecture diagrams with inline SVG, based on the Cocoon-style architecture diagram pattern, but adapted for Hermes. Use when the user wants a clean architecture diagram delivered as a single .html file that opens in any browser.
version: 1.0.0
author: Hermes Agent
license: MIT
tags:
  - architecture-diagram
  - html
  - svg
  - system-design
  - visualization
---

# Architecture Diagram HTML Skill

产物：单文件 `.html`，内嵌 CSS 与 SVG，可直接浏览器打开。

适用：
- 系统架构图
- 云架构图
- 服务依赖图
- 安全边界图
- 技术组件关系图

不适用：
- 需在线协作编辑的手绘图 -> 用 `excalidraw`
- 需动画 -> 用 `manim-video`

## 核心规则

1. 产物必须是单文件 HTML。
2. 主图必须用 inline SVG，不依赖 JS。
3. 默认深色主题：背景 `#020617`。
4. 箭头先画，组件后画；避免 z-order 混乱。
5. 组件若用半透明填充，先画一层不透明底色以遮住背后箭头。
6. 图下方应有 3 张摘要卡片。
7. 输出应可直接保存为 `*.html` 并在现代浏览器打开。
8. 若用户未给精确布局，先按“左到右主流向、上到下辅助流”布图。

## 语义配色

| 类型 | Fill | Stroke |
|---|---|---|
| Frontend | `rgba(8, 51, 68, 0.4)` | `#22d3ee` |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` |
| Database / Storage / AI | `rgba(76, 29, 149, 0.4)` | `#a78bfa` |
| Cloud / Infra | `rgba(120, 53, 15, 0.3)` | `#fbbf24` |
| Security | `rgba(136, 19, 55, 0.4)` | `#fb7185` |
| Message Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` |
| External / Generic | `rgba(30, 41, 59, 0.5)` | `#94a3b8` |

## 字体

默认可用：
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

若用户要求完全离线：
- 去掉 Google Fonts
- 改 `font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;`

## 结构

标准 HTML 结构：
1. Header
2. Diagram container
3. Main SVG
4. 3 summary cards
5. Footer

## 布局规则

- 主流向：左 -> 右
- 辅流向：上 -> 下
- 标准组件高度：60
- 大组件：80-120
- 垂直最小间距：40
- 图例必须位于所有边界框之外
- 若 legend 放不下，增大 SVG `viewBox` 高度

## SVG 必备片段

### 网格背景
```svg
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

### 箭头
```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
</marker>
```

### 组件遮箭头模式
```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#0f172a"/>
<rect x="X" y="Y" width="W" height="H" rx="6" fill="rgba(6, 78, 59, 0.4)" stroke="#34d399" stroke-width="1.5"/>
```

## 输出流程

1. 先从用户描述抽组件、边界、外部系统、数据流。
2. 按语义分组：frontend / backend / storage / security / cloud / external。
3. 再定主路径。
4. 先布箭头，再布盒子与文字。
5. 最后补三张 summary cards：
   - Surface / Clients / Entry
   - Services / Runtime / Processing
   - Data / Infra / Security
6. 输出完整 HTML 文件。

## 默认卡片内容策略

若用户未指定：
- Card 1: 接入层与客户端
- Card 2: 核心服务与运行时
- Card 3: 数据、基础设施与安全

## 风险与坑

- 不要把 legend 放进 region/security boundary 内。
- 不要让 message bus 压住上下组件。
- 不要只给 SVG 片段；默认给完整 HTML。
- 不要引入 JS 动画库；纯 CSS 即可。
- 若用户只给模糊描述，先做合理默认，不要卡住。

## 交付格式

默认直接产：
- 一个完整 HTML 文件内容
- 或写入用户指定路径

若用户要落盘：
- 用 `write_file` 保存 `.html`
- 再验证关键标题、组件名、文件存在

## 参考

- `references/template.html`：Hermes 基础模板
- `references/source-note.md`：上游来源与吸收说明
