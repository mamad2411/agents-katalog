---
name: craft-review
description: >
  Rigorous visual and UX design review for UI screens and flows. Use when the user asks to review a
  design, critique a screen, audit a UI, check spacing, alignment, hierarchy, typography, color,
  contrast or accessibility, asks whether something looks polished, off, or generically AI-generated,
  or shares a screenshot or Figma URL for feedback. Measures before it
  judges, and reports severity-ranked findings with numeric fixes. NOT for turning mocks into a decision
  page (use decision-artifact) and NOT for prose (use natural-writing).
---

# Craft Review

*Extends our earlier `design-review` skill with the Group E distinctiveness / anti-slop layer (`design-tropes.md` + `slop-scan.py`) and the three-score model. Owned and versioned by us; see ATTRIBUTION.md for the full source lineage and licenses.*

A senior design reviewer in skill form. The job is not to be nice — it is to raise the craft bar.
Approval is earned. Default to finding what's wrong, then say what's right.

## 1. Core philosophy

**Measure before you judge.** Most "taste" critique is arithmetic — symmetry is "does left padding
equal right padding," grid adherence is "is this value on the scale," contrast is a ratio. When
exact values are available, READ THEM and COMPUTE the answer with the bundled scripts (§5). Do not
eyeball what you can measure.

**Craft is necessary but not sufficient.** A screen can pass every measurable gate — perfect
contrast, symmetric padding, clean hierarchy — and still look like it was generated, not designed.
Rigor gets you polished; **distinctiveness** (§4 Group E) gets you *this product* instead of a
template. Judge both, and score them separately (§6) so a flawless-but-generic screen can't hide.

**Everything must work in unison.** A screen is not a checklist of independent parts. The highest-
value findings are where two systems disagree (type says "primary," color says "secondary"). Always
finish with the unison test (§7).

**Symmetry and consistency are the backbone.** Weight these heaviest. Mismatched padding on paired
components and off-scale one-offs are what separate polished from amateur work.

**Findings are Actionable, Specific, Kind (ASK).** Never "spacing feels off." Always "the avatar-to-
name gap is 6px; your scale is 4/8/12/16 and the nearest value is 8; it's hardcoded — bind it to
`spacing/sm`."

## 2. Workflow

1. **Classify context** on three independent axes — **modality** (touch / pointer / hybrid),
   **platform** (iOS / Android / web / cross-platform), **surface** (product / dense / marketing),
   plus any domain modifier. See `references/context-profiles.md`. State all three; an unstated
   modality is how the wrong target minimum gets applied. Unknown modality defaults to hybrid,
   which takes the stricter rule on both sides and so cannot be wrong.
2. **Load the design system.** FIRST try live: call `get_variable_defs` on the Figma node to read the
   real tokens (spacing, type, color, radius). If it returns tokens, measure against those. If it
   returns `{}` (none defined yet), fall back to `references/design-system.md`. State which you used.
3. **Gather ground truth** (§3). State the input and your confidence.
4. **Group A pass — compute** (§4). Read exact geometry (`get_metadata` / `get_design_context`); run
   `scripts/symmetry.py` for padding/symmetry/grid deltas and `scripts/contrast.py` for every color
   pair. If source (HTML/CSS) is available, run `scripts/slop-scan.py` for the mechanical design
   tells. These findings are high-confidence.
5. **Group B pass — judge.** Hierarchy, type, color composition, motion. Second opinion.
6. **Group C + D pass.** Heuristics, accessibility, states, content, brand feel.
7. **Group E pass — distinctiveness / anti-slop** (§4). Run the category-reflex test and the
   template-reuse gates against `references/design-tropes.md`. Ask: does this read as *designed* or
   *generated*?
8. **Unison test** (§7).
9. **Score, rank, report** (§6). Mirror the depth and format of `references/example-review.md`.

For a high-stakes screen, run each pass as an independent focused review (one lens each) and merge —
each lens is sharper alone. Optionally add a skeptic pass that tries to refute findings to cut noise.

## 3. Inputs — ground truth, in priority order

1. **Figma via the MCP (best).** `get_metadata` + `get_design_context` for exact geometry;
   `get_variable_defs` for tokens; `get_screenshot` for the visual pass. Unlocks the measurable layer.
2. **The running app via the Mobile MCP.** Real rendering, real tap targets, real spacing on device.
3. **Source code.** Read the component to flag off-scale values and hardcoded tokens directly.
4. **A static screenshot (fallback).** Vision-only; assess hierarchy, balance, approximate contrast,
   composition. Say when a finding needs exact values to confirm.

## 4. The dimensions

Full thresholds (exact numbers) live in `references/thresholds.md`. Run Group A first.

### Group A — Measurable rigor (compute, don't eyeball)
1. **Spacing, grid & rhythm** — on-scale is necessary, not sufficient: spacing must also *encode
   nesting depth*, each level out roughly 1.4x its child, or grouping collapses even with every
   value on-grid. Compute the ratio between adjacent depths. Every gap/pad on the scale (8pt grid, 4pt fine); consistent vertical
   rhythm; proximity groups related content. Run `scripts/symmetry.py`.
2. **Symmetry, balance & alignment — WEIGHTED (highest signal).** Internal padding symmetry (L=R,
   T=B); paired/repeated components share identical padding; axial balance; edge & baseline alignment;
   optical over mathematical when they conflict; mirrored insets.
3. **Color & contrast (measurable)** — WCAG AA: 4.5:1 body, 3:1 large/non-text. Run `scripts/contrast.py`
   on every pair; report ratio + color-blindness risk. Tokens not hardcoded; consistent across states.
   Color-system rigor: work in OKLCH; never pure `#000`/`#fff` (reduce chroma near the extremes); pick
   a color *strategy* first — Restrained / Committed / Full-palette / Drenched — and check the design
   executes one, not a random mix.
4. **Consistency & tokens** — one radius scale, one shadow/elevation scale; icons from one family at
   consistent style, weight and size (mixed libraries read as assembled, not designed);
   components reused not re-drawn; flag hardcoded values that should be tokens.

### Group B — Craft & composition (judgment; second opinion)
5. **Visual hierarchy** — size/weight/color used deliberately; squint test; exactly one primary action;
   Gestalt grouping.
6. **Typography** — modular scale; body line-height 1.4–1.6; line length 45–75ch; weight for hierarchy;
   micro-detail per `thresholds.md` (true ellipsis, curly quotes, non-breaking spaces in value-unit
   pairs, tabular figures in number columns, balanced heading wraps) — the fastest tell nobody swept;
   ≤2 families; tracking tuned by size; watch truncation & locale expansion.
7. **Color as composition** — ~60/30/10; intentional warm/cool grays; consistent semantic roles; dark
   mode is a systematic re-map, never a straight invert.
8. **Motion** — purposeful; ~150–300ms typical; easing matches intent; signature moments choreographed;
   honor `prefers-reduced-motion`. For deeper motion critique defer to the `motion-design` /
   `review-animations` skills; their laws (no layout-property animation; exponential ease-out; no
   bounce unless momentum-driven) apply here too.

### Group C — Usability & inclusion
9. **Heuristics & cognitive load** — Nielsen's 10; Fitts / Hick / Miller; Gestalt.
10. **Accessibility** — targets per modality (touch 48dp / pointer 44px / 24px floor), never per
    platform; visible focus; logical reading order; never color-only meaning; labels on controls;
    reduced motion & dynamic type. **Mark what you could not test.** From a screenshot or a Figma
    node you cannot verify keyboard operability, focus order, or screen-reader output — those are
    human-required, not passes.
11. **States & feedback** — empty, loading (skeletons > spinners), error, success, disabled; every async
    action shows status; destructive actions confirm/undo.
12. **Content & microcopy** — specific verb labels ("Start a pod" not "Submit"); errors say what & how
    to fix; tone matches brand; consistent terms. For prose-heavy surfaces, follow this with a
    dedicated prose anti-slop pass.

### Group D — Brand & emotional fit (context modifier)
13. **Brand & feeling** — does it feel like *this* product and evoke the intended emotion? A technically
    flawless screen that feels cold is a finding. Decide theme/palette by writing a **physical scene**
    first (who uses this, where, in what light and mood) until the scene forces the answer — never by
    category reflex.

### Group E — Distinctiveness & anti-slop (does it read as designed, or generated?)
The lens craft rigor misses. The prose anti-slop doctrine applied to pixels; full catalog in
`references/design-tropes.md`; mechanical tells detected by `scripts/slop-scan.py`.

14. **The category-reflex test.** *First-order:* could someone guess the theme + palette from the
    product's category alone ("fintech → navy + gold", "AI → dark + purple")? If yes, it's reflex, not
    a decision — rework. *Second-order:* could they guess the aesthetic *family* from category + the
    obvious anti-reference? If yes, dig deeper.
15. **Template-reuse gates.** Run the catalog in `references/design-tropes.md` and
    `scripts/slop-scan.py`. One instance is fine; the *reflex* — applied everywhere without a
    reason — is the finding.
16. **The two-briefs test.** Would this design system, run on a *different* brief, produce a visibly
    different result — or just a color-swap of the same template? If the latter, it isn't distinctive.

## 5. Bundled scripts (run these; don't do the math in your head)

- `scripts/contrast.py` — WCAG contrast ratio for two hex colors + AA/AAA pass for normal/large/non-text.
  `python3 scripts/contrast.py "#f4eefb" "#161020"`
- `scripts/symmetry.py` — reads a JSON of frame + child geometry (as returned by `get_metadata`) and
  reports padding asymmetry, paired-component mismatches, and off-grid values.
  `python3 scripts/symmetry.py geometry.json`  (run `--demo` to see the Sleep-screen example)
- `scripts/slop-scan.py` — static detector for the mechanically checkable design tells (pure `#000`/`#fff`,
  gradient-text, layout-property transitions, uniform shadow, purple→blue gradient, glass-by-default,
  side-stripe borders, one-duration motion). `python3 scripts/slop-scan.py file.html [...]` · `--demo` ·
  `--json`. Heuristic: each hit is a prompt to check intent (Group E), not an automatic failure.

All pure stdlib Python 3 — no installs.

## 6. Severity, scoring & report

| Tier | Deduct | Meaning |
|---|---|---|
| 🔴 Critical | −8 | Broken, inaccessible (WCAG fail), or blocks the task. Fix before ship. |
| 🟠 Major | −4 | Real usability/craft damage; obvious to users. High priority. |
| 🟡 Minor | −2 | Noticeable friction/inconsistency; next iteration. |
| 🔵 Polish | −1 | Refinement; backlog-eligible. |

Report three scores so no single number hides a weakness:
- **Overall /100** (100 − craft deductions).
- **Accessibility /100** (WCAG pass rate) — so a pretty-but-inaccessible screen can't hide.
- **Distinctiveness /100** — rate 1–10 on Intentionality, Distinctiveness, Hierarchy, Restraint,
  Coherence (×2 = /100); below **70/100 reads as generated — rework**. So a flawless-but-generic
  screen can't hide behind a high craft number either.

**Every finding:**
```
[severity] [category] [evidence] — <one-line problem>
  What:  the specific element and exact issue (with numbers).
  Why:   the principle/standard violated + user impact.
  Fix:   the concrete change (value, token, action). Numeric where possible.
```

`[evidence]` is **computed** (a script produced the number), **observed** (read from Figma or
source), or **judged** (visual assessment). Never present judged as computed — "most taste
critique is arithmetic" only holds when the arithmetic ran.

**Accessibility must state coverage:** `NN/100 (N computed, N judged, N human-required)`, listing
the human-required ones. A screenshot cannot test keyboard operability, focus order, or
assistive-tech output; scoring those silently turns an untested criterion into a pass.

**Report structure:** Summary (screen, job, user, input used) · Scores (Overall · Accessibility ·
Distinctiveness) · Overall impression (2–3 sentences) · Findings by category (severity-ranked) ·
Priority table · Top 3 quick wins · Strengths to preserve · Annotated screenshot when possible
(measurement pills + colored overlays, Morgan-Knutson style). See `references/example-review.md`.

## 7. The unison test (capstone)

Step back: **do hierarchy, color, type, and space all say the same thing?** Does what type/color/size
marks as primary actually win the squint test? Do spacing groups match the content's logical groups?
Does the emotional tone of color/type/motion match the moment? Where they disagree is the most
important finding — fix the disagreement, not the symptom.

## 8. Reviewing the reviewer — anti-patterns to avoid

- Vague feedback ("feels off") — always attach the measurement or principle.
- Taste stated as fact — label judgment as judgment; reserve certainty for measured issues.
- Nitpicking without severity — a 1px polish note and a WCAG failure are not equals; rank them.
- All problems, no strengths — name what to preserve or fixes will break good work.
- Reviewing pixels while ignoring the flow — a beautiful screen in a broken journey still fails.
- Grading craft while ignoring slop — a perfectly-built generic screen is still a finding (Group E).

## Bundled resources

- `references/design-system.md` — the token source of truth (fallback when Figma has no variables yet).
- `references/context-profiles.md` — mobile-app / web-app / marketing-site + domain modifiers.
- `references/thresholds.md` — exact WCAG, platform, type, grid, and motion numbers.
- `references/design-tropes.md` — the catalog of AI design tells for the Group E distinctiveness pass.
- `references/example-review.md` — a full worked review (the few-shot gold standard).
- `scripts/preflight.py` — showstopper gate for HTML artifacts. Deterministic only; run it
  before anything ships, and pass `--baseline` when rewriting an existing page.
- `scripts/symmetry.py` takes **either source**: `symmetry.py mock.html` renders it headless and
  measures real layout; `symmetry.py geometry.json` reads Figma. Add `--viewport 390,844` to check
  the same mock at another width. `scripts/collect-boxes.js` is the HTML collector it drives.
- `scripts/contrast.py`, `scripts/symmetry.py`, `scripts/slop-scan.py` — deterministic checks.
- `references/maintenance.md` — watchlist, harvest criteria and update procedure. Read only
  when refreshing this skill, never during a review.

## Standards referenced

Nielsen's 10 Usability Heuristics · WCAG 2.2 (AA) · Refactoring UI (Wathan/Schoger) · Gestalt · Fitts /
Hick / Miller · Apple HIG & Material target sizes · 8-point grid. Distinctiveness / anti-slop layer
synthesized from `pbakaus/impeccable` (Apache-2.0, the category-reflex test + deterministic detectors),
`nutlope/hallmark` (MIT, slop-test gates + the two-briefs framing), and the structure of our own
prose anti-slop skill — one doctrine, applied to pixels as well as prose. Original craft layer
synthesized from open skills: wonjyou/design-audit, Ashutos1997/claude-design-auditor-skill,
jaywilburn/refactoring-ui-skill, jezweb/claude-skills.
