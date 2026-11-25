---
name: health
description: Take the target repo's health pulse on demand — run its test/lint/typecheck (and any extra) checks and emit one pass/fail summary. Auto-detects the repo's checks (package.json scripts or Makefile) with explicit --cmd override. Opt-in; not wired into the default pipeline. Output streams live but is never captured (secret-safe). Use to answer "is the repo green right now?" before shipping or after a major change.
---

# /health — is the repo green right now?

Goal: one command that runs the repo's checks (test, lint, typecheck, …) and tells you
PASS or FAIL — on any project, with a secret-free record. This is a green/red **pulse**,
not a coverage gate (the pipeline `/harness-claude:test` skill owns the 80% floor).

> **Opt-in.** No default-pipeline skill or hook invokes `/health`. It shell-executes the
> repo's own check commands with your privileges — run it deliberately. Git boundary: it
> only reads and runs; it never commits, pushes, or branches.

## When to run
- Before `/harness-claude:ship`, or after a major change, to confirm the repo is still green.
- On a fresh checkout / unfamiliar repo, to see what passes with one command.
- As the `--score` half of a `/benchmark` run, or any time you want a quick health check.

## Secret-safety (hard invariant)
Each check's output **streams live to your terminal** (same as running the command yourself)
but is **never captured** — it cannot reach the summary, the JSON artifact, or any log. The
artifact records only `name / command / pass / durationMs` + the gate. A secret printed by a
check stays on your tty and out of every persisted file.

## Discovery
With no `--cmd`, the runner auto-detects checks:
- **package.json** `scripts` — `test`, `lint`, `typecheck` (run as `<pm> run <name>`; the
  package manager is detected from the lockfile — pnpm / yarn / npm). Non-standard scripts
  (e.g. `build`) are ignored.
- else **Makefile** — `test` and `lint` targets (`make test` / `make lint`).

`--cmd '<shell>'` (repeatable) **replaces** the detected set when present.

## Do this
1. **Inspect (optional):** see what will run without running it.
   ```
   node scripts/eval/continuous.js --list
   ```
2. **Run the pulse:**
   ```
   node scripts/eval/continuous.js                       # auto-detect
   node scripts/eval/continuous.js --cmd 'pytest -q' --cmd 'ruff check .'   # explicit
   ```
   Exit **0** = all checks PASS · **1** = any check FAIL · **2** = nothing to run (no `--cmd`
   and nothing detectable). Per-check timeout defaults to 300s (`--timeout-ms` overrides); a
   timed-out check counts as FAIL and the run continues.
3. **Read the result.** The summary lists each check (`PASS|FAIL  <name>  <dur>`, with a
   `→ re-run: <command>` hint on failure) and a gate line. The full machine record is written to
   `.claude/eval/continuous/<timestamp>.json` (and `latest.json`) — metrics only, no output.
4. **Act on it.** On FAIL, re-run the named command yourself to see the captured output (it was
   streamed live, never stored), fix, and re-run `/health`.

## Security & trust
- Detected / `--cmd` commands are author-authored shell — same trust boundary as the repo's own
  `npm test` / build scripts and the `eval` fences in `checkpoint.js`. Don't point `/health` at
  a repo whose `package.json` scripts / `Makefile` you don't trust.
- The artifact never contains output, env, or secrets — only the commands you ran and pass/fail.

## Notes
- Self-contained: pure Node + shell, reuses `_lib.js`; no companions (mgrep/graph/context7), no
  network, zero new deps.
- Distinct from the pipeline `/harness-claude:test` skill: it enforces coverage during Verify;
  `/health` is an on-demand pass/fail pulse you can run against any repo.

## Exit criterion
A continuous-eval run has produced a pass/fail summary (and `.claude/eval/continuous/latest.json`),
and you've acted on any FAIL — repo confirmed green, or the failing checks identified for fixing.
