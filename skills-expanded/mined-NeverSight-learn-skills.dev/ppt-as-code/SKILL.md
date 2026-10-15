---
name: ppt-as-code
description: >
  Build HTML-based web presentations with a creator-first workflow: keep quick mode lightweight,
  use basic mode for confirmed deck planning plus script plus image flow, and use advanced mode
  for reference-driven decks, static-first delivery, optional motion follow-up, and safe
  fallbacks when file persistence or web search is unavailable.
---

# PPT as Code

> Plan and build HTML-based presentations with a creator-first staged workflow.

**Core Pipeline**: `Ingest -> Route Mode -> Load References -> Diagnose Gaps -> Produce Artifacts -> Confirm Key Decisions -> Deliver HTML`

---

## Mandatory Rules

> [!CAUTION]
> ### Serial Execution & Gate Discipline
>
> This workflow is a strict serial pipeline.
>
> 1. **SERIAL EXECUTION**: Steps must execute in order; output of each step becomes input for the next.
> 2. **BLOCKING = HARD STOP**: A `BLOCKING` step requires explicit user confirmation before continuing.
> 3. **NO SPECULATIVE EXECUTION**: Do not pre-build future artifacts before the current gate is cleared.
> 4. **KEEP THE ROUTE PROPORTIONAL**: Do not escalate a lightweight deck into a heavier stack unless the request clearly needs it.
> 5. **DEFAULT TO SHIPPING**: Deliver usable artifacts, prompts, or HTML handoff routes, not theory essays.
> 6. **FINAL ARTIFACT MUST RUN**: If the user wants a direct handoff, prefer a self-contained file or a locally runnable folder over a CDN-only prototype.

> [!IMPORTANT]
> ### Creator-First Delivery
>
> - Default delivery is **staged artifacts + HTML route or prompt pack + image plan**, not a long code dump.
> - When the user is a creator or wants to move fast, prefer staged prompts and intermediate artifacts over large code blocks by default.
> - Use full implementation only when the user explicitly asks for code or the workflow has reached the final HTML stage.

> [!IMPORTANT]
> ### Persistence Strategy
>
> - Default to **conversation-first artifacts**.
> - Only write files when the user explicitly wants persisted deck materials, or when the repo already has a clearly compatible project structure that invites file-based output.
> - When persistence is enabled, use conventional artifact names such as `deck_brief.md`, `theme_breakdown.md`, `style_options.md`, `deck_script.md`, `image_plan.md`, `index.html`, and `assets/`.

> [!IMPORTANT]
> ### PPT-First Grammar
>
> - `PPT-like` means stage-like: one active slide at a time, clear page state, and visible presentation furniture.
> - Do not let a deck drift into a long webpage, editorial article, or dashboard shell when the user explicitly asked for a presentation.
> - A finished deck must preserve clear slide roles such as cover, hook, concept, compare, quote, data, divider, and conclusion when relevant.

> [!IMPORTANT]
> ### Style Lock Rules
>
> - `quick` and `basic` still need a real visual direction; do not return a bare technical skeleton.
> - If style is undecided, recommend **3 to 4 design directions** before starting final HTML work.
> - Do not lock the final visual direction before the reference-image step when the chosen mode requires reference selection and browsing is available.
> - Once a reference is chosen, or the workflow has explicitly fallen back to style-word synthesis, translate the direction into structured design constraints before final implementation.

> [!IMPORTANT]
> ### Image Workflow Rules
>
> - Image quality beats image quantity. A weak image is worse than no image.
> - Never search body images from the full deck topic alone.
> - For each page that needs an image, first compress the page into one thesis, then derive page-level keywords, then search.
> - If image download fails, keep the source link, record the failure, and hand the link to the user for manual download instead of blocking the run.

> [!IMPORTANT]
> ### Network And Tool Fallbacks
>
> - If browsing or downloading is unavailable, do not block the workflow.
> - In `advanced`, if web reference search is unavailable, skip the web-reference branch and derive structured design constraints directly from the chosen style direction and any user-provided inspiration.
> - If file persistence is unavailable or undesired, keep the same staged artifacts in conversation instead of forcing repo writes.

> [!IMPORTANT]
> ### Runtime Source Of Truth
>
> - Runtime behavior must come from `SKILL.md` and the active mode/reference files.
> - Stable feedback should be integrated into the main docs, not left in logs.

### Role Dispatch Protocol

This skill operates as a single inline agent - no role switching required.

---

## Resource Manifest

### UI Metadata

| File | Path | Purpose |
|------|------|---------|
| skill interface metadata | `${SKILL_DIR}/agents/openai.yaml` | display name, short description, and default prompt |

### References

| Resource | Path | Runtime Use |
|----------|------|-------------|
| quick mode workflow | `${SKILL_DIR}/references/quick-mode.md` | required only when mode = `quick` |
| basic mode workflow | `${SKILL_DIR}/references/basic-mode.md` | required only when mode = `basic` |
| advanced mode workflow | `${SKILL_DIR}/references/advanced-mode.md` | required only when mode = `advanced` |
| visual and image workflow | `${SKILL_DIR}/references/visual-and-images.md` | required when style, references, or images are in scope |
| component library guidance | `${SKILL_DIR}/references/component-libraries.md` | required only when the route needs libraries |

### Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `mode-delivery` | `${SKILL_DIR}/workflows/mode-delivery.md` | mode routing and output shaping |

---

## Workflow

### Step 1: Input Ingestion

`GATE`: The request is about a web-based presentation, HTML deck, slide system, reveal.js deck, presentation page, or a closely related deck-building workflow.

`EXECUTION`:

1. Extract the request shape:
   - topic
   - audience
   - delivery context: live presentation, shared link, async reading, or screen recording
   - current stack: native HTML, React, Next.js, reveal.js, or unspecified
   - what the user already provided: notes, outline, raw material, references, images, existing code
2. Diagnose missing inputs:
   - theme breakdown
   - style direction
   - audience positioning
   - deck structure
   - visual references
   - image assets
3. Identify whether the request is about:
   - building from scratch
   - refining an existing deck
   - choosing a route
   - improving script, style, imagery, or motion
4. Decide the artifact persistence strategy:
   - default to conversation-first artifacts
   - enable file persistence only if the user asks for it or the repo clearly supports it
5. If persistence is enabled, choose the nearest reasonable project folder or deck folder that matches repo conventions.
6. Define the canonical artifact set for non-trivial runs:
   - `deck_brief.md`
   - `theme_breakdown.md`
   - `style_options.md`
   - `deck_script.md`
   - `image_plan.md`
   - `index.html`
   - `assets/`

`CHECKPOINT`:

```markdown
## Step 1 Complete
- [x] Presentation request identified
- [x] Missing inputs diagnosed
- [x] Persistence strategy defined
- [ ] Next: auto-proceed to Step 2
```

---

### Step 2: Mode Routing

`GATE`: Step 1 complete; the request is clear enough to choose a mode.

`EXECUTION`:

1. Read `${SKILL_DIR}/workflows/mode-delivery.md`.
2. Respect an explicit user choice of `quick`, `basic`, or `advanced`.
3. If the user did not choose a mode, infer it:
   - choose `quick` for MVP decks, lightweight prototypes, and "get it running first"
   - choose `basic` for creator-facing deck planning that needs confirmed breakdown, confirmed script, and image handling before HTML
   - choose `advanced` for reference-driven deck design, richer style decisions, or a static-first then motion-follow-up workflow
4. Preserve the smallest route that satisfies the request.

`CHECKPOINT`:

```markdown
## Step 2 Complete
- [x] Execution mode chosen
- [x] Routing rationale prepared
- [ ] Next: auto-proceed to Step 3
```

---

### Step 3: Reference Loading

`GATE`: Step 2 complete; one execution mode has been chosen.

`EXECUTION`:

1. Load exactly one primary mode reference:
   - `quick` -> `${SKILL_DIR}/references/quick-mode.md`
   - `basic` -> `${SKILL_DIR}/references/basic-mode.md`
   - `advanced` -> `${SKILL_DIR}/references/advanced-mode.md`
2. Load `${SKILL_DIR}/references/visual-and-images.md` when style, references, or images are relevant.
3. Load `${SKILL_DIR}/references/component-libraries.md` only when the route truly needs component or chart libraries.

`CHECKPOINT`:

```markdown
## Step 3 Complete
- [x] Primary mode reference loaded
- [x] Supporting references loaded only if relevant
- [ ] Next: auto-proceed to Step 4
```

---

### Step 4: Artifact Setup And Gap Diagnosis

`GATE`: Step 3 complete; the active mode workflow is loaded.

`EXECUTION`:

1. Define the artifact set for the chosen mode.
2. For `basic` and `advanced`, prepare the brief artifact first.
   - If persistence is enabled, materialize it as `deck_brief.md`.
   - Otherwise, keep it inline in the conversation.
3. Decide which artifacts are required now versus later:
   - `quick`: brief or outline, style directions, minimal HTML route
   - `basic`: brief, breakdown, style options, script, image plan, HTML
   - `advanced`: same as `basic`, plus structured design constraints and optional motion follow-up
4. Record the missing gaps that must be resolved before HTML is allowed to begin.

`CHECKPOINT`:

```markdown
## Step 4 Complete
- [x] Artifact list defined for the chosen mode
- [x] Immediate gaps recorded
- [ ] Next: branch into the chosen mode workflow
```

---

### Step 5: Quick Workflow

`GATE`: Chosen mode is `quick`.

`EXECUTION`:

1. Produce a lightweight deck brief:
   - topic
   - audience
   - core message
   - missing inputs
2. If the theme is still vague, create a lightweight outline before implementation.
3. If style is missing, recommend **3 to 4 style directions** and clearly mark one as the default recommendation.
4. Continue with the recommended direction unless the user explicitly wants to choose.
5. Produce:
   - a minimal slide structure
   - one cover direction
   - a minimum viable HTML route or short prompt pack
6. If the user asked for images in `quick`, use the page-thesis keyword workflow from `visual-and-images.md`, but keep the image plan lightweight.
7. Include an upgrade path toward `basic`.

`CHECKPOINT`:

```markdown
## Step 5 Complete
- [x] Lightweight structure prepared
- [x] Visual direction prepared
- [x] Minimal HTML route or prompt pack prepared
- [ ] Next: auto-proceed to Step 15
```

---

### Step 6: Basic Workflow A - Breakdown First

`GATE`: Chosen mode is `basic`.

`EXECUTION`:

1. Prepare the brief artifact with current inputs and missing gaps.
2. Recommend **3 to 4 design directions** in the style-options artifact.
3. Always include arrow / progress / page-furniture suggestions as part of the style pack, using options such as:
   - floating
   - transparent
   - large footprint
   - small footprint
4. Prepare the theme-breakdown artifact before any slide script exists.
5. The theme-breakdown artifact must define:
   - the deck thesis
   - the page sequence
   - what each slide is trying to say
   - which pages likely need images
6. If persistence is enabled, materialize these as `deck_brief.md`, `style_options.md`, and `theme_breakdown.md`.

`BLOCKING`: Ask the user to confirm the theme breakdown before any script generation begins.

`CHECKPOINT`:

```markdown
## Step 6 Complete
- [x] Brief artifact prepared
- [x] Style options prepared
- [x] Theme breakdown prepared
- [ ] Next: BLOCKING - wait for breakdown confirmation
```

---

### Step 7: Basic Workflow B - Script Lock

`GATE`: Chosen mode is `basic`, and the user has confirmed the theme breakdown.

`EXECUTION`:

1. Lock the chosen style direction.
2. If local writing-style notes exist, scan likely style docs such as `voice_profile.md`, `brand.md`, `writing_style.md`, or project notes.
3. Prepare the deck-script artifact.
4. The deck-script artifact must define slide by slide:
   - scene or page purpose
   - headline or core copy
   - supporting copy or cue text
5. If persistence is enabled, materialize it as `deck_script.md`.
6. Do not start keyword extraction or image search yet.

`BLOCKING`: Ask the user to confirm the slide script before image work begins.

`CHECKPOINT`:

```markdown
## Step 7 Complete
- [x] Style locked
- [x] Local voice guidance applied when available
- [x] Deck script prepared
- [ ] Next: BLOCKING - wait for script confirmation
```

---

### Step 8: Basic Workflow C - Image Plan

`GATE`: Chosen mode is `basic`, and the user has confirmed the slide script.

`EXECUTION`:

1. Prepare the image-plan artifact.
2. For each slide that needs imagery:
   - compress the slide into one thesis
   - derive exactly **1 to 2 page-level keywords**
   - search using those keywords plus the chosen style direction when browsing is available
   - if browsing is unavailable, provide search strings and image intent instead of pretending search happened
3. Attempt to download selected images into `assets/` only when downloading is available and persistence is enabled.
4. If download fails, record in the image-plan artifact:
   - slide number
   - keywords
   - source URL
   - failure reason
   - note: `user needs to download manually`
5. If persistence is enabled, materialize the plan as `image_plan.md`.
6. Do not hide failed downloads. Surface the links to the user.

`BLOCKING`: Ask the user to confirm the script plus image plan before HTML implementation begins.

`CHECKPOINT`:

```markdown
## Step 8 Complete
- [x] Image plan prepared
- [x] Slide-level keywords extracted
- [x] Download attempts or fallback links recorded
- [ ] Next: BLOCKING - wait for script and image confirmation
```

---

### Step 9: Basic Workflow D - Static HTML

`GATE`: Chosen mode is `basic`, and the user has confirmed the script and image plan.

`EXECUTION`:

1. Generate the static HTML output.
2. Keep the deck presentation-first:
   - one active slide at a time
   - clear navigation state
   - visible progress or page furniture
3. If persistence is enabled, materialize the final output as `index.html`.
4. If the user wants a final artifact, prefer a self-contained HTML file or a locally runnable folder.

`CHECKPOINT`:

```markdown
## Step 9 Complete
- [x] Static HTML generated
- [x] Presentation grammar preserved
- [ ] Next: auto-proceed to Step 15
```

---

### Step 10: Advanced Workflow A - Direction Selection

`GATE`: Chosen mode is `advanced`.

`EXECUTION`:

1. Prepare the brief artifact.
2. Recommend **3 to 4 design directions**.
3. If browsing is available, search for direction-shaping inspiration when it helps the choice.
4. In the style-options artifact, explain each direction in terms of:
   - tone
   - hierarchy
   - palette mood
   - imagery
   - page furniture
   - arrow / progress styling
5. If persistence is enabled, materialize the brief and style artifacts as `deck_brief.md` and `style_options.md`.

`BLOCKING`: Ask the user to choose one direction before final visual locking begins.

`CHECKPOINT`:

```markdown
## Step 10 Complete
- [x] Brief artifact prepared
- [x] Style options prepared
- [ ] Next: BLOCKING - wait for direction choice
```

---

### Step 11: Advanced Workflow B - Reference Lock Or Fallback

`GATE`: Chosen mode is `advanced`, and the user has chosen a direction.

`EXECUTION`:

1. If browsing is available, search for **3 PPT or slide-design reference images** that match the chosen direction.
2. Present found references with:
   - link
   - short label
   - why it fits
   - what to borrow from it
3. If browsing is unavailable, do not block on web references.
4. In the no-browsing path, derive the visual lock directly from:
   - the chosen style direction
   - any user-provided inspiration
   - the deck topic and audience
5. Do not lock the final visual direction before this step completes.

`BLOCKING`: Ask the user to choose one reference image if web references were produced. If the workflow used the no-browsing fallback, skip this blocking step and proceed automatically.

`CHECKPOINT`:

```markdown
## Step 11 Complete
- [x] Reference branch or no-network fallback completed
- [x] Final visual not locked prematurely
- [ ] Next: proceed to Step 12
```

---

### Step 12: Advanced Workflow C - Script And Image Plan

`GATE`: Chosen mode is `advanced`, and either a reference image has been selected or the no-browsing fallback has completed.

`EXECUTION`:

1. Translate the chosen reference, or the chosen style direction in fallback mode, into structured design constraints before HTML work begins.
2. Use a JSON design style system or an equivalent structured constraint format.
3. If local writing-style notes exist, scan likely style docs such as `voice_profile.md`, `brand.md`, `writing_style.md`, or project notes.
4. Prepare the deck-script artifact.
5. For each slide that needs imagery:
   - compress the slide into one thesis
   - derive exactly **3 to 4 page-level keywords**
   - search using those keywords plus the chosen style direction when browsing is available
   - if browsing is unavailable, provide search strings and image intent instead of pretending search happened
6. Attempt to download images into `assets/` only when downloading is available and persistence is enabled.
7. If download fails, record the same fallback fields required by `basic` and surface the source link to the user.
8. If persistence is enabled, materialize these as `deck_script.md` and `image_plan.md`.

`BLOCKING`: Ask the user to confirm the script and image plan before static HTML begins.

`CHECKPOINT`:

```markdown
## Step 12 Complete
- [x] Structured design constraints prepared
- [x] Deck script prepared
- [x] Image plan prepared
- [ ] Next: BLOCKING - wait for script and image confirmation
```

---

### Step 13: Advanced Workflow D - Static HTML First

`GATE`: Chosen mode is `advanced`, and the user has confirmed the script and image plan.

`EXECUTION`:

1. Generate the static HTML output first.
2. Keep the approved content order and visual hierarchy intact.
3. Do not add advanced motion in this step unless the user explicitly asked to skip the static-first pass.
4. If persistence is enabled, materialize the output as `index.html`.

`BLOCKING`: Ask the user whether they want a motion pass after reviewing the static deck.

`CHECKPOINT`:

```markdown
## Step 13 Complete
- [x] Static HTML generated
- [x] Static-first delivery preserved
- [ ] Next: BLOCKING - wait for motion decision
```

---

### Step 14: Advanced Workflow E - Optional Motion Pass

`GATE`: Chosen mode is `advanced`, and the user explicitly asked for a motion pass after reviewing the static deck.

`EXECUTION`:

1. Add motion only after the static deck is approved.
2. Treat motion as pacing, not decoration.
3. Use `transform` and `opacity` by default.
4. Preserve:
   - one active slide at a time
   - keyboard navigation
   - `prefers-reduced-motion`
5. Do not rewrite the approved script to justify animation.

`CHECKPOINT`:

```markdown
## Step 14 Complete
- [x] Motion layer added after approval
- [x] Reduced-motion support preserved
- [ ] Next: auto-proceed to Step 15
```

---

### Step 15: Delivery

`GATE`: The chosen mode workflow has completed.

`EXECUTION`:

1. Deliver in this order:
   - chosen mode and why
   - artifact status
   - visual direction or chosen reference or fallback direction
   - script status
   - image status, including failed downloads and manual-download links
   - static HTML status
   - optional motion status when relevant
2. Before calling the deck final, verify:
   - it still feels like a presentation
   - page furniture exists where needed
   - slide roles read clearly
   - images are page-fit, not just topic-related
   - the deck is self-contained enough for the requested handoff

`CHECKPOINT`:

```markdown
## Step 15 Complete
- [x] Final delivery follows the staged artifact order
- [x] Presentation-first checks performed
- [x] Image fallback links surfaced when needed
```
