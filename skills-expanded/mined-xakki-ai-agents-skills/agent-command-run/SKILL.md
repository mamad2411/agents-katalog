---
name: agent-command-run
description: 'Run a noisy command and report compact output without losing failure evidence or confusing process outcomes. Use when command output is too large to review interactively. RU: длинный вывод команды, сжать вывод.'
---

# Compact command reporting

Use when command output is too large for useful interactive review. Run the actual authorized command with its arguments unchanged; capture full output to an access-controlled location when needed and permitted. Print a bounded digest with both line and byte limits, a clear truncation indicator and the path to retained evidence without exposing secrets. A short routine command does not need a capture wrapper.

Preserve each command's real exit status, signal, timeout and completion state separately from capture, transport or parser errors. A launched process or partial tail is not a completed result. Check the full retained artifact for relevant failures and counts before reporting success; a search with zero matches is meaningful only if its scope and instrument were validated. Report filtered or truncated excerpts as excerpts.

## Capture wrapper

The bundled [capture wrapper](scripts/hermes-log-run.py) runs one command and keeps its merged stdout and stderr in a private log (a `0700` directory under `TMPDIR`, file mode `0600`). Resolve the skill location through the current runtime's plugin interface, then run `python3 <skill-dir>/scripts/hermes-log-run.py [--tail-lines N] [--tail-bytes N] -- <command and exact argv>`. It prints `LOG_PATH=<path>` first, then one `RESULT` line, then a bounded tail.

- The `RESULT` line carries `classification` (`OK`, `FAIL`, `INTERRUPTED` or `LOG_ERROR`), the wrapper and child exit codes, `log_state` and the raw size and line counts. `classification=OK` means the child exited `0`, the log was finalized and no signal interrupted the wrapper; a printed success message alone is never enough. The child's own status (including `126` and `127`) is preserved; a logging failure exits `125`.
- The tail defaults to 80 lines and 8192 bytes. Explicit limits must be positive and are capped at 10,000 lines and 65,536 bytes, so a single enormous line cannot flood the context.
- On `INT` or `TERM` the wrapper forwards the signal to the command's own process group, waits 2 seconds, then sends `SIGKILL` to that group. An interrupted run leaves a partial log (`log_state=partial`); report it as partial, never as a complete result.
- The wrapper captures output only. It does not authorize the wrapped command, redact secrets (bounds are not redaction) or clean up old logs; retention is a separate, explicitly confirmed operation.

Self-test: `python3 <skill-dir>/scripts/test_hermes_log_run.py --artifact-root <private-dir> --report-path <new-file>` uses `scripts/fixture_emitter.py` as a deterministic child process and needs no network. `--report-path` must not exist yet.

For structured, mixed or long-running output and retention boundaries, use [outcome and capture checks](references/outcome-and-capture.md). Do not expose raw credentials or private payloads in logs or excerpts; use the runtime's available interface and follow the project's retention policy.

When implementing or reviewing structured capture pipelines, use [receipt verification](references/structured-receipts.md) for producer, reader and parser boundaries.
