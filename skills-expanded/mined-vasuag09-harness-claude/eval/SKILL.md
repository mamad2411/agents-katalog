---
name: eval
description: Checkpoint a change against its spec's acceptance criteria — run the machine-checks, adjudicate the prose ones, and gate ship until every criterion passes. Opt-in; not wired into the default pipeline. Use late in Verify, alongside /test and /verify.
---

# /eval — acceptance-criteria checkpoint

Goal: prove the work satisfies *the spec it was built against*, criterion by criterion.
Green tests show the code runs; this shows it meets what was promised.

> **Opt-in.** This skill is not invoked by any default-pipeline skill or hook. Running it
> is always explicit; it changes no baseline behavior. (Fulfills v0.4 AC-6 / v0.3 AC-E5.)

## Do this
1. **Locate the spec.** Default to the latest `docs/specs/*.md`; let the user name one if
   the change targets an older spec. Confirm it's the spec this change was built against.
2. **Run the deterministic gate:**
   ```
   node scripts/eval/checkpoint.js [spec.md]
   ```
   It prints a per-criterion table (PASS / FAIL / MANUAL) and exits **0** (all PASS, none
   manual) · **1** (a check FAILED) · **2** (no failures, but MANUAL criteria remain).
   - Each criterion may carry an inline ` ```eval ` fenced shell command — that's its
     machine-check. Add one to an AC when a deterministic check exists (port it from the
     spec's own test commands).
3. **On FAIL (exit 1):** the criterion is objectively unmet. Fix the implementation (not
   the criterion) and re-run. Do not proceed while any check FAILs.
4. **Adjudicate MANUAL (exit 2):** for each prose criterion the script can't decide, gather
   concrete evidence (run the app, read the diff, check `.claude/traces/` for what fired)
   and judge PASS or FAIL yourself. The script never auto-passes prose — closing these is
   your job. If a MANUAL criterion is genuinely verifiable, prefer adding an ` ```eval `
   fence so it's deterministic next time.
5. **Gate.** Ship only when every criterion is PASS — checks green *and* every MANUAL
   adjudicated PASS with evidence. Report the verdict criterion by criterion.

## Security & trust
- **` ```eval ` fences are shell-executed** (via `_lib.sh` → `execSync`) with your privileges.
  They are author-authored, committed markdown — trust them exactly like the repo's own test
  scripts or build hooks. **Review specs from untrusted branches/PRs before running `/eval`.**
- `checkpoint.js --list` is the safe inspect-before-run path: it parses and shows which ACs
  carry a check, but executes nothing.
- **Secret-safe:** a check's output is never printed. On FAIL the report shows only the exit
  code + the command (committed text), so you re-run it yourself to inspect output.
- Each check is bounded by a 60s timeout.

## Notes
- Self-contained: the runner is pure Node and needs no companions (mgrep/graph/context7).
- Complements `harness-claude:test` (suite + coverage) and `harness-claude:verify`
  (observe real behavior); this one ties the change back to its acceptance criteria.

## Exit criterion
Every acceptance criterion in the spec is PASS (machine-checked or evidence-adjudicated).
Then `harness-claude:ship`.
