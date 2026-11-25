---
name: deep-dive-html
description: Create polished standalone HTML deep-dive explainers for research, investigations, architecture, strategy, and technical communication. Turns a task, system, plan, repo investigation, or technical explanation into a single-file HTML artifact with strong information design, inline SVG diagrams, and a technical publication aesthetic. Use when the output deserves more than markdown but less than a full app.
---

# Deep Dive HTML

## When to use this

Use this skill when:
- The output is a technical explanation, investigation, architecture overview, plan, or comparison
- The audience will read it in a browser (shared link, PR artifact, local file)
- Visuals (diagrams, tables, matrices) would genuinely help understanding
- The output should feel polished enough to send to a CTO or put in a design review

Do NOT use this when:
- A markdown file or Mermaid diagram in a PR description is sufficient
- The content is purely code (use a code review or diff instead)
- The content is ephemeral (a quick answer in chat is fine)
- The user just wants data, not a narrative

## Default narrative arc: State → Intent → Direction

Every deep dive follows this arc by default. The reader cannot understand intent without ground truth, and cannot evaluate direction without intent.

### 1. Current State (always first, always biggest)

The "you are here" map. This is the ground truth the reader needs before anything else makes sense. Lead with a visual — topology, dependency graph, data flow, or ownership matrix — then annotate it with prose.

This section answers: *What exists right now? What are the boundaries, relationships, and key metrics?*

### 2. Intent / Gap

Why are we looking at this? What's the delta between current and desired? Show it visually: before/after paired diagrams, gap table, coverage matrix showing what's missing, or a diff-style overlay.

This section answers: *What's the motivation? What's broken, missing, or changing?*

### 3. Direction

Specific path forward. Phased timeline, decision tree, implementation sequence, ranked recommendations. This is where options and tradeoffs live.

This section answers: *What do we do about it? In what order? What are the tradeoffs?*

Other structural patterns (investigation, comparison, etc.) are opt-in variants of this arc — they may reweight sections but should still ground the reader in current state first.

## Default page contract

Unless the user explicitly wants something more editorial or visually expressive, default to:
- A single main content column
- A lightweight top-of-page TOC for multi-section pieces
- One direct hero with thesis and lede
- **Visual-first sections**: every major section leads with a diagram, table, or visual — prose annotates the visual, not the other way around
- 3-5 focused sections after the opening
- 2-4 diagrams total for most pieces (more than before — visuals are the spine now)
- Tables for status, comparisons, or coverage when they scan better than cards
- One primary surface style and at most one secondary emphasis style
- Every scroll-viewport should have at least one visual element

Avoid by default:
- Sticky sidebars for short documents
- Decorative side rails
- Text-first sections where a diagram could lead instead
- Architecture-first openings when the real task is prioritization or readiness
- Glassmorphism, ornamental gradients, or concept-page styling
- Too many card types, grid systems, or visual motifs in one page
- Diagrams that repeat headings instead of answering a reader question
- Filler diagrams that exist only to meet a visual quota — quality over quantity

When in doubt, choose the calmer, more memo-like option.

## Output format

One self-contained `.html` file:
- Inline CSS (no external stylesheets)
- Inline SVG for all diagrams (no external images unless user provides URLs)
- CSS variables for all colors (including SVG fills) so dark mode works
- Dark mode via `prefers-color-scheme: dark`
- Print styles via `@media print`
- Minimal or zero JavaScript (smooth-scroll TOC is the exception)
- Opens cleanly via `file://` protocol
- Default location: `docs/<slug>.html` in the working repo

## Workflow

### 1. Determine artifact type

| Type | When |
|------|------|
| System deep dive | Explaining how a system works end-to-end |
| Investigation summary | Reporting findings from a codebase or system audit |
| Architecture explainer | Documenting boundaries, ownership, data flow |
| Product walkthrough | Step-by-step how a feature or workflow operates |
| Plan / roadmap | Phased delivery, migration, or strategy |
| Technical comparison | Evaluating options, tradeoffs, approaches |

### 2. Gather source material

Read only the artifacts needed to explain the task accurately: repo files, notes, schema, screenshots, or relevant pages. If the user already has a draft artifact, inspect that before redesigning.

**Key rule:** Read before you write. Never fabricate system details.

### 3. Decide whether the artifact is for decision-making or reference

If decision-making, lead with:
- Thesis
- Current state visual (ground truth first)
- Gap or recommendation
- Ranked findings, priorities, or status

Only move into deeper architecture after the reader understands what exists now and what matters.

If reference, still open with a concise thesis, a current-state visual, and an orientation block before deeper sections.

### 4. Plan the narrative structure

Good technical deep dives follow the State → Intent → Direction arc:
1. **TOC** at the top (with anchor links) when 3+ sections
2. **Lede / thesis** — one paragraph that tells the reader what this is about and why it matters
3. **Current State** — lead with a visual (topology, dependency graph, data flow). Prose annotates the visual. This is the largest section.
4. **Intent / Gap** — before/after paired diagram, gap table, or coverage matrix. What's the delta between now and desired?
5. **Direction** — ranked recommendations, phased timeline, or decision tree. Each option with tradeoffs.
6. **Supporting sections** — each leads with a visual, followed by concise prose that annotates it
7. **Closing** — ranked takeaways, acceptance criteria, or next steps

### 5. Choose visualizations

Use the lightest visualization that makes the point clearer than prose alone.

| Visualization | Use when |
|--------------|----------|
| Topology / boundary diagram | Reader needs to know what lives where |
| Dependency / relationship graph | Show what depends on what, what breaks if X changes |
| Before/after paired diagrams | Current vs. target state side-by-side — ideal for Intent/Gap sections |
| Sequence / swimlane | Time order matters (request flows, pipelines) |
| State / loop diagram | System revisits components or branches |
| Status or comparison table | Reader needs to scan multiple items quickly |
| Coverage / gap matrix | What exists vs. what's needed (heatmap-style) |
| Ownership matrix | Many-to-many relationships (components, teams) |
| Ranked board / scorecards | Order matters more than topology |
| Timeline | Phased plans, incidents, rollouts |

Prefer a table over a card grid when the content is mostly labels, status, and short explanations.

**Section structure rule:** Major sections lead with a visual, then prose annotates it. The visual is the primary information vehicle; text explains what the visual shows and why it matters.

**Anti-patterns:**
- Do not write a section as prose-first with an optional diagram at the end
- Do not add visuals that restate a heading
- Do not use decorative charts with no underlying data
- Do not turn every paragraph into a card
- Do not repeat the same visualization type throughout
- Do not spend the opening screen on architecture if the real job is priorities or readiness
- Do not use many equal-weight card grids where a table would scan faster
- Do not add filler diagrams just to have visuals — if no diagram genuinely helps, use a table or skip

### 6. Apply a visual budget

For most artifacts:
- 1 hero block
- 1 current-state visual (the anchor diagram — this is the most important visual)
- 1 intent/gap visual (before/after, gap table, or coverage matrix)
- 1 direction visual (timeline, decision tree, or ranked board)
- 0-2 additional supporting figures in the body
- 0-2 tables when they improve scan speed

The State → Intent → Direction arc naturally produces 3 primary visuals. Additional figures should earn their place.

If the page starts accumulating many card species, competing grids, or multiple ornamental motifs, simplify. Prefer one strong figure and one strong table over five decorative cards.

### 7. Build the HTML

**Visual direction:**
- White or near-white background
- Restrained accent colors through CSS variables
- Clean sans-serif typography
- Generous whitespace
- Strong figure captions on every diagram
- Low-noise cards and separators
- Tables for high-density status or comparison content

**Avoid:**
- Beige/paper textures (unless explicitly requested)
- Heavy ornamental gradients
- Giant walls of paragraph text
- Generic AI landing-page aesthetic
- Decorative diagrams that don't explain anything
- Hardcoded SVG colors when CSS variables will do
- Many equal-weight modules before the core thesis lands

### 8. Add metadata

Include in the artifact:
- Title and subtitle
- Date with minute precision (for active decision-making artifacts)
- Scope statement (what this covers and what it doesn't)
- Author or source attribution if relevant

### 9. Verify

At minimum:
- [ ] HTML opens cleanly in browser
- [ ] First screen explains the thesis before deep detail
- [ ] Hierarchy reads well — headings, spacing, visual weight guide the eye
- [ ] Diagrams are legible without zooming
- [ ] Tables or ranked boards scan quickly
- [ ] Page doesn't feel like blocks of text or like a design exercise
- [ ] Dark mode looks correct
- [ ] No placeholder text remains

## Structural Patterns

All patterns are variants of the default State → Intent → Direction arc. They reweight sections but always ground the reader in current state first.

### Investigation / research
1. Lede and thesis
2. **Current state** — what exists now (dependency graph, system topology, or evidence snapshot)
3. **Intent/gap** — what we found vs. what was expected (evidence table, coverage matrix)
4. **Direction** — ranked findings or recommendations with next steps

### System deep dive
1. Thesis
2. **Current state** — topology diagram + dependency graph (lead with these)
3. **Intent/gap** — runtime lanes or sequence view showing where things break or are insufficient
4. **Direction** — ownership or schema visuals, failure-path callouts, remediation plan

### Plan / roadmap
1. Concise thesis
2. **Current state** — what exists now (before diagram)
3. **Intent/gap** — current-vs-target paired diagrams, gap table
4. **Direction** — ranked work board, milestone/dependency visualization, success criteria

### Technical comparison
1. Explicit winner or tradeoff thesis
2. **Current state** — what we have now and why we're evaluating alternatives
3. **Intent/gap** — comparison table near the top, 2-4 focused dimensions
4. **Direction** — closing recommendation with tradeoffs visualized

## SVG Diagram Guidelines

When building inline SVGs:
- Use `var(--ink)`, `var(--muted)`, `var(--blue)`, `var(--jade)` etc. for colors so they adapt to dark mode
- Use `role="img"` and `aria-label` for accessibility
- Keep text labels short (2-4 words per node)
- Use rounded rectangles (`rx="8"`) for nodes
- Use clear directional arrows for flows
- Size viewBox to content — don't pad excessively
- Always add a `<figcaption>` describing what the diagram shows
- Test that the diagram is legible at the rendered width without zooming

## Output Standard

Deliver a static HTML artifact that:
- Looks like a polished technical company post
- Reads like a clear internal deep dive rather than a marketing page
- Makes the main thesis understandable from the first screen
- Grounds the reader in current state before intent or direction
- Leads major sections with visuals, using prose to annotate
- Uses before/after paired diagrams and dependency graphs where they clarify state vs. intent
- Uses tables when they improve scan speed over cards
- Is clear enough to skim in under 30 seconds
- Is self-contained enough to keep as `docs/*.html` or delete without cleanup
