---
name: strategic-foresight-viz
version: 1.0.1
description: >
  Create strategic foresight and futures-analysis diagrams through draw.io MCP.
  Use for PESTLE scans, trend matrices, weak-signal maps, scenario planning,
  futures cones, and VUCA/CATUR assessments. Selects from 24 foresight techniques.
  Route hypothesis, organizational, and decision-analysis visuals such as ACH,
  Cultural Web, and Pre-Mortem to intana-viz.
---

# Strategic Foresight Visualization Skill

Create strategic foresight and futures analysis visualizations using draw.io MCP tools. Each visualization opens directly in draw.io for viewing, editing, and export.

## Before Generating Any Visualization

1. Read `references/technique-catalog.md` to find the matching technique and its recommended diagram type.
2. Read `references/diagram-templates.md` to get the exact layout spec (canvas size, node positions, colors, style strings) for that diagram type. Follow the template precisely for visual consistency.
3. Read `references/use-cases.md` if the user needs help choosing the right technique for their foresight assessment.

## Available draw.io Tools

### 1. `mcp__drawio__open_drawio_xml` (Primary — most techniques)
Generates draw.io XML (mxGraphModel format). Supports precise positioning, custom shapes, colors, containers, layers. Use for:
- Environmental scanning matrices (PESTLE/GRNO)
- Trend stage matrices (Impact × Lifecycle)
- Cross-impact tables (Trend-on-Trend, What If/Then)
- Scored assessments (VUCA, CATUR)
- Hub-and-spoke diagrams (Perception Analysis)
- Futures Cone (concentric arcs)
- Dator's Archetypes (2×2 quadrant)
- Comparison tables (Three Futures, Analogical Reasoning)

### 2. `mcp__drawio__open_drawio_mermaid` (Flows and trees)
Generates Mermaid.js syntax. Best for:
- Process flows (Lum's Four Steps, What/So What/Now What)
- Decision trees and branching logic (If/Then chains)
- Hierarchical analysis (Macro/Meso/Micro decomposition)
- Stakeholder trees

### 3. `mcp__drawio__open_drawio_csv` (Tabular data)
Generates diagrams from CSV. Best for:
- Org-chart style hierarchies
- Simple relationship diagrams from tabular data

## User Inquiry Protocol

Before creating any diagram, ask the user for the specific data required by that technique. Each technique in the catalog lists the exact fields to inquire about. This ensures diagrams contain real analytical content rather than placeholder data.

**General inquiry pattern:**
1. Confirm the technique (or help them choose one using `references/use-cases.md`)
2. Ask for the data fields specific to that technique (listed in the catalog)
3. If the user provides unstructured text, extract entities and data points, show the extraction for confirmation, then generate

## Color Palette

Use these hex colors consistently across all diagrams:

```
Background:  #F8FAFC (light slate)
Card/Node:   #FFFFFF (white fill)
Border:      #334155 (slate-700)
Text:        #334155 (slate-700)
Accent:      #2563EB (blue-600) — primary highlights, current trends
Supporting:  #059669 (emerald-600) — positive outcomes, best case, opportunities
Warning:     #F59E0B (amber-500) — caution, emerging trends, likely case
Critical:    #DC2626 (red-600) — risks, worst case, collapse scenarios
Neutral:     #64748B (slate-500) — established trends, secondary items
Highlight:   #8B5CF6 (violet-500) — transformation, wildcards, uncertain
Grid/Axis:   #CBD5E1 (slate-300)
```

## Technique-to-Diagram Quick Reference

All 24 techniques from `references/technique-catalog.md`. For full layout specs, color mapping, and required input fields, read the catalog before generating.

| Technique | Diagram Type | Tool |
|-----------|-------------|------|
| PESTLE / GRNO Scan | Multi-Column Matrix | XML |
| Macro / Meso / Micro Analysis | Three-Row Layered Matrix | XML |
| Trend Stage Analysis | Quadrant / 2×2 Matrix | XML |
| Trend Impact Analysis (Layered) | Comparison Table | XML |
| Trend Impact Analysis (Temporal) | Comparison Table | XML |
| Trend-on-Trend Cross-Impact | 5×5 Cross-Impact Matrix | XML |
| Countertrends & Cycles | Comparison Table | XML |
| Threat / Opportunity Analysis | Comparison Table | XML |
| Perception Analysis (See / Hear / Think / Feel) | Hub-and-Spoke | XML |
| What / So What / Now What | Process Flow | Mermaid |
| Weak Signal Analysis I | Comparison Table | XML |
| Weak Signal Analysis II | Comparison Table | XML |
| Three Futures (Best / Likely / Worst) | Three-Column Comparison | XML |
| Futures Cone | Concentric Arcs / Cone | XML |
| Dator's Four Archetypes | Quadrant / 2×2 Matrix | XML |
| Intuitive Logics | Quadrant + Comparison Table | XML |
| Lum's Four Steps to the Future | Sequential Process Flow | Mermaid |
| Layered Timeline (Lum) | Multi-Row Swimlane | XML |
| VUCA Analysis | Scored Assessment Matrix | XML |
| CATUR Analysis | Scored Assessment Matrix | XML |
| What If / Then Cross-Impact | Cross-Impact Matrix | XML |
| Consequence Analysis | Comparison Table | XML |
| Analogical Reasoning | Two-Column Comparison | XML |
| Stakeholder Analysis (Lum) | Hub-and-Spoke or Comparison Table | XML |

## Input Handling

### Structured Data
When the user provides scores, lists, or formatted data, map directly to diagram elements.

### Raw Text / Analyst Notes
When the user provides unstructured text:
1. Extract entities, relationships, and data points
2. Show the user what was extracted for confirmation
3. Generate the diagram

### Multiple Techniques
If the analysis requires multiple diagrams (e.g., a full foresight cycle), generate them sequentially, one tool call per diagram.

## Output

Call the appropriate draw.io MCP tool directly. The diagram opens in the user's draw.io editor. After opening, briefly explain what the diagram shows and how to modify it in draw.io.

## Fallback when draw.io MCP is unavailable

If `mcp__drawio__open_drawio_xml` / `..._mermaid` / `..._csv` are not registered, render the diagram as **Mermaid markdown** inside a fenced ```` ```mermaid ```` block in chat. Tell the user they can paste it into Typora, Obsidian, or VS Code with the "Markdown Preview Mermaid Support" extension. Many of the foresight techniques in this catalog rely on precise spatial layout (cones, swimlanes, 2×2 quadrants with named cells, multi-panel matrices) that Mermaid renders only approximately — emit the closest Mermaid equivalent (`flowchart`, `quadrantChart`, `gantt`, or simple grouped subgraphs) and call out the lost styling so the user knows the artifact is provisional. Do **not** write `.drawio` XML files to disk as a fallback.

## Routing to intana-viz

This skill owns the foresight catalog (24 techniques across the 7 categories listed in `references/technique-catalog.md`). When the user asks for an analytic technique outside that scope — ACH, Pre-Mortem, Red Teaming, Cultural Web, McKinsey 7S, Six Thinking Hats, Futures Wheel, Fishbone, Five Whys, Argument Mapping, etc. — hand off to the **intana-viz** skill instead of improvising. intana-viz has 80+ techniques catalogued with the same draw.io styling conventions.

Rule of thumb: if the request is about *anticipating the future* (trends, scenarios, weak signals, foresight assessments, environmental scans), stay here. If it is about *analyzing a hypothesis, decision, organization, or argument*, route to intana-viz. Some techniques sit at the boundary (What If / Then, Stakeholder Analysis) — this skill owns the foresight-flavored variants; intana-viz owns the intelligence-analysis variants.

## Cross-skill handoff

When foresight feeds another skill, export a compact context packet instead of a prose recap:

- Scenarios: best, likely, worst, wildcard, or named archetypes.
- Drivers: trends, weak signals, constraints, and timing.
- Assumptions: what must be true for each scenario.
- Early warnings: what evidence would move the user from one scenario to another.
- Decision impact: which options, payoffs, or risks change under each scenario.

Use this packet with `game-theory-negotiation` when a future condition changes BATNA, ZOPA, reservation price, a concession plan, or a payoff matrix. Use it with `investigation-theory` when a scenario depends on whether another party's claim is true. Use it with `intana-viz` when the scenario rests on contested assumptions that need ACH, Red Teaming, Key Assumptions Check, or Pre-Mortem analysis.
