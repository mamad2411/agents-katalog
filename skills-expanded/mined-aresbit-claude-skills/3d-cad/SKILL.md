---
name: 3d-cad-skill
description: Create and iteratively refine parametric 3D CAD models through progressive refinement with inspectable feedback. Use when the task involves OpenSCAD, build123d, STL/STEP/3MF output, fixture/enclosure/adapter design, or debugging shape accuracy from renders or screenshots. Covers both generation and editing as a unified workflow.
---

# 3D CAD Skill — Progressive Refinement

Use this skill for parametric 3D modeling where geometry must be correct, manufacturable, and easy to revise. Design is inherently iterative — this skill treats generation and editing as a single unified loop, not separate tasks.

## When To Use It

Trigger this skill when the user asks for:

- A 3D printable or CAD-ready part
- OpenSCAD or build123d model generation
- Edits to an existing parametric model
- Iterative refinement of a model through multiple rounds of feedback
- Shape debugging from screenshots, renders, or exported meshes
- Precise dimensions, fit checks, tolerances, wall thicknesses, or hole placement

## Core Rule

Do not trust mental visualization of 3D geometry. Write code, render or export a view, inspect the result, then revise. One change at a time.

If the environment supports screenshots or image inspection, use them after every meaningful geometry change. If not, inspect through deterministic evidence: multi-angle orthographic projections, section cuts, bounding-box checks, and explicit dimension calculations.

Prefer multi-turn interactive refinement over attempting a perfect one-shot model. Evidence shows that iterative refinement with inspection between turns dramatically improves success rates for both novices and experts.

## Progressive Refinement Philosophy

CAD design is not a single-step task. The workflow below treats every model as a draft that improves through structured iteration:

- **Generation is the first edit** — creating a model from scratch is just the initial step in a refinement chain
- **Each turn produces inspectable evidence** — never advance without verifying the current state
- **Qualitative and quantitative checking are complementary** — visual inspection catches proportion errors; numerical checks catch dimensional errors
- **Parameter consistency is proactive** — validate that related parameters are mutually consistent before rendering (e.g., inner radius < outer radius, wall thickness > 0)
- **Multi-turn dialogue reduces error** — breaking complex designs into a sequence of simpler refinements produces better results than one-shot generation

## Workflow

### 1. Capture The Design Brief

Before modeling, extract:

- Target output: `stl`, `step`, `3mf`, source code only, or all of them
- Modeling stack: prefer the user's requested tool; otherwise default to the simplest proven option
- Critical dimensions and units
- Mating parts, clearances, print orientation, and strength constraints
- Whether the goal is appearance, fit, mechanism, or manufacturability

If requirements are incomplete, make explicit assumptions and keep the first version simple.

### 2. Structured Reasoning (Before Writing Code)

Before generating or editing geometry, reason through four steps explicitly:

1. **Intent Understanding** — Restate what the user wants in spatial terms. What should the model look like? What are the key features and their relationships?
2. **Modeling Analysis** — Identify which primitives, boolean operations, and transforms are needed. Which parts are base bodies, which are cutouts, which are additive features?
3. **Parameter Computation** — Compute all critical dimensions, positions, and transforms. Check that parameters are mutually consistent (no impossible geometry).
4. **Position Identification** — For edits, identify exactly which parts of the existing model need to change and what the edit sequence should be.

### 3. Build The Smallest Correct Parametric Skeleton

Start with a coarse model that proves overall proportions and alignment:

- Define top-level parameters first.
- Separate base body, cutouts, mounts, and cosmetic details.
- Keep transforms and coordinate frames explicit and minimal.
- Delay fillets, chamfers, text embossing, and decorative features until base geometry is correct.
- Validate parameter consistency before rendering: check that holes are smaller than the bodies containing them, clearances are positive, and wall thicknesses are printable.

Structure code so a later pass can adjust one concern without rewriting the whole model.

### 4. Render And Inspect (Multi-View + Dual Modality)

After each meaningful change, inspect the result systematically from multiple angles.

**Qualitative inspection (visual):**
- Check silhouette and proportions from at least 3 orthogonal views (front, side, top) plus an isometric view
- Check symmetry and centering across all major axes
- Check whether holes, cutouts, and mating faces are centered and aligned
- Check whether the model matches the user's stated intent, not just whether the code runs

**Quantitative inspection (numerical):**
- Verify critical dimensions against the design brief with explicit measurements
- Check bounding box dimensions
- Validate hole diameters, wall thicknesses, and clearance distances
- Confirm that parameter relationships are logically consistent

**Fabrication risk:**
- Check printability: unsupported spans, wall thickness, trapped voids, and impossible overhangs
- Check for sharp internal corners where a radius is likely needed
- Identify thin or fragile members

Read [`references/geometry-iteration.md`](/home/ares/.claude/skills/3d-cad-skill/references/geometry-iteration.md) for the full inspection loop and diagnostic patterns.

### 5. Fix One Geometric Issue At A Time

When something looks wrong:

- Name the defect precisely (not "it looks wrong" but "the left mounting hole is offset +2mm in X")
- Identify the smallest parameter or operation likely causing it
- Change one thing
- Re-render and compare against the previous result
- If the user provides feedback, treat it as an editing instruction — localize the affected geometry and apply the minimal edit

Avoid broad rewrites unless the part architecture is clearly wrong.

### 6. Deliverables

Default deliverables:

- The source model
- A short list of exposed parameters
- Assumptions and unresolved risks
- Export instructions if the environment cannot generate meshes directly

When useful, also provide:

- Recommended print orientation
- Suggested tolerance ranges
- Notes on likely failure points or reinforcement options

## Quality Bar

The final result should be:

- **Parametric** rather than hard-coded — critical dimensions are named variables
- **Geometrically valid** — code executes without errors, booleans produce manifold geometry
- **Internally consistent** — no contradictory parameters (e.g., cutout larger than its parent body)
- **Easy to inspect and revise** — operations are grouped by concern, transforms are explicit
- **Dimensionally explicit** — key measurements are stated, not buried in expressions
- **Realistic for the intended fabrication method** — wall thicknesses, clearances, and overhangs are appropriate
- **Honest about assumptions** — unverified fit, estimated dimensions, and design risks are flagged
