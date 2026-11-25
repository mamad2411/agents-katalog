---
name: color-audit
description: Audit a design system's color palette against measurable color-science disciplines — WCAG/APCA contrast of declared token pairs, perceptual (OKLCH) ramp uniformity, color-blindness safety of status/categorical sets, token architecture (primitives → semantic → components), dark-mode integrity, and hue budget — and produce evidence-cited findings with concrete fixes. Use this skill whenever the user asks to review, evaluate, or fix design-system colors, palettes, ramps/scales, themes, or dark mode; asks "are our colors accessible/consistent?", "is this palette reasonable?", or "audit our tokens"; wants to add or change a theme, accent, or status color safely; or reports contrast/readability/color-blindness concerns — even if they don't say "audit". For behavioral/semantic UX review of views (labels, states, redundancy), use ux-semantics-audit instead; this skill owns everything palette- and token-level about color.
---

# Color Audit

Evaluate a design system's color selection against the codified disciplines from color science and design-system practice (WCAG/APCA, Material HCT, Radix scale semantics, Adobe Leonardo, Stripe's accessible-palette work) and emit findings a coding agent can directly act on. This is a *linter for the palette*, not an aesthetic critique: most rules are mechanically checkable, and the bundled analyzer computes the numbers so no check is eyeballed.

## Design philosophy (shared with ux-semantics-audit — it shapes every judgment call)

1. **Precision over recall.** A false positive costs more than a miss: the consuming agent will "fix" a non-problem and degrade a palette someone chose deliberately. When in doubt, don't flag.
2. **No evidence, no finding.** Every finding cites the token source (file, line, value) and — for Tier 1 rules — the measured number from the analyzer. If you cannot point at the value and the measurement, the finding does not exist.
3. **Exceptions are where precision lives.** Each rule in `references/rules.md` has an enumerated exceptions list; check it before flagging. Deliberate design (documented OLED black, brand-pinned steps, compressed dark ramps) is a pass, not a borderline flag.
4. **Severity is trust calibration.** `block` = mechanical and near-certain (a declared pair failing WCAG *is* failing). `warn` = judgment involved. Never promote a judgment call to `block`.
5. **Measure, don't estimate.** Never state a contrast ratio, lightness value, or CVD verdict from intuition — run `scripts/analyze-palette.mjs`. A report whose numbers are wrong is worse than no report.

## Workflow

### Step 1 — Locate the palette

Find where color truth lives. Look for, in rough order: CSS custom properties (`:root`/theme blocks), a theme/token definition module, Tailwind config, and the framework vocabulary layer that exposes tokens to components.

In **this repo** the layers are:
- Primitives (oklch ramps): `packages/web/src/styles/primitives.css`
- Semantic values per theme × mode: `packages/web/src/lib/themes.ts` (light/dark halves per theme)
- Component-facing vocabulary: the `@theme inline` block in `packages/ui/src/styles.css` (its token comments are also the step-semantics documentation)

If the palette lives only in scattered component styles with no token layer, that is itself the headline `token-architecture` finding — audit what exists and say so.

### Step 2 — Extract a palette file

Write the extracted colors into `palette.json` in your scratchpad, following the schema documented at the top of `scripts/analyze-palette.mjs`:

- `ramps` — the primitive scales, step → color
- `pairs` — every declared fg/bg pairing with its `use` (`text` | `large-text` | `ui`). Derive pairs from the system's own pairing convention (`*-foreground` partners, `on-*` tokens, status `-fg`/`-bg` families). One palette file **per theme × mode** — light and dark are separate audits.
- `groups` — meaning-carrying sets that must stay mutually distinguishable (status family, categorical/chart series, diff colors)

The script accepts hex, `rgb()`, and `oklch()` syntax directly, so paste values as-is. Resolve `var()` chains and `color-mix()` by hand to concrete values (note any you had to approximate).

### Step 3 — Run the mechanical checks (Tier 1)

```bash
node .claude/skills/color-audit/scripts/analyze-palette.mjs <palette.json> all
```

Run per theme × mode. The script covers `declared-contrast-pairs` (WCAG + APCA), `ramp-uniformity` (OKLCH lightness tables, spacing irregularity, cross-ramp interchangeability), and `cvd-safety` (protan/deutan/tritan simulation, collapse detection). Its ⚠ flags are *advisory* — the rules in `references/rules.md` decide what becomes a finding, and their exceptions lists are the rubric.

### Step 4 — Load the ruleset and run structural checks (Tier 2)

Read `references/rules.md` in full. Then run the grep-backed checks: `token-architecture` (raw hex/oklch/primitive references/raw framework shades in component code), `step-semantics` (is there a documented role per step/token; are near-duplicate tokens used interchangeably), `state-derivation` (ad-hoc hover/active values bypassing the system's state rule), `dark-mode-integrity` (independently authored dark half + the full contrast rerun against dark values).

### Step 5 — Judged review (Tier 3)

`hue-budget`: list every hue family and its nameable job. Also verify the exceptions you relied on in earlier steps (e.g. the CVD redundant-channel exception requires actually checking usage sites — don't assume icons exist).

### Step 6 — False-positive sweep

Re-examine every finding and drop any that:
- matches an enumerated exception,
- lacks a concrete citation (token source + measured number for Tier 1),
- depends on an assumption you did not verify (an "undocumented" intent you didn't search the docs for; a usage site you didn't read),
- would require the fix to violate another rule.

If a finding survives with genuine uncertainty, keep it at `warn` and say what would confirm it.

### Step 7 — Emit the report

Use exactly this structure:

```markdown
# Color Audit: <scope> (<theme> × <mode(s)>)

## Summary
<2-4 sentences: overall assessment, count of block/warn findings, and the
remediation order when findings depend on each other (ramps → contrast/states;
see the cross-references section of rules.md).>

## Findings

### [BLOCK|WARN] <rule-id>: <one-line title>
- **Where**: <token/ramp/component> — `<file>:<lines>`
  ```<lang>
  <minimal quoted value or snippet>
  ```
- **Measured**: <the analyzer's numbers, for Tier 1 rules>
- **Why it matters**: <1-2 sentences tied to this palette, not a rule recital>
- **Suggested fix**: <concrete change — target values or token restructure; a
  code sketch when it fits in a few lines>
- **Confidence**: high | medium (warn-tier only; say what would confirm a medium)

## Passes worth keeping
<2-5 things the palette gets right that a fix must not regress.>

## Not flagged (borderline)
<Candidates examined and declined, each with the exception or reason.>
```

Order findings: all `block` first, then `warn`, each group by leverage (user impact × fix cheapness). Zero findings is a valid result — say so and fill in "Passes worth keeping".

When proposing replacement values, propose them in OKLCH (adjust L to hit the contrast target while preserving hue/chroma identity) and verify the proposal by running it back through the analyzer — a suggested fix that fails its own target is the fastest way to lose the reader's trust.

**Exception: brand-pinned fills.** If the failing color is a brand/identity value (documented as such, or the owner says so), changing it is usually not on the table — proposing "darken the brand" wastes the finding. Present the brand-preserving alternatives ladder from the `declared-contrast-pairs` rule (flip label polarity, split brand vs action token, demote the fill to non-text duty, soft-fill variant) with each option's measured number, and state the trade-off that picks between them. When the reader may not know the contrast scale, anchor the numbers once: 1:1 invisible, 3:1 large-text floor, 4.5:1 the AA line for body text, 21:1 black-on-white.

### Step 8 — Build the shareable report (Rome surfaces)

When the audit covers a Rome surface and the user wants an artifact to look at, share, or triage, reuse **ux-semantics-audit's report app** at `.claude/skills/ux-semantics-audit/report/` — do not hand-author an HTML page. `findings.tsx` and `repros.tsx` are gitignored per-run outputs rewritten by every audit (seeded from the committed `*.example.tsx` when missing); the chrome, filtering, triage and prompt export are fixed, and the deliverable is the built HTML, never the source. Read `.claude/skills/ux-semantics-audit/references/report-app.md` for the authoring contract, then:

1. Rewrite `findings.tsx` against the `AuditReport` type (rule ids from this skill's ruleset slot straight into `Finding.rule`; use `surface` values like `palette`, `dark-mode`, `status colors`).
2. Rewrite `repros.tsx`. For color findings the honest reproduction is usually **the real tokens doing the wrong thing**: a swatch/ramp strip rendered from the live CSS custom properties, real `@rome-os/ui` components on the failing pair, side-by-side shipped/fixed values, or a CVD-simulated rendering (the analyzer's matrices are in `scripts/analyze-palette.mjs` if a repro needs them inline). "Shipped" mode must show the defect — a failing pair renders at its actual illegible contrast.
3. `node .claude/skills/ux-semantics-audit/report/build.mjs` → single self-contained `dist-report/index.html`.

## Division of labor with ux-semantics-audit

| Question | Skill |
|---|---|
| Is the palette itself sound (contrast pairs, ramps, CVD, tokens, themes)? | **color-audit** |
| Does a *view* misuse color (color-only status, emphasis budget, missing states)? | **ux-semantics-audit** |

The seam is `color-not-sole-channel`: the per-view rule lives in ux-semantics-audit; this skill's `cvd-safety` covers the palette-level half and hands per-view violations off. When one root cause spans both (e.g. no status tokens exist, so views hand-roll colored text), report it here as the palette finding and name the ux-semantics-audit follow-up in the summary.

## What this skill does NOT do

- Aesthetic judgment — whether the brand hue is *pretty* is not auditable; whether it can carry AA text is.
- Full WCAG conformance beyond color (focus order, semantics, zoom) — recommend axe-core.
- Per-view UX review — that's ux-semantics-audit.
- Choosing a brand identity — this skill evaluates and repairs a system around the hues it's given; it only proposes hue changes when a hue cannot meet its assigned job at any lightness.
