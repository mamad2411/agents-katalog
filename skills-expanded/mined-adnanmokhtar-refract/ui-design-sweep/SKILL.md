---
name: ui-design-sweep
description: Codifies the 19 UI/UX design closure verbs as detector + procedure + verify triples. Used by /polish on frontend-* stacks, /ui-sweep, /enhance-ui, and any /align-recheck run that hits a UI/UX class. Each verb has a fingerprint (what triggers it), a procedure (how to apply it safely), a verify step (what must stay green visually + a11y), and a citation (WCAG / iOS HIG / Material / Refactoring UI). Behaviour-preserving — design changes ship through visual baseline diff + a11y re-check, never blind rewrite.
kind: skill
pack: ui-ux
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: ui-design-sweep

> **19 verbs across 16 axes** — the counts differ on purpose: some axes carry more than one verb (e.g. the `tokens` axis has both `consolidate-tokens` and `extract-token`; `states` has `wire-empty/loading/error-state`). 19 ≠ 16 is expected, not a drift.

## Purpose

Apply UI/UX design corrections as closure verbs in `/polish` (frontend branch), `/ui-sweep`, `/enhance-ui`, and `/align-recheck`. Each verb is a small, named, design-system-respecting transformation with a clear fingerprint and verification step. The skill does NOT invent verbs; it operates from a **closed vocabulary of 19 verbs** drawn from `ui-principles.md` axes + the project's `_extracted-idioms.md` token / wrapper / surface inventory.

This skill is the **frontend half of `/polish`** — the structural twin of `api-consistency-audit` (backend) and `schema-consistency-audit` (data). The backend half checks envelope / error / pagination drift; this skill checks design-token / hierarchy / state / focus / motion / surface drift.

## When to use

- Dispatched by `/polish` on `frontend-*` (and `mobile-*` falling back) stacks.
- Dispatched by `/ui-sweep` Phase 5 (FIX) — each of its 8 detectors maps to one or more verbs (`ui-sweep.md § UI/UX-specific verb taxonomy`); detector 8 maps to none.
- Reached via `/enhance-ui`'s `/align-recheck` cleanup step (UI/UX classes) when the align pack is installed — `/enhance-ui` composes `/align-recheck`, which routes UI/UX-axis findings here; without the align pack, `/enhance-ui` dispatches this skill directly for its cleanup step.
- Dispatched by `/align-recheck` (align pack, when installed) when the finding's class is a UI/UX axis (see its Phase 4 per-class routing table).
- NOT for new components / pages (use `/add-component` / `/add-feature`).
- NOT for fixing broken behaviour (use `/fix-bug`).
- NOT for *mechanically enforcing an EXISTING token / a11y rule / ui-state contract* — that is `/align`'s job (enforce what exists, no creative work). This skill owns the *creative finish* verbs (extract NEW tokens, wire missing states, rhythm / hierarchy / motion / cta / surface). Boundary table: `_orchestration-sync.md`.
- NOT for responsive / breakpoint or dark-mode / theme-mode drift — defer to `/enhance-ui` (deliberately outside the closed 19-verb set).

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Codebase root | Orchestrator | YES |
| `PROJECT_KIND` (must be `frontend-*` or `mobile-*`) | `_extracted-codebase.md § Gold standards` | YES |
| Design tokens | `_extracted-idioms.md § Tokens` (color / spacing / type / radius / shadow / motion) | YES (without it, the canonical token set is unknown — halt) |
| Shared wrappers | `_extracted-idioms.md § Wrappers` | YES (without it, `unify-component` / `extract-pattern` cannot run) |
| Surface prototypes | `_extracted-idioms.md § Surfaces` | NO (when missing, `normalize-surface` falls back to its **built-in composite-surface table-stakes** catalog for data-table / dashboard — see verb 19 — instead of skipping; warn that the generic floor, not a project prototype, is in use) |
| Voice guide | `_extracted-idioms.md § Voice` | NO (skip voice-related closures; warn) |
| Breakpoints | `_extracted-idioms.md § Breakpoints` | NO (default 360 / 768 / 1280) |
| Playwright MCP | runtime | NO (skill degrades to text-only if missing — but visual verbs lose verify capability) |

## Outputs (precise contract)

A finding-draft array — one row per detected design-fingerprint match. Each row:

```yaml
class: ui-design
subclass: <one of the 19 verbs below>
axis: <one of: tokens | hierarchy | rhythm | density | states | contrast |
                focus | iconography | motion | tap-target | cta | affordance |
                surface | type-scale | wrappers | patterns>
site: <component-path:line>
canonical: <what _extracted-idioms.md or ui-principles.md says — the token / wrapper / scale step / contrast tier>
divergence: <what this site does differently>
closure_verb: <one of the 19 verbs>
risk: low | medium | high
citation: <WCAG / iOS HIG / Material / Refactoring UI / project-idiom reference>
```

## The 19 closure verbs

### Cross-cutting carve-outs (framework-library controls · charts) — applied INSIDE the verbs below, NEVER a 20th verb

Two element classes do NOT inherit the design-token / theme layer, so several verbs below carry a **carve-out**: when the fix TARGET is one of these, the standard token-swap procedure is wrong — it either misses the element entirely or gets reverted by the visual-baseline oracle. **The closed set stays 19 verbs / 16 axes — these are carve-outs on existing verbs, not new verbs. `unify-component` (verb 3) is NOT the answer here — it swaps a raw element for the project's OWN shared wrapper; these carve-outs style a LIBRARY's internals / a CHART's config in place.**

**A. Framework component-library controls — the filter / control bar, the #1 miss.** A design-token / theme layer styles the project's OWN elements; it does NOT reach the internals of a component library — PrimeVue (`SelectButton` / `Calendar` / `InputText` / `Dropdown`), MUI, Ant, Vuetify, Radix / shadcn primitives render with their DEFAULT theme unless explicit `:deep()` / `::v-deep` / theme-token / CSS-var overrides are written for their inner classes (`.p-button`, `.p-inputtext`, `.p-highlight`, …). The filter / control bar (date pickers, segmented toggles, selects, action buttons) is almost always built from these controls, so it stays default-styled while authored elements look new. **"Styled the tokens, the controls follow" is FALSE — they do not follow.** So `consolidate-tokens`, `apply-type-scale`, `lift-contrast`, `align-focus-ring`, and `normalize-motion` carve this out: when the site is a library control, the fix is explicit `:deep()` / `::v-deep` / theme-token / CSS-var overrides on the library's inner classes, and each control — especially the whole filter / control bar — is graded as a **first-class component from the RENDER, `below-bar` until it visibly matches the target language.**

**B. Charts / data-viz.** A chart-library chart (Chart.js / ECharts / Recharts / ApexCharts / D3) holds its colors, axis / grid lines, fonts, legend, and tooltip in its OWN config object — NOT design tokens — so token / theme changes alone leave it in the old palette, and blind-replacing a config literal with a `var(--token)` a canvas chart can't resolve makes the chart render wrong (the visual-baseline oracle then reverts + halts it). So `consolidate-tokens` and `lift-contrast` carve this out: detect a chart config object; do NOT blind-replace its literals with a token reference; re-theme the chart's config explicitly through its theming API — series / dataset colors → the palette, grid / axis → the hairline / neutral, ticks / labels → the type, legend + tooltip → the surface, no-data → the empty language — or resolve the token to a build-time literal the chart can consume. **Verify from the chart's ACTUAL rendered colors (the screenshot), not "a chart is present."**

### 1. consolidate-tokens

**Fingerprint**:
- ≥2 hardcoded values for the same conceptual token across the codebase (color hex, spacing px, radius, shadow, font-size, motion duration / easing).
- An equivalent token EXISTS in `_extracted-idioms.md § Tokens`.

**Procedure**:
1. Cluster the hardcoded values per concept (`#3b82f6`, `#3a83f7`, `#4090ff` → all "primary blue").
2. Pick the canonical token from `_extracted-idioms.md` (e.g., `$color-primary` / `var(--color-primary)` / `theme.colors.primary`).
3. Replace every hardcoded site in one fix (one verb = one PR-able batch, even if 50 sites).
4. Update test snapshots if any pin colors.
5. Run visual baseline: per-route screenshots before/after must be pixel-equivalent (within tolerance: ±1 channel for color rounding).

**Carve-out (library controls · charts)** — see "Cross-cutting carve-outs" above: if a hardcoded value lives on a **component-library control's inner class** (`.p-inputtext`, `.p-highlight`, …) or inside a **chart config object**, do NOT blind-replace it with `var(--token)`. A canvas chart can't resolve a CSS var and the library control's inner class never sees your token — the swap either renders the chart wrong (baseline oracle reverts + halts) or silently no-ops on the control. Fix the control via `:deep()` / theme-token override; re-theme the chart through its config API (or resolve the token to a build-time literal) and verify from the rendered chart pixels.

**Verify**: visual diff < 0.5%; a11y re-check (contrast didn't drop); lint green.

**Citation**: project's `_extracted-idioms.md § Tokens`.

### 2. extract-token

**Fingerprint**:
- ≥3 hardcoded duplicates of the same value with NO existing token to replace them with.

**Procedure**:
1. Confirm the value is conceptual (not a one-off measurement).
2. Propose a token name (`$spacing-card-padding`, `$shadow-modal`, etc.) — naming follows `_extracted-idioms.md § Token-naming`.
3. Add the token to the design-token file (`tokens.json` / `theme.ts` / Tailwind config / CSS custom properties).
4. Run `consolidate-tokens` to apply at all sites.
5. Update `_extracted-idioms.md § Tokens` with the new entry.

**Verify**: visual baseline equivalent; new token referenced in ≥3 sites; idiom file updated.

**Citation**: Refactoring UI Ch. 1 (start with a system, not a screen); project idioms.

### 3. unify-component

**Fingerprint**:
- A shared wrapper exists in `_extracted-idioms.md § Wrappers` (e.g., `<AppButton>`, `<BaseInputText>`, `<CrudActions>`, `<BaseModal>`).
- Raw HTML / raw library component used at ≥1 site that fits the wrapper's contract.

**Procedure**:
1. Identify the wrapper's prop contract (slots / variants / sizes / disabled / loading / icon).
2. Map the raw site's props to the wrapper's contract.
3. Replace the raw component with the wrapper at every eligible site.
4. Remove the now-unused raw imports / styles.
5. Run visual baseline and component-snapshot tests.

**Verify**: visual baseline < 1% diff (wrapper may add/remove ~1-2px); component-snapshot tests updated; no orphan imports.

**Citation**: project's `_extracted-idioms.md § Wrappers`; align-discipline.md "Reinvented Wrapper" anti-pattern.

### 4. extract-pattern

**Fingerprint**:
- ≥5 instances of the same affordance pattern across the codebase with NO shared wrapper (e.g., 7 list-pages each renders its own `<header><filter><table><pagination>` ad-hoc).

**Procedure**:
1. Identify the common skeleton (props it would need, slots it would expose).
2. Author a new shared wrapper in the project's wrapper directory (`src/components/base/` or framework-equivalent).
3. Add the wrapper to `_extracted-idioms.md § Wrappers` with a 1-line contract.
4. Run `unify-component` to apply at all instances.
5. Update Storybook / component catalog if the project has one.

**Verify**: ≥5 sites adopt the wrapper; visual baseline equivalent; idiom file updated.

**Citation**: Refactoring UI Ch. 9 (re-use, don't reinvent); project idioms.

### 5. normalize-hierarchy

**Fingerprint**: page hierarchy score < 80 (per ui-sweep Detector 1):
- Primary action (the verb-noun CTA — "Save changes", "Buy now") not visually dominant (font weight / color / position), OR
- Two primary-styled elements competing in same viewport, OR
- Heading levels skipped (`<h1>` then `<h3>` with no `<h2>`).

**Procedure**:
1. Pick exactly ONE primary action per screen (`ui-principles.md § Should: one primary action per screen`).
2. Apply primary-action token (color / weight / size from design system).
3. Demote competing buttons to secondary / tertiary variants.
4. Fix heading levels — `<h1>` for page title, descend logically.
5. Re-run hierarchy score; target ≥ 80.

**Verify**: hierarchy score ≥ 80; a11y heading-order check green; visual baseline shows one dominant CTA.

**Citation**: Refactoring UI Ch. 2 (hierarchy is everything); WCAG 2.4.6 (Headings and Labels); `ui-principles.md`.

### 6. apply-type-scale

**Fingerprint**: `font-size` value used in any component does NOT match one of the project's declared scale steps (in `_extracted-idioms.md § Tokens § Type` — e.g., `12 / 14 / 16 / 18 / 20 / 24 / 32 / 48`). Includes off-by-one values like `17.5px`, `13px` when only even steps exist.

**Procedure**:
1. Identify the off-scale value's intent (body / caption / heading / display).
2. Pick the nearest matching scale step.
3. Replace the literal with the scale token (`text-base` / `theme.fontSize.lg` / `var(--text-md)`).
4. Verify the visual change is intentional — sometimes a designer's 17.5px IS load-bearing; halt if uncertain and surface to user.

**Carve-out (library controls)** — see "Cross-cutting carve-outs" above: a component-library control's font-size lives on the library's inner class (`.p-button`, `.p-inputtext`), not on your element, so a scale token written at your level never reaches it. Snap it via a `:deep()` / `::v-deep` / theme-token override on the control's inner class, and grade the control from the render — the token layer does not reach it.

**Verify**: visual baseline < 2% diff (font-size delta is small); no remaining literal `font-size` outside scale; a11y zoom check still passes.

**Citation**: Refactoring UI Ch. 7 (limit your type scale); modular scale theory; `ui-principles.md`.

### 7. tighten-rhythm

**Fingerprint**: vertical OR horizontal `margin` / `padding` / `gap` value not a multiple of the project's spacing token base (typically 4px or 8px). Examples: `margin: 13px`, `padding: 7px 11px`, `gap: 18px` when the base is 8px.

**Procedure**:
1. Identify the spacing's role (section gap, card padding, inline gap, between siblings).
2. Pick the nearest spacing token (`space-2` / `space-3` / theme equivalent).
3. Replace literal with token.
4. Adjust adjacent sites if rhythm is broken visually.

**Verify**: visual baseline shows consistent rhythm; no literal spacing outside token grid.

**Citation**: Refactoring UI Ch. 4 (work in spacing/sizing system); 8pt grid theory; `ui-principles.md`.

#### Control-size sub-fingerprint (a deepening of verb 7 — NOT a 20th verb)

Verb 7 polices spacing against the token grid; `expand-tap-target` polices a **minimum**. Between them nothing asks whether two controls **in the same row agree with each other**. A 38px input beside a 42px button passes both and the row still reads as broken — and it is invisible in source, because a control's height is padding + line-height + border, three declarations that are each individually correct.

**Equal height is the wrong goal** — partition the row by control CLASS first. Text-entry (input · select · combobox · date field) and action (button · segmented · dropdown trigger) ride the control-height scale; **binary controls (switch · checkbox · radio) carry an intrinsic size that is theirs, not the row's**, and icon-only controls carry a square step. Forcing a switch to a 40px box to match the field beside it produces a stretched toggle with dead padding — a worse row than the one the verb was sent to fix.

**Fingerprint**, within one rendered control row — **same landmark REGION, vertical centres within ~6px, AND horizontally adjacent** (all three; a sidebar item is adjacent to the content it abuts and is never in its row); a shared height alone is a page layout, not a row, and grouping on it alone returned 8 findings on 4 real admin views of which 8 were false — **same class**, heights differing by **≥2px** without both snapping to a declared step of that class's scale; OR same class *and* role (two buttons, two inputs) differing **at all**; OR — across ANY classes — **vertical centres** offset by ≥2px, which is an alignment fault with a different repair. A **declared variant** (a deliberately large primary CTA) is a decision, and a cross-class height difference is a contract; neither is a finding. **Also excluded, each after a measured false positive**: a composite control is measured at its WRAPPER not its inner field (a tag-input's inner input read 24 against a 36 sibling while its own wrapper was 36 and correct); a brand mark rendered as a button is not a control; and a table row is not a control row.

**Fix** at the wrapper by snapping one class's members to one step. Across classes never touch height — repair centres on the row. No scale declared → emit `extract-token` and stop; inventing a height per row is how a project acquires eleven button heights. Never pad one control until it looks right.

Row grouping, the ≥2px rationale, and the tap-target trade: **`references/measured-from-the-render.md` § B**. The measurement is `scripts/measure.ts` → `controlRows` (§ E).

### 8. simplify-density

**Fingerprint**:
- A single surface mixes density classes (compact + comfortable in same view).
- A surface uses density inappropriate for its context (compact in a primary marketing page; comfortable in a high-volume admin table).

**Procedure**:
1. Pick the right density per surface type — list/admin → compact; marketing/onboarding → comfortable; form → cozy (project-specific from `_extracted-idioms.md § Surfaces § density`).
2. Apply consistently across the surface.
3. Reduce visual weight: collapse non-critical borders, increase whitespace between primary affordances, demote secondary chrome.

**Verify**: visual baseline shows a single density per surface; user-test feedback (if available) doesn't regress.

**Citation**: Refactoring UI Ch. 5 (don't design too much chrome); Material Density spec; iOS HIG.

### 9. wire-empty-state

**Fingerprint**: a data-fetching component (uses `useCrud` / `useFetch` / `useQuery` / equivalent) renders no specific empty-state UI when the result set is empty. Symptoms: blank table, blank list, no helper text, no primary CTA to create the first item.

**Procedure**:
1. Author / reuse the project's empty-state wrapper (`<EmptyState>` from idioms, OR ad-hoc per surface).
2. Provide: short headline ("No orders yet"), 1-line context, ONE primary action ("Create your first").
3. Render conditionally on `data.length === 0 && !loading && !error`.
4. Use copy from `_extracted-idioms.md § Voice` if it exists.

**Verify**: empty-state renders in component tests on empty input; a11y check (text + button reachable); copy reviewed against voice guide.

**Citation**: `ui-principles.md § Must: Empty states explain what goes here AND offer one primary action`.

### 10. wire-loading-state

**Fingerprint**: data-fetching component renders no skeleton, no spinner, no placeholder during the fetch. User sees blank screen → suddenly data appears.

**Procedure**:
1. Pick the project's loading primitive (`<Skeleton>` / `<Spinner>` / `<LoadingOverlay>` from idioms).
2. Render conditionally on `loading && !data.length`.
3. For lists / tables: skeleton with N placeholder rows matching the eventual layout.
4. For modals / pages: full-surface skeleton or centered spinner.
5. NEVER render data + spinner simultaneously (creates layout shift).

**Verify**: loading state visible in component tests; no Cumulative Layout Shift (CLS > 0.1) regression.

**Citation**: `ui-principles.md § Must: Loading … states exist`; Web Vitals CLS; Refactoring UI Ch. 11 (skeleton screens).

### 11. wire-error-state

**Fingerprint**: data-fetching component swallows errors silently (renders empty state on error, OR renders nothing, OR shows generic "Something went wrong" without a retry).

**Procedure**:
1. Differentiate error from empty (different render branches).
2. Show user-facing error message — name the failure ("Couldn't load orders"), don't expose stack traces.
3. Provide a retry affordance — button that re-runs the fetch.
4. If the error is recoverable (network), include "try again". If not (auth), redirect.
5. Log the error to the project's error handler (named in `_extracted-idioms.md § Error handler`) — never swallow.

**Verify**: error state visible in component tests on rejected promise; logged to error handler; retry button re-fetches.

**Citation**: `ui-principles.md § Must: error … states exist`; align-discipline.md "Silent Catch" anti-pattern.

### 12. lift-contrast

**Fingerprint**: text or UI component contrast ratio fails WCAG 2.2 AA:
- Body text < 4.5:1, OR
- Large text (≥18pt or ≥14pt bold) < 3:1, OR
- Non-text UI component (button border, focus ring, icon) < 3:1, OR
- **Indistinct container boundary — the "floating surface"** (see the sub-section below).

**Procedure**:
1. Measure with `axe-core` / Lighthouse / Chrome DevTools contrast picker — get the actual ratio.
2. Pick the next-darker token from the design system that meets the threshold.
3. Replace the literal / token at all instances of the same role.
4. Re-verify the new ratio at every interactive state (default / hover / focus / disabled).

#### Floating-surface sub-fingerprint (a deepening of verb 12 — NOT a 20th verb)

Every check above measures something *against* a surface — text on a card, an icon on a button. **Nothing measured the surface against what it sits on.** A `#ffffff` card on a `#f8fafc` page is **1.04:1**: it passes every text check, every axe rule and every token audit while its edges are invisible.

**Fingerprint**: a container whose boundary is resolvable by **none** of three cues — no border / outline reaching ≥3:1 against the adjacent fill, AND no elevation cue that survives the render, AND a surface-pair luminance ratio **< 1.2:1** against the fill immediately outside its edge. The three **combine**: grading one alone is a false positive.

**Fix** at the role, with the project's existing elevation language, in order: border token → elevation token → surface-step token. Sample against the **nearest painted ancestor, not the page** — a container whose fill equals its ancestor's is a layout box, not a surface, and comparing inner divs to `body` reported 28 false positives on one real app. Never invent a grey (that is `extract-token`). **Separation is the container's edge and its shadow — never the page's weight.** Verify in dark mode too.

Full fingerprint, the measured calibration behind the 1.2 threshold, and the darken-the-page anti-pattern: **`references/measured-from-the-render.md` § A**. The measurement is `scripts/measure.ts` → `floatingSurfaces`, once per theme (§ E).

**Citation**: WCAG 2.2 SC 1.4.11 (Non-text Contrast — *"boundaries of components needed to identify them"*).

### 13. align-focus-ring

**Fingerprint**:
- Interactive element with `outline: none` (or `outline: 0`) and NO replacement focus indicator, OR
- No `:focus-visible` style on a custom interactive element, OR
- Focus indicator < 3:1 contrast against adjacent colors.

**Procedure**:
1. Remove `outline: none` declarations OR add a replacement.
2. Add `:focus-visible` style: 2-3px ring, color from design tokens, contrast ≥ 3:1.
3. Use the project's focus-ring mixin / utility if one exists (`@apply focus-ring` / `theme.focus`).
4. Verify keyboard tab order — ring must be visible at every step.

**Carve-out (library controls)** — see "Cross-cutting carve-outs" above: a component-library control renders its OWN focus style (`.p-focus` / a default outline the library ships), so adding or replacing the `:focus-visible` ring requires a `:deep()` / `::v-deep` / theme-token override on the control's inner class — a ring style at your element level does not reach it. Grade the ring by keyboard-tabbing the RENDER, `below-bar` until the control's ring matches the target language. (The ring IS a rendered pixel change — this verb's visual baseline is required, not warn-only.)

**Verify**: keyboard tab through the page → ring visible at every interactive element; `axe-core` focus-order check green.

**Citation**: WCAG 2.2 SC 2.4.7 (Focus Visible) + 2.4.11 (Focus Not Obscured); `ui-principles.md § Must: :focus-visible style on every interactive element`.

### 14. unify-iconography

**Fingerprint**: icons from MORE than one icon set used in the codebase (e.g., Heroicons + Material Symbols + FontAwesome mixed). Project declares ONE canonical set in `_extracted-idioms.md § Icons`.

**Procedure**:
1. Identify the canonical set.
2. Find the equivalent icon for every off-set occurrence (most icon sets have a stroke / fill / outline equivalent).
3. Replace imports + JSX / template references.
4. Remove the now-unused icon-set dependencies (`pnpm remove`).
5. Update Storybook / icon-catalog page if the project has one.

**Verify**: no imports from non-canonical icon sets; visual baseline shows consistent icon style; bundle-size reduction.

**Citation**: project's `_extracted-idioms.md § Icons`; `ui-sweep` Detector 7 (Design-language coherence).

### 15. normalize-motion

**Fingerprint**:
- Animation `duration` / `easing` not in the project's motion-token set (e.g., `transition: all 350ms ease-in` when tokens are `150ms / 250ms / 400ms` and `cubic-bezier(...)`).
- ONE OR MORE of: `prefers-reduced-motion` not respected; animation on `transform` / `opacity` only is fine, but on `width` / `height` / `top` / `left` is forbidden (layout-thrash).

**Procedure**:
1. Pick the right motion token per intent — `fast` 150ms (micro-interaction) / `base` 250ms (UI transition) / `slow` 400ms (page transition). **These numbers are cited from `motion.md § The duration scale`, which owns them; do not restate a different value here.**
2. Replace literal with token.
3. Wrap animation in `@media (prefers-reduced-motion: no-preference)` OR use the project's motion mixin that handles it. Gate on the **trigger**: interaction- and scroll-triggered motion needs the branch regardless of duration.
4. Re-target layout-thrashing animations to `transform` / `opacity`. `filter` is NOT in the cheap set — it shades per frame and `blur()` scales with area.

**Carve-out (library controls)** — see "Cross-cutting carve-outs" above: a component-library control's transitions live in the library's own CSS (`.p-*` transition / animation rules), so a motion-token change on your element leaves the control's animation on the library default. Duration-match / retarget it via a `:deep()` / `::v-deep` override on the control's inner class, and confirm the change from the render — the token layer does not reach the control's animation.

**Verify**: animations respect reduced-motion; no jank in DevTools performance panel; visual feel unchanged.

**Citation**: WCAG 2.2 SC **2.3.3** (Animation from Interactions) — **Level AAA**, so a missing reduced-motion branch is a house-rule violation, NOT an AA failure; the criterion that binds below AAA is SC **2.2.2** (Pause, Stop, Hide) — **Level A** — for motion that auto-starts, runs past five seconds, and sits beside other content. `motion.md § The duration scale` (durations + easing classes); `ui-principles.md § Should` (prefers-reduced-motion).

### 16. expand-tap-target

**Fingerprint**: interactive element hit-area below the applicable threshold at the mobile breakpoint (360px viewport). Symptoms: small icon-only buttons, dense link clusters, undersized close-X.

**Two thresholds, and they are not interchangeable — conflating them is this verb's historical defect:**

| Threshold | Criterion | Level | Role |
|---|---|---|---|
| **24 × 24 CSS px** | [SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | **AA** | The **conformance floor.** A finding below 24 is a WCAG 2.2 AA failure. Five exceptions: **Spacing** (a 24px-diameter circle centred on each undersized target's bounding box does not intersect another target's), **Equivalent**, **Inline**, **User agent control**, **Essential**. |
| **44 × 44 CSS px** | [SC 2.5.5 Target Size (Enhanced)](https://www.w3.org/TR/WCAG22/) | **AAA** | The **house design target**, matching Apple HIG's 44pt and sitting under Material's 48dp. A finding between 24 and 44 is a house-rule improvement, not an AA failure — grade and report it as such. |

**Procedure**:
1. Measure the hit-area (border-box width × height including padding) at 360px.
2. Below 24: check the five 2.5.8 exceptions FIRST — an inline link in a sentence, or an undersized control with a conforming equivalent elsewhere on the page, is not a violation. If no exception applies, this is a conformance fix and it is not optional.
3. Between 24 and 44: a house-target improvement. Apply it unless the spacing exception is doing real work and enlarging would crowd neighbouring targets.
4. Add padding (preferred) OR `min-width` / `min-height`. For icon-only buttons, pad inside a fixed-size wrapper. For tight link clusters, increase line-height OR convert to a button group.
5. Preserve visual size where needed via transparent padding + smaller visual content — the criterion is about the hit area, not the ink.

**Verify — name which threshold each check proves:**
- `axe-core`'s `target-size` rule implements **2.5.8 at 24×24** including the spacing alternative ([Deque rule docs](https://dequeuniversity.com/rules/axe/4.10/target-size)), and it **runs only when the run's tags include `wcag22aa`**: axe ships it disabled, so "axe clean" from a run without that tag says nothing about 24 (`precedents/ui.md` § 49). With the tag, "axe clean" proves **24, never 44** — it passes every element between the two.
- The 44 house target needs a **measured border-box** at 360px. Print both, with the tag set: `target-size: axe wcag22aa clean (2.5.8 AA, 24×24) · house 44: 3 below (measured)`, or `target-size: NOT RUN (axe ran without wcag22aa)`.
- Visual baseline shows no unintended layout change.

**Citation**: WCAG 2.2 SC **2.5.8** Target Size (Minimum) — **Level AA**, the floor; SC **2.5.5** Target Size (Enhanced) — **Level AAA**, 44×44, the house target; iOS HIG (44pt); Material touch targets (48dp); `ui-principles.md § Must` (pointer targets).

### 17. unify-cta-placement

**Fingerprint**: primary CTA position differs across surfaces of the same type:
- List page A has "Create" in header; List page B has "Create" floating bottom-right; List page C has "Create" inline in toolbar.
- Form page A has "Save" top-right; Form page B has "Save" bottom-left.
- Modal A has actions left-aligned; Modal B has actions right-aligned.

**Procedure**:
1. Pick the canonical placement per surface type from `_extracted-idioms.md § Surfaces § cta-placement` (or set one if missing).
2. Move CTAs to canonical position at all outlier sites.
3. If the surface uses a shared wrapper (`<PageHeader>`, `<ModalFooter>`), confirm the wrapper enforces the placement.
4. Update the surface prototype example in `_extracted-idioms.md § Surfaces` if changed.

**Verify**: every surface of the same type shows the CTA in the same position; visual baseline diff documented per page.

**Citation**: `ui-principles.md § Should: one primary action per screen`; Refactoring UI Ch. 2 (hierarchy).

### 18. clarify-affordance

**Fingerprint**:
- Action element styled as non-interactive (no hover / focus / cursor change), OR
- Icon-only button with no `aria-label` AND no visible tooltip, OR
- Disabled button with no tooltip / message explaining WHY.

**Procedure**:
1. For non-interactive-looking actions: add hover state (background / border / color shift) + `cursor: pointer`.
2. For icon-only buttons: add `aria-label` ("Delete order"); add tooltip via `title=` or design-system tooltip wrapper.
3. For disabled buttons: add `aria-describedby` + visible tooltip explaining the requirement ("Save: complete required fields first").
4. NEVER use color alone to convey state — pair with text, icon, or shape.

**Verify**: a11y screen-reader check (icon button announces label); hover/focus visible; disabled-with-reason pattern used at every disabled site.

**Citation**: WCAG 2.2 SC 1.4.1 (Use of Color), 4.1.2 (Name, Role, Value), 3.3.2 (Labels or Instructions); `ui-principles.md § Must not: Disabled buttons without … explaining WHY` + `Icon-only buttons without aria-label`.

### 19. normalize-surface

**Fingerprint**: a page diverges structurally from the prototypical example for its surface type (list-page / detail-page / form-page / modal / dialog) — e.g., the prototypical list-page uses `<PageHeader> + <DataTable> + <Pagination>` but this list-page uses `<div class="header"> + raw <table> + <Button>Next</Button>`.

**Procedure**:
1. Read the prototype from `_extracted-idioms.md § Surfaces § <type>`.
2. Diff the divergent page against the prototype: which wrappers missing? Which structure differs?
3. Apply `unify-component` for missing wrappers.
4. Restructure the page's skeleton to match the prototype.
5. Preserve unique business logic (the divergent page may have special filtering / actions — keep those, only normalize the structural skeleton).

**Verify**: page now uses the same top-level wrappers as the prototype; component-snapshot tests pass; visual baseline shows alignment with sibling pages of the same type.

**Citation**: project's `_extracted-idioms.md § Surfaces`; `ui-sweep` Detector 4 (Cross-surface consistency).

#### Built-in composite-surface table-stakes (verb-19 fallback prototype — NOT a 20th verb)

`normalize-surface` compares a page against the prototype in `_extracted-idioms.md § Surfaces`. Per the Inputs table, that section is **optional** — so when a project has NOT authored it, the verb historically skipped-with-warn and a composite surface got **no completeness floor at all**. This built-in catalog is the verb's **fallback prototype**: when the project's Surfaces section is absent for a surface type, grade the surface against the generic table-stakes below instead of skipping. **A project's authored `§ Surfaces` prototype ALWAYS overrides this** — the catalog is the floor, never a ceiling, and never re-audits an axis the 16-axis catalog already owns. This is a fallback prototype for the EXISTING verb; the closed set stays **19 verbs / 16 axes** (same status as the framework-control / chart carve-outs above — a deepening of a verb, not a new verb or a 17th axis).

The composite surfaces the primitive-level contracts (`design-system-architect` variant/state enums · `ux-reviewer` §5/§9) and the per-element axes do **not** fully cover are **data-table** and **dashboard**. A few of their affordances are ALREADY floor-owned (a table's search/filter/sort/pagination — `ui-principles.md § Should` · `ux-reviewer` §9): those are cited, not re-claimed. The **genuinely new content** is the rest — row-selection + bulk actions, export, sticky header, per-row affordances, responsive frozen-column, the dashboard composition, and the composite `N/M` completeness GRADE itself. Emit a coverage line `<surface> affordances: N/M present — missing: <list>` and treat each missing item as a **candidate to surface**, scaled by the surface's job (see the discipline below):

| Surface type | Table-stakes affordance set (the completeness floor) |
|---|---|
| **data-table** (job: browse / manage a collection) | persistent (sticky) header · a toolbar with search · filter · sort *(already floor-owned — `ui-principles.md § Should` · `ux-reviewer` §9; cited, not new)* · row selection + bulk actions · export · pagination (or virtualized infinite scroll) *(already floor-owned)* · per-row hover + row-level affordances · empty / loading / error states (defer to verbs 9–11) · responsive stack-or-horizontal-scroll-with-frozen-column |
| **dashboard** (job VARIES: analytics/BI · operational-home · monitoring/status) | **Universal (count toward M always):** labeled metric / stat tiles with trend or context (NOT bare numbers) · charts re-themed to the design language (NOT library defaults — see the chart carve-out) · a widget / section grid with deliberate hierarchy (flag a flat plain-card grid with no ranking) · a period / time-range control where the data is time-bound. **Job-conditional (count toward M only when the dashboard's job includes it, mirroring the data-table scale-gate):** a recent-activity / change feed and quick-actions belong to an operational/home dashboard — an analytics/BI or status dashboard legitimately has neither, and flagging them there is a false positive. |
| **form / detail** (cross-reference — do NOT duplicate) | already owned by `ux-reviewer` §5/§9 + `design-system-architect`: 2-col→1-col reflow · sectioned field groups · inline-validation-on-blur · error summary linking to fields · autofill attributes · multi-step indicator when multi-step. Cite them; the built-in catalog does not re-specify the form contract. |

**Discipline (prevents both enforcement-theater and over-reach):**

1. **Detect + report, do NOT auto-build.** The verb's output here is a coverage finding (`data-table affordances: 4/8 — missing: sticky header, bulk actions, export, sort`), not a silent feature graft.
2. **Scale-gated candidacy, not a blanket mandate.** Not every instance needs every affordance — a 5-row reference table needs no pagination / export / bulk-select. Flag ABSENCE as a **candidate for the reviewer/user to judge**, using the surface's scale as the trigger (pagination / search / sort / filter are table-stakes only once a list is expected to exceed ~50 items in production — `ui-principles.md § Should`).
3. **A genuinely NEW affordance system is out of scope — route it out.** Adding a bulk-actions system, an export pipeline, or a new chart is a FEATURE / RE-COMPOSITION, not a structural normalization — it exceeds verb 19's re-paint/normalize boundary (`§ Hard rules — re-PAINT, not re-COMPOSE`). HALT-and-surface and route to `/redesign` (re-composition within the existing language) or `/add-feature` (new capability). The verb itself only normalizes the surface's STRUCTURE toward the prototype and preserves business logic — unchanged from its existing contract.
4. **Stays generic.** `export` / `bulk-select` / `sticky-header` / `metric-tile` are generic data-management + status-surface affordances — no domain terms, no product names.

## Procedure (the skill's overall flow)

1. **Receive finding** with `class: ui-design`, `subclass: <verb>`, evidence `<path:line>`, `axis: <one of 16>`.
2. **Pre-flight**:
   - `PROJECT_KIND` is `frontend-*` or `mobile-*`.
   - `_extracted-idioms.md` populated with required sections (Tokens / Wrappers; Surfaces / Voice / Breakpoints if the verb requires).
   - Working tree clean (or `--allow-dirty` set on parent run).
   - Lint + typecheck green at HEAD.
   - Visual baseline captured (Playwright MCP). The skip-visual-verify decision is **deterministic** — read it off the verb, not off a judgement call:
     - **Baseline REQUIRED (the baseline diff is the verify oracle): verbs 1-8 and 12-19.** This INCLUDES `align-focus-ring` (verb 13): its `:focus-visible` ring IS a rendered pixel change, verified by keyboard-tabbing the render — it is NOT a "doesn't change visuals" exception.
     - **Render REQUIRED but baseline-EQUIVALENCE does not apply: the state-wiring verbs 9-11 (`wire-empty/loading/error-state`).** These intentionally add NEW UI, so a before/after equivalence diff would always differ; the verify oracle is instead the component-test render that shows the newly-wired state (see each verb's Verify). A render is still required — never skipped.
     - **The ONLY warn-only case is Playwright unavailable** — then the whole skill degrades to `--no-visual-verify` and every affected row is marked `pending-review` (never `done`), per the Playwright-not-wired failure mode. There is NO per-verb "this verb doesn't change visuals, skip the baseline" carve-out.
3. **Apply the verb's procedure** above.
4. **Verify**:
   - Lint green.
   - Typecheck green.
   - Component-snapshot tests green (or updated with reviewed diff).
   - Visual baseline diff within the verb's tolerance.
   - a11y re-check — axe with the `wcag22aa` tag set shows no new violation on the route (a Lighthouse score is not a conformance claim, `precedents/ui.md` § 51).
   - For `lift-contrast`: contrast ratio **computed** at every interactive state, in every theme the project ships — never estimated.
   - For `expand-tap-target`: hit-area measured at 360px viewport, reported against **both** thresholds — `2.5.8` (AA, 24×24, what axe proves when its tags include `wcag22aa`) and the 44 house target (what only a measurement proves). A verify line that says "44×44 verified with axe" is invalid; axe implements the 24 rule.
   - For `wire-empty/loading/error-state`: state visible in component test for the matching condition.
5. **Commit** with message `polish(<surface>): <verb> — <one-line description>`.
6. **Re-detect** the finding's fingerprint — should now return zero hits at the original location.

## Hard rules

- **Behaviour-preserving.** The page's data flow / API calls / route navigation are unchanged. Only visual / design-system / a11y attributes change.
- **One verb per commit.** Don't bundle (`consolidate-tokens` + `wire-empty-state` in same commit is forbidden — they have different verify steps).
- **No new abstractions outside the closed verb set.** If a finding doesn't match one of the 19 verbs, halt and surface — don't invent a 20th verb. Architectural moves go to `architectural-diagnosis`; new wrappers go through `extract-pattern` (which IS in the set). Responsive / breakpoint drift and dark-mode / theme-mode drift are deliberately NOT in the set — defer those to `/enhance-ui`.
- **This skill re-PAINTS; it does not re-COMPOSE — route composition findings out.** The 19 verbs restyle elements in place; they do not move them. When a finding's real fix reshapes the **information architecture, grouping, section order, action ranking, or spatial rhythm** (relocating elements to build a stronger hierarchy, not restyling them where they sit), that is out of scope — mirroring `redesign.md` lens 15's recompose-not-repaint boundary (a same-skeleton restyle is polish; a redesign moves things). Route it to **`/redesign`** (rebuild the surface within the existing language), or **`/art-direct`** when the visual LANGUAGE itself must be decided first; a **whole-surface rethink** goes to the read-only **`/design-review`** to diagnose before any rebuild. Applying a paint verb to a composition problem leaves the surface half-fixed — halt and route, don't force-fit a verb.
- **No frontend compensation for backend gaps.** If the API is missing a field, file a backend ticket — don't add a UI workaround. Mark the finding `halted` with explicit dependency.
- **Visual baseline is the verify oracle.** Skipping baseline = skipping verify. If Playwright is unavailable, the verb runs in `--no-visual-verify` mode and the row is marked `pending-review` (not `done`).
- **a11y must not regress.** Every verb's verify includes an a11y re-check; a verb that improves visuals but drops a11y score is a halt, not a fix.
- **Re-detect after each fix.** Fingerprint must disappear at the source location.

## Failure modes

- **Visual baseline diff > tolerance** (without intentional reason from the verb) → revert; mark `halted` with screenshot evidence; surface for user.
- **a11y score drops** → revert; the verb was wrong choice or applied wrong; surface.
- **Wrapper contract doesn't fit a site** (during `unify-component`) → halt; surface as user-decision (the wrapper may need extension OR the site is genuinely a one-off — the user decides; do NOT silently fork).
- **Token doesn't exist for the value** (during `consolidate-tokens`) → switch to `extract-token` instead.
- **Off-scale font-size is intentional** (during `apply-type-scale`) → halt; surface to designer; do NOT auto-snap.
- **Playwright not wired** → run in `--no-visual-verify`; mark each row `pending-review`; surface to user.
- **Project has no design-token system at all** → halt the entire skill run; route to `/setup-project --refine` to populate `_extracted-idioms.md § Tokens` first.

## Examples per verb

(See "The 19 closure verbs" section above; each verb has a worked fingerprint + procedure + verify.)

## References

- `ui-principles.md` (this pack) — the closed axis names + the routing rule this skill's `axis:` field is drawn from (the always-loaded half).
- `axis-catalog.md` (this pack, pattern) — the per-axis detection heuristic and the verb that closes each axis (the dispatch-loaded depth behind those names). Read it when naming or closing a finding; do not restate it into a rule.
- `design-token-audit.md` (this pack) — the DETECTOR that feeds `consolidate-tokens` / `extract-token`: it resolves which token is correct and whether the swap holds contrast; this skill owns the edit and the visual verify. Neither restates the other.
- `motion.md` (this pack) — **owns the duration scale + easing classes** `normalize-motion` applies. A duration in this file that disagrees with it is drift.
- `motion-audit.md` (this pack) — feeds `normalize-motion` findings.
- `a11y-quick-check.md` (this pack) — feeds `lift-contrast` / `align-focus-ring` / `clarify-affordance` / `expand-tap-target`.
- `design-iterate.md` (this pack) — for the visual variant generator step in `/enhance-ui --with-iterate` (NOT a closure verb — operates above this skill).
- `redesign.md` (this pack) — the **re-COMPOSITION escalation**: a finding whose fix reshapes IA / grouping / order / rhythm is out of this skill's re-paint scope; route it here to rebuild the surface within the existing language (its lens 15 owns the recompose-not-repaint boundary + the canonical framework-control / chart carve-out vocabulary this skill mirrors).
- `art-direct.md` (this pack) — the re-composition escalation when the **visual language itself** must be decided before rebuilding (upstream of `/redesign`); shares the framework-control / chart coverage-gate vocabulary.
- `design-review.md` (this pack) — the **read-only whole-surface rethink** escalation: diagnose the surface before any rebuild when the fix is bigger than a verb.
- `visual-check.md` (frontend pack, when installed; without it, drive the Playwright MCP directly under the same contract) — the Playwright render / baseline / authenticated / blocked-render harness this skill's visual verify runs on (the same harness the ui-ux design commands — `/redesign`, `/art-direct`, `/add-theme-variant`, `design-iterate` — standardize on; a blocked auth-wall render HALTs, no harness → `pending-review`).
- `api-consistency-audit.md` (backend pack) — sibling skill for backend `/polish`.
- `schema-consistency-audit.md` (database pack) — sibling skill for data `/polish`.
- `refactoring-sweep.md` (code-quality pack) — sibling closed-verb skill for code-structure.
- `align-discipline.md` (align pack) — closed-vocabulary discipline this skill inherits.
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- iOS Human Interface Guidelines (HIG)
- Material 3 Design Guidelines
- Refactoring UI (Adam Wathan & Steve Schoger) — design-system theory cited per verb.
