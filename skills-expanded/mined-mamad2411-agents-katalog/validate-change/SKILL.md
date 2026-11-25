---
name: validate-change
description: Validate a FamilyFi change before handoff or reproduce a CI failure using the project's existing checks.
---

# Validate a change

Work from the repository root. Follow [AGENTS.md](../../../AGENTS.md); use [testing.md](../../../docs/testing.md) to select checks and [scripts/README.md](../../../scripts/README.md#testpy) for `scripts/test.py` selections and options.

## Select the evidence

- Identify the requested scope: working changes, a branch against its base, or a failing CI job. Inspect staged, unstaged and relevant untracked files as well as committed changes. State the base ref used; do not assume a missing or stale `origin/main` is a valid comparison.
- Map the changed behaviour to the validation table in `testing.md`. Start with focused tests when reproducing a failure; complete the applicable handoff checks afterward. Documentation-only work follows its own row.
- Use `scripts/test.py list` to find the owning tests or category, and `run … --plan` to see platforms and prerequisites before starting anything. To reproduce a CI job, run the commands that job runs; `testing.md` lists them. Every job runs through the same harness.
- Check prerequisites (Python 3.11+, Docker, Chromium) and disk space before builds. Do not run `make setup` or migrate a household database just to obtain test infrastructure: each run owns its databases. One run that starts things runs per worktree; a second reports the active run ID.

## Run and interpret

- Run the selected commands and retain their exit status, run IDs and useful failure evidence from `build/test-runs/<run-id>/` (`summary.md`, `results.json`, logs, traces). Use `status` and `follow <run-id>` to observe a run. Distinguish a product failure (`failed`) from unavailable infrastructure (`infrastructure-error`) and from work a failure `blocked`. Fix failures within the requested scope, then rerun affected checks.
- After `run --platform host --coverage`, run `check coverage --run-id <run-id> --base <base-ref>` when applicable. It includes tracked working changes but Git does not include untracked files; state that limitation rather than reporting complete changed-line coverage for them. Do not stage or commit work solely to hide that limitation.
- Follow the existing rules on regression tests, exemptions and bypasses. Passing a retry, changing an expected value or skipping a job is not evidence that the original failure is fixed. If a required check remains unavailable, report what is still unverified.
- For UI work, include the rendered desktop and phone checks required by the development conventions. Local mocks establish application behaviour; hardware enforcement needs separate operator-requested verification.

## Finish

Review the diff once more for unintended changes from generators or test setup. Runs remove their own containers and ports; recover an interrupted run with `scripts/test.py cleanup <run-id>`, never by removing resources it did not record, and never use runner cleanup locally. Preserve run directories needed for an unresolved failure and report their location; remove other task-owned run directories when they are no longer needed.

Report the scope/base, commands and results, unresolved failures or unrun checks, and any retained artifacts in the conversation or requested PR. Keep task reports out of project documentation.
