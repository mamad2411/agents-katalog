---
name: design-canvas
description: Draft a surface, a flow, or a whole product as ARTBOARDS on one pan/zoom canvas — a link a non-engineer can open, react to and annotate — BEFORE any product code is written. Lifts the app's resolved design-system values when `$SOURCE=system`, or designs free of the repo when `$SOURCE=independent`. Writes only under `ai/design/canvas/`, never product source. The visual approval gate `/redesign` and `/art-direct` hand their proposal to; the only artifact in this pack a designer or a stakeholder can answer without reading a diff.
kind: skill
pack: ui-ux
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: design-canvas

Every other artifact in this pack ends in a diff. A diff is not something you send to a client, a designer or a founder and get "yes, but move that" back. This skill produces the thing you send.

## Premise

**This skill designs; it does not implement.** Its entire output lives under `ai/design/canvas/` — artboards plus one canvas page. It touches no component, no token file, no route. The canvas is an *input* to `/redesign` (which owns the rebuild inside the system) or `/art-direct` (which owns the language), never a substitute for either.

The failure this prevents: a redesign proposal that exists only as prose gets approved by someone who pictured something else, and the disagreement surfaces after the code is written. A canvas moves the disagreement to before.

**Two renderers, one authored artboard — and the authoring targets the weaker one.** An artboard is a plain HTML body fragment (`<Name>.artboard.html`): no framework, no build step, no imports, no template language, no logic class. It renders two ways:

| Renderer | Where | What the viewer gets |
|---|---|---|
| **static** (always) | any tool, any machine | one self-contained `canvas.html` — pan/zoom, every artboard in its own sandboxed frame. Opens in a browser; publishable as a link. View, annotate, print/PDF. |
| **editable** (opportunistic) | Claude Code only, when its bundled design-canvas payload is present | the same artboards inside a WYSIWYG canvas — click-to-select, properties panel, inline text editing, Save |

The editable renderer is a **precompiled payload pinned to the CLI build** (it lives under a versioned `bundled-skills/` path). It cannot be vendored into a project, shipped in this pack, or depended on. So: **author every artboard so the static renderer is sufficient, and treat the editable one as a bonus that may be absent.** An artboard that needs the rich runtime to look right is a defect — it is invisible to every other tool this repo supports.

## The one question this skill asks — and why asking is correct here

Before drawing anything, resolve `$SOURCE`:

- **`system`** — the design must speak the app's existing visual language. Token values are lifted from the repo and matched exactly.
- **`independent`** — the design is free of the repo: a landing page, a new product, a surface deliberately allowed to leave the system.

**Ask the user. Do not infer this one.** That sits beside — not against — [`redesign.md § Phase 1 — THE LANGUAGE-OR-COMPOSITION TEST`](../../commands/redesign.md), which forbids asking whether the fault is the page's composition or the app's language. The two are different kinds of question:

- *Is our visual language the problem?* is a **diagnosis** — an output, earned from a render and a token source. The user cannot answer it and should not be asked to.
- *Is this surface allowed to leave our design system?* is a **permission** — an input, owned by whoever owns the product. No render produces it.

Asking for a diagnosis is offloading work. Asking for a permission is not guessing at authority. Halt rather than assume `independent` for an in-repo surface.

Two more inputs, defaulted rather than asked:

- `$FIDELITY` — **`wireframe`** (structure only: grey boxes, real copy, no colour decisions — for exploring 3–5 approaches) | **`hifi`** (default when `$SOURCE=system`, because the system already settles the look).
- `$FRAMES` — which viewports get artboards. Default: the app's own primary. Common frames: phone **390×844**, tablet **834×1194**, desktop **1440×900**. A responsive claim needs two frames of the same surface, not one.

## Halt conditions

- **Halt on `var(--x)`, a utility class, or any unresolved token reference inside an artboard.** The artboard renders in a sandboxed frame with none of the app's cascade — an unresolved reference paints as nothing, silently, and the canvas looks broken for reasons nobody can see. Every value is a literal.
- **Halt on a `system` artboard whose values were not read out of the repo this run.** Each artboard carries its source citations in the manifest. Recreating the app's look from memory of the app is the single most common way this skill produces a confident lie.
- **Halt on any write outside `ai/design/canvas/`.** No component, no token file, no route, no config.
- **Halt on an artboard set that is happy-path only.** See § 3 — the states are most of the value.
- **Halt on an artboard that renders LTR for an app whose resolved direction is RTL** (or vice versa). Direction is not a detail on an Arabic or Hebrew product; a mirrored layout is a different design.
- **Halt on a handover with no computed usability floor and no explicit `NOT RUN`.** See § The usability floor. An omitted contrast check must never read as a passing one.
- **Halt on a handover with no self-critique.** See § The quality bar. Drawing once and shipping it is how a canvas that satisfies every rule above still comes out mediocre.
- **Halt on presenting the canvas as the change.** The handover names the command that implements it.

## When to use

- Before `/redesign` or `/art-direct` on anything a human other than you has to approve.
- When the ask is a *deliverable to discuss* — "something I can send someone" — rather than a change to the app.
- Whole-product redesign: one canvas per feature, not one canvas of everything (§ 4).
- Greenfield surfaces with no code yet — landing pages, an unbuilt flow, a pitch.

Not for: adopting an external reference as real HTML/CSS (**`/clone-design`**); a look decision that needs directions and a scorecard first (**`/art-direct`**, which then hands its chosen direction here); screenshotting what already exists (**`visual-check`** / **`/ui-crawl`**).

## Procedure

### 1. Resolve the design system (when `$SOURCE=system`)

Read, in this order, and resolve every value to a **literal**:

1. `_extracted-idioms.md` § Tokens / Surfaces / Voice / Breakpoints — the index of where things live.
2. The token source it names (`tokens.css`, `theme.ts`, a `tailwind.config.*` theme, Style Dictionary output, a Flutter/RN theme file).
3. **The real source of the components the surface actually uses** — not the token file alone. Anatomy, control heights, icon sizes, and state styling live in the component, and they are what makes an artboard read as *this* app rather than a generic one.

**The indirection trap.** Token files chain: `--color-primary: var(--brand-600)`, and `--brand-600` is defined in a second file, possibly per theme. Resolve the whole chain to the final literal. A one-hop resolution that stops at another `var()` produces an artboard that renders nothing, and it renders nothing *quietly*.

**One artboard is one theme.** Light and dark are different literals and therefore different artboards. Pick the app's default, say which in the manifest, and add the other only when the ask is about theming.

Lift exact numbers. Never round a `13px` padding or a `6px` radius to a 4/8 grid — the grid is your habit, not their system, and the mismatch is exactly what a designer notices first.

Record, in one line for the handover, what you matched: *"matching `lib/src/core/theme` — Cairo 16/24, 12px radii, `#0F766E` primary, 48px controls, RTL."*

### 2. Inventory the surfaces

One artboard per surface. For each, name its **primary verb** (the thing the user is there to do) — that is what the composition has to rank, and it is the input to an IA archetype from [`direction-vocabulary.md`](../../ai-patterns/direction-vocabulary.md) when the layout is being rethought rather than reproduced.

### 3. Draw the states, not just the screen

**A canvas of happy paths is a brochure.** The states are where a design is actually decided, and they are precisely what a screenshot of a working app never shows because nobody can reach them on demand. For every surface, an artboard exists for each state that surface can genuinely be in:

- **empty** — first run, no data yet. The highest-value artboard in most sets and the most frequently skipped.
- **loading** — skeleton or spinner, and *which*.
- **error** — the real failure the surface has (offline, forbidden, not-found), with real copy.
- **full / overflow** — long names, 3-digit counts, wrapped headlines, the longest string the domain permits. On an Arabic product this is also where a 40%-longer translation breaks the layout.

Skip a state only when the surface genuinely cannot enter it, and say which you skipped and why. The halt above is on silently shipping the happy path alone.

### 4. Lay out the canvas

Artboards go in a grid, grouped by surface (one row per surface: default state, then its states across). Leave **≥ 80 px** between frames in a row and **≥ 120 px** between rows — each frame carries a name strip above it, and tighter spacing makes the labels collide.

**One canvas per feature, never one per product.** A 17-screen canvas is unreadable at every zoom level: too far out to read a label, too far in to compare. Split by feature (orders / reports / settings) and name each canvas after it.

Write `canvas.json` beside the artboards:

```json
{
  "artboards": [
    { "file": "OrdersList.artboard.html",       "x": 0,    "y": 0,   "w": 390, "h": 844 },
    { "file": "OrdersListEmpty.artboard.html",  "x": 470,  "y": 0,   "w": 390, "h": 844 },
    { "file": "OrdersListError.artboard.html",  "x": 940,  "y": 0,   "w": 390, "h": 844 }
  ],
  "annotations": [
    { "id": "note-empty", "x": 470, "y": -110, "w": 300, "text": "Empty state is new — the app has no equivalent today." }
  ],
  "launch": { "view": "canvas" }
}
```

`x`/`y`/`w`/`h` are CSS px at zoom 1; `w`/`h` are the **frame** size and neither scale nor crop, so they match the artboard root's fixed size. Annotations are sticky notes on the canvas — use them for the questions you want answered ("keep this filter?"), which is what turns a canvas into a conversation instead of a presentation.

### 5. Render

**Static (always).** Assemble `canvas.html`: one self-contained page, every artboard embedded in its own sandboxed frame at its manifest position, with pan (drag), zoom (wheel / pinch), and a name strip per frame. No external requests except a webfont the design genuinely uses. This file is the deliverable and it must stand alone — it is what a Cursor or Windsurf user gets, and it is what survives being emailed.

**Editable (when available).** In Claude Code, if the bundled design-canvas payload is present, hand the *same* fragments to it for the WYSIWYG canvas: each fragment is already a valid static artboard for that runtime — it needs no holes, no tweaks, and no logic class, which is exactly why § Premise forbids authoring with them. Its absence is not an error and is not worth narrating; the static canvas is the contract.

Either way, publish the result as a link when the tool can, and hand over the file path when it cannot.

### 6. Check what you drew, then hand over

Run § The usability floor and § The quality bar **before** the handover, in that order — the floor is pass/fail and cheap, the bar is a judgement and costs a revision. Fix what they find, then hand over with both results printed and every deferred lens named.

### 7. Hand over, and name what comes next

The canvas is a gate, not a finish. The handover names the command that implements the approved version, and says plainly that nothing in the app has changed yet:

| The canvas you drew | What implements it |
|---|---|
| `$SOURCE=system`, one surface or flow | **`/redesign <scope> --from-canvas=<path>`** — the artboards are the spec; its § Phase 4.5 checks provenance, scope and encodability, and the gate does not re-run |
| `$SOURCE=independent`, direction sketches | **`/art-direct <scope>`** — the language is still undecided, which is its job, not `/redesign`'s |

**An `independent` canvas is not a `/redesign` input and `/redesign` refuses it** — building it would import a visual language the app has not adopted. The route is `/art-direct`, whose build chain codifies the language into tokens *first*; only a canvas re-drawn at `$SOURCE=system` after that codification is a valid `--from-canvas` input. Re-draw it — never edit a manifest to say `system`, which fakes the check rather than satisfying it.

## The usability floor — computed, not asserted

**Every value in an artboard is a literal — which is exactly what makes this computable here and awkward everywhere else.** In a running app, contrast depends on the cascade, the theme and whatever the component resolved to at runtime, so it has to be measured from a render. On a canvas the numbers are sitting in the markup. There is no excuse for guessing, and no excuse for skipping.

Run this **before** handover, and print the result:

1. **Text contrast** — for every text-on-background pair, compute the WCAG relative-luminance ratio from the two literals. Thresholds by role (WCAG 2.2 SC 1.4.3): **4.5:1** body text, **3:1** large text (≥ 24px, or ≥ 18.66px bold). Print the ratio, not a checkmark.
2. **Non-text contrast** — UI boundaries that carry meaning (input borders, focus rings, chart series, icon-only buttons) need **3:1** against their adjacent surface (SC 1.4.11). This is the one people skip, and it is why "accessible" apps still have invisible input fields.
3. **Target size** — interactive elements are at least **24×24 px** (SC 2.5.8, AA). Where the app's platform convention is stricter, it wins: **44pt** on iOS (HIG), **48dp** on Android (Material). Measure the drawn box, not the icon inside it.
4. **Not by colour alone** — any state the design signals with colour (error, selected, required, status) carries a second signal: a glyph, a label, a weight, a position (SC 1.4.1). Status chips are where this fails most often.
5. **Reflow** — where a phone frame is drawn, nothing requires horizontal scrolling at **320 px** (SC 1.4.10).

**`NOT RUN` is a real state and must be printed as one.** If a check could not be performed — a gradient or image background where no single literal exists, a value that resolves per theme — say `NOT RUN` and why. An omitted check silently reads as a pass, and a canvas approved on a silent pass is worse than one approved with a known gap, because nobody goes looking.

**What this floor is NOT.** It is not a substitute for `a11y-quick-check` or `ux-reviewer` against the built surface: focus order, keyboard traps, screen-reader semantics and live regions cannot be scored on a drawing at all. It catches the subset that is decided *at design time* and therefore expensive to discover after approval — which is precisely the class that currently reaches `/redesign` and fails there, after someone has already said yes.

## The quality bar — score what a drawing can carry, defer the rest by name

The halts above make a canvas **correct**. Nothing in them makes it **good**. Score the drawn artboards against [`redesign.md § Design principles`](../../commands/redesign.md) — the same rubric `/redesign` diagnoses and builds against, cited rather than restated, because a second design vocabulary in this pack would be the drift, not the fix.

A static artboard cannot carry every lens, and pretending otherwise is how "approved" comes to mean more than it should:

| The canvas CAN be scored on | The canvas CANNOT — defer and say so |
|---|---|
| information architecture · visual hierarchy (the squint test works on a drawing) · layout & rhythm · cognitive load & flow · states · consistency · locale & direction · modern register · content & micro-copy | **motion** (a build output — a drawing cannot have a hover state) · **performance** · focus order and keyboard behaviour · anything that needs interaction to exist |
| accessibility, *partially* — contrast and target size are computed above | the rest of accessibility — see § The usability floor, "what this floor is NOT" |
| responsive, *only* where two or more frames of the same surface were drawn | responsive, where one frame was drawn — do not claim it |
| **beats the current surface**, where a baseline screenshot of today's screen exists to compare against | the comparison, where nothing was captured — say `NOT COMPARED`, never assume the new one wins |

**Self-critique before handover, not after.** Score the draft, name its weakest lens, fix that, re-score. Only then hand over. This is the same discipline `/redesign` applies at its gate and `design-iterate` applies in `refine` mode; a canvas that skips it outsources quality control to whoever you sent the link to.

**The deferred lenses are named at handover, every time.** "Approved" must not quietly come to mean the motion, the performance and the interaction behaviour were approved too — they were not drawn, so they were not seen, and they get decided later by whoever is typing. That is the exact failure the state artboards exist to prevent, one layer up.

## Encodability — the check that keeps a canvas honest

Every artboard must be buildable in the app's real stack at a cost someone would actually pay. Before handing over, each surface gets one line:

| Artboard | Builds from | New work |
|---|---|---|
| OrdersList | existing `AppRecordCard`, `AppSearchField` | none |
| OrdersListEmpty | `AppEmptyState` | new illustration slot |
| OrdersListError | — | **new**: inline retry affordance the system has no component for |

A canvas whose "new work" column is empty on every row is usually a restyle wearing a redesign's clothes. A canvas whose every row is new work is a fantasy. Both are worth seeing before anyone approves it.

## Inputs

- `$SCOPE` — the surface, flow, or feature.
- `$SOURCE` — **`system`** | **`independent`**. Asked, never inferred (§ The one question).
- `$FIDELITY` — `wireframe` | `hifi` (default `hifi` when `$SOURCE=system`).
- `$FRAMES` — viewports (default: the app's primary).

## Outputs

```
ai/design/canvas/<scope>/
├── MANIFEST.md                    # what was matched + its source citations, states drawn/skipped,
│                                 # encodability table, the computed usability floor (ratios + any NOT RUN),
│                                 # the quality-bar scores + deferred lenses, open questions
├── canvas.json                    # layout
├── canvas.html                    # the deliverable — self-contained, opens anywhere
└── <Name>.artboard.html           # one per artboard
```

## Failure modes

- **An artboard the system cannot build.** A component invented because it looked right, presented beside real ones and indistinguishable from them. The encodability table exists to surface it before approval, not after.
- **Values rounded to a grid instead of lifted.** `13px` became `12px`, `6px` radii became `8px`, and the result reads as *an* app rather than *this* app. The whole value of `$SOURCE=system` is exactness.
- **Recreated from memory.** The app's look reproduced from training-data familiarity with similar apps rather than from the repo's source. Confident, plausible, and wrong in every specific.
- **An unresolved `var()` or utility class.** Renders as nothing, silently. No error, no warning, just an artboard that looks broken for reasons the viewer will attribute to the design.
- **Happy path only.** Shipped as a redesign; approved as a redesign; the empty, loading, error and overflow states then get decided during implementation by whoever is typing — which is the situation this skill exists to prevent.
- **Direction ignored.** An RTL product drawn LTR because the artboard's markup defaulted that way. Not a polish issue — a mirrored layout is a different design, and it invalidates every spacing decision on the canvas.
- **The canvas mistaken for the change.** Someone approves it and expects the app to have changed. The handover has one job: say that nothing has, and name the command that will.
- **Correct but mediocre.** Right tokens, right direction, every state drawn, fully buildable — and nobody would be pleased to receive it. Every halt in this file is a correctness check; § The quality bar is the only thing between a compliant canvas and a good one.
- **A checkmark where a ratio belongs.** `contrast ✓` is an assertion; `4.61:1 (body, AA)` is a measurement. The first hides a guess, and on a canvas — where every value is a literal — guessing is not even necessary.
- **A skipped check that read as a pass.** The `NOT RUN` state exists because silence is indistinguishable from success, and nobody audits a canvas that appeared to pass.
- **"Approved" taken to cover what was never drawn.** Motion, performance and interaction behaviour are not on a static artboard; if the handover did not name them as deferred, someone will reasonably assume they were settled.
- **One canvas for the whole product.** Unreadable at every zoom. Split per feature.
- **Authored for the rich renderer.** Holes, tweaks or a logic class snuck in, so the artboard is fine in Claude Code and blank everywhere else — including for the person who was sent the link.

## Related

- [`/redesign`](../../commands/redesign.md) — the implementer. `--canvas` dispatches this skill to draw the Phase-4 proposal before gating on it; `--from-canvas=<path>` consumes an approved canvas as the spec (its § Phase 4.5). `/redesign` owns the rebuild and every code edit; this skill owns none.
- [`/art-direct`](../../commands/art-direct.md) — upstream when the visual *language* is undecided. Its `--canvas` draws the three directions here at `$FIDELITY=wireframe` (structure is what is being chosen, so structure is what gets drawn); after its build chain codifies the chosen language into tokens, the direction comes back here at `$SOURCE=system` to feed `/redesign --from-canvas`.
- [`/clone-design`](../../commands/clone-design.md) — the opposite output: real, adoptable HTML/CSS from an external reference. This skill's artboards are never adopted as product code.
- [`design-iterate`](../design-iterate/SKILL.md) — variants of something that already renders in the app; this skill is for what does not exist yet.
- [`direction-vocabulary.md`](../../ai-patterns/direction-vocabulary.md) — the IA archetypes a rethought composition picks from (§ 2).
- [`axis-catalog.md`](../../ai-patterns/axis-catalog.md) — the per-surface completeness axes the state set in § 3 answers to.
- `@ux-reviewer` (this pack, the single WCAG owner) with [`a11y-quick-check`](../a11y-quick-check/SKILL.md) as its fast path — the floor against the BUILT surface. This skill computes the design-time subset (contrast, target size) from literals; focus order, keyboard behaviour and screen-reader semantics are judged there, since a drawing carries none of them.
