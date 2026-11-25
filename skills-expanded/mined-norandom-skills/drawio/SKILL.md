---
name: drawio
version: 1.0.1
description: >-
  Create draw.io diagrams through MCP using Mermaid, XML, or CSV. Use for
  general diagram requests, Mermaid-to-draw.io rendering, and executive or
  boardroom styling. Includes tool selection, XML checks, and Hermes link
  presentation. For domain-specific analysis, use the relevant specialist skill.
---

# Draw.io Diagram Creation

General-purpose draw.io diagramming via MCP tools. For domain-specific diagram types, load the
relevant skill first (intana-viz for intelligence analysis, architecture-diagram for cloud/infra).
For the executive/boardroom Gartner-style palette, see the Domain-Specific Palettes section below.

## Available MCP Tools

| Tool | Best For | Output |
|---|---|---|
| `mcp_drawio_open_drawio_mermaid` | Flows, trees, sequences, state diagrams | Mermaid.js rendered in draw.io |
| `mcp_drawio_open_drawio_xml` | Spatial layouts, matrices, precise positioning | Native draw.io XML (mxGraphModel) |
| `mcp_drawio_open_drawio_csv` | Tabular data to diagram conversion | draw.io from CSV |
| `mcp_drawio_get_mermaid_reference` | Look up Mermaid syntax | Reference doc (call before mermaid tool) |
| `mcp_drawio_get_xml_reference` | Look up XML styles, shapes, edge routing | Reference doc (call before XML tool) |

### CRITICAL: Call Reference Tools Before Generating

- **Before `open_drawio_mermaid`**: call `get_mermaid_reference` if unsure about syntax for a specific diagram type. Covers all 26 supported Mermaid types.
- **Before `open_drawio_xml`**: ALWAYS call `get_xml_reference` first. Don't skip it — the XML reference is the source of truth for styles, shapes, edge routing rules, containers, layers, and the full property table. It returns ~30KB of Markdown.
- **Before `open_drawio_csv`**: avoid CSV unless explicitly requested — it's unreliable. Prefer Mermaid for org charts and hierarchies.

### Reference Files

| File | Content |
|---|---|
| `references/xml-checklist.md` | Pre-flight checklist for XML generation (shadow=1, unescaped &, edge geometry, XML comments, etc.) |
| `references/gartner-palette.md` | Gartner-style risk palette: colors for Critical/High/Medium/Positive/Warning |
| `references/blindspot-pattern.md` | Blindspot-from-Premortem diagram pattern: hidden assumption → cascading failures → process assumptions |

## URL Presentation in Hermes WebUI (CRITICAL)

Draw.io URLs embed the entire diagram source in the URL fragment (`#create=` with `%`-encoded
JSON). These URLs are very long (often thousands of characters).

**Always present the bare URL on its own line.** Do NOT use Markdown's labeled-link
form (bracketed display text followed by a parenthesized URL). The WebUI's Markdown renderer can mangle long URLs containing `%` escapes and
`#` fragments, producing broken links the user cannot open.

```
https://draw.because-security.com/?grid=0&pv=0&border=10&edit=_blank#create=%7B...
```

The WebUI auto-linkifies bare URLs. This avoids all Markdown rendering corruption.

When the user explicitly asks for "a clickable link" or "just give me the link," give them
ONLY the bare URL — no surrounding analysis text, no table, no prose. They asked for the
diagram link, not an essay. After presenting the URL, mention what the diagram shows in
1-2 lines only.

### Verification

After generating a diagram URL, curl-verify it returns 200:
```
curl -s -o /dev/null -w "%{http_code}" "<URL>"
```
If the URL returns 200 server-side but the user reports it's broken, the problem is in the
WebUI's Markdown rendering, not the URL itself.

## Mermaid Quick Reference

Call `mcp_drawio_get_mermaid_reference` before generating Mermaid diagrams. Key reminders:

- **Direction:** `TD`/`LR`/`RL`/`BT`
- **Node shapes:** `[rect]`, `(rounded)`, `{rhombus}`, `((circle))`, `[(cylinder)]`
- **Edges:** `-->` arrow, `---` no arrow, `-.->` dotted, `==>` thick
- **Subgraphs:** `subgraph ID["Label"] ... end`
- **Styling:** `style NODE fill:#xxx,stroke:#xxx,color:#xxx`
- **Classes:** `classDef name fill:#xxx; class A,B name`
- **Quotes:** Use `\"` for labels with special characters (colons, parens)
- **No trailing punctuation on node IDs**

## When to Prefer XML Over Mermaid

- Precise coordinates / custom positions
- draw.io-native shapes (AWS, Azure, GCP, Cisco)
- Mixed shape libraries or complex multi-layer diagrams
- Anything needing exact per-element color variations at scale
- Diagrams that will be extensively edited in draw.io after generation

## Domain-Specific Palettes

### Boardroom / Executive Palette (Gartner-Inspired)

For executive, compliance, and boardroom diagrams use a darker, more severe palette — authoritative navy, deep burgundy, rich amber — instead of default analytical colors. The Gartner look signals "sober risk analysis" rather than "collaborative workshop output."

Always load `intana-viz` first for the technique catalog and diagram templates. This palette is a styling layer on top.

**Trigger:** User says "business theme", "Gartner look", "executive style", "boardroom-ready", or audience is a board/C-suite/compliance committee/external regulator.

**Color scheme** (full spec in `references/gartner-palette.md`):

| Role | Fill | Stroke | Text | Detail Text |
|---|---|---|---|---|
| Background | `#F8FAFC` | — | — | — |
| Title | — | — | `#0F172A` (16pt bold) | — |
| Central node | `#0F172A` | `#020617` | `#FFFFFF` | near-black navy |
| Critical | `#991B1B` | `#7F1D1D` | `#FFFFFF` | deep burgundy; detail `#FECACA` |
| High | `#B45309` | `#92400E` | `#FFFFFF` | rich amber; detail `#FDE68A` |
| Medium | `#6D28D9` | `#5B21B6` | `#FFFFFF` | deep violet; detail `#DDD6FE` |
| Low | `#64748B` | `#475569` | `#FFFFFF` | slate |
| Positive/Safe | `#D1FAE5` | `#059669` | `#047857` | (rarely used in boardroom context) |
| Warning | `#FEF3C7` | `#F59E0B` | `#B45309` | (rarely used in boardroom context) |
| Edges | — | `#94A3B8` (1.5pt) | — | no arrowheads |
| Legend border | — | `#E2E8F0` (1pt) | — | — |

Note: `shadow=1` is desirable on primary nodes for the executive look, but shadows in complex XML can cause "invalid distance too far back" decompression errors. See the XML Generation pitfall below — use single-line labels on first render, add details later.

**Key difference from default analytical palette:** Darker and more severe. No bright red (`#DC2626`), no bright green (`#059669`). Every color reads as a severity tier descending from critical to low. The central node uses near-black navy instead of dark slate.

**Diagram types commonly used with this palette:** Pre-Mortem Analysis, Key Assumptions Check, If/Then Analysis, Four Ways of Seeing (2×2), High Impact/Low Probability (2×2), Analysis of Competing Hypotheses (ACH).

## Common Pitfalls

### XML Generation
Before generating XML, run through `references/xml-checklist.md` — every item is a blocker the server will reject.

**Most common XML failure:** `shadow=1` on nodes → "invalid distance too far back" error. Remove `shadow=1` from ALL nodes and regenerate with plain-text values only.

**Boardroom palette decompression failure:** Complex XML with many HTML-escaped labels, long detail text, or deep nesting can produce a compression blob that fails decompression server-side. **Fix:** Regenerate with simpler labels — remove `<br>` detail lines, keep labels to 1-2 words per node, strip `<font>` subtags. The diagram structure and palette stay the same; only label complexity is reduced. Add detail text in draw.io's editor after opening. **Prevention:** For first render, use single-line labels with no HTML escaping. Add detail text in a second pass only after the diagram opens successfully.

### Mermaid Generation
- **Cause:** Misspelled diagram type keyword (e.g., `flowchart` vs `flowchrt`)
- **Fix:** Check the type keyword — draw.io supports 26 types: `flowchart`, `sequenceDiagram`,
  `classDiagram`, `stateDiagram-v2`, `erDiagram`, `gitGraph`, `journey`, `pie`, `gantt`,
  `mindmap`, `timeline`, `quadrantChart`, `requirementDiagram`, `sankey-beta`, `xychart-beta`,
  `block-beta`, plus C4 and architecture variants
