---
name: safvr-brand-design-guardrails
description: "Apply and protect SAFVR Landingpage2.0 visual system with scaffolding, consistency checks, and brand guardrails. Use when asked to style/refactor SAFVR UI, adjust Tailwind tokens, tune typography or spacing, polish CTA blocks, or review branding drift."
cluster: design
version: 1.0.0
origin: "craft-agent workspace"
globs:
  - "src/**/*.{ts,tsx,css}"
  - "src/app/**/*.{ts,tsx,css}"
  - "src/components/**/*.{ts,tsx,css}"
  - "tailwind.config.ts"
  - "src/lib/links.ts"
  - "Docs/design-dna.json"
---

# SAFVR Brand Design Guardrails

A SAFVR-specific design skill for **scaffolding, consistency enforcement, and anti-drift QA** across Landingpage2.0.

Target project root:
`safvr/Landingpage2.0`

## What this skill does

1. Loads brand context before any visual change
2. Applies a deterministic SAFVR design scaffold (tokens, typography, spacing, component shape)
3. Runs repeatable consistency checks (colors, fonts, CTA styles, link constants)
4. Produces concise brand QA output for every significant UI update

---

## Trigger Signals (Keyword-Aware)

Treat this skill as active when user intent includes terms like:
- **Brand work:** “safvr branding”, “design dna”, “visual identity”, “brand consistency”
- **UI polish:** “make it cleaner”, “landing page polish”, “premium look”, “blueprint style”
- **System work:** “tailwind tokens”, “typography hierarchy”, “spacing rhythm”, “cta style”
- **QA work:** “consistency check”, “off-brand review”, “design audit”, “visual regression”

If request is SAFVR UI-related and ambiguous, default to this skill.

---

## Hard Gate: Read Before Designing

Before making any visual or UX changes, read in this order:

1. `AGENTS.md`
2. `Docs/design-dna.json`
3. `tailwind.config.ts`
4. `src/app/globals.css`
5. `src/lib/links.ts`
6. Relevant page/component files being changed

Conflict precedence:
1. explicit user request
2. AGENTS.md constraints
3. design-dna.json/tailwind tokens
4. existing implementation conventions

No styling work starts before this context is loaded.

---

## Brand Foundation (Non-Negotiable)

### Typography
- Display/headings: `font-display` (Archivo)
- Body/UI: `font-body` (Figtree)
- No ad-hoc font families unless explicitly approved

### Palette + Tokens
- Use `blueprint-*` colors from Tailwind config
- Prefer semantic tokens/classes over raw hex
- Avoid adding one-off color values if token exists

### Visual Language
- Light blueprint aesthetic with crisp linework
- Rectangular CTAs (avoid pill shapes)
- Lucide line icons with restrained stroke
- Pattern/grid effects are supportive texture, not visual noise
- Keep critical copy as HTML (not baked into images)

### Spacing + Rhythm
- Preserve generous section spacing
- Reuse nearby spacing cadence; avoid per-section custom scales

---

## Scaffold Workflow (Default for non-trivial design tasks)

### Refinement mode (required)
Use a **2–3 pass loop** for meaningful SAFVR UI work:
1. **Pass 1 — Brand alignment:** establish token/type/shape truth from references
2. **Pass 2 — Component normalization:** align implementation to canonical patterns
3. **Pass 3 — Deterministic QA:** run harness checks and report findings

### 1) Brand Snapshot
Capture:
- typography roles used
- token palette for this task
- spacing rhythm and section cadence
- component shapes/states that must remain consistent
- one-line “visual truth” statement

### 2) Change Plan
For each touched area:
- what changes visually
- which classes/tokens are used
- why it remains on-brand
- responsive impact

### 3) Implement Minimal Changes
- smallest viable change set
- prefer extending existing patterns over creating parallel systems

### 4) Consistency Check
Run deterministic checks (see `references/prompting.md` harness commands).

### 5) QA Summary
Return:
- files changed
- checks passed/failed
- exceptions with rationale
- optional follow-up opportunities

---

## Deterministic Consistency Checker

### Token Drift
- detect newly introduced raw hex colors where blueprint token should be used
- detect hardcoded font stacks bypassing `font-display` / `font-body`
- detect accidental “pill” CTA radius patterns on primary actions

### Structural Integrity
- CTA links must use centralized constants (`src/lib/links.ts`)
- typography hierarchy must remain coherent (display vs body roles)
- spacing should align with neighboring section rhythm

### UX + Readability
- maintain usable contrast on light blueprint surfaces
- keep motion subtle/purposeful and reduced-motion safe
- prevent key text from being moved into raster assets

---

## Output Contract

For substantial design tasks, always return:
1. **Brand Snapshot** (2–6 bullets)
2. **Implemented Changes** (file-by-file)
3. **Consistency Findings** (pass/fail)
4. **Exceptions** (if any)
5. **Next Recommendations** (optional)

---

## Anti-Patterns

- introducing arbitrary colors when blueprint tokens exist
- skipping AGENTS/design-dna read before styling
- mixing unrelated visual styles in one flow
- moving critical copy into static images
- decorative over-animation
- one-off fixes that increase visual entropy

If exceptions are required, document them clearly.

---

## When to read reference files

| Task | File |
| ---- | ---- |
| Full SAFVR token table, typography roles, spacing + visual rules | `references/design-system.md` |
| Reusable UI patterns: buttons, cards, nav, sections, forms | `references/components.md` |
| AURA phase semantics, ribbon behavior, and color/motion boundaries | `references/aura-visual-language.md` |
| AURA implementation adjudication using good-vs-bad examples | `references/aura-examples.md` |
| Task workflow, consistency/audit commands, keyword triggers, pre-ship checklist | `references/prompting.md` |
| Tailwind/global CSS hook points and safe extension patterns | `references/tailwind-config.md` |
