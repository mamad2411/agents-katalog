---
name: diagramming
description: Create diagrams, mind maps, flowcharts, architecture sketches, and relationship graphs. Trigger on simple Chinese requests like "帮我画个结构图", "帮我画个脑图", "画个脑图", "画个关系图", as well as diagram, mindmap, Mermaid chart, flowchart, sequence diagram, or dependency graph. Default to Mermaid as the primary text-based format and produce local files. Use local Excalidraw only when the user explicitly wants a hand-drawn whiteboard style or interactive editing.
---

# Diagramming

这个 skill 用来统一处理 `脑图`、`关系图`、`flowchart`、`mindmap`、`sequence diagram`、`architecture diagram`。

## 默认策略

1. **默认首选 `Mermaid`**
   适合版本管理、CLI、Markdown、Git diff、长期维护。

2. **默认产出本地文件**
   除非用户明确只要聊天内展示，否则至少产出：
   - `*.mmd`
   - `*-outline.md`
   - `*.html`（可直接浏览器打开）

3. **`Excalidraw` 只作为补充**
   仅在用户明确要“手绘感 / 白板感 / 互动编辑”时使用本地 `excalidraw` MCP。
   不把 `create_view` 当作唯一交付物。

4. **不要默认使用 `excalidraw_remote`**
   如果本地 `excalidraw` MCP 不可用，就退回 `Mermaid` 文件方案。

## 何时选哪种图

### 选 `Mermaid`

- 层级清晰的脑图
- 关系图 / 调用链 / 模块图
- 流程图 / 决策树
- 时序图
- 需要落到仓库里的图

优先语法：

- 脑图：`mindmap`
- 流程：`flowchart TD`
- 时序：`sequenceDiagram`
- 状态：`stateDiagram-v2`

### 选 `Excalidraw`

- 用户明确要“手绘风”
- 需要白板感表达
- 需要后续人工拖拽编辑
- 需要临时演示而不是长期维护

## 默认输出目录

如果用户没指定路径，优先写到当前工作区下：

`./tmp/diagrams/`

文件名用短 `slug`，例如：

- `./tmp/diagrams/hive-relationship.mmd`
- `./tmp/diagrams/hive-relationship-outline.md`
- `./tmp/diagrams/hive-relationship.html`

## Mermaid 工作流

1. 先判断图类型
2. 生成 `Mermaid` 源文件
3. 同时生成一个 `outline.md`，把图的层级/结论/补充说明写成纯文本
4. 用 `scripts/create_diagram_bundle.py` 生成本地 bundle
5. 在回复里给出三个绝对路径

命令：

```bash
python3 scripts/create_diagram_bundle.py \
  --title "Diagram Title" \
  --slug diagram-title \
  --diagram INPUT.mmd \
  --outline INPUT-outline.md \
  --output-dir ./tmp/diagrams
```

### outline.md 结构

最少包含：

```md
# 标题

## 一句话结论

## 结构拆解
- 节点 A
- 节点 B

## 关键关系
- A -> B: 为什么

## 备注
- 补充说明 / 风险 / 待确认项
```

## Excalidraw 工作流

1. 只有在用户明确需要时才走 `Excalidraw`
2. 优先本地 `excalidraw` MCP，不用 remote
3. 如果当前客户端不渲染 `create_view`，不要只给内嵌图
4. 至少补一个本地文本产物或说明退回 `Mermaid`

## 可移植性

- 文档和脚本示例里不要写死个人机器路径
- 对外仓库默认使用相对路径，例如 `scripts/create_diagram_bundle.py`
- 本地安装可以通过 symlink 完成，但仓库主体本身不依赖某个固定绝对路径

## 回复规范

- 简单图：直接给一句说明 + 文件路径
- 复杂图：说明你选了 `Mermaid` 还是 `Excalidraw`，以及为什么
- 如果是 `Excalidraw` 路线，明确说明聊天内嵌图可能在某些客户端不可见

## 经验规则

- 用户说“脑图”时，不要机械地总用 `Excalidraw`
- 对工程内容，`Mermaid` 往往比白板图更实用
- 如果图会进入仓库、文档、PR，优先 `Mermaid`
- 如果图只是用来讲一次，才考虑 `Excalidraw`
- 默认把“图”和“文字稿”一起交付，避免只剩图没有上下文
