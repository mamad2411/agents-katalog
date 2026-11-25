---
name: cmd
description: Delegate a bounded build/fix/refactor task to the Command Code CLI (`cmd`) in isolated headless mode, then verify the result from the filesystem instead of trusting the harness self-report.
---

# cmd

Use this skill when the user wants Command Code (`cmd`) to take a bounded coding task off OpenCrabs' plate — a fix, a build, a refactor, a "go implement X" — and run it as a delegated sub-harness.

## What this does

This does **not** open an interactive `cmd` TUI. Bash has no TTY and stdin is `/dev/null`, so a bare `cmd` session hangs forever. That would be fake-magic bullshit.

Instead, it drives Command Code in **headless print mode** (`-p`): takes a prompt, runs autonomously, streams events, exits. OpenCrabs stays the operator — it frames the task, launches `cmd`, watches the output, then **verifies the resulting world state from files/build/tests** instead of trusting `cmd`'s self-report.

## The PATH gotcha (non-negotiable)

`cmd`'s shebang is `#!/usr/bin/env node`, and OpenCrabs' bash runs a stripped PATH that **drops `/opt/homebrew/bin`**. Without the fix every invocation dies with `env: node: No such file or directory` (exit 127). **Every** `cmd` call in this skill MUST be prefixed:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

Binary lives at `/opt/homebrew/bin/cmd` (node sits right next to it). Auth is already set up — logged in as `moneyacademyKE` via the Command Code provider.

## Required behavior

- **Always headless.** Run via `-p "<brief>"`. Never launch bare `cmd`, `cmd -t` without `-p`, or any REPL/interactive shape — it hangs on `/dev/null`.
- **Always bounded.** Pass `--max-turns <n>` (default 50; raise for big builds, lower for tiny fixes). It exits `8` on cap — treat that as "ran out of budget," not success.
- **Isolate by default.** Use `-w/--worktree` to run in a fresh git worktree (requires a git repo). This is the delegated-sub-harness pattern: `cmd` can't nuke the main tree. Only skip `-w` (run in-tree) if the user explicitly says so.
- **Parse the output.** Use `--output-format json` for an NDJSON event stream + a final result line. Read structured events, don't eyeball prose.
- **Use the trust flags.** `-t` (auto-trust the project), `--auto-accept`, `--yolo`, `--permission-mode standard` — these stop `cmd` hanging on permission prompts during an unattended run.
- **Skip ceremony.** `--skip-onboarding` for automated runs.
- **Verify, don't trust.** After `cmd` exits, prove success from the filesystem: required files exist, diff looks sane, the repo's check (`cargo test` / `bb -m ...` / `npm run build` / whatever) actually passes. A clean exit is necessary, not sufficient.
- **Don't let it escape.** `cmd` gets file/edit/shell power in the worktree only. It must NOT push, deploy, email, or post. OpenCrabs reviews the diff before anything leaves the machine.

## Inputs to gather from the user request

Extract or infer:
- the target repo (default: the current working directory — confirm with `pwd`)
- the thing to build / fix / refactor
- required artifacts, files, or content
- the repo's build/test command (for verification)
- whether to run in a worktree (default yes) or in-tree

If the task is too vague to verify, tighten it into concrete artifacts + a passing check before launching.

## Suggested command shape

The canonical delegation invocation:

```bash
export PATH="/opt/homebrew/bin:$PATH"
cd "<target-repo>"
cmd -p "<tight task brief>" \
  -t --auto-accept --yolo --permission-mode standard \
  -w \
  --output-format json \
  --max-turns 50 \
  --skip-onboarding
```

Typical user invocations:
- `/cmd fix the login redirect in web/`
- `/cmd add a health-check endpoint and a test for it`
- `/cmd refactor models.rs under 250 lines`
- `/cmd build the dashboard, run the test suite`

Interpret the trailing text as the task brief, then execute the workflow above. After the run, report what `cmd` did, what the structured output said, and **what the filesystem/build proves**.

## Success criteria

Successful only when the observed world proves it:
- required files/content exist
- repo build/test check actually passes (not just "`cmd` exited 0")
- worktree diff is sane and reviewable
- nothing was pushed, deployed, or otherwise exfiltrated
