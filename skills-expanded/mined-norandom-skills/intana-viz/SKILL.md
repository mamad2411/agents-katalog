---
name: intana-viz
version: 1.0.1
description: >
  Visualize intelligence analysis and structured analytic techniques in draw.io.
  Use for hypothesis comparison, argument maps, decision or risk matrices,
  stakeholder analysis, assumption checks, premortems, wargaming, and root-cause
  diagrams. Selects from 80+ techniques when the user needs an analytical visual,
  even without naming the technique.
---

# Intelligence Analysis Visualization Skill

Create intelligence analysis visualizations using the draw.io MCP tools. Each visualization opens directly in draw.io where the user can view, edit, export, and share.

## When to Read the References

Before generating any visualization:
1. Read `references/technique-catalog.md` to find the matching technique and its recommended diagram type.
2. Read `references/diagram-templates.md` to get the exact layout spec (canvas size, node positions, colors, style strings) for that diagram type. Follow the template precisely to ensure visual consistency across all diagrams.

## Available draw.io Tools

Three MCP tools are available. Choose the best fit for each technique:

### 1. `mcp__drawio__open_drawio_xml` (Primary — use for most techniques)
Generates draw.io XML (mxGraphModel format). This is the most flexible option — supports precise positioning, custom shapes, colors, containers, layers, and complex layouts. Use this for:
- 2×2 matrices and quadrant diagrams (Prioritisation Map, Four Ways of Seeing, Opportunity Matrix)
- Hub-and-spoke diagrams (Pre-Mortem, Failure Causation)
- Network diagrams (Burke-Litwin, Cultural Web, Blindspots)
- Radar-like scored displays (Devil's Advocacy, 12R Model)
- Any diagram requiring precise spatial layout or color-coding

### 2. `mcp__drawio__open_drawio_mermaid` (Flowcharts and sequences)
Generates Mermaid.js syntax. Best for:
- Process flows (Red Teaming phases, What/So What/Now What)
- Decision trees and branching logic (If/Then Analysis)
- Timeline sequences (String of Pearls, Critical Path)
- Hierarchical trees (Argument Mapping, Five Whys, Negative Brainstorming)
- State diagrams (Piaget's Learning Cycle, OODA loops)

### 3. `mcp__drawio__open_drawio_csv` (Structured tabular data)
Generates diagrams from CSV. Best for:
- Org-chart style hierarchies
- Simple relationship diagrams from tabular data
- Resource Checklists and structured matrices when data is already tabular

## Core Principles

1. **One technique, one diagram.** Each visualization is a single draw.io diagram opened via one tool call.
2. **Choose the right tool.** XML for spatial layouts and precise styling. Mermaid for flows and trees. CSV for tabular-to-diagram conversion.
3. **Professional analytic styling.** Use muted, intelligence-grade colors. Never use bright/playful colors.
4. **Labels carry meaning.** Since draw.io diagrams are static (no hover tooltips like code), encode all important information in node labels, annotations, and color legends.
5. **Include a legend.** Add a legend box explaining color codes, shape meanings, and scoring scales.

## Color Palette

Use these hex colors consistently in draw.io styles:

```
Background:  #F8FAFC (light slate)
Card/Node:   #FFFFFF (white fill)
Border:      #334155 (slate-700)
Text:        #334155 (slate-700)
Accent:      #2563EB (blue-600) — interactive elements, primary highlights
Supporting:  #059669 (emerald-600) — positive, supporting, "Do It Now"
Warning:     #F59E0B (amber-500) — caution, assumptions, "Park for Later"
Critical:    #DC2626 (red-600) — risks, contradicting, "Discard"
Neutral:     #64748B (slate-500) — deprioritise, secondary items
Highlight:   #8B5CF6 (violet-500) — neutral/uncertain items
```

Apply colors via the `fillColor`, `strokeColor`, and `fontColor` style attributes in XML.

## Input Handling

### Structured Data
When the user provides scores, lists, or formatted data, map directly to diagram elements.

### Raw Text / Analyst Notes
When the user provides unstructured text:
1. Extract entities, relationships, and data points
2. Briefly show the user what was extracted so they can correct misinterpretations
3. Generate the diagram

## Technique-to-Diagram Mapping

### Matrix / Quadrant Diagrams (XML)
**Use for:** Prioritisation Map, Four Ways of Seeing, Problem Solving Strategies, Signal Detection, Opportunity Matrix (Ansoff).

**Pattern:** Draw the 2×2 grid using four large colored rectangles as quadrant backgrounds. Add axis labels as text elements. Place items as rounded rectangles positioned within their quadrant based on scores. Add a title and legend.

**XML structure:**
- Four background rectangles (one per quadrant, colored by action: green=Do Now, blue=Park Later, grey=Deprioritise, red=Discard)
- Axis lines as edges with labels
- Items as styled rounded-rectangle nodes placed at approximate x,y within their quadrant
- Legend as a grouped container in the corner

### Hub-and-Spoke Diagrams (XML)
**Use for:** Pre-Mortem, Failure Causation, Stakeholder Analysis.

**Pattern:** Central circle node with radiating edges to spoke nodes arranged in a circle. Color spokes by severity/category. Add detail text as labels or attached notes.

### Hierarchical Trees (Mermaid)
**Use for:** Argument Mapping, Five Whys, Negative Brainstorming, Spiderweb Chart.

**Pattern:** `graph TD` (top-down) tree. Color-code nodes using Mermaid class definitions. Supporting evidence in blue, contradicting in red, assumptions in amber.

**Mermaid example:**
```
graph TD
    H[Hypothesis X] --> S1[Supporting: Evidence A]
    H --> S2[Supporting: Evidence B]
    H --> C1[Contradicting: Evidence C]
    classDef support fill:#059669,color:#fff
    classDef contradict fill:#DC2626,color:#fff
    class S1,S2 support
    class C1 contradict
```

### Process Flows (Mermaid)
**Use for:** Red Teaming phases, What/So What/Now What, Task Analysis, CoA Phasing.

**Pattern:** `graph LR` (left-to-right) or `graph TD` flow. Use subgraphs for phases. Decision diamonds for branching.

### Sequential Chains (Mermaid)
**Use for:** String of Pearls, Critical Path, Adversary Wargaming.

**Pattern:** `graph LR` linear chain with numbered nodes. Highlight critical path nodes with a distinct style class. Add risk annotations as note nodes.

### Circular / Cycle Diagrams (Mermaid)
**Use for:** Piaget's Learning Cycle, Situation-Cues-Patterns-Actions, OODA loops.

**Pattern:** `graph LR` with the last node connecting back to the first, creating a visual cycle. Or use XML for more precise circular layout.

### Comparison Matrices (XML)
**Use for:** CoA Comparison, Resource Checklist, If/Then Analysis, Devil's Advocacy scorecard.

**Pattern:** Table-like layout using draw.io container shapes. Header row with criteria, data rows with colored cells for RAG scoring (Red/Amber/Green). Or use a series of labeled bar-segments for scoring.

### Scored Assessments (XML)
**Use for:** Devil's Advocacy (5Cs + CATUR), 12R Model, Weisbord's Six Box.

**Pattern:** Since draw.io can't render radar charts natively, use a horizontal bar-chart layout: one bar per dimension, filled proportionally and color-coded. Add numeric labels. Group related dimensions (e.g., 5Cs group and CATUR group).

### Organizational Models (XML)
**Use for:** Burke-Litwin, Leavitt's Diamond, McKinsey 7S, Cultural Web.

**Pattern:** Use positioned shapes matching the model's canonical layout (diamond for Leavitt's, star/wheel for 7S, web for Cultural Web). Connect with bidirectional arrows. Label each element with assessment details.

## Handling Ambiguous Requests

When the user's request doesn't clearly map to a single technique:

1. Check `references/technique-catalog.md` for the closest match
2. If multiple techniques apply, briefly explain the options and recommend the best fit
3. If the request is a general concept (e.g., "show me the risks"), ask which analytical structure they want

## Cross-skill handoff

Structured analysis often sits inside another workflow. Preserve the user's context when routing:

- For `game-theory-negotiation`, send hypotheses, assumptions, deception risks, candidate strategies, and confidence levels. Good fits: ACH for why a party is behaving a certain way, Red Teaming for the other side's likely moves, Pre-Mortem for deal failure, and Key Assumptions Check for BATNA or payoff estimates.
- For `strategic-foresight-viz`, send the external drivers and uncertain futures that need scenario work.
- For `investigation-theory`, send claims that need evidence, sources to check, contradictions, and open questions.

When drawing cross-functional work in draw.io, keep actor names, claim IDs, scenario names, and option names stable. A user should be able to compare an ACH matrix, a futures cone, an investigation timeline, and a payoff matrix without translating labels.

## Output

Call the appropriate draw.io MCP tool directly. The diagram opens in the user's draw.io editor where they can view, edit, rearrange, and export to PNG/SVG/PDF.

After opening the diagram, briefly explain what it shows and how the user can modify it in draw.io.
