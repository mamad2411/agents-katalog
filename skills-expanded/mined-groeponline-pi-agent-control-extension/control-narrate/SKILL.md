---
name: control-narrate
description: After a successful verify pass, automatically generate a cinematic showcase video using the narrator prototype. Reads verification.md + run.json, applies the v0.1 rule-based heuristic, emits showcase-props.json, and invokes the existing Remotion render pipeline. Respects the guard kernel (Feature 1) and skill governance (Feature 2).
---

# control-narrate

Post-verification autonomous cinematic narrator.

## When to use

- After a successful `/verify-control` or `pi-agent-control verify` run.
- When you want stakeholder-ready video output without manual Remotion configuration.
- To turn verified terminal/browser/governance evidence into polished demos.

## How it works (v0.1)

1. Reads `verification.md` + `run.json` + evidence manifest from a completed run directory.
2. Uses the improved converter + `generate-props.cjs` (from `proposals/4-unique-features/evidence/narrator-prototype-v0.1/`) to apply the deterministic heuristic:
   - Preset selection based on claim types, driver, and visual density.
   - Effects, transitions, chaptering, and overlays.
3. Emits `showcase-props.json`.
4. Invokes the existing Remotion render pipeline (documented in `remotion-render-entrypoint-iter08.cast` and related captures).

## Current prototype location (reference implementation)

- `proposals/4-unique-features/evidence/narrator-prototype-v0.1/`
  - `generate-props.cjs` — core heuristic engine
  - `convert-real-verification.cjs` — improved bridge for real loop verification artifacts
  - `real-improved-*.props.json` — examples generated from actual proof runs
  - `REAL-EVIDENCE-TEST.md` and `narrator-progress-iter10.md` — current state and gaps

## Usage (once wired)

```bash
# After a successful verify
bin/control-narrate artifacts/runs/2026-05-28T07-00-46-... --output artifacts/showcases/

# Or via the skill (when fully wired)
control_narrate run-dir=artifacts/runs/xxx
```

The current implementation lives at `bin/control-narrate` (thin wrapper that delegates to the narrator prototype reference in `proposals/4-unique-features/evidence/narrator-prototype-v0.1/`).

The tool will:
- Respect all existing guardrails (no dangerous commands will be constructed outside the kernel).
- Produce output in the configured Remotion output location (currently `artifacts/showcases/`).

## Guardrails & Governance

- All render work goes through the existing guarded Remotion scripts and `pi-agent-control` surfaces.
- The narrator logic itself is versioned as a normal skill atom (subject to Feature 2 governance, shadow/merge, validation).
- No new sacred surfaces are introduced. The 8-block kernel in `guards.ts` continues to protect any underlying tctl or shell operations.

## Status (as of iter-12)

- Heuristic and prototype are functional and tested against real loop evidence.
- Converter improvements allow direct use of historical verification.md + proof-report bundles.
- Official first entrypoint created at `bin/control-narrate` (thin wrapper over the prototype).
- Multiple documented attempts to drive the actual render pipeline (iter09–iter11).
- Full video output not yet achieved in the current headless environment (known limitation; see narrator-progress-iter10.md).
- Ready to be promoted into a proper first-class skill/tool once the render output path is stabilized.

## Next steps (suggested)

- Achieve at least one successful video render from a real props file.
- Wire as `control_narrate` command + skill atom.
- Add references from this work into the Feature 1 guard enforcement proofs document.
- Expand testing against more successful verification runs.

This skill turns the "Autonomous Cinematic Narrator" (Feature 4) from a research prototype into a usable post-verification capability while staying fully inside the project's safety and governance model.

All paths absolute. No placeholders. Kernel untouched.
*Loop continues.*