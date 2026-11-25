---
name: verify
description: Run the verification gate before claiming work complete. Lint, typecheck, tests, plus the staff-engineer review checklist. Manual companion to the Stop hook.
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

# Verify

Verification-before-completion. Never claim "done" without running this.

## Steps

1. **Working tree state**: `git status` — note staged vs unstaged changes.
2. **Lint** the changed surface (Python: `ruff check`; TS: `eslint`; TF: `terraform fmt -check`).
3. **Typecheck** if applicable (`tsc --noEmit`, `mypy`, `pyright`).
4. **Run tests** scoped to the change (full suite if you can spare it).
5. **Self-review** every changed file against `knowledge/staff-engineer-review/SKILL.md`:
   - No bare `except:` / `catch (e)` swallowing errors.
   - All I/O has timeouts.
   - Logs include enough context to diagnose at 3am.
   - Tests cover error paths, not just the happy path.
   - No hardcoded secrets, no `console.log`/`print` debug residue.
6. **If touching auth/input/secrets/network/file I/O**: run the `security-reviewer` subagent.

## Output

Report pass/fail per step with the actual command output for any failure. Do not summarize "tests pass" without showing the run.

If anything failed: stop. Fix it. Do not commit. Do not open a PR. Re-run `/verify`.

## Why this exists

Tests passing locally is not the same as the change being correct. The Stop hook (`verify-on-stop.sh`) runs lint+typecheck automatically; this skill is the manual companion that adds the staff-engineer review pass and security check.
