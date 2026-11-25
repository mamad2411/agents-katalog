---
name: make-mermaid
description: >-
  Generate Mermaid diagrams from code analysis or user descriptions, render to PNG/SVG images.
  Supports all Mermaid diagram types: sequence diagram, flowchart, class diagram, state diagram,
  ER diagram, gantt chart, pie chart, git graph, mindmap, timeline, user journey.
  Use when: (1) user asks to draw/generate/create any diagram or chart,
  (2) user says 顺序图/时序图/流程图/类图/状态图/ER图/甘特图/思维导图/分支图/饼图/时间线/旅程图,
  (3) user asks to visualize code architecture, call chains, database schema, or business processes,
  (4) user says "画图", "画个图", "diagram", "mermaid", "sequence", "flowchart", "class diagram",
  (5) user wants to export diagrams as PNG/SVG images.
  Default language is Chinese; switch to English with --lang en.
---

# Make Mermaid

Analyze code or user descriptions to generate Mermaid diagrams, then render to PNG/SVG.

## Workflow

```
1. Determine diagram type  →  2. Gather context  →  3. Write .mmd  →  4. Render image  →  5. Verify
```

### Step 1: Determine Diagram Type

Map user intent to diagram type. Read [references/diagram-types.md](references/diagram-types.md) for syntax templates and trigger keywords.

| User Intent | Diagram Type |
|------------|-------------|
| 调用链、交互流程、接口调用 | `sequenceDiagram` |
| 业务流程、决策流程 | `flowchart` |
| 对象关系、继承结构 | `classDiagram` |
| 生命周期、状态转换 | `stateDiagram-v2` |
| 数据库表关系 | `erDiagram` |
| 项目排期、里程碑 | `gantt` |
| 占比分布 | `pie` |
| 分支策略 | `gitGraph` |
| 知识结构、分类 | `mindmap` |
| 发展历程 | `timeline` |
| 用户体验流程 | `journey` |

If ambiguous, ask user to clarify.

### Step 2: Gather Context

**From code** — Read [references/code-analysis.md](references/code-analysis.md) for extraction strategies per diagram type:
- Identify architecture pattern (MVVM, MVC, microservice, etc.)
- Read relevant source files (ViewModels, Services, Models, Controllers)
- Trace call chains, state transitions, or entity relationships

**From description** — Parse user's natural language into structured participants, messages, and conditions.

### Step 3: Write .mmd Files

Output path: `docs/sequence-diagrams/` (or `docs/diagrams/` for non-sequence types). Create directory if needed.

Naming: `<topic>-<type>.mmd` — e.g., `login-sequence.mmd`, `patient-er.mmd`, `order-flowchart.mmd`

Language rules:
- **Default**: Chinese labels, technical terms (class names, SQL keywords) in English
- **`--lang en`**: All labels in English
- **`--lang mixed`**: Business terms in Chinese, code identifiers in English (default behavior)

Always include `autonumber` for sequence diagrams.

### Step 4: Render to Image

Use `@mermaid-js/mermaid-cli` via npx:

```bash
npx @mermaid-js/mermaid-cli -i <input>.mmd -o <output>.png -b white -s 2 -w 1600 -H 1200
```

Parameters:
- `-b white` — white background (use `-b transparent` if user requests)
- `-s 2` — 2x scale for high resolution
- `-w 1600 -H 1200` — page dimensions (increase for complex diagrams)
- Output format: `.png` default, `.svg` if user requests vector format

For multiple diagrams, render in parallel.

### Step 5: Verify

- Confirm all `.png` files exist and have non-zero size
- Read the generated images to visually verify correctness
- Report file paths and sizes to user

## Options

| Flag | Effect | Example |
|------|--------|---------|
| `--lang en` | English labels | `/make-mermaid --lang en` |
| `--lang zh` | Chinese labels (default) | `/make-mermaid --lang zh` |
| `--format svg` | SVG output instead of PNG | `/make-mermaid --format svg` |
| `--bg transparent` | Transparent background | `/make-mermaid --bg transparent` |
| `--scale N` | Custom scale factor | `/make-mermaid --scale 3` |
| `--out <path>` | Custom output directory | `/make-mermaid --out ./images` |

## Examples

**From code analysis:**
```
/make-mermaid 根据项目代码画3个顺序图
/make-mermaid 画出数据库ER图
/make-mermaid Draw class diagram for Models/ --lang en
```

**From description:**
```
/make-mermaid 画一个用户下单的流程图：浏览商品→加入购物车→结算→支付→完成
/make-mermaid 画一个项目甘特图：需求分析2周，开发4周，测试2周
```
