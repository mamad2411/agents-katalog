---
name: ras-inspect
description: >-
  Use when Codex needs to inspect, summarize, report, or browse existing local RAS history with `ras status`, `ras show`, `ras report`, or `ras serve`. Use for requests such as "show this RAS run", "what happened in this run", "generate a RAS report", "open the RAS web UI", or "check stale run status". Do not use to start new reviews, verification, fixing, or implementation loops.
---

# RAS Inspect

Use RAS inspection commands when the user wants stored run history, synthesized output, reports, stale-run summaries, or the local read-only web UI.

## Operating Model

`ras status`, `ras show`, `ras report`, and `ras serve` read local RAS state and artifacts. They do not start reviewer, verifier, or builder agents. `ras report` writes a Markdown report by default unless `--output -` is used.

## Before Running

1. Confirm the current directory is the intended git repository or pass explicit `--workspace` / `--project` flags for aggregate inspection.
2. Inspect `git status --short --branch` for operator awareness; inspection should not edit source files.
3. Check that `ras` is available with `command -v ras`.
4. If an active RAS command is still running, prefer that command's own output for live progress. Use inspection for explicit diagnostics, not as a polling loop, and do not pair inspection with cleanup/admin mutations against state that may still be active.

## Status And Synthesis

List recent runs and stale running runs:

```bash
ras status
ras status --json
```

Inspect one run:

```bash
ras status <run-id>
ras status <run-id> --json
```

Print the synthesized fix queue:

```bash
ras show <run-id>
ras show <run-id> --json
```

For agent-readable diagnostics, prefer the JSON forms. `ras status --json` returns recent run summaries plus stale-run metadata, `ras status <run-id> --json` returns structured run detail with stale metadata when applicable, and `ras show <run-id> --json` returns structured run detail even when a run is still running or has no synthesis artifact yet.

## Reports

Write or print a Markdown report:

```bash
ras report <run-id> --output -
ras report <run-id> --output reports/ras-run.md
ras report --pr 42 --latest --output -
```

Use aggregate report mode for multiple projects:

```bash
ras report --workspace ~/code --project-id <slug> <run-id> --output -
```

## Web UI

Serve local RAS history:

```bash
ras serve
ras serve --background
ras serve status
ras serve stop
```

Use explicit sources when inspecting multiple repositories:

```bash
ras serve --workspace ~/code
ras serve --project ~/code/repo-a --project ~/code/repo-b
```

## Handling Output

When reporting back, include the run id or project source, status, key artifact/report paths, stale-run notes, server URL when started, and any missing/unreadable project diagnostics.

## Safety Notes

- Do not treat inspection output as a fresh review or verification result.
- Do not start `ras serve` on a public interface unless the user intentionally asked for that binding.
- Do not overwrite a report path without noticing whether the user supplied it; use `--output -` for ephemeral inspection.
- Do not use inspection commands as a polling loop while guarded fixer or verification commands are actively mutating RAS state.
- Do not run cleanup/admin mutations from an inspection workflow while another RAS command may still own the listed run state.
