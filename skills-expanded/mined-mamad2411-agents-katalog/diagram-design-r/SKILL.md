---
name: diagram-design-r
description: Create branded architecture, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, swimlane, quadrant, radar/spider, polar chart, loop/flywheel, nested, tree, org chart, layer stack, Venn, pyramid/funnel, treemap, bar, line, Gantt, scatter, high-level, process, medallion, data flow, DP integration, DP security matrix, Sankey, fishbone, Wardley map, kanban, user journey, deployment, dependency graph, UML class, story map, or database schema diagrams as standalone HTML/SVG/PNG. Redraw .drawio or Mermaid sources; onboard brand tokens from a website.
license: Adapted from cathrynlavery/diagram-design (MIT)
metadata:
  version: "1.0"
  skill-author: ResearchCraft
  source: https://github.com/cathrynlavery/diagram-design
---

# Diagram Design (ResearchCraft Edition)

Create visual diagrams as self-contained HTML files with inline SVG and CSS, following an opinionated editorial design system.

Thirty-nine visual types. Semantic patterns describe behavior independently; type references describe layout.

## Philosophy

**The highest-quality move is usually deletion.**

- Every node represents a distinct idea. Two nodes that always travel together are one node.
- Every connection carries information. If the relationship is obvious from layout, remove the line.
- Coral is **editorial, not a flag.** 1–2 focal nodes per diagram. Using it on 5 nodes erases the signal.
- The schematic isn't done when everything is added. It's done when nothing can be removed.

**Target density: 4/10.** Enough to be technically complete. Not so dense it needs a guide. Above 9 nodes, it's probably two diagrams.

## When to use

Use for any of the 39 visual types when a reader will learn more from a visual than from prose, a table, or a bulleted list.

**Don't use for:**
- Quick unicode diagrams
- Lists of things → table or bullets
- Simple before/after → table
- One-shape "diagrams" → just write the sentence

Before drawing, ask: _Would the reader learn more from this than from a well-written paragraph?_ If no, don't draw.

## Selection: semantic pattern, then visual type

When behavior, state, enforcement, or risk carries the meaning, first choose a semantic pattern, then the nearest visual type for layout.

| Behavioral trigger | Semantic pattern → nearest type |
| --- | --- |
| Fan-in, queue depth, bottleneck | Fan-in queue / bottleneck → Data flow |
| Repeated Question/Input/Governance/Output slots | Stage framework with semantic slots → Process |
| Conversation becomes structured artifact | Unstructured input → structured artifact → Data flow |
| Trust boundaries plus permitted/forbidden paths | Secure paved road → Architecture |
| Controls grouped by enforcement location | Governance / control catalog → Layer stack |

## Visual-type guide (39)

| If you're showing… | Use |
| --- | --- |
| Components + connections in a system | Architecture |
| Legacy IT landscape grouped by phase/department | IT current-state |
| Decision logic with branches | Flowchart |
| Time-ordered messages between actors | Sequence |
| States + transitions + guards | State machine |
| Entities + fields + relationships | ER / data model |
| Events positioned in time | Timeline |
| Cross-functional flow | Swimlane |
| Two-axis positioning | Quadrant |
| Multi-axis comparison | Radar / spider |
| Cyclic magnitude · linear radius | Polar chart |
| Reinforcing cycle + shared hub | Loop / flywheel |
| Hierarchy by containment | Nested |
| Parent → children | Tree |
| Ownership + routing | Org chart |
| Stacked abstractions | Layer stack |
| Set overlap | Venn |
| Ranked hierarchy or drop-off | Pyramid / funnel |
| Part-of-whole by area | Treemap |
| Categorical comparison | Bar chart |
| Trends over time | Line chart |
| Tasks + phases on a timeline | Gantt |
| Distribution + correlation | Scatter plot |
| End-to-end stack on a cluster | High-Level |
| Multi-actor sequential workflow | Process |
| Multi-tier data storage | Medallion |
| Role-scoped pipeline steps | Data flow |
| Sources → core → consumers | DP integration |
| Per-role access permissions | DP security matrix |
| Quantities that split + merge | Sankey |
| Grouped causes → one effect | Fishbone |
| Value chain × evolution | Wardley map |
| Work in progress by state | Kanban |
| Stages, actions + sentiment | User journey |
| Zones, hosts + artifacts | Deployment |
| Fan-in, ranks + cycles | Dependency graph |
| Classes, operations + typed relations | UML class |
| Backbone × release slices | Story map |
| Physical tables + column FKs | Database schema |

## Output

Always produce a single self-contained `.html` file:
- Embedded CSS (no external except Google Fonts)
- Inline SVG (no external images)
- Static by default; minimal inline JavaScript only for explicit animation controls

### Accessible SVG contract

1. `<svg>` carries `role="img"` and `aria-labelledby` naming the diagram's `<title>` and `<desc>`.
2. `<title>` is the first child of `<svg>`, before `<defs>`.
3. IDs prefixed per diagram and variant: `<slug>-title` / `<slug>-desc`.
4. `<title>` is the short name of the subject (~60 chars or fewer).
5. `<desc>` is one sentence stating what the diagram shows in terms a reader needs without the image.

## Brand onboarding

Out of the box, diagrams render in jet-black + atomic-tangerine palette (white-smoke paper, jet-black ink, atomic-tangerine accent, blue-slate muted, silver hairlines).

For branded output, extract tokens from a website:
- `<body>` background → `paper` token
- Primary text color → `ink` token
- Secondary / caption text → `muted` token
- Most-used brand color (CTA, link, heading) → `accent` token
- `<h1>` font family → `title` font
- `<body>` font family → `node-name` font

## Exporting to PNG / SVG

When the user asks to export, save the diagram as `.png` or `.svg`. Both formats deliver the diagram only (the `<svg>` node) — editorial wrappers like cards and headers are dropped by design. Export is **manual** — never produce export files unprompted.

## Related files

| File | Open when |
| --- | --- |
| `references/style-guide.md` | Default tokens and customization |
| `references/onboarding.md` | Brand extraction workflows |
| `references/semantic-patterns.md` | Behavior-driven pattern selection |
| `references/animation.md` | When motion clarifies ordered change |
| `references/export.md` | PNG/SVG export procedures |

## Attribution

This skill adapts conventions from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (31.7k stars, MIT license).
