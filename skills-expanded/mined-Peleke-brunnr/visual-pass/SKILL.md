---
name: visual-pass
description: "Scan existing educational content (notebooks, tutorials, articles) and identify where to inject visual assets. Produces a prioritized injection manifest with per-visual rendering instructions — delegates actual rendering to inline-svg-architecture-diagrams, Manim MCP, ComfyUI MCP, Mermaid, and engagement-pass. The analysis layer between content generation and visual production."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F441\uFE0F"
---

# Visual Pass

Scan existing educational content and identify where to inject visual assets. This skill does NOT render visuals; it produces a prioritized manifest and delegates to rendering tools. It sits between content generation and visual production in the pipeline: content is written first, visual-pass analyzes it, then rendering tools execute the manifest.

Complements `engagement-pass`. Engagement-pass adds interactive exploration (Plotly, widgets, concept maps). Visual-pass adds structural/architectural visuals and high-production assets (SVG diagrams, Manim videos, ComfyUI hero images, before/after panels). They run independently and their outputs compose without conflict.

Reads `_educational-suite-conventions.md` for shared contracts.

---

## Step 0: Inputs

Before scanning, you need:

1. **Content artifact** — one of:
   - A Jupyter notebook (.ipynb)
   - A tutorial draft (from `technical-tutorial`)
   - An article draft (from `article-draft`)
   - A lesson module (from `lesson-generator` / `notebook-builder`)
   - Any markdown or prose-plus-code teaching document
2. **Content type** — notebook / tutorial / article / lesson. Determines budget defaults and which visual types are eligible.
3. **Rendering context** — where the final artifact will be consumed:
   - Jupyter notebook (inline SVG, HTML embeds, cell outputs)
   - Static site / blog (external SVG files, embedded images, video embeds)
   - PDF export (static fallbacks required for everything)
   - Slide deck (simplified visuals, larger fonts)
4. **Available rendering tools** — which MCP servers and skills are accessible in this session:
   - `inline-svg-architecture-diagrams` skill (always available)
   - Mermaid / D2 (always available; text-based)
   - Manim MCP server (check availability)
   - ComfyUI MCP server (check availability; provides `generate_image`, `img2img`, `stylize_photo`, `generate_with_controlnet`, `imagine`)
   - FuncAnimation / matplotlib (always available in notebook context)
   - Plotly (always available; overlaps with engagement-pass)
5. **Budget overrides** (optional) — override default visual budgets per type. See Phase 3 for defaults.

If the content artifact is missing or incomplete (still being drafted), do NOT run visual-pass. Wait for a complete draft. Visual-pass analyzes finished content; it does not guide content creation.

---

## Phase 1: Content Scan

Read the entire content artifact. For every paragraph, code cell, section header, and transition, evaluate against the signal detection table below.

### Signal Detection Table

| Signal in Prose | Visual Type Candidate | Confidence | Example |
|----------------|----------------------|------------|---------|
| "consists of", "made up of", "composed of N components" | Type 1: Static Diagram | High | "The encoder consists of three layers: embedding, attention, and projection" |
| "flows from X to Y", "passes through", "pipeline" | Type 1: Static Diagram | High | "Data flows from the tokenizer through the encoder to the decoder" |
| Class/struct definitions with 3+ fields or components | Type 1: Static Diagram | High | A dataclass with 5 fields that relate to each other |
| "architecture", "system design", "how it fits together" | Type 1: Static Diagram | High | Section titled "System Architecture" |
| "you are here", progress through a multi-part series | Type 1: Static Diagram (progress map) | High | Module 3 of an 8-module arc |
| Tensor shape descriptions, dimension annotations | Type 1: Static Diagram (shape diagram) | Medium | "Input shape (batch, seq_len, d_model) becomes (batch, heads, seq_len, d_k)" |
| "step by step", "gradually", "one at a time" | Type 2: Animation | Medium | "The posterior updates step by step as each observation arrives" |
| "over time", "converges to", "evolves" | Type 2: Animation | Medium | "Loss converges to a minimum over 100 epochs" |
| Loops that modify state (training loops, MCMC, EM) | Type 2: Animation | Medium | A for-loop that updates weights and prints loss |
| "accumulates", "builds up" | Type 2: Animation | Low | "Evidence accumulates across trials" |
| Existing matplotlib scatter with per-point meaning | Type 3: Interactive Chart | High | Scatter plot where each dot is a named entity |
| "try changing", "experiment with", "what happens if" | Type 3: Interactive Chart (or widget) | Medium | "Try changing the learning rate and observe the effect" |
| Parameter sweep sections, grid search results | Type 3: Interactive Chart | Medium | Table of hyperparameters and their results |
| 3D surface plots, multi-dimensional data | Type 3: Interactive Chart | High | Loss landscape, decision boundary surface |
| Matrix operations, linear transformations | Type 4: Manim Video | Medium | "Multiply the rotation matrix by the input vector" |
| Coordinate system changes, projections | Type 4: Manim Video | Medium | "Project from 3D to 2D using the camera matrix" |
| Embedding space transformations | Type 4: Manim Video | Medium | "Watch how the embedding space reorganizes during training" |
| Loss landscapes, optimization trajectories | Type 4: Manim Video | Low | "Gradient descent follows the surface toward the minimum" |
| Code cells with assert/print verifying correctness | Type 5: Expected Output | High | `assert len(tokens) == 5` followed by `print(tokens)` |
| "the output should look like", "you should see" | Type 5: Expected Output | High | "Running this cell should print: [1, 2, 3]" |
| Non-executable contexts (article prose describing output) | Type 5: Expected Output | Medium | Article section describing terminal output |
| "before vs. after", "without X vs. with X" | Type 6: Before/After | High | "Without dropout, the model overfits. With dropout, it generalizes." |
| "compared to", "naive vs. optimized" | Type 6: Before/After | High | "The naive implementation takes 45s. The vectorized version takes 0.3s." |
| Gradient/performance tables showing improvement | Type 6: Before/After | Medium | Table showing metrics before and after applying a technique |
| Module/arc openings, section headers needing visual anchors | Type 7: ComfyUI Image | Low | "Part 3: The Attention Mechanism" (hero image candidate) |
| Abstract concepts that resist diagramming | Type 7: ComfyUI Image | Low | Conceptual illustration of "information bottleneck" |
| Landing pages, course overviews | Type 7: ComfyUI Image | Medium | Course landing page needing a hero banner |

### Scan Output Format

For each detected opportunity, record:

```markdown
| # | Location | Signal | Type | Confidence | Notes |
|---|----------|--------|------|------------|-------|
| 1 | Section 2, para 3 | "The encoder consists of embedding, attention, and projection layers" | Type 1 | High | Architecture diagram — show all three layers with data flow |
| 2 | Section 4, code cell 7 | Training loop with loss printing | Type 2 | Medium | Animate loss curve building up over epochs |
| 3 | Section 5, matplotlib scatter | Per-entry scatter with salience scores | Type 3 | High | Plotly conversion — hover shows entry name and task |
```

### The Progressive Reveal Rule

When scanning for Type 1 (static diagram) opportunities in multi-section content, do NOT plan a single "big picture" diagram that shows the entire system. Instead, plan a series of incremental reveals:

1. First occurrence: show 1-2 components, everything else grayed or absent
2. Each subsequent section: add the component that section introduces, highlight it, keep prior components visible but de-emphasized
3. Final section: show the complete system with all components active

This produces 3-6 diagram variants from one base architecture, each scoped to its section. The reader builds the mental model incrementally instead of parsing a complex diagram upfront.

Track these as a single "diagram family" in the manifest:

```markdown
| # | Family | Variant | Section | Components Shown | Highlighted |
|---|--------|---------|---------|-----------------|-------------|
| 1 | encoder-arch | 1/4 | Section 2 | Embedding only | Embedding |
| 2 | encoder-arch | 2/4 | Section 3 | Embedding + Attention | Attention |
| 3 | encoder-arch | 3/4 | Section 5 | Embedding + Attention + Projection | Projection |
| 4 | encoder-arch | 4/4 | Section 7 | Full system | None (all active) |
```

---

## Phase 2: Visual Opportunity Map

Transform the raw scan output into a structured opportunity map. Group related opportunities, identify conflicts with engagement-pass territory, and flag dependencies.

### Grouping Rules

1. **Same-section, same-type opportunities merge.** If a section has three separate signals for Type 1 (static diagram), they likely belong to a single diagram, not three separate ones.
2. **Reveal families are one logical unit.** A progressive reveal series counts as ONE diagram toward the budget, not N separate diagrams.
3. **Type 3 (interactive chart) overlaps with engagement-pass.** If engagement-pass will handle Plotly conversions, mark Type 3 opportunities as "delegate to engagement-pass" and do not include them in the visual-pass manifest. Visual-pass owns Type 3 ONLY when engagement-pass is not being run.
4. **Type 5 (expected output) never conflicts.** These are always additive and low-cost.

### Conflict Resolution with Engagement-Pass

| Visual-Pass Type | Engagement-Pass Pattern | Resolution |
|-----------------|----------------------|------------|
| Type 1 (static diagram) | Concept map | Both run. Concept map shows module relationships; static diagram shows internal architecture. Different purposes. |
| Type 2 (animation) | FuncAnimation | Visual-pass owns animations for architectural/process reveals. Engagement-pass owns animations for data exploration (convergence, Monte Carlo). If ambiguous, engagement-pass wins. |
| Type 3 (interactive chart) | Plotly conversion | Engagement-pass wins. Visual-pass marks these as "delegate" in the manifest. |
| Type 6 (before/after) | None | Visual-pass owns exclusively. |
| Type 7 (ComfyUI image) | None | Visual-pass owns exclusively. |

### Opportunity Map Format

```markdown
## Visual Opportunity Map: [Artifact Title]

### Type 1: Static Diagrams
- [ ] **[ID-1]** Section 2: Encoder architecture (reveal family, 4 variants)
  - Tool: inline-svg-architecture-diagrams
  - Components: embedding, attention, projection, output
  - Style: CSS-var (notebook) / hand-drawn (article)
  - Dependencies: none
  - Intent: detected

### Type 2: Animations
- [ ] **[ID-2]** Section 4: Training loop convergence
  - Tool: FuncAnimation + to_jshtml()
  - Shows: loss curve building up frame by frame
  - Dependencies: training loop code cell must exist
  - Note: check if engagement-pass claims this
  - Intent: detected

### Type 6: Before/After
- [ ] **[ID-3]** Section 6: Naive vs. vectorized performance
  - Tool: CSS grid side-by-side
  - Left: naive output (45s, high memory)
  - Right: vectorized output (0.3s, low memory)
  - Dependencies: both code cells must run
  - Intent: detected

### Delegated to engagement-pass
- Section 5 scatter plot → Plotly conversion (engagement-pass)
- Section 7 parameter sweep → Widget (engagement-pass)
```

---

## Phase 3: Prioritized Injection Plan

Apply budgets, rank by impact, and produce the final ordered plan.

### Budget Defaults (per artifact)

| Visual Type | Min | Max | Required? | Notes |
|------------|-----|-----|-----------|-------|
| Type 1: Static Diagrams | 2 | 6 | Yes (min 2) | Reveal families count as 1 |
| Type 2: Animations | 0 | 2 | No | Expensive; only where static fails |
| Type 3: Interactive Charts | 0 | 4 | No | Only if engagement-pass not running |
| Type 4: Manim Videos | 0 | 1 | No | Arc-level, not module-level; max 1 per arc |
| Type 5: Expected Output | 0 | unlimited | No | Zero cost; add wherever helpful |
| Type 6: Before/After Panels | 0 | 3 | No | High impact when applicable |
| Type 7: ComfyUI Images | 0 | 2 | No | Hero images only; not decoration |

### Budget Adjustments by Content Type

| Content Type | Type 1 Adj | Type 2 Adj | Type 4 Adj | Type 7 Adj |
|-------------|-----------|-----------|-----------|-----------|
| Notebook | +0 | +1 (animations render inline) | eligible | -1 (hero images less needed) |
| Tutorial article | +0 | -1 (animations need JS fallback) | eligible | +1 (hero images valuable) |
| Article | -1 (fewer diagrams) | -1 | not eligible | +1 |
| Slide deck | +2 (more diagrams needed) | -2 (animations risky in slides) | not eligible | +1 |
| PDF export | +0 | set to 0 (no animation in PDF) | not eligible | +0 |

### Ranking Criteria

Rank each opportunity by multiplying these scores:

| Factor | Score Range | Description |
|--------|-----------|-------------|
| **Concept density** | 1-5 | How many concepts does this visual explain simultaneously? |
| **Static failure** | 1-5 | How badly does prose alone fail to convey this? (5 = impossible without visual) |
| **Reader effort saved** | 1-5 | How much re-reading/confusion does this visual prevent? |
| **Production cost** | 5-1 (inverted) | 1 = Manim video, 5 = expected output screenshot |

**Impact score** = concept_density * static_failure * effort_saved * cost_efficiency

Sort opportunities by impact score descending. Apply budget caps. Cut anything below the budget floor.

### Injection Plan Format

```markdown
## Injection Plan: [Artifact Title]

Budget: 4 static / 1 animation / 0 interactive / 0 manim / 3 expected output / 1 before-after / 1 comfyui
Total visuals: 10

### Priority 1 (must have)
1. **[ID-1]** Encoder architecture family (Type 1, impact: 100)
   - Render with: inline-svg-architecture-diagrams (CSS-var style)
   - 4 progressive variants, inject at Sections 2, 3, 5, 7
   - Highlight current component per variant
   - Intent: specified | Assignee: inline-svg skill

2. **[ID-5]** Training output verification (Type 5, impact: 75)
   - Render with: direct cell output capture
   - Show expected output after training loop cell
   - Intent: specified | Assignee: self (direct insertion)

### Priority 2 (should have)
3. **[ID-3]** Naive vs. vectorized comparison (Type 6, impact: 60)
   - Render with: CSS grid side-by-side panel
   - Left panel: naive timings + memory usage
   - Right panel: vectorized timings + memory usage
   - Intent: specified | Assignee: self

### Priority 3 (nice to have)
4. **[ID-7]** Hero image for notebook header (Type 7, impact: 30)
   - Render with: ComfyUI MCP (imagine tool)
   - Prompt: "Technical illustration of neural network encoder architecture, clean minimalist style, dark background, purple accent lighting"
   - Style: digital_art
   - Output: header-hero.png
   - Intent: specified | Assignee: comfyui_mcp

### Cut (over budget)
- [ID-4] Attention mechanism animation (Type 2, impact: 25) — over animation budget
```

---

## Phase 4: Manifest Output

Transform the injection plan into **visual intents** — self-contained briefs that carry both the creative specification ("what this should be") and the rendering instructions ("how to produce it"). Each intent is a complete specification that a rendering tool, external artist, or future pass can execute without additional context.

Every manifest entry is an intent. On the first visual-pass, all intents are `specified` — fully described but not yet rendered. Resolution happens later (see Phase 5).

### Manifest Entry: Type 1 (Static Diagram)

```yaml
visual_id: ID-1
type: static_diagram
tool: inline-svg-architecture-diagrams
inject_at: Section 2, after paragraph 3
style: css-var  # or: hand-drawn
intent:
  status: specified        # detected | specified | commissioned | rendered | injected
  assignee: inline-svg     # who/what resolves: tool name, "designer", "self", "deferred"
  resolution_notes: null   # filled when resolved — path to asset, commit ref, or "skip" reason
spec:
  layers:
    - id: embedding
      label: "01 · EMBEDDING"
      title: "Token → Vector"
      icon: database
    - id: attention
      label: "02 · ATTENTION"
      title: "Self-Attention"
      icon: knowledge-graph
      grayed: true  # not yet introduced
    - id: projection
      label: "03 · PROJECTION"
      title: "Linear → Output"
      icon: gear
      grayed: true
  connections:
    - from: embedding
      to: attention
      label_left: "vectors"
      label_right: "queries, keys, values"
    - from: attention
      to: projection
      label_left: "context"
  highlight_layer: embedding
  caption: "The encoder's first layer: embedding converts tokens to vectors. Attention and projection (grayed) come next."
  reveal_family: encoder-arch
  variant: 1/3
```

**All manifest entries carry the `intent` block.** The `spec` provides the full rendering brief; the `intent` tracks the lifecycle. Subsequent examples show `intent` in abbreviated form.

### Manifest Entry: Type 2 (Animation)

```yaml
visual_id: ID-2
type: animation
tool: funcanimation
inject_at: Section 4, after code cell 7
intent: { status: specified, assignee: self, resolution_notes: null }
spec:
  what_animates: "Loss curve building up over training epochs"
  x_data: epoch numbers (1 to N)
  y_data: loss values from training loop output
  frame_count: 100
  fps: 20
  display: HTML(anim.to_jshtml())
  show_static_first: true
  annotations:
    - frame_counter: "Epoch {i}/{N}"
    - running_metric: "Loss: {loss:.4f}"
  static_fallback: "Final loss curve (static matplotlib) shown before animation"
```

### Manifest Entry: Type 4 (Manim Video)

```yaml
visual_id: ID-4
type: manim_video
tool: manim_mcp
inject_at: Section 6, after "the attention mechanism transforms the input space"
intent: { status: specified, assignee: manim_mcp, resolution_notes: null }
spec:
  scene_description: |
    Show a 3D vector space with 5 input vectors (colored dots).
    Apply the attention transformation: vectors move to new positions.
    Show query-key dot products as connecting lines with varying opacity.
    Fade in the output vectors at their new positions.
    Camera rotates slowly to show the 3D structure.
  duration: 15s
  resolution: 1080p
  style: 3b1b  # dark background, colored vectors, smooth transitions
  static_fallback: |
    Before/after diagram showing input vectors and output vectors
    with attention weights as line thickness between them.
  embed_as: mp4_in_notebook  # or: gif_in_markdown, mp4_link
```

### Manifest Entry: Type 5 (Expected Output)

```yaml
visual_id: ID-5
type: expected_output
tool: direct_insertion
inject_at: Section 4, after code cell 8 (the training loop)
intent: { status: specified, assignee: self, resolution_notes: null }
spec:
  format: code_block  # or: terminal_screenshot, inline_text
  content: |
    Epoch 1/10 - Loss: 2.3421
    Epoch 2/10 - Loss: 1.8754
    ...
    Epoch 10/10 - Loss: 0.0342
    Training complete. Final accuracy: 97.3%
  purpose: "Reader verifies their output matches before proceeding"
```

### Manifest Entry: Type 6 (Before/After)

```yaml
visual_id: ID-3
type: before_after
tool: css_grid  # or: plotly_subplots, juxtapose_js
inject_at: Section 6, replacing the two separate output cells
intent: { status: specified, assignee: self, resolution_notes: null }
spec:
  layout: side_by_side  # or: stacked, slider
  left:
    label: "Naive (for-loop)"
    content_type: code_output  # or: plot, image
    content: |
      Time: 45.2s
      Memory: 2.1 GB
      Throughput: 22 items/sec
  right:
    label: "Vectorized (NumPy)"
    content_type: code_output
    content: |
      Time: 0.31s
      Memory: 180 MB
      Throughput: 3,225 items/sec
  highlight_winner: right
  caption: "Vectorization delivers a 145x speedup by replacing Python loops with NumPy operations."
```

### Manifest Entry: Type 7 (ComfyUI Image)

```yaml
visual_id: ID-7
type: comfyui_image
tool: comfyui_mcp
inject_at: Cell 1 (notebook header) or article hero position
intent: { status: specified, assignee: comfyui_mcp, resolution_notes: null }
spec:
  mcp_tool: imagine  # or: generate_image, stylize_photo, generate_with_controlnet
  description: "Technical illustration of a neural network encoder, clean minimalist style, layers of processing shown as translucent geometric planes stacked vertically, data flowing upward as light particles, dark background with purple and blue accent lighting"
  style: digital_art
  model_family: flux  # or: sdxl, illustrious
  width: 1024
  height: 576  # 16:9 for hero banner
  output_path: assets/hero-encoder.png
  usage_context: |
    Hero image at the top of the notebook/article.
    Sets the visual tone. Should feel technical but approachable.
    Must not contain text (AI-generated text is unreliable).
  anti_patterns:
    - No text in the image (AI text rendering is poor)
    - No photorealistic humans (uncanny valley)
    - No generic "brain with circuits" cliche
    - No stock-photo aesthetic
  fallback_if_unavailable: "Skip hero image; use the first Type 1 diagram as the visual anchor instead"
```

---

## Phase 5: Intent Resolution

Visual-pass produces intents, not finished visuals. Resolution is a separate step — it can happen immediately, incrementally, or not at all.

### The Intent Lifecycle

```
detected → specified → commissioned → rendered → injected
    ↑          ↑            ↑             ↑          ↑
  Phase 1   Phase 4    Resolution    Resolution  Final
  (scan)   (manifest)   (external)    (tool)     (insert)
```

| Status | Meaning | Who Sets It |
|--------|---------|-------------|
| `detected` | Signal found during content scan; not yet fully specified | Phase 1 (opportunity map) |
| `specified` | Full intent brief written: spec + rendering instructions + assignee | Phase 4 (manifest output) |
| `commissioned` | Intent sent to an external tool, artist, or queue for production | Resolution step |
| `rendered` | Asset exists (file path, embed code, or cell output) but not yet placed in content | Resolution step |
| `injected` | Asset placed at `inject_at` location in the content artifact | Final insertion step |

### Resolution Methods

| Method | When to Use | Flow |
|--------|-------------|------|
| **Immediate** | Tool is available in this session (e.g., inline-svg skill, direct insertion) | `specified → rendered → injected` in one pass |
| **Deferred** | Tool unavailable or asset needs human review | `specified → (wait)` — revisit in a later session |
| **Commissioned** | External artist, design tool, or async pipeline | `specified → commissioned → (wait for delivery) → rendered → injected` |
| **Generated (subsequent pass)** | Re-run visual-pass after new tools become available | `specified → (re-run visual-pass) → rendered → injected` |

### Incremental Resolution

Intents can be resolved **one at a time, in any order**. The manifest tracks each intent's status independently. A partially-resolved manifest is a normal state — not an error.

Typical workflows:

1. **All-at-once**: every available tool resolves its intents in one session.
2. **Cherry-pick**: resolve the 3 highest-priority intents now, defer the rest.
3. **Commission batch**: export all Type 7 (ComfyUI) intents as briefs for an image pipeline, resolve Type 1 and Type 5 immediately.
4. **Progressive enrichment**: first pass resolves Type 5 (expected output) and Type 1 (static diagrams). Second pass adds Type 2 (animations). Third pass commissions Type 7 (hero images).

### Re-run Behavior

When visual-pass is re-run on content that already has a manifest:

1. **Skip resolved intents.** If `intent.status == injected`, the visual already exists in the content. Do not duplicate.
2. **Update stale intents.** If the content changed since the intent was specified, re-evaluate the spec. Flag changes.
3. **Detect new opportunities.** New content may introduce new signals. Add new intents at `detected` status.
4. **Promote deferred intents.** If a previously unavailable tool is now available, update the assignee and flag for resolution.

### Commission Brief Format

When commissioning an intent externally (to a designer, an image pipeline, or a separate MCP session), export the intent as a standalone brief:

```markdown
## Visual Brief: [visual_id]

**Type:** [visual type name]
**For:** [artifact title], [inject_at location]
**Priority:** [1/2/3 from injection plan]

### What It Should Show
[human-readable description extracted from the spec]

### Rendering Guidance
- **Tool suggestion:** [tool from manifest]
- **Style:** [style from spec]
- **Dimensions/constraints:** [from spec]
- **Anti-patterns:** [from spec, if any]

### Acceptance Criteria
- [ ] Shows [key elements from spec]
- [ ] Matches color palette (suite shared: #2196F3, #FF9800, #4CAF50, #E91E63, #9C27B0)
- [ ] Has static fallback (for Types 2, 3, 4)
- [ ] Does not contain text (for Type 7)
- [ ] Caption provided: "[caption from spec]"

### Context
[1-2 sentences about what the reader is learning at this point in the content]
```

### Manifest Summary Table

After the full manifest, produce a summary showing intent status across the artifact:

```markdown
## Intent Summary: [Artifact Title]

| ID | Type | Priority | Assignee | Status | Asset Path |
|----|------|----------|----------|--------|------------|
| ID-1 | Static Diagram | P1 | inline-svg | specified | — |
| ID-2 | Animation | P2 | self | specified | — |
| ID-3 | Before/After | P2 | self | specified | — |
| ID-5 | Expected Output | P1 | self | rendered | — |
| ID-7 | ComfyUI Image | P3 | comfyui_mcp | specified | — |

Resolved: 0/5 | Commissioned: 0/5 | Pending: 5/5
```

---

## Review Mode

When reviewing an existing visual-pass manifest (not creating one from scratch), run these passes in order.

### Pass 1: Coverage Audit

Verify the manifest covers all high-confidence signals from the content:

```
[COVERAGE] Section N: Signal "<signal text>" → Type X: COVERED by [ID] / MISSING / DELEGATED
[COVERAGE] High-confidence signals covered: N/M
[COVERAGE] Missing high-confidence signals: [list]
```

### Pass 2: Budget Compliance

```
[BUDGET] Type 1 (static diagrams): N planned, budget 2-6: OK / OVER / UNDER
[BUDGET] Type 2 (animations): N planned, budget 0-2: OK / OVER
[BUDGET] Type 3 (interactive): N planned, budget 0-4: OK / OVER / DELEGATED
[BUDGET] Type 4 (manim): N planned, budget 0-1: OK / OVER
[BUDGET] Type 5 (expected output): N planned, no cap: OK
[BUDGET] Type 6 (before/after): N planned, budget 0-3: OK / OVER
[BUDGET] Type 7 (comfyui): N planned, budget 0-2: OK / OVER
[BUDGET] Minimum 2 static diagrams met: YES / NO
```

### Pass 3: Tool Availability

```
[TOOLS] inline-svg-architecture-diagrams: AVAILABLE — N manifest entries depend on it
[TOOLS] Manim MCP: AVAILABLE / UNAVAILABLE — N manifest entries depend on it
[TOOLS] ComfyUI MCP: AVAILABLE / UNAVAILABLE — N manifest entries depend on it
[TOOLS] FuncAnimation: AVAILABLE (notebook context) / UNAVAILABLE (static context)
[TOOLS] Entries with unavailable tools: [list with fallback status]
```

### Pass 4: Progressive Reveal Coherence

For every diagram family using progressive reveals:

```
[REVEAL] Family "[name]": N variants planned
  Variant 1: shows [components], highlights [component] — Section N: OK
  Variant 2: shows [components], highlights [component] — Section M: OK
  ...
  Final variant shows all components: YES / NO
  Variants ordered by section number: YES / NO (must be sequential)
  No component appears before its introducing section: YES / VIOLATION at variant N
```

### Pass 5: Engagement-Pass Coordination

```
[COORD] Type 3 opportunities delegated to engagement-pass: N
[COORD] Type 2 ambiguities resolved: N (visual-pass: N, engagement-pass: N)
[COORD] No visual-pass entry conflicts with engagement-pass patterns: YES / CONFLICT at [list]
[COORD] Engagement-pass concept map and visual-pass static diagrams serve different purposes: YES / OVERLAP at [list]
```

### Pass 6: Rendering Feasibility

For each manifest entry, verify the spec is complete enough for the rendering tool:

```
[RENDER] [ID-1] Type 1 via inline-svg: layers defined: YES, connections defined: YES, style set: YES — READY
[RENDER] [ID-7] Type 7 via ComfyUI: description adequate: YES, anti-patterns listed: YES, fallback defined: YES — READY
[RENDER] [ID-4] Type 4 via Manim: scene described: YES, duration set: YES, static fallback: YES — READY
[RENDER] [ID-2] Type 2 via FuncAnimation: data source identified: NO — INCOMPLETE (need to specify which cell outputs to animate)
```

### Pass 7: Intent Status Audit

```
[INTENT] Total intents: N
[INTENT] Status breakdown: specified: N, commissioned: N, rendered: N, injected: N
[INTENT] Stale intents (content changed since spec): [list or "none"]
[INTENT] Deferred intents with now-available tools: [list or "none"]
[INTENT] Commission briefs exported: N (Type 7: N, Type 4: N, etc.)
```

### Review Output Format

```markdown
# Visual Pass Review: [Artifact Title]

## Summary
- Signal coverage: N/M high-confidence signals addressed
- Budget compliance: OK / N violations
- Tool availability: N/N tools available
- Progressive reveal coherence: N families, all sequential: YES/NO
- Engagement-pass coordination: N delegated, 0 conflicts
- Rendering readiness: N/N entries ready
- Intent resolution: N/N intents resolved

## Critical (blocks rendering)
<items>

## Major (degrades quality)
<items>

## Minor (polish)
<items>
```

---

## Decision Heuristic: When to Use Which Type

Use this table when a signal is ambiguous and could map to multiple types.

| Situation | First Choice | Why | Fallback |
|-----------|-------------|-----|----------|
| Architecture with 3+ components | Type 1 (static diagram) | Shows relationships and structure at a glance | Mermaid if SVG is overkill |
| Process with clear sequential steps | Type 1 (static diagram with numbered steps) | Steps are discrete, not continuous | Type 2 if steps involve state evolution |
| Process with continuous state change | Type 2 (animation) | Static snapshots lose the continuity | Type 1 (3-panel before/during/after) if animation budget is full |
| Data with per-point context | Type 3 (interactive chart) | Hover reveals individual data stories | Delegate to engagement-pass |
| Mathematical transformation | Type 4 (Manim) | Geometric motion is the concept | Type 1 + Type 2 if Manim unavailable |
| Code output verification | Type 5 (expected output) | Zero cost, always helpful | Never skip this; no fallback needed |
| Technique comparison | Type 6 (before/after) | Side-by-side makes the improvement visceral | Two separate code cells (worse) |
| Module/course opening | Type 7 (ComfyUI) | Visual anchor sets tone and breaks text monotony | Type 1 (progress map) as alternative anchor |
| Concept too abstract to diagram | Type 7 (ComfyUI) | Generated illustration provides a visual handle | Metaphor in prose (no visual) |
| Tensor/matrix shapes | Type 1 (shape diagram) | Spatial relationships between dimensions | ASCII art in code comment (last resort) |
| Loss landscape | Type 4 (Manim) if budget allows, else Type 3 (Plotly 3D) | 3D surface benefits from camera rotation | Static 3D matplotlib with good angle |
| Training convergence | Type 2 (animation) | The *process* of converging is the insight | Static final curve (loses the journey) |
| "What does this look like in the real world?" | Type 7 (ComfyUI) | Conceptual illustration grounds abstract ideas | Skip; not every concept needs a photo |

### The "Static Failure" Test

Before approving any Type 2, 4, or 7 visual (the expensive ones), ask: **"Does a static image fail to convey this?"**

- If a static diagram tells 80% of the story, use Type 1. Save the animation/Manim budget for concepts where static genuinely fails.
- If the concept is inherently about motion, transformation, or accumulation over time, static fails. Approve the animation.
- If the concept is inherently spatial and 3D, static fails at the rotation/perspective. Approve Manim or Plotly 3D.
- If the concept is abstract with no obvious diagrammatic representation, a generated illustration (Type 7) might provide a visual anchor. But if good prose handles it, skip the visual entirely.

---

## Anti-Patterns

### Manifest anti-patterns

1. **Decoration over explanation.** Every visual must serve a teaching purpose. Hero images (Type 7) are the sole exception, and even those must set the right conceptual tone. A beautiful SVG diagram that doesn't help the reader understand anything is waste.
2. **Animation for linear processes.** If the process is A then B then C with no state evolution, a numbered static diagram beats an animation. Animations earn their cost when something *changes over time*.
3. **Manim for everything.** Manim videos are high-production, high-cost anchor content. One per arc, maximum. Using Manim for something FuncAnimation handles is like renting a crane to hang a picture frame.
4. **ComfyUI as clip art.** Generated images are for hero/anchor positions only. Do not sprinkle AI-generated illustrations throughout the content as decoration. Two maximum per artifact.
5. **Ignoring engagement-pass territory.** If engagement-pass is also running on this artifact, visual-pass must NOT generate Plotly conversion instructions. Duplicate instructions from two skills cause confusion. Delegate clearly.
6. **One giant architecture diagram.** The progressive reveal rule exists for a reason. A single diagram showing the entire system teaches less than 4 progressive reveals showing one component at a time. The reader builds the mental model; the diagram does not pre-load it.
7. **Visuals before the concept is earned.** Following the DO→NOTICE→CODE→NAME contract: diagrams go AFTER the reader has experienced the component, not before. A diagram that shows all three layers before the reader has built the first one violates the pedagogical model.
8. **No static fallback for dynamic content.** Every animation, interactive chart, and Manim video must have a static fallback specified in the manifest. Content degrades to PDF, nbconvert, and print. Visuals that vanish in static rendering are not production-ready.
9. **Overriding the content author's flow.** Visual-pass injects visuals alongside existing content. It does NOT restructure sections, reorder cells, or rewrite prose. The narrative flow is sacred. If a visual requires restructuring to work, flag it as a "requires content edit" note, do not execute the restructuring.

### Signal false positives

These prose patterns look like visual signals but usually are not:

| False Signal | Why It's Not a Visual | What to Do |
|-------------|----------------------|------------|
| "In other words" | Rephrasing, not architecture | Skip |
| "For example" followed by a single concrete instance | One example is text; three examples might be a comparison table | Skip unless 3+ examples |
| "There are two types" | If the types are simple, prose handles it | Only diagram if types have sub-components |
| "The key insight is" | Prose emphasis, not visual content | Skip |
| "Imagine a..." | Metaphor in prose; the imagination IS the visual | Only Type 7 if the metaphor is sustained across 3+ paragraphs |
| Simple class with 1-2 fields | Not complex enough for a diagram | Skip; code IS the diagram |

---

## Pipeline Position

```
lesson-generator ──→ outline-writer ──→ notebook-builder ──┐
                                                           │
technical-tutorial ──→ ┐                                   │
                       ├──→ VISUAL PASS ──→ engagement-pass
article-draft ────→ ──┘        │
                               ├── inline-svg-architecture-diagrams (Type 1)
                               ├── FuncAnimation (Type 2)
                               ├── Plotly (Type 3, only if no engagement-pass)
                               ├── Manim MCP (Type 4)
                               ├── Direct insertion (Type 5)
                               ├── CSS grid / juxtapose.js (Type 6)
                               └── ComfyUI MCP (Type 7)
```

### Handoff Contract

**Visual-pass receives:**
- Complete content artifact (notebook, tutorial, article)
- Content type and rendering context
- List of available rendering tools

**Visual-pass produces:**
- Visual opportunity map (all detected signals, grouped and deduplicated)
- Prioritized injection plan (budgeted, ranked, with cut list)
- **Intent manifest** (self-contained briefs per visual — spec + rendering guidance + lifecycle status)
- Intent summary table (status dashboard across all intents)
- Delegation list (opportunities handed to engagement-pass)
- Commission briefs (exportable specs for external production, when applicable)

**Visual-pass does NOT produce:**
- Rendered visuals (rendering tools and commissioned artists resolve intents)
- Prose rewrites (that is the content skill's job)
- Interactive widgets (that is engagement-pass's job)
- Restructured content (narrative flow is sacred)

---

## Appendix: Quick Reference Checklist

### Pre-scan
- [ ] Content artifact is complete (not a draft-in-progress)
- [ ] Content type identified (notebook / tutorial / article / lesson / slides)
- [ ] Rendering context identified (Jupyter / static site / PDF / slides)
- [ ] Available rendering tools checked (inline-svg, Manim MCP, ComfyUI MCP)
- [ ] Budget overrides applied if specified

### Phase 1 (content scan)
- [ ] Every section scanned for all 7 signal types
- [ ] High-confidence signals (3+ component architectures, explicit "before vs. after") all captured
- [ ] Medium-confidence signals evaluated for static failure test
- [ ] Low-confidence signals evaluated conservatively (when in doubt, skip)
- [ ] False positives filtered ("in other words", simple rephrasing, etc.)
- [ ] Progressive reveal rule applied: multi-section architectures planned as reveal families

### Phase 2 (opportunity map)
- [ ] Related opportunities merged (same section, same type)
- [ ] Engagement-pass conflicts resolved (Type 3 delegated when engagement-pass runs)
- [ ] Animation ownership clarified (visual-pass = structural reveals; engagement-pass = data exploration)
- [ ] Opportunity map written in structured format

### Phase 3 (injection plan)
- [ ] Budget applied per content type
- [ ] Impact scores computed (concept_density * static_failure * effort_saved * cost_efficiency)
- [ ] Opportunities ranked by impact score
- [ ] Minimum 2 static diagrams met
- [ ] Maximum 1 Manim video respected (arc-level)
- [ ] Maximum 2 ComfyUI images respected
- [ ] Cut list documented with reasons

### Phase 4 (manifest output)
- [ ] Every manifest entry has: visual_id, type, tool, inject_at, intent, spec
- [ ] Every entry has intent block with status, assignee, resolution_notes
- [ ] Every Type 1 entry has: layers, connections, style, caption
- [ ] Every Type 2 entry has: what_animates, frame_count, show_static_first, static_fallback
- [ ] Every Type 4 entry has: scene_description, duration, style, static_fallback
- [ ] Every Type 6 entry has: left panel, right panel, layout, caption
- [ ] Every Type 7 entry has: description, style, anti_patterns, fallback_if_unavailable
- [ ] Every dynamic visual (Types 2, 3, 4) has a static fallback specified
- [ ] No manifest entry requires content restructuring (inject alongside, not replace)
- [ ] Delegation list complete (all engagement-pass handoffs documented)
- [ ] Intent summary table produced with status dashboard

### Phase 5 (intent resolution)
- [ ] Resolution method chosen per intent (immediate / deferred / commissioned / subsequent pass)
- [ ] Commission briefs exported for externally-resolved intents
- [ ] Acceptance criteria defined in each brief
- [ ] Re-run behavior: resolved intents not duplicated, stale intents flagged

### Review mode
- [ ] Coverage audit: all high-confidence signals addressed
- [ ] Budget compliance: no type exceeds maximum
- [ ] Tool availability: fallbacks specified for unavailable tools
- [ ] Progressive reveal coherence: reveal families are sequential and complete
- [ ] Engagement-pass coordination: no conflicts, delegations clear
- [ ] Rendering feasibility: every entry has enough spec detail to execute
- [ ] Intent status audit: all intents tracked, stale intents flagged, deferred intents reviewed

### Voice and pedagogy (inherited from suite)
- [ ] No visual placed before the concept it depicts is earned (DO→NOTICE→CODE→NAME)
- [ ] Diagram captions are complete sentences, not labels
- [ ] Color palette consistent across all visuals in the artifact (suite shared palette)
- [ ] Visuals clarify; they do not distract from the narrative flow
