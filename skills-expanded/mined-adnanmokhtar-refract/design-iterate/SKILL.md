---
name: design-iterate
kind: skill
pack: ui-ux
description: Two modes. `pick` (attended) — generate 2–3 style variants at the correct design-system layer (leaf scoped styles, shared wrapper, or design tokens), screenshot via Playwright MCP, present side-by-side so the user picks. `refine` (unattended, for /redesign Phase 6 + /art-direct build) — render the approved design, self-critique the PIXELS against the caller's rubric, fix the weakest lens (depth/motion/modern/perf/i18n), re-render, loop up to $MAX_REFINE rounds until it clears the bar. Honors $SCOPE_TIER so the same affordance is not duplicated across pages. Invoke for "try a few variants" / "iterate on the design", or as the quality loop that turns a one-pass build into a good design.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Design Iterate

For when the user isn't sure what they want and "just describe it" isn't working. You generate 2–3 variants, screenshot each, and let them point. **Layer depends on `$SCOPE_TIER`** — see Inputs.

## Inputs

- `$TARGET` — file path:
  - **`leaf-local`** — `.vue` / `.tsx` / `.svelte` page or leaf component.
  - **`wrapper-variant`** — shared wrapper component named in `_extracted-idioms.md`.
  - **`token`** — design tokens / theme file (SCSS variables, CSS custom properties module, `tailwind.config` extension — path from idioms).
  - **`wrapper-extract`** — **do not invoke this skill** until the orchestrator has finished extraction and re-targets `wrapper-variant`; if called prematurely, halt and return to `/enhance-ui`.
- `$SCOPE_TIER` — **`leaf-local`** | **`wrapper-variant`** | **`token`** | (never **`wrapper-extract`** at iterate time). Default **`leaf-local`** when omitted (backward compatible).
- `$CONSUMER_ROUTES` — optional list of routes / URLs / story paths to screenshot when `$SCOPE_TIER` is **`token`** or **`wrapper-variant`**. Provided by `/enhance-ui` Phase 1.5. When absent, fall back to `visual-check` resolution for `$TARGET` only (legacy behaviour).
- `$DIRECTION` — optional: "more minimal", "more colorful", "card-based", etc.

## Steps

### All tiers — variants A/B/C

Generate three variants (polished / bolder / minimal) unless user tune requests otherwise:

- **Variant A** — closer to current, polished (spacing tighter, cleaner borders).
- **Variant B** — bolder (more color, larger type, heavier shadows).
- **Variant C** — minimal (flat, less chrome, more whitespace).

Use **design tokens** (`$primary`, `$space-md`, CSS vars, Tailwind theme keys) — no arbitrary hex in variants unless the project's idiom allows it.

### Tier-specific — what to edit

| `$SCOPE_TIER` | Step 1 — Read | Step 3 — Apply variants to |
|---|---|---|
| **`leaf-local`** | Scoped `<style>` / CSS modules / styled blocks on `$TARGET` only. | Scoped style block only — **no template or script changes.** |
| **`wrapper-variant`** | Wrapper component's styles + existing props API from `_extracted-idioms.md`. | Wrapper scoped styles; **template / script / prop changes only after explicit user confirmation** in Step 5 (e.g. new `variant=` prop). |
| **`token`** | Token definitions in `$TARGET` (theme file). | Token values only — no component template edits in this skill (orchestrator may chain a separate token-sync doc edit). |

### Steps (numbered)

1. Read `$TARGET` and capture the editable style surface per tier (table above).
2. **Baseline screenshots** — If `$CONSUMER_ROUTES` is non-empty, run `visual-check` (or Playwright) on **each** consumer route and save baselines. If empty, run `visual-check` on the route that renders `$TARGET` (legacy).
3. Generate 3 variants (stash / branch / patch workflow per repo convention). Each variant modifies only the allowed layer for that tier.
4. For each variant: apply, screenshot via Playwright MCP — **when `$CONSUMER_ROUTES` is set, capture each route** so propagation is visible; save to `.claude/artifacts/design-iterate/<timestamp>/<variant>-<route-slug>.png`, then revert before the next variant.
5. Leave `$TARGET` in original state until pick. Present:
   - Screenshots side-by-side (group by variant or by route — whichever reads clearer).
   - One-line tradeoffs per variant.
   - For **`wrapper-variant`**: if a variant needs a new prop or slot, say so and **ask confirm** before applying template/script edits.
   - "Pick A/B/C or tune" as CTA.
6. Once they pick, apply that variant. Run **`visual-check` on every route in `$CONSUMER_ROUTES`** again for final verification; if empty, single-route check.

### Refine mode (`$MODE=refine` — unattended: render → critique → improve → re-render)

The steps above are **`pick` mode** (attended): make 3 variants, a human chooses. In an unattended / `--yes` flow (e.g. `/redesign` Phase 6, `/art-direct` build), there is no human to pick — so this skill runs the **refine loop** instead, which is how a one-pass build becomes a genuinely good design:

1. Apply the approved design, screenshot the rendered surface (`$SCOPE_TIER` allowed layer only; `$CONSUMER_ROUTES` if set) at the breakpoints × theme × locale. **Authenticate first if the surface is auth-gated** — per `visual-check`'s "Authenticated rendering" contract, a headless/isolated browser with no session lands on `/login` and every screenshot is worthless. **If the render is BLOCKED** (login wall / redirect off the route / surface-unique marker absent — `visual-check`'s blocked-render halt), the refine loop **cannot run** — you cannot self-critique a page you did not render. HALT with `RENDER BLOCKED — cannot verify components; establish an authenticated session and re-run`; do NOT fall through to "SKIPPED (no harness)" (that is only for when no harness exists at all), and do NOT grade a login screenshot as the surface.
2. **Look at the render and self-critique it against the caller's rubric** — the `/redesign` Design-principles lenses (hierarchy, rhythm, states, motion-actually-implemented, modern register, performance, a11y, RTL). Score each `✓ / Δ / ✗` from the *pixels*, not the code. **Then run the per-component pass:** enumerate EVERY distinct component in the render (buttons, inputs/selects, filter bar, tabs, cards, table header/row/cell, badges, chart series/axis/legend/tooltip/no-data, pagination, empty/loading/error) and grade EACH from the pixels — a holistic "looks modern ✓" is not enough; each component **defaults to `below-bar`** and earns `✓` only when it shows intentional depth (not the framework default), scale-based type, rhythm spacing, purposeful AA color, real hover/focus/active/disabled states, consistent geometry, and is **not a raw library default** (unstyled `<select>`, default zebra, stock spinner). A single ugly component is a fail even if the page reads modern overall.
3. **Fix the weakest lens OR the worst below-bar component in code, then re-render.** Each round must move a named lens `Δ`→`✓` or a named component `below-bar`→`✓` (e.g. "flat/no depth → add the elevation token + hover lift"; "native `<select>` still stock → wrap in the styled combobox"; "table rows cramped, no hover → apply row rhythm + hover token"; "raw i18n key visible → add the locale strings"). Do not restate the same score twice. Two below-bar fixes have a **fix layer that a token edit cannot reach** — apply them where the fix actually lives, not in the token file:
   - **A `below-bar` framework library control is fixed by OVERRIDING it, not rewrapping it.** The "native `<select>` → wrap in the styled combobox" move above is for a raw HTML element; a component-library control (PrimeVue `SelectButton`/`Calendar`/`InputText`/`Dropdown`, MUI, Ant, Vuetify, Radix/shadcn primitives) is NOT rewrapped — a design-token/theme layer does **not** reach the internals of a component library, so it renders with the library's DEFAULT theme unless you write explicit **`:deep()` / `::v-deep` / theme-token / CSS-var** overrides for its inner classes (`.p-button`, `.p-inputtext`, `.p-highlight`, …). The filter / control bar (date pickers, segmented toggles, selects, action buttons) is almost always built from these controls, which is exactly why it stays `below-bar` while your authored cards look new. "Styled the tokens, assumed the controls follow" is the specific failure — they do NOT follow; grade each library control as a first-class component from the render and override it explicitly until it visibly matches the target language.
   - **A `below-bar` chart is fixed in the chart's config object, NOT the tokens.** A chart-library chart (Chart.js / ECharts / Recharts / ApexCharts / D3) holds its colors, axis/grid lines, fonts, legend, and tooltip in its **own config/options object — NOT design tokens** — so a token edit alone leaves it in the old palette (and a `$SCOPE_TIER == token` refine with fix layer "token values only" burns its `$MAX_REFINE` budget on values the chart ignores). Locate the chart library's config/options and re-theme it explicitly: series/dataset colors → the palette, grid/axis → the hairline/neutral, ticks/labels → the type, legend + tooltip → the surface, no-data → the empty language. Verify from the chart's ACTUAL rendered colors (the screenshot), not "a chart is present."
   - **When the tier forbids that layer** (`$SCOPE_TIER == token` — token values only, no component edits in this skill), a below-bar chart config or library-control `:deep()` override is **outside the allowed layer**: report it as a residual `Δ` naming the fix that lives elsewhere ("chart still in old palette — needs a Chart.js config re-theme, outside the token layer"), per step 5's honesty rule — never silently edit the component, never hide it as `✓`.
4. Loop steps 2–3 up to **`$MAX_REFINE`** rounds (default 3). Stop early when every targeted lens + motion/modern/performance is `✓` **AND no component is `below-bar`** — never while a single enumerated component is still below the bar.
5. Leave the surface in the improved state; emit the per-round lens deltas so the caller's scorecard shows what each round bought. A residual `Δ` that couldn't clear in the budget is reported honestly, never hidden.

Refine mode never invents a NEW visual language (that is `creative-director` / `/art-direct`) and never changes the approved structure (that is fixed by `/redesign`'s gate) — it drives the approved design to the quality bar by iterating on the rendered result.

## Rules

- **Template / script:** **NEVER** change template or script when `$SCOPE_TIER == leaf-local`. For **`wrapper-variant`**, template / prop-API changes require **explicit user confirmation** before applying the picked variant.
- **NEVER** leave a variant applied without user confirmation (pick step).
- Use design tokens — no hardcoded raw values where the project supplies a token.
- **Stay scoped** — no global style bleed unless `$SCOPE_TIER == token` and the tokens file is the intentional global surface.
- **`wrapper-extract`** is not handled here — orchestrator runs extraction first.

## Cross-references

- **`visual-check`** (frontend pack, when installed; without it, the Playwright MCP under the same authenticated / blocked-render contract, else `SKIPPED (no harness)`) — the Playwright / authenticated / blocked-render harness this skill inherits for every screenshot: baselines, per-route capture, the "Authenticated rendering" contract, and the blocked-render HALT the refine loop honors (a login-wall screenshot is never graded as the surface).
- **`creative-director`** (agent) — owns inventing a NEW visual language / art direction; this skill never invents one, it drives an already-approved design to the quality bar.
- **Callers** — `/redesign` (Phase 6 refine loop), `/art-direct` (build step), `/enhance-ui` (`--with-iterate` variant generator). Those own the caller's rubric and scorecard; this skill applies the refine loop against them and emits per-round lens/component deltas back.
