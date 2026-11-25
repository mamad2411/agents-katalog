---
name: graphviz-ai
description: >
  Guide for working with the graphviz_master AI integration — DotGenerator, LayoutPlanner, VisionClient,
  and validation pipeline — plus a strict-layout-rules diagram mode. Use this skill whenever working on
  graphviz_master AI features, troubleshooting API authentication (including Claude Code OAuth tokens from
  ~/.claude/.credentials.json), modifying the generation or vision pipelines, debugging rate limit / retry
  behavior, or using the layout research knowledge base. Also use when the user mentions DOT generation,
  diagram AI, layout research, layout planning, structured diagram input, or vision analysis. ALWAYS use it
  when the user asks for an architecture/flow diagram with layout rules — straight or right-angle arrows,
  orthogonal routing, "no overlapping/crossing elements", arrows centered on containers or ports, spacing
  between arrows, minimum/readable text size, or complaints that a diagram is too spaced-out or its text
  too small — even if they don't say "graphviz": it has the ortho-port pitfalls and the hand-routed
  SVG generator with a rule audit that those requests need. Also use it when the user wants one of these
  diagrams exported or converted to PowerPoint/pptx (or "editable in PowerPoint"), a high-resolution PNG
  (--scale), or asks to re-render an existing strict-diagram spec JSON — the converters live in this skill.
---

# Graphviz AI Integration

AI-powered diagram generation, validation, and layout research system in `graphviz_master/`.

## Architecture Overview

```
User Request (text or InputGraph JSON)
    |
    v
LayoutPlanner (NEW)                   DotGenerator                    VisionClient
(layout_planner.py)                   (dot_generator.py)              (vision_client.py)
    |                                     |                               |
    v                                     v                               v
Compute deterministic                 Build prompt from:              Encode image (base64)
constraints from:                       - layout type + plan           + analysis prompt
  - InputGraph nodes/edges              - content description              |
  - Knowledge base profiles             - style guide                      v
  - Auto-detect layout type             - design profile               Claude Vision API
    |                                   - layout plan constraints      claude-opus-4-6
    v                                     |                            max_tokens: 1024
LayoutPlan                                v                               |
  - rankdir, spacing                  Claude Messages API                 v
  - node sizes, clusters              claude-opus-4-6                Parse JSON → ~30 properties
  - rank constraints                  max_tokens: 4096               → ExtractedProperties
  - invisible edges                       |                               |
    |                                     v                               v
    +--→ injected as constraints      Clean response (strip fences)   LayoutResearchDB
         in prompt                        |                           → KnowledgeBase
                                          v                           → DesignProfile
                                    Validate (2-tier):
                                      T1: StaticValidator (syntax, fonts)
                                      T2: SVGAnalyzer (ratio, overlap)
                                          |
                                          v (if issues found)
                                    Retry with violation feedback
                                    (max 2 retries)
```

## Component 1: LayoutPlanner (NEW)

**File:** `graphviz_master/layout_planner.py`

Computes deterministic DOT constraints BEFORE sending to AI. Prevents AI hallucination on structural decisions.

### Data Structures

```python
InputNode(id, label, group=None, shape=None)
InputEdge(source, target, label=None, style=None)
InputGraph(nodes, edges, title=None, layout_type=None)
```

### 7-Step Planning Algorithm

1. **Resolve layout type** — auto-detect from graph topology if not specified
2. **Direction & strategy** — linear, multi-column, clustered, swimlane
3. **Node sizing** — width/height computed from text content length
4. **Spacing** — ranksep/nodesep from knowledge base statistical profiles
5. **Rank ordering** — crossing minimization via topological analysis
6. **Cluster planning** — subgraph grouping with 8-color palette rotation
7. **Invisible edges** — structural helpers for alignment

### Output

`LayoutPlan.to_prompt_constraints()` → mandatory DOT constraints injected into the AI prompt.

## Component 2: DotGenerator

**File:** `graphviz_master/dot_generator.py`

### API Call

```python
response = self._client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    system=SYSTEM_PROMPT,  # DOT syntax rules, Segoe UI font
    messages=[{"role": "user", "content": prompt}],
)
```

### Generation Pipeline

1. Load design profile from `knowledge_base.json` via `KnowledgeBase.to_prompt_context(layout_type)`
2. Load layout preset from `config.py` — rankdir, target aspect ratio, spacing
3. **Optionally compute LayoutPlan** via LayoutPlanner when `InputGraph` is provided
4. Build prompt: layout type + content + style guide + design profile + layout constraints
5. Call API → clean response (strip markdown fences)
6. **Validate** through 2-tier pipeline: StaticValidator → SVGAnalyzer
7. **Retry on failure** — feeds violation messages back to Claude (max 2 retries)

### 4 Style Guides

`modern` (clean, minimal), `corporate` (professional, navy), `minimal` (whitespace), `colorful` (vibrant)

## Component 3: VisionClient

**File:** `graphviz_master/layout_research/vision_client.py`

Analyzes diagram images via Claude Vision to extract ~30 layout properties.

### API Call

```python
response = self._client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", ...}},
            {"type": "text", "text": analysis_prompt}
        ]
    }],
)
```

### Extracted Properties (~30 fields)

`flow_direction` (TB/LR/radial), `rank_count`, `node_shape`, `edge_style`, `has_clusters`, `cluster_count`, `spacing_ranksep`, `spacing_nodesep`, `nodes_equal_width`, `aspect_ratio`, and more.

### Batch Processing

`VisionClient.analyze_batch()` — sequential with 1s delay, ~$0.05/image, exponential backoff on rate limits.

## Component 4: Validation Pipeline

### Two-Tier Validation

| Tier | Validator | Checks |
|------|-----------|--------|
| **T1 Static** | `static_validator.py` | Syntax validity, min fontsize (9pt), known shapes/arrowheads, ratio attributes |
| **T2 Visual** | `svg_analyzer.py` | Width/height ratio, text overlaps, shape overlaps, rank alignment |

### Agent Orchestration (`agent.py`)

```python
agent = GraphvizMasterAgent()
result = agent.run("diagram.dot")        # single file
results = agent.run_directory("diagrams/") # batch
```

Regeneration loop: validate → detect layout → apply template defaults → re-validate (max 3 attempts).

### Regenerator (`regenerator.py`)

- Preserves semantic content (nodes, edges, labels, clusters)
- Replaces: graph attributes, default styles, out-of-range font sizes
- Auto-detects layout type and applies layout-specific restructuring

## Authentication

**File:** `graphviz_master/auth.py` — `resolve_api_key()`

Priority order:
1. Explicit `api_key` parameter
2. `ANTHROPIC_API_KEY` environment variable
3. **Claude Code OAuth token** from `~/.claude/.credentials.json` (automatic fallback)

OAuth fallback checks token expiry and `user:inference` scope. No manual setup needed inside Claude Code.

```bash
# Extract token manually
python scripts/get_oauth_token.py
python scripts/get_oauth_token.py --check  # show status/expiry
export ANTHROPIC_API_KEY=$(python scripts/get_oauth_token.py)
```

## Layout Research Knowledge Base

**File:** `graphviz_master/layout_research/data/knowledge_base.json` (19 KB)

Statistical profiles built from 400+ analyzed reference images across 7 categories.

### 7 Layout Categories

`process`, `hierarchy`, `matrix`, `list`, `cycle`, `pyramid`, `relation`

### Profile Data (per category)

- sample_count, aspect_ratio (mean/std/min/max)
- flow_direction distribution (TB%, LR%, radial%)
- rank_count, nodes_equal_width %, spacing means
- edge routing, clustering patterns, grid structure

### Usage in Generation

```python
kb = KnowledgeBase.load()
context = kb.to_prompt_context("process")  # → natural language for AI prompt
```

## Configuration (`config.py`)

### 8 Layout Types

`LIST`, `PROCESS`, `CYCLE`, `HIERARCHY`, `RELATION`, `MATRIX`, `PYRAMID`, `AUTO`

### Key Settings

| Setting | Default | Purpose |
|---------|---------|---------|
| min_fontsize | 9 | Minimum readable font size |
| target_ratio | varies | Layout-specific aspect ratio (e.g., PROCESS=0.55) |
| max_retries | 3 | Validation/regeneration attempts |
| Font | Segoe UI | Default font family |

## Rate Limit Handling

Both DotGenerator and VisionClient use identical retry:

```python
for attempt in range(max_retries):  # default: 3
    try:
        response = self._client.messages.create(...)
        return response
    except Exception as e:
        if "rate" in str(e).lower() or "429" in str(e).lower():
            wait = 2 ** (attempt + 1)  # 2s, 4s, 8s exponential backoff
            time.sleep(wait)
            continue
        raise
```

## CLI Usage

```bash
# Generate DOT
python scripts/generate_dot.py "Login flow with 5 steps" --type process
python scripts/generate_dot.py "Org chart" --type hierarchy --style corporate -o org.dot

# With structured input (NEW)
python -m graphviz_master generate --type process --input-json nodes.json -o diagram.dot

# Validate
python -m graphviz_master validate diagrams/
python -m graphviz_master diagrams/ --layout process --max-retries 3

# Vision analysis
python scripts/analyze_image.py diagram.png
python scripts/analyze_image.py *.png --batch -o results.json

# Layout research
python -m graphviz_master.layout_research status
python -m graphviz_master.layout_research analyze <image_id>
python -m graphviz_master.layout_research recommend
```

## Layout Techniques — Spine + Detail Rail (LR Diagrams)

For complex LR diagrams with detail nodes hanging off a main flow:

### Three-Layer Architecture

1. **Spine nodes** — main flow, `group="spine"`, OUTSIDE clusters
2. **Detail clusters** — `subgraph cluster_*` blocks without spine nodes
3. **Cross-cutting cluster** — utilities at the bottom

### Key Techniques

```dot
// High-weight spine (keeps straight):
start -> discover [weight=10]

// Low-weight details (won't distort):
discover -> d_ref [weight=1, lhead=cluster_disc_d]

// Invisible detail rail (forces same side):
map_d -> d_ref [style=invis, weight=2]

// Required attributes:
graph [rankdir=LR, compound=true, splines=true, newrank=true]
```

### Font Tips

- Set `fontname` once on defaults — no redundant `FACE="..."` in HTML labels
- Minimum 7pt for readability. 3-char hex colors (`#555`) are invalid — always 6-char.
- Custom fonts: install to `~/.local/share/fonts/`, run `fc-cache -fv`

## Strict Layout Rules Mode (hard-constraint diagrams)

When the user demands hard layout rules — straight axis-parallel arrows, right-angle
attachment, no overlaps/pass-throughs (arrow×arrow crossings only), **arrows attached at
side centers / multi-arrow groups centered**, corridor spacing — read
`references/strict-layout-rules.md` FIRST. The short version:

- Rules R1/R2/R4/R6 alone → graphviz `splines=ortho` + **mid-label-node** pattern
  (plain edge labels overlap nodes under ortho).
- The center-port rule (R5) → **graphviz cannot do it** (2.43 ortho ignores compass AND
  html-cell ports and stabs edges into node centers — probe-verified). Author a spec
  JSON and use the bundled generator, which renders AND audits all ten rules (incl. R7:
  the final segment into an arrowhead stays ≥24px so the last bend reads as a right angle;
  and R8: no segment may run parallel to and overlap a node/cluster border, or it merges
  into the box outline — clearance `"border_clear"`, default 4; and R10: component
  borders never touch or crowd — every node/cluster pair keeps ≥ `"component_clear"`
  px, default 12, contained components included via their inner margins) with coordinates:

  ```bash
  python3 scripts/strict_svg_diagram.py spec.json out.svg --png out.png
  # exit 0 = audit clean; exit 1 = violations printed — fix numbers, re-run
  # prints the hop count, e.g. "wrote out.svg (3 hops)"
  ```

  Iterate until exit 0. Do not trust an eyeball pass — on the first real diagram the
  audit caught 3 violations (2–3px chip/node overlaps, a forgotten corridor) that a
  careful visual check missed. Worked example spec: the ims.ai repo's
  `docs/bug-stack-architecture.spec.json`.

- **Two edges sharing a bend level can render as ONE merged line (R6).** When several
  edges leave the same node side and share a bend coordinate — correct for true siblings
  (one node fanning out, or several merging into one), since that's what makes them read
  as a matched pair — an unrelated edge sharing that same level with a *different*
  destination can end up exactly collinear with another edge's corridor for its whole
  length. Read "Same bend level, different destinations" in
  `references/strict-layout-rules.md` before wiring up any fan-out/fan-in; the fix is a
  ~20–40px offset on the non-sibling edge's bend, not a structural change.

- **Hops at crossings (R4).** Every allowed arrow×arrow crossing is auto-rendered as a
  small semicircular **hop** — the horizontal wire arcs over the vertical one — so a
  crossing reads as a line-jump, never a junction. On by default; per-spec knobs
  `"hops": false` (draw plain crossings) and `"hop_radius": 6`. Graphviz cannot draw
  hops, so if the user wants line-jumps you must use this generator, not ortho mode.

- **Alignment (declare intent, stop hand-computing coords).** Instead of hand-picking
  every `cx/cy` and edge pixel, declare what should line up and let the solver assign
  exact coordinates. Three opt-in keys (a spec with none renders byte-identical):
  - `"grid": 20` — snap every un-pinned coordinate to a lattice. One number, global tidy.
  - `"align": [{"type":"row","nodes":[…],"at":Y}, {"type":"col","nodes":[…]}]` — `row`
    shares `cy`, `col` shares `cx`; omit `at` to align to the group's current mean. Add
    `"between":[lo,hi]` or `"gap"+"start"` to also space them evenly on the other axis
    (this is how "distribute evenly" folds into the same mechanism).
  - **Symbolic edge endpoints** — `"points":[["L1:e"],["R1:w"]]` resolves to those side
    **centers** *after* nodes move, so edges follow alignment instead of detaching. A
    waypoint can borrow an axis: `["VT1:cx", 300]`. Multiple edges into the **same side
    auto-spread** (symmetric about center, `port_spacing` default 14) → R5's
    "group-centered, separated" holds by construction — the hardest rule to hand-satisfy.
  Author with intent; the audit still validates the resolved geometry against R1–R10.

- **PowerPoint export.** `python3 scripts/spec_to_pptx.py spec.json out.pptx` converts the
  same spec into NATIVE pptx shapes (rounded rects, freeform wires with arrowheads, text) —
  fully editable in PowerPoint, not an embedded image. **Slide sizing** (PowerPoint facts:
  default slide = 13.333×7.5 in widescreen 16:9 = 12192000×6858000 EMU, 914400 EMU/inch;
  vector — "resolution" only exists at raster export, ~96 dpi): the DEFAULT output fits +
  centers the diagram on that standard 16:9 slide, so copy-paste into another deck arrives
  at sane size (a slide sized to the diagram pastes as a 27-inch group — "way too big",
  verified). `--slide native` gives the wall-chart: slide sized 1:1 to the spec with a
  12pt nominal floor (`MIN_PT`). **If the user wants bigger text relative to the boxes,
  that is a SPEC change, not a converter change**: hold the canvas, raise `min_font`, let
  R9 flag the nodes that must widen, re-layout. Scaling page+font together is a visual
  no-op (also verified the hard way). And on a single slide, nominal pt is a DENSITY
  property (≈ 936pt / (canvas_px/min_font_px)) — lowering min_font shrinks the canvas
  with it and changes nothing. "Readable on one slide" (≥10pt) = author a separate
  CONDENSED variant spec alongside the wall-chart (2-line nodes, 1–2-word chips, merged
  node groups, ~16:9 aspect, ≤ ~1500×840px @ min_font 16) — recipe in
  `references/strict-layout-rules.md` step 8, worked example pair in the ims.ai repo. To reuse in a 16:9 deck,
  select-all and paste — arrives as scalable shapes. Requires python-pptx. Caveat: text
  boxes must set `auto_size = NONE` — the python-pptx default `spAutoFit` + `wrap="none"`
  re-centers the shrunk box and silently defeats left/right paragraph alignment (fixed
  in the script).

## Key Files

| File | Purpose |
|------|---------|
| `auth.py` | API key resolution (env → OAuth fallback) |
| `dot_generator.py` | AI DOT generation |
| `layout_planner.py` | **NEW** — Deterministic layout constraint computation |
| `layout_research/vision_client.py` | Vision API wrapper |
| `layout_research/knowledge_base.py` | Statistical profile builder |
| `layout_research/data/knowledge_base.json` | Compiled profiles (7 categories, 400+ images) |
| `config.py` | Layout presets, validation thresholds |
| `agent.py` | Validation + regeneration orchestration |
| `static_validator.py` | Tier 1: syntax & font checks |
| `svg_analyzer.py` | Tier 2: visual ratio/overlap checks |
| `regenerator.py` | Template-safe DOT rewriting |
| `<skill>/scripts/strict_svg_diagram.py` | Hand-routed SVG generator + R1–R10 rule audit (the R5 path) |
| `<skill>/scripts/check_svg_rules.py` | Independent geometric grader for ANY svg (no spec needed) — R1, R3, R5, R6 (incl. collinear-overlap), R7; hop-aware |
| `<skill>/scripts/spec_to_pptx.py` | Same spec JSON → native editable PowerPoint shapes (python-pptx; hops as polyline arcs) |
| `<skill>/references/strict-layout-rules.md` | Strict-rules playbook: decision tree, ortho port facts, port math, corridor budgeting |
