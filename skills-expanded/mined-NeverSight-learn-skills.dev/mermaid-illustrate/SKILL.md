---
name: mermaid-illustrate
description: A comprehensive skill for creating all types of Mermaid diagrams including flowcharts, sequence diagrams, class diagrams, state diagrams, entity relationship diagrams, user journey diagrams, Gantt charts, pie charts, quadrant charts, requirement diagrams, Git graphs, C4 diagrams, mindmaps, timelines, ZenUML, Sankey diagrams, XY charts, block diagrams, packet diagrams, Kanban boards, architecture diagrams, radar charts, and treemaps. Use this skill whenever the user requests to create, draw, or visualize any diagram, flowchart, or structured chart using Mermaid syntax.
version: 1.0.0
author: zhiweio
license: MIT
tags:
  - mermaid
  - diagram
  - visualization
  - flowchart
  - architecture
  - blueprint
  - ibm-carbon
---

## When to use this skill

Use this skill whenever the user wants to create any diagram, flowchart, sequence/class/state diagram, ER diagram, user journey, Gantt chart, pie/quadrant chart, requirement diagram, Git graph, C4 architecture diagram, mindmap, timeline, ZenUML, Sankey, XY chart, block diagram, packet diagram, Kanban board, architecture diagram, radar chart, or treemap — anything Mermaid supports.

## Design methodology: Blueprint (IBM Carbon · C4)

All diagrams follow the **Blueprint** design system — IBM Carbon v11 color tokens combined with C4 model layered thinking. Restrained, semantic, dark-mode ready.

**Core principles**: (1) Semantic coloring — color carries meaning before labels are read (blue = processing, teal = data, amber = decision, green = success, red = error, grey = external). (2) Restrained palette — default to 4–6 colors. (3) Hierarchy first — border weight and color intensity guide the eye. (4) Dark-mode ready. (5) **No emoji** — strictly prohibited in all diagram text; use icons or semantic coloring instead. (6) Icon first — prefer icons from `icon-catalog.md` over text labels.

The full palette, `classDef` templates, `themeVariables` (light/dark), and mindmap-specific variables live in **`examples/design-system.md`** — always load it first when a diagram supports styling. Do not duplicate those definitions here.

## How to use this skill

1. **Identify the diagram type** and load its example file. Each diagram maps to one keyword and one reference file:

   | Request / 中文 | Keyword | Example file |
   |---|---|---|
   | Flowchart / 流程图 | `flowchart` / `graph` | `examples/flowchart.md` |
   | Sequence / 时序图 | `sequenceDiagram` | `examples/sequence.md` |
   | Class / 类图 | `classDiagram` | `examples/class.md` |
   | State / 状态图 | `stateDiagram`(-v2) | `examples/state.md` |
   | Entity relationship / 实体关系图 | `erDiagram` | `examples/er.md` |
   | User journey / 用户旅程图 | `journey` | `examples/journey.md` |
   | Gantt / 甘特图 | `gantt` | `examples/gantt.md` |
   | Pie / 饼图 | `pie` | `examples/pie.md` |
   | Quadrant / 象限图 | `quadrantChart` | `examples/quadrant.md` |
   | Requirement / 需求图 | `requirementDiagram` | `examples/requirement.md` |
   | Git graph / Git图 | `gitGraph` | `examples/gitgraph.md` |
   | C4 / C4图 | `C4Context` / C4 types | `examples/c4.md` |
   | Mindmap / 思维导图 | `mindmap` | `examples/mindmap.md` |
   | Timeline / 时间线图 | `timeline` | `examples/timeline.md` |
   | ZenUML / 禅UML | `zenuml` | `examples/zenuml.md` |
   | Sankey / 桑基图 | `sankey` | `examples/sankey.md` |
   | XY chart / XY图 | `xychart` | `examples/xychart.md` |
   | Block / 方块图 | `block-beta` | `examples/block.md` |
   | Packet / 数据包图 | `packet-beta` | `examples/packet.md` |
   | Kanban / 看板图 | `kanban` | `examples/kanban.md` |
   | Architecture / 架构图 | `architecture-beta` | `examples/architecture.md` |
   | Radar / 雷达图 | `radar-beta` | `examples/radar.md` |
   | Treemap / 树状图 | `treemap-beta` | `examples/treemap.md` |

2. **Load the design system reference first**: `examples/design-system.md` (Blueprint palette, `classDef` templates, `themeVariables`). Load `examples/icon-catalog.md` only when the diagram needs icons.

3. **Load the matching example file** from `examples/` and follow its Blueprint styling and syntax.

4. **Apply Blueprint styling** — but only for directives the diagram type actually supports (see the matrix below). Use the Blueprint palette, never ad-hoc colors. Use semantic class names: `bpProcess`, `bpData`, `bpDecision`, `bpWarning`, `bpSuccess`, `bpError`, `bpExternal`, `bpUser`, `bpInfo`.

5. **Generate valid Mermaid code** wrapped in a Markdown fenced block with the `mermaid` language tag. Always use real syntax, never placeholders. **Save the diagram** to the project directory (default `docs/diagrams/` or `diagrams/`) as a `.md` file, tell the user the path, then display the code block. This wrap-and-save rule applies to every diagram regardless of type.

### Styling support by diagram type

This matrix is the **single source of truth** for which styling directives each diagram type accepts. Apply a directive only where marked; remove it everywhere else.

| Diagram | `classDef`+`class`/`cssClass` | `style` | `linkStyle` | `themeVariables` |
|---------|:---:|:---:|:---:|:---:|
| `flowchart` / `graph` | Yes | Yes | Yes | Yes |
| `stateDiagram` / `stateDiagram-v2` | Yes | Yes | No | Yes |
| `classDiagram` | Yes (`cssClass`) | Yes | No | Yes |
| `erDiagram` | Yes | Yes | No | Yes |
| `requirementDiagram` | Yes | Yes | No | Yes |
| `quadrantChart` | Yes | Yes (per-point) | No | No |
| `treemap-beta` | Yes (`:::` shorthand) | No | No | No |
| `block-beta` | Yes | Yes | No | Yes |
| `sequenceDiagram` | No (use `box` color) | No (use `box`/`rect`) | No | Yes |
| `gantt` | No (use `done`/`active`/`crit`/`milestone`) | No | No | Yes (via frontmatter `themeCSS`) |
| `pie` | No | No | No | Yes |
| `journey` | No | No | No | Yes |
| `gitGraph` | No | No | No | Yes |
| `timeline` | No | No | No | Yes |
| `mindmap` | No (use `:::` shorthand inline) | No | No | Yes (mindmap-specific vars only) |
| `C4Context` / C4 types | No (use `UpdateElementStyle`/`UpdateRelStyle`) | No | No | No |
| `architecture-beta` | No | No | No | No |
| `sankey` | No | No | No | No |
| `xychart` | No | No | No | No |
| `kanban` | No | No | No | No |
| `packet` | No | No | No | No |
| `radar-beta` | No | No | No | No |
| `zenuml` | No | No | No | No |

**Key rules:**
- **`linkStyle` is flowchart/graph ONLY.** Remove it from sequence, class, state, Gantt, and all other diagram types.
- **`classDef` + `class`** is supported only in flowchart, state, class (`cssClass`), ER, requirement, block-beta, treemap-beta (`:::`), and quadrantChart (per-point radius must be ≤ 6). Remove `classDef`/`class` from every other type.
- **`themeVariables`** is supported in flowchart, sequence, state, ER, class, requirement, timeline, journey, Gantt, pie, gitGraph, block, and mindmap (mindmap uses its own `mindmapRootColor`/`mindmapTextColor`/`mindmapMainColor`/`mindmapSecondaryColor`/`mindmapLineColor`; general variables like `primaryColor` have no effect there). For unsupported types, remove the `%%{init: ...}%%` directive.
- **C4** uses its own styling: `UpdateElementStyle()` / `UpdateRelStyle()` — no `classDef`/`linkStyle`/`themeVariables`.
- For diagrams without styling support, convey semantics through naming, structure, or built-in tags (e.g., Gantt's `done`/`active`/`crit`/`milestone`).
- In flowcharts, apply `linkStyle` for flow emphasis: primary flows thicker/blue, data flows teal with dashes.

### Icons and images — pick ONE syntax per diagram

Load `examples/icon-catalog.md` to find the right icon (600+ pre-listed icons across 6 sets). Then choose syntax by registration state — **do not mix the two in one diagram**:

- **Icon packs registered** (self-hosted / bundler / mkdocs) → icon-pack syntax: flowchart `@{ icon: "pack:icon-name", form: "square", label: "Label", pos: "t", h: 60 }` (only set `h`, minimum 48); architecture-beta `service id(pack:icon-name)[Label]`.
- **Icon packs NOT registered** (mermaid.live / GitHub / no setup) → remote-URL fallback, works everywhere: `@{ img: "https://api.iconify.design/{prefix}/{icon-name}.svg", label: "Label", pos: "b", h: 48, constraint: "on" }`.
- **Aspect-ratio rule**: never set both `w` and `h` — it stretches non-square icons. Set only `h` and enable `constraint: "on"`. SVG URL pattern: `https://api.iconify.design/{prefix}/{icon}.svg`.

The canonical 6-pack registration snippet (logos, skill-icons, devicon, codicon, gcp, vscode-icons) and FontAwesome notes live in **`examples/icon-catalog.md`**. The three icon approaches for architecture diagrams are in `examples/architecture.md`.

6. **Validate** the syntax: required elements present, relationships and connections properly defined, date formats correct for Gantt, data formats correct for pie/quadrant/etc.

If the request matches no example, refer to the [Mermaid documentation](https://mermaid.js.org/) or ask the user for clarification on the desired visualization.

## Keywords

mermaid, diagram, flowchart, flow chart, sequence diagram, class diagram, state diagram, entity relationship, ER diagram, user journey, Gantt chart, pie chart, quadrant chart, requirement diagram, Git graph, C4 diagram, mindmap, timeline, ZenUML, Sankey diagram, XY chart, block diagram, packet diagram, Kanban, architecture diagram, radar chart, treemap, icon pack, iconify, devicon, codicon, aws icons, cloud architecture, 流程图, 时序图, 类图, 状态图, 实体关系图, 用户旅程图, 甘特图, 饼图, 象限图, 需求图, Git图, C4图, 思维导图, 时间线图, 桑基图, XY图, 方块图, 数据包图
