---
name: hunter-visual
description: >-
  Adjudicate visual and layout deviations from captured screenshots against
  objective thresholds. Load when you hold a screenshot, DOM/computed-style
  capture, or design artifact and must decide whether what rendered deviates
  from what was intended. Specifies a systematic sweep order and objective
  thresholds — WCAG 2.2 contrast ratios, touch-target minimums, overflow and
  clipping, truncation, z-index occlusion, responsive breakpoint integrity,
  dark-mode parity, loading/empty/error states, font fallback, layout shift —
  and strictly separates objective defects (promotable to a Find) from
  subjective critique (advisory, never a Find). Use to inspect a capture, grade
  layout, check contrast, or measure a visual Sign.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hunter Visual

Assumes `hunter-doctrine` is loaded. This skill adjudicates pixels; it does not
capture them — `hunter-web-probe` supplies the screenshots and, where possible,
the DOM/computed-style dump. You read the capture yourself; confirming a file
exists is not inspection. A screenshot of a crash dialog is still a `.png`.

## The line that keeps the bag honest

Every finding here is one of two kinds, and they never mix:

- **Objective defect** — measurable against a stated threshold from a capture:
  a contrast ratio, a pixel dimension, an overflow, an occlusion, a missing
  state. It has a number and a rule. It is promotable to a Find via
  `hunter-repro`.
- **Subjective critique** — an aesthetic opinion: "the spacing feels cramped",
  "the palette is dated", "the hierarchy could be stronger." It has no
  threshold. **It is NEVER a Find.** Record it in a separate `advisory` list,
  clearly labelled, and let it stop there.

Blurring these is the failure this skill exists to prevent. An aesthetic opinion
in the bag makes every real Find easier to dismiss. When unsure which kind a
finding is, ask: can I state the exact threshold it violates from the capture? If
no, it is advisory.

## Inputs

- One or more captures per surface: full-page screenshot per viewport, and
  ideally a computed-style/accessibility-tree dump for exact measurement.
- The intended state, if declared: a design system, style guide, or baseline
  screenshot (sets `conformance`/`regression`); otherwise universal correctness
  (`defect`).
- Coverage context: which viewports, modes, and states are represented. Note
  gaps up front — a single light-mode desktop capture yields at most a limited-
  coverage verdict, never a global PASS.

## Sweep order

Walk in this order for every capture. Order matters: show-stoppers first so they
are not buried, measurable defects next, advisory last.

### 1. Triage — is the intended content even here

Before measuring anything, check the content rendered at all. These are CRITICAL
objective defects:
- empty regions where content belongs (unrendered charts, broken `<img>`
  placeholders, blank-but-bordered containers)
- literal `undefined` / `null` / `NaN` / `[object Object]` rendered as text
- placeholder residue: `Lorem ipsum`, `TODO`, `John Doe`, dummy emails in
  production-looking UI
- visible error/stack output, `500 Internal Server Error`, unstyled-content
  flash (default browser button styling on a custom design = font/CSS load
  failure)

### 2. Contrast — WCAG 2.2, objective

Text and meaningful non-text must meet these ratios. Prefer exact computation
from the computed-style dump (foreground vs resolved background); fall back to
the estimation table only when no style data exists, and flag such findings for
tooled confirmation.

| Element | AA (promotable threshold) | AAA (advisory target) |
|---|---|---|
| Body text (< 18pt, or < 14pt bold) | ≥ 4.5:1 | ≥ 7:1 |
| Large text (≥ 18pt, or ≥ 14pt bold) | ≥ 3:1 | ≥ 4.5:1 |
| UI components, focus indicators, graphical objects | ≥ 3:1 | — |

Below AA is an objective defect. Between AA and AAA is advisory (state the ratio;
do not promote unless the design system declares AAA as the authority). When only
a screenshot exists, use these cues and mark the finding `contrast-estimated`:

| Cue | Likely ratio | Action |
|---|---|---|
| Legible, full saturation | probably ≥ 4.5:1 | pass; flag for tooled check |
| Noticeably soft/faded | probably 3.0–4.5:1 | MEDIUM, needs tooled check |
| Required squinting to read | probably < 3.0:1 | HIGH–CRITICAL |
| Pale grey on white / grey on grey | likely fails AA | CRITICAL |

### 3. Target size — WCAG 2.2

Interactive targets: **≥ 24×24 CSS px** is the WCAG 2.2 AA floor; **≥ 44×44 px**
is the comfortable/iOS-HIG target. Below 24×24 (without the spacing exception) is
an objective defect. Also flag overlapping hit areas and gaps below 8px between
adjacent targets. Measure from the DOM box where available; estimate from the
screenshot with the viewport scale when not.

### 4. Overflow, clipping, truncation

- text bleeding outside its container, or overlapping other text
- content clipped mid-line without a scroll affordance
- horizontal scrollbar at mobile width (content wider than viewport)
- text silently truncated **without** an ellipsis or visible scroll — the silent
  case is the defect; an intentional ellipsis on constrained text is not
- badges/labels overlapping adjacent sections

### 5. Z-index and occlusion

- a control or text covered by another element (modal backdrop over its own
  close button, sticky header over first content row, tooltip clipped by
  `overflow:hidden`)
- an occluded interactive target is both a visual and a functional defect — note
  it for `hunter-web-probe` to confirm the interaction is actually blocked

### 6. Responsive breakpoint integrity

Compare the three viewports supplied by `hunter-web-probe` (1440×900, 768×1024,
375×812). Objective defects:
- layout breaking at a breakpoint (columns not collapsing, fixed-width overflow)
- nav failing to collapse into a working menu at mobile width
- content reflowing to overlap or clip
- tap targets shrinking below the §3 floor on the smaller viewports

### 7. Dark-mode parity

When both modes are supplied (or the product advertises dark mode):
- pure white (`#FFF`) text/surfaces on a dark background (glare)
- dividers/borders that vanish in one mode
- status colours that fail contrast in one mode (re-run §2 per mode)
- glass/blur surfaces washing out content, or transparent cards in light mode
Absence of a dark mode the product never claimed is **advisory**, not a defect.

### 8. State rendering — loading, empty, error

For each state supplied:
- **loading**: skeleton/shimmer or a determinate indicator, not frozen stale
  content and not a spinner where content should already be
- **empty**: a meaningful zero-state message, not a blank bordered box (per the
  brand, field-condition phrasing, not "No results")
- **error**: visible and specific, not swallowed and not a raw trace
A state that is missing from the evidence is **dark**, not passing — record it as
a coverage gap.

### 9. Font fallback and layout shift

- fallback font visibly substituted (metrics differ: wrong weight/width) →
  webfont load failure
- FOUT/FOIT residue captured mid-swap
- layout shift: if before/after captures around load are supplied, flag content
  jumping after first paint (the objective proxy for CLS); note the shifted
  element and direction

## Severity mapping

Map objective defects onto the doctrine verdict inputs; advisory items carry no
severity that can gate a verdict.

| Severity | Objective defect examples |
|---|---|
| CRITICAL | content unreadable, overlapping text, missing/placeholder content, contrast < 3:1 on body, occluded core control |
| HIGH | broken layout, target < 24×24, contrast 3–4.5:1 on body, nav not collapsing, error state swallowed |
| MEDIUM | inconsistent spacing measurable against a token, suspect contrast (estimated), weak-but-present signifier |
| LOW | cosmetic alignment drift measurable but non-blocking |

## Outputs

Per capture, emit visual Signs for `hunter-repro` and a separate advisory list.

```json
{
  "sign_id": "sign/3d1e",
  "surface": "GET /dashboard @ 375x812 — 'Sync' status text",
  "observed": "muted status text contrast 2.9:1 against card background",
  "measurement": { "ratio": 2.9, "threshold_aa": 4.5, "source": "computed-style" },
  "authority": "spec: wcag-2.2 SC-1.4.3 (AA body text >= 4.5:1)",
  "artifacts": ["web/dashboard/mobile/initial.png",
                "web/dashboard/mobile/computed-style.json"],
  "element": ".sync-status",
  "severity": "HIGH",
  "kind": "objective"
}
```

```json
{
  "advisory": [
    { "surface": "GET /dashboard", "note": "KPI card hierarchy reads flat; a
      larger primary metric would aid scanning", "kind": "subjective" }
  ]
}
```

Plus a coverage line stating which axes were represented and which are dark:
`visual: dashboard — light+desktop, light+mobile probed · dark-mode dark ·
error-state dark`.

## Handoff

- Objective Signs → `hunter-repro`. Note: visual promotion still requires 2 of 2,
  which for a static capture means the deviation is present in two independent
  captures of the same surface under the same conditions, or one capture plus the
  computed-style measurement that proves it. A single unmeasured screenshot is a
  Sign.
- Occlusion/false-affordance Signs → `hunter-web-probe` to confirm the
  interaction is actually blocked before promotion.
- Advisory list → the report as advisory only. It never enters the bag and never
  moves a verdict.

## Never

- **NEVER** put an aesthetic opinion in the bag. Subjective critique is advisory,
  full stop.
- **NEVER** state an exact contrast ratio from a screenshot alone; mark it
  `contrast-estimated` and flag for tooled confirmation.
- **NEVER** mark a missing state or mode as passing. Missing is dark.
- **NEVER** claim PASS from a single-axis capture; that is at most limited
  coverage.
