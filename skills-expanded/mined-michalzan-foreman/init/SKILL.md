---
name: init
description: Audit a repository's checks and set it up for Foreman unattended runs. It inventories linters and test suites, proves each can fail, proposes fixes and writes .foreman.toml. Use when the user invokes /foreman:init, asks to set a project up for the harness, or the doctor reports a missing or stale audit.
---

# Foreman init

The goal is a check command that is complete and has been seen to fail. Propose everything; apply only what the user approves.

## 1. Inventory

Read the Makefile, `package.json` files, `pyproject.toml`, the pre-commit config and the CI pipeline. List every linter, formatter check, type checker and test suite the repo has, and the command that runs each.

## 2. Compare

Decide which single command should be the project check (often `make check`). Trace what it actually runs. List every item from the inventory that it does not run, and anything CI or pre-commit runs that it does not.

## 3. Prove each gate can fail

Every gate in the proposed check gets a canary: test suites and type checkers, and also linters, formatter checks, migration checks and docs or site builds. Plant one at a time, because a check often stops at its first failure and would hide the rest.

| Gate | Canary |
|------|--------|
| test suite | a test asserting `1 == 2` |
| type checker | a line with a deliberate type error |
| linter | an unused import, or another rule the config enforces |
| formatter check | a few lines in a format it rewrites |
| migration check | a model change with no migration |
| docs or site build | a page with a broken link or reference |

1. Put the canary in a new file named `foreman_canary` with the gate's extension, where that gate looks (inside its test paths or include globs). Where only a change to a tracked file can trip the gate, as with most migration checks, pick a file with no uncommitted changes and restore it with `git checkout -- <file>` afterwards.
2. Run the proposed check command. It must exit non-zero and name the canary.
3. Remove the canary and confirm `git status` shows no trace of it.

A gate whose canary does not turn the check red is a no-op gate: report it as a gap. A gate you could not trip without touching something the user would mind is "not proven": say which and why. Never call the check proven while a gate is in neither list nor turned red.

## 4. Propose

Show the user one list:

- each gate with its canary result: red, no-op, or not proven
- each gap, and the change that closes it (for example, adding a frontend test target to `check`)
- the drafted `.foreman.toml`: check command and timeout, working and protected branches, frontend path prefixes, decisions log, parked file
- anything you left out on purpose and why (a slow suite, for instance)

Wait for the user's answer. Apply only what they approve.

## 5. Write

1. Apply the approved build-file changes and re-run the check to confirm it passes.
2. Create the decisions log and the parked file if they do not exist.
3. Add `.foreman/` to `.gitignore`.
4. Compute the audit fingerprint from the project root, over every build file you read:
   `uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/audit.py" <file> <file> ...`
5. Write `.foreman.toml` with today's date, that fingerprint and that file list under `[audit]`. The guard will ask the user to approve this write; that is expected.
6. Ask the user to read `.foreman.toml`, then approve it. The guard will prompt them; only a person approves:
   `uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/trust.py" approve`
   Until it is approved, and again after any later change to it, every gate is off for this project.
7. Run the doctor: `uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/doctor.py" --cli`. It must print `foreman: ok`.
8. If the project publishes through an allow-list or similar, confirm `.foreman.toml` is not published.

## Declaration format

    [check]
    command = "make check"
    timeout_seconds = 900

    [branches]
    protected = ["test", "main"]

    [frontend]
    paths = ["frontend/src/"]

    [plan]
    decisions_log = ".planning/DECISIONS-LOG.md"
    parked = ".planning/PARKED.md"

    [audit]
    date = "YYYY-MM-DD"
    fingerprint = "sha256:..."
    files = ["Makefile", "frontend/package.json"]

`frontend.paths` are path prefixes. Keep `timeout_seconds` at 1100 or below.
