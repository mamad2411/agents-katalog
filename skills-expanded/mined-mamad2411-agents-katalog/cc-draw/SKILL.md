---
name: cc-draw
argument-hint: "<图描述> [输出到 <路径>] [风格说明]"
model: opus
description: |
  把自然语言描述生成为简洁的技术图（架构图 / 流程图 / 时序图 / 状态机
  / 数据流 / ER / 概念图 等）。**不让 LLM 画 SVG**——LLM 只输出 JSON
  描述节点和边，确定性 Python 渲染器算 Manhattan 走线、避撞、标签放置，
  保证 layout 100% 干净。默认 Ledger 风格（暖白底 + teal accent + 深灰描边）。
  通过 `rsvg-convert` 同时产出 PNG。

  TRIGGER when user asks to: 画图, 画一张, 帮我画, 画个, 出图, 生成图,
  做个图, 架构图, 流程图, 时序图, 状态机图, ER 图, 可视化一下, draw,
  diagram, visualize, chart it.
---

# cc-draw — 技术图生成

**核心理念**：LLM 不画像素。LLM 只输出 JSON 描述「有什么节点 / 什么边 / 用什么风格」，`scripts/generate-from-template.py`（1800 行 Python，**Forked from yizhiyanhua-ai/fireworks-tech-graph @ MIT**）算 Manhattan 路由、节点对齐、避撞、标签布局。

这避免了 LLM 写 SVG 时反复出现的「斜穿容器边界 / Bezier 跨层 / 圆柱侧壁出箭头」等几何错误。

## ⚠️ MANDATORY READ ORDER

**写 JSON 前，按顺序读这几个文件**：

### 1. 默认 Ledger 风格 token

`Read references/style-8-ledger.md` —— 默认风格的颜色 / 字号 / 箭头语义。除非用户明确要别的风格，**始终用 `style: 8`**。

### 2. 看一个最接近的 fixture

按用户描述匹配，Read **一个** fixture：

| 关键词 | Read 这个 |
|---|---|
| 架构 / 微服务 / 多组件 | `fixtures/ai-work-architecture-style8.json` |
| 流程 / 流水线 / 步骤 | `fixtures/api-flow-style7.json` |
| 多 agent / 协作 | `fixtures/multi-agent-style5.json` |
| 工具调用 / 决策 | `fixtures/tool-call-style2.json` |
| 内存 / 存储分层 | `fixtures/agent-memory-types-style4.json` |
| 微服务依赖 | `fixtures/microservices-style3.json` |

匹配多个时挑**最具体**的那个。

### 3. THEN write JSON, **based on the fixture**

把 fixture 的 `nodes` / `arrows` 改成用户场景的内容，**保留**它的整体网格布局（x/y 坐标可以平移整片，但节点间距维持）。

把 `style` 改成 `8`（除非用户指定别的）。

## JSON Schema（最简）

```json
{
  "template_type": "architecture",
  "style": 8,
  "width": 1440,
  "height": 720,
  "title": "...",
  "subtitle": "...",
  "containers": [
    {"x": 160, "y": 96, "width": 1240, "height": 96, "label": "L1 · 接入"}
  ],
  "nodes": [
    {"id": "n1", "kind": "rect", "x": 220, "y": 128, "width": 170, "height": 48, "label": "..."},
    {"id": "db", "kind": "cylinder", "x": 200, "y": 360, "width": 130, "height": 70, "label": "Postgres"}
  ],
  "arrows": [
    {"from": "n1", "to": "db", "kind": "write", "label": "写入"}
  ],
  "legend": [{"label": "主流程", "kind": "data"}],
  "footer": "draw · Ledger"
}
```

`template_type` 可选值：`architecture` · `flowchart` · `sequence` · `data-flow` · `state-machine` · `timeline` · `use-case` · `er-diagram` · `comparison-matrix` · `agent-architecture`

`kind` 可选值：
- 节点：`rect` · `cylinder` · `hexagon` · `diamond` · `ellipse` · `cloud`
- 箭头：`data` · `control` · `write` · `read` · `async` · `feedback` · `neutral`

## 工作流

1. 按 MANDATORY 步骤读 fixture + style 文档
2. 写 JSON 到 `/tmp/cc-draw/<name>.json`
3. 渲染（`<SKILL_DIR>` 是 skill 安装目录，通常 `~/.agents/skills/cc-draw/`）：
   ```bash
   python3 <SKILL_DIR>/scripts/generate-from-template.py \
     <template_type> /tmp/cc-draw/<name>.svg < /tmp/cc-draw/<name>.json
   ```
4. 转 PNG：
   ```bash
   mkdir -p ~/Downloads/cc-draw
   rsvg-convert /tmp/cc-draw/<name>.svg -f png -w 1920 \
     -o ~/Downloads/cc-draw/<name>.png
   ```
5. **自检**：`Read ~/Downloads/cc-draw/<name>.png` 看效果
6. 报告 PNG 路径 + 一行说明

## 输出路径规则

| 文件 | 路径 |
|---|---|
| **PNG**（默认）| `~/Downloads/cc-draw/<name>.png` |
| **SVG** 缓存 | `/tmp/cc-draw/<name>.svg` |
| **JSON** 缓存 | `/tmp/cc-draw/<name>.json` |

用户在 prompt 里指定路径（"输出到 ~/Desktop/"）则覆盖默认。

**所有文件路径统一规则**：除 `/tmp/cc-draw/` 外，**禁止**写任何文件到 `/tmp` 根目录。

## 节点定位原则

JSON 里 `x/y` 是绝对像素坐标。建议网格：

- **横向架构图**：x 间距 200，y 间距 116（每层节点居中分布）
- **layered 分组**：containers 高度 = 节点高 + 上下 padding 各 28
- **状态机 / ring**：环形布局，半径 ≈ canvas_width × 0.3
- **sequence 时序**：垂直时间线 + 水平 actor，时间步距 60-80
- **节点最小间距**：水平 60px，垂直 40px（保证箭头标签有地方放）

不需要算箭头几何——`generate-from-template.py` 自己算 Manhattan 路由。

## 不做

- **不要直接写 SVG**（这正是换路线的原因）
- 不要为每个节点配不同颜色（Ledger 只用 teal 一种 accent）
- 不要用渐变 / 阴影 / 3D
- 不要内嵌外部图片或网络字体
- 不要重复输出整个 JSON 给用户看（写完文件给路径就行）

## 上游致谢

渲染引擎 fork 自 [`yizhiyanhua-ai/fireworks-tech-graph`](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)（MIT License）。我们做的修改：
- 加 Ledger 风格（style 8）作为默认
- 中文化 SKILL.md 和 README
- 加交易所测试平台 fixture

## Version

- v0.5.0 (2026-05-08) — **重大架构切换**：弃用「LLM 直接画 SVG」路线，改用「LLM 写 JSON → Python 渲染器算 layout」。Fork from fireworks-tech-graph (MIT)，加 Ledger style 作为默认。彻底解决 v0.4.x 系列遗留的「斜穿容器 / Bezier 跨层 / 扇出炸开」等几何问题。Layout 100% 干净，出图 ~2 秒。
- v0.4.7 (2026-05-08) — 老路线最后一版（[tag v0.4.7-final](https://github.com/QA-Ray/cc-draw/tree/v0.4.7-final)）。历史 changelog 见该 tag。
