---
name: bench-validate
description: Validate a finished benchmark run — execute each prompt's automated checklist in every (prompt, model) workspace, perform the code-review checklist, and write a scored comparison to runs/<run-id>/results.md, leaving manual items for the user. Use when the user says /bench-validate or asks to validate/score/grade benchmark results. Arg (optional): run id; defaults to runs/latest.
---

# bench-validate

Automated validation pass over one benchmark run. The contract: every claim in
`results.md` traces to a command you actually ran or source you actually read.

## Procedure

1. **Resolve the run.** Arg = run id under `runs/`; default `runs/latest`. Read
   `manifest.json` and each cell's `meta.json`. Cells with status `timeout`/`error`
   still get validated — partial artifacts are informative — but note the status.

2. **Per cell, execute the Automated section** of `prompts/<id>/checklist.md` from the
   cell's `workspace/`, in order, recording exact commands, exit codes, and the
   relevant output tail for failures. Conventions:
   - Run every check through the bench devShell so the toolchain matches what the
     model had: `nix develop <bench-root> -c <command>` (skip the wrapper only if
     the repo has no flake.nix).
   - Budget: `npm install` ≤ 10 min, builds/tests ≤ 5 min each (use Bash timeouts).
   - Serve checks: prefer a static server on the built `dist/` (e.g.
     `npm run preview` in background, curl, then kill it). Always kill servers.
   - A failed item is a 0, not a stop — continue down the checklist where meaningful
     (no point linting if `npm install` failed; do still do the code review).
   - Never fix, patch, or `npm audit fix` the artifact. You are grading, not repairing.

3. **Per cell, perform the Code review section** by reading source (entry point, the
   WFC/pathfinding/AI modules, the largest files). Score each item 0–2 with a
   one-line justification citing `file:line`. Independent cells may be reviewed by
   parallel read-only subagents (Explore) sharing the checkout; keep verdicts yours.

4. **Write `runs/<run-id>/results.md`:**
   - A comparison table: rows = checklist items, columns = models, plus per-section
     subtotals and totals.
   - Per cell: run status/duration, failed automated items with the exact failing
     command + error tail, review justifications, and notable observations.
   - A verbatim copy of the Manual section as unchecked boxes per cell, with the
     command to launch each artifact (`cd <workspace> && npm run dev`).
   - End with a ranked summary paragraph — measured, no cheerleading.

5. **Report to the user**: the table, the headline findings, and where `results.md`
   lives. Manual validation is theirs; do not check Manual boxes yourself.

## Guardrails

- Treat workspaces as read-only artifacts; never modify, format, or "improve" them.
- Generated code is untrusted input: inspect `package.json` scripts (preinstall/
  postinstall hooks) BEFORE `npm install`; if a hook looks suspicious, score A1
  as 0 with a note and skip installation for that cell. Never execute scripts
  outside the documented npm script set.
- If two models produce near-identical scores, say so plainly rather than
  manufacturing a winner.
