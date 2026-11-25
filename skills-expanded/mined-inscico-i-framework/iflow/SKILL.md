---
name: iflow
description: The front door / orchestrator for the I-Framework. Reads the Product/ folder, determines which stage (Intent, Ideation, Innovation) you're in from the artifacts and their gates, reports the risk-burndown state, and routes you to the next step. Use to start or resume the Intent → Ideation → Innovation flow.
allowed-tools: Read, Glob, Grep
---

# /iflow — orchestrator & router

You are the map. You read state from disk and tell the founder where they are, which risk is next to retire, and what to run. You do **not** write artifacts (the stage skills do that).

## Procedure

1. **Find the product.** Look for `Product/` in the current directory.
   - **Absent:** this is a fresh start. Explain the flow (Intent → Ideation → Innovation → a `Product/Features/` spec) and recommend `/intent`.

2. **Read state.** Check which of these exist and read their frontmatter `gate:` field:
   - `Product/intent.md` → stage 1, retires *founder–problem* risk.
   - `Product/ideation.md` → stage 2, retires *solution & demand* risk.
   - `Product/innovation.md` → stage 3, retires *market/value/moat* risk.
   - `Product/Features/` → the deliverable; count the files.

3. **Determine position & next step.** The current stage is the furthest artifact that exists; the next action is the first stage whose gate is `open` or whose artifact is missing. Respect the soft-gate philosophy — recommend, never block.

4. **Report a risk-burndown snapshot**, e.g.:

   ```
   I-Framework status
   ─────────────────────────────────────────────
   ✅ Intent       gate passed   (founder–problem risk retired)
   🔄 Ideation     gate open     (solution & demand risk — IN PROGRESS)
   ⬜ Innovation   not started   (market/value/moat risk)
   ⬜ Features     0 files
   ─────────────────────────────────────────────
   Next: finish converging in /ideate (set a demand hypothesis), then /innovate.
   ```

5. **Offer the next command.** Recommend the single next skill to run, and mention `/product-status` for a full dashboard once features exist. If the founder explicitly wants to jump ahead past an open gate, let them — just name the risk they're leaving open.
