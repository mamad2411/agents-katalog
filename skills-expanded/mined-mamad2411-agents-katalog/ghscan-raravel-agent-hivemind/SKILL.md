---
description: "Run verification stages from verify.md against the current branch. Use when the user wants to check if the code passes all verification steps, or run a specific stage (lint/type/test/build). Args: optional stage name to run only that stage (e.g. 'test', 'lint')."
---

# hv-verify — Run verification stages from verify.md

Reads the project's `verify.md` and executes each stage's commands. Reports pass/fail per stage. Does not modify any code.

## When to use

- User asks "does everything pass?", "run the tests", "check the build"
- Before opening a PR
- After a manual code change outside of `hv-task`
- User asks the `hv` plugin to run verification, optionally for a single stage

## Steps

### 1. Identify the project

```bash
cat .hivemind-link.json     # for project name
hv config data_path         # for the absolute data dir
```

If `.hivemind-link.json` is missing, ask the user to run `hv-init` first.
The link file under v4 carries only `{project, prefix}`; data_path is
derived from the global config's location and surfaced via `hv config`.

### 2. Load verify.md

Read `{data_path}/projects/{project}/verify.md`.
Fallback: `{data_path}/projects/{project}/build-verify.md`.

If neither exists, stop and tell the user to generate `verify.md` before proceeding.

### 3. Parse stages

Extract every `## <stage>` section that contains a fenced `bash` code block. The stage name is the heading text (e.g. `lint`, `type`, `test`, `build`). Skip `## completion` — it is not executable.

Example parsed structure:
```
stages:
  lint:  "python3 -m ruff check src/ tests/"
  type:  "python3 -m mypy src/"
  test:  "python3 -m pytest"
  build: "python3 -m build --wheel"
```

### 4. Determine which stages to run

- **No args**: run all stages in the order they appear in verify.md.
- **Arg given** (e.g. `verify only the test stage`): run only that stage. If the stage name does not exist in verify.md, list the available stages and stop.

### 5. Run each stage

For each selected stage, run its command via Bash. Capture exit code, stdout, and stderr.

Display progress as you go:

```
▶ lint ... ✓
▶ type ... ✓
▶ test ... ✗
▶ build ... skipped (earlier failure)
```

Rules:
- Run stages sequentially.
- If a stage fails (non-zero exit), print the full stdout+stderr for that stage, then **stop** — do not run subsequent stages. This matches how CI pipelines work and avoids noise from cascading failures.
- If all stages are explicitly named in the args (single stage), do not apply the stop-on-fail rule — just report the result.

### 6. Report results

**All pass:**
```
✓ All N stages passed.
```

**Failure:**
```
✗ <stage> failed (exit <code>)

<stdout/stderr output>

Remaining stages: <list> — not run.
```

Then suggest next steps based on the failure:
- `lint` failed → "Fix the reported issues, then ask the hv plugin to run the lint stage again."
- `type` failed → "Resolve type errors in the listed files."
- `test` failed → "Investigate the failing tests. Use `hv-task` to implement a fix."
- `build` failed → "Check the build output for packaging errors."

## Rules

- NEVER modify source files. This skill only reads and runs.
- NEVER invent commands. Only run commands extracted verbatim from verify.md.
- If verify.md has multiple bash blocks in one section, run them in order.
- Do NOT run the `## completion` section — it contains prose criteria, not commands.
