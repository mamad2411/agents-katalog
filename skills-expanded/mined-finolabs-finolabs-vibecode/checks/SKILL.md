---
name: checks
description: Verify before claiming or accepting work. Use before saying done, fixed or passing; on "is it done?", "did the tests pass?" or "is it ready to merge?"; before accepting a delegated run; when picking tests; before heavy container or e2e runs; when CI fails, is slow or out of quota, or checks need setup locally or in CI.
---

# Checks

A report is a claim. The diff and the test output you read yourself are the evidence.

Pairs with `tdd` and `diagnosing-bugs` from [mattpocock/skills](https://github.com/mattpocock/skills), which produce the red and green evidence this skill reads.

## Choose the tests

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

- Run the **targeted tests** at checkpoints, not after every edit: those covering the changed code and its traced consumers, plus the project's lint and unit checks for those packages. Pick them from the diff (packages, test name patterns, the end-to-end suite only when the user-facing path changed). Say when no test covers the change; when that change alters runtime behavior, name the gap and propose a test rather than skip it. Advisory (agent judgment): `<this skill folder>/scripts/select_tests.py [--base <ref>]` lists the test modules that name a changed file.
- Run a **full suite** only when the owner asks. Gates and pull requests use targeted tests; CI runs the rest after an authorized push. When the change touches widely shared code whose consumers you cannot trace in full, propose a full suite and wait for the owner's yes.
- A repository's stored check list (set by `/setup add checks`) runs with `<this skill folder>/scripts/checks.py run [--changed] [--base <ref>]`; see [references/checks.md](references/checks.md) for `--changed`, light checks (outside the heavy-job lock), the local receipt and the pre-push hook, and [references/ci.md](references/ci.md) for a cheaper cloud workflow and `checks.py usage`.
- Keep local fixtures small (about 1,000 items) unless the owner asks for larger stages.
- **Heavy jobs** (container-backed suites, scale measurements, end-to-end runs) run one at a time per machine through `delegate`'s `heavy_run.py` (it also waits for load, memory pressure and swap-outs); without it, run one at a time yourself and start only when the one-minute load is below `Load limit` (host config, default 25) and memory pressure is normal. Run at most two test modules per command. Light targeted runs may overlap and skip the lock and the load gate, but still wait while memory pressure is critical (`delegate` "Heavy jobs" defines light). Keep the machine awake for long runs.

## Read the evidence

- Read the output, not the exit code alone: count what ran, what skipped and what was filtered out. A skipped or partially green run is not a pass.
- Missing setup, a missing API or credential is not a behavioral pass: report it as blocked.
- Enabled configuration, a tool's DONE, a tick in a task list or a moved HEAD is not proof of behavior.
- For queries, reports, infrastructure changes and forecasts, a run that completed is not proof the result is right: see `coding-router` `references/non-code-work.md`.

## Bind proof to final bytes

Evidence belongs to the exact revision, contracts, dependencies, configuration and environment it ran on. A later change invalidates only the evidence it affects; rerun those checks and keep the required final ones.

Report each check as **PASS**, **FAIL**, **PENDING**, **SKIP**, **WAIVED** (with who waived it and why) or **N/A**. Only the owner waives a check; an agent proposes the waiver with its reason and leaves the check **PENDING** until the owner agrees, unless the project's rules already waive it.

`run_env.py` is the only way the plugin starts a delegate or test command: it builds an allowlisted child environment, shared with `delegate_env.py`, `verify_claim.py` and `checks.py` (script-enforced).
For a manual targeted test: `python3 -I <this skill folder>/scripts/run_env.py -- <test argv>`.
The quota probe and `ps` snapshot keep their own scoped allowlists under the `CLAUDE.md` exceptions.
Never print, dump, log or assert on the process environment; test synthetic mappings and key names only.

## Accepting someone else's work

Before accepting a delegated report, the coordinator checks the branch and base, every hunk's acceptance-criterion trace, and the targeted test output (advisory, agent judgment), and runs the self-contained `<this skill folder>/scripts/verify_claim.py`. Read [references/accepting.md](references/accepting.md) for its command, the JSON brief, what it checks, the receipt and the ledger gate.

## Claims

State what was run and what it showed. Distinguish drafted, verified, integrated, delivered and parked. Verification grants no publication, push or deploy authority.
