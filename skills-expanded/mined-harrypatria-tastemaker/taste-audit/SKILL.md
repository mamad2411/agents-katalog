---
name: taste-audit
description: Reviews an existing UI, screenshot, URL or codebase for AI slop, UX debt, accessibility failures and design-system drift, then returns a scored, prioritised fix plan and (on request) applies it. Use for "review my UI", "why does this look AI-generated", "audit", "make it look professional", "roast my landing page", "is this accessible", or before a launch.
---

# Taste Audit: diagnose, score, fix

Find what makes the interface feel generated or hard to use, rank it by user impact, and fix it with the smallest diffs.

## Inputs (any)

Code (repo or files) · screenshot(s) · live URL (use a browser tool if available) · description. With code, run the scanner first; with images, apply the catalog by eye.

## Procedure

1. **Context** (3 lines): who uses it, the critical flow, platform. Infer; do not interrogate.
2. **Automated pass** (code only): `node <taste-guard>/scripts/slop-scan.mjs <src> --project --json`.
3. **Heuristic pass**, by lens, using catalog IDs where they exist:
   - **Slop**: V/C-series visuals and copy, including Review-only items (V15, V17, C07).
   - **Hierarchy**: one focal point per view? primary action obvious within 3 seconds? squint test.
   - **Consistency**: radius, spacing, type scale, color roles, icon set; count distinct values.
   - **States**: loading, empty, error, permission on each async surface (U10).
   - **Accessibility**: contrast (measure, don't guess), keyboard path, names, focus visibility, reflow at 320px, motion.
   - **Copy**: specific, verb-led, consistent voice, no hype.
   - **Responsiveness and performance**: layout shift, image weight, font loading, mobile tap targets.
4. **Score**: Taste score from the scanner (or estimate from findings) + BASIC (0-2 each for Beauty, Accessibility, Simplicity, Intuitiveness, Consistency).
5. **Prioritise**: P0 blocks use or excludes users (a11y errors, broken states) · P1 erodes trust (slop, inconsistency) · P2 polish.
6. **Fix plan**: for each finding, the exact change (file:line, class or token to use). Group by component so fixes are batched.
7. **Apply** (when asked or when the user said "fix"): P0 then P1, smallest diffs, re-scan, report before/after score.

## Output

```
Tastemaker audit: <product/page>
Score <before>/100 (<grade>) · BASIC <n>/10 · <e> errors · <w> warnings
Top 3 problems (user impact first):
1. <finding> [ID] -> <fix>
...
P0 | P1 | P2 tables: ID · where · problem · fix
After fixes (if applied): score <after>/100, remaining items with reasons
```
Keep the summary to 12 lines; tables only as long as the findings.

## Rules

- Measure contrast with `taste-tokens/scripts/contrast.mjs`; never eyeball a borderline pair.
- Do not restyle what works. A good layout with slop copy gets copy fixes, not a redesign.
- Screenshot audits: state what cannot be verified from pixels (keyboard, screen-reader names, states not shown).
- Never invent analytics or user research to justify a finding; reason from heuristics and say so.
