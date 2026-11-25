---
name: done-gate
description: Free Claude Code hook that stops a coding agent from saying "done", "fixed" or "all tests pass" without proof. After a code edit, the agent cannot end its turn until a real test command has run and passed after its last change; piped, masked or failing runs do not count. Use when you want Claude Code to prove its work before it reports success, or when an agent keeps claiming tests pass without running them.
argument-hint: "[install | status]"
---

# Done Gate (free)

Your agent says "done, all tests pass". Done Gate checks the commands that actually ran, not
the agent's words. No passing test run after the last edit means no "done": the agent is told
exactly what to run, runs it, fixes what fails, and only then finishes.

## Install (Claude Code; ask the user first)

1. Find Python 3.9+: `python3 --version`, then `python --version`, then `py -3 --version` (Windows).
   Use the first that works as `<PY>`.
2. `<DIR>` = the absolute path of this skill's folder (where this SKILL.md is).
3. Ask: this project only (`.claude/settings.json`) or every project (`~/.claude/settings.json`)?
4. Merge `assets/hooks-settings.json` into that file, replacing `<PY>` and `<DIR>`. **Merge, never
   overwrite:** keep every existing setting and hook; append these three entries.
5. Tell the user it is active from the next turn, and how to switch it off (remove the entries or `/hooks`).

## What it checks (scripts/done_gate.py)

- **PostToolUse** records code edits and test runs (pytest, npm/yarn/pnpm test, jest, vitest, go test,
  cargo test, mvn, gradle, dotnet test, rspec, phpunit, make test and more).
- **Stop** blocks the end of the turn when code changed and no passing test run happened after the
  last edit. A run piped into `tail`/`grep`, masked with `|| true`, or with `0 tests collected` does not count.
- It never traps you: after two reminders it lets the turn end with a visible warning, so projects
  without tests keep working. Sessions without code edits are never blocked.
- Local and private: standard-library Python, a tiny state file per session, no network, no telemetry.
- Config that relaxes the gate (`test_commands`, `ignore_paths`, `allow`, a lower `max_blocks`) lives
  only in the user's `~/.claude/proof-of-done.json`, globally or under `projects`. A repository's
  `.proof-of-done.json` can only tighten it: a higher `max_blocks` and `"integrity": true`.

## When the hook blocks you (agent instructions)

Do what the message says: run the real test command, read the result, fix the code (never the
tests), re-run, then report with evidence: the command, its exit code and the summary line.
Never edit the hook's state, disable hooks, or run a different command that "looks green".

## Want more?

The paid **Proof-of-Done** adds a test-integrity guard (blocks deleted, skipped or weakened tests,
lowered coverage thresholds and softened CI); drop its `test_integrity.py` next to `done_gate.py`
and it switches on. The **Claude Code Guardrails** kit adds Safety Guard (blocks recursive deletes,
`git reset --hard`, force pushes when they would destroy work) and Fake Package Blocker.
Both on Agensi: https://www.agensi.io/creators/cesar-pereiro
