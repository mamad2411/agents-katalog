---
name: opencode-current-session-id
description: Composer — discover and verify the current opencode session ID and title from the logger logs
category: OpenCode
---

# OpenCode Current Session ID (v1)

## Composition Rationale

This skill is a **composer**: it does NOT re-implement glob-sorting or YAML parsing. It sequences two base skills:

1. [`file-glob-sort-by-mtime`](../../general/file/file-glob-sort-by-mtime/SKILL.md) — finds the newest `.yaml` file in
   `.opencode/logs/`
2. [`yaml-field-extract`](../../general/yaml-field-extract/SKILL.md) — extracts `session.id` and `title` from the YAML
   header

The composer's value-add: orchestrating the pipeline, resolving relative script paths, and cross-verifying the state
file exists.

## When to Use

- You need to know the current opencode session ID programmatically
- You are composing a larger workflow that needs the session ID for traceability

## Environment & Dependencies

| Requirement | Version | Notes |
| ------------- | --------- | ------- |
| Python | 3.12+ | Stdlib only |
| PyYAML | any | Required by yaml-field-extract (PEP 723 inline metadata) |
| `.opencode/logs/` | — | Must exist (created by opencode logger plugin) |

## CLI Contract

| Argument | Required | Description |
| ---------- | ---------- | ------------- |
| _(none)_ | — | Runs the full pipeline with auto-discovered repo root and log dir |
| `--log-dir PATH` | No | Override `.opencode/logs/` directory (default: `<repo-root>/.opencode/logs` or `$OPENCODE_LOGS_DIR`) |
| `--repo-root PATH` | No | Override repo root discovery (default: `$OPENCODE_REPO_ROOT` / `$AI_SUITE_ROOT`, then `git rev-parse --show-toplevel`, then legacy `parents[4]`) |
| `--json` | No | Emit single-line JSON instead of human-readable text |
| `--state {exists,missing,any}` | No | Gate on state-file presence (default: `any`; mismatch exits 2) |
| `--since ISO_TIMESTAMP` | No | Filter sessions by `st_mtime >= timestamp` (e.g. `2026-09-19T10:00:00`) |
| `--pending-ttl SECONDS` | No | In-flight (`*-pending-*.yaml`) markers older than this are stale; `0` disables (default: `3600`) |
| `--dry-run` | No | Print discovered paths (repo_root, log_dir, base scripts) as JSON and exit without extractors |

**Output (text, default):**

```text
Session ID: ses_XXXXXXXXXXXXX
Title: My Session Title
State file: exists
Pending marker: yes
```

**Exit codes:**

- `0` — session ID found (and state gate satisfied when `--state` given)
- `1` — any pipeline step failed (missing log, missing key, etc.)
- `2` — session found but `--state` gate mismatched (`--json` still prints the payload)

**Output (`--json`):**

```json
{"session_id": "ses_XXXXXXXXXXXXX", "title": "My Session Title", "state": "exists", "pending": true, "yaml_path": "<path>", "log_dir": "<path>"}
```

`title` is `null` when the YAML header has no `title` key.

## Protocol

1. Run `python3 scripts/find-current-session.py`
2. Read stdout for session ID, title, state-file presence, and the pending-marker flag.
3. Verify before use: `Pending marker: yes` confirms the winning session has an
   in-flight turn — the strongest "you are inside this session" signal.
   `Pending marker: no` means selection fell back to newest-mtime; accept it only
   when no other session could plausibly be active, otherwise treat the result as
   ambiguous and surface the candidates instead of guessing.
4. Never substitute a session ID remembered from artifact filenames, scratch
   folders, or earlier conversation — IDs change on fork; re-run discovery at the
   point of use.

## Edge Cases

- **No YAML logs exist**: exits 1 with "could not find newest YAML log"
- **YAML header missing session.id**: exits 1 with the header path and base stderr detail
- **Newest header corrupt**: next-newest `ses_*/` dir is tried before the flat fallback
- **No state file**: still succeeds (reports "missing") unless `--state exists` (exits 2)
- **`--since` filters all sessions**: exits 1 with "could not find newest YAML log"
- **Symlinked log dir**: follows symlinks via `Path.rglob`
- **Concurrent sessions in the same repo**: selection is pending-marker-first —
  the active session has an in-flight `NNN-pending-*.yaml` in its dir — then
  newest-mtime. When two sessions are genuinely in-flight, the script warns on
  stderr and selects the newest pending one; treat that as ambiguous, verify
  against your own context, and surface the candidates instead of guessing.
- **Stale pending marker**: a crashed or force-quit turn can leave an orphan
  `NNN-pending-*.yaml` behind; markers older than `--pending-ttl` (default
  3600s) are ignored.
- **Deduced ID (never)**: an ID seen in artifact filenames, scratch folders, or
  prior conversation is not the current session's ID after a fork — re-run
  discovery instead of passing a remembered value.

## Prohibited Actions

- Do NOT re-derive the sort or YAML extraction logic inline — always delegate to the base skill scripts.
- Do NOT hardcode log directory paths — use `.opencode/logs/` relative to repo root.
- Do NOT deduce, carry, or reuse a session ID from artifact filenames, scratch
  directories, or prior conversation context — IDs change when a session is
  forked. Resolve via discovery in the current run and verify the pending-marker
  flag before passing the ID to consumer scripts.

## Script Reference

`find-current-session.py`:

1. Resolves repo root via `$OPENCODE_REPO_ROOT` / `$AI_SUITE_ROOT`, git top-level, legacy `parents[4]` fallback (cached
   per-process via `lru_cache`)
2. Resolves base script paths under repo root (with `SCRIPT_DIR`-relative fallback)
3. Resolves log dir via `--log-dir`, `$OPENCODE_LOGS_DIR`, or `<repo-root>/.opencode/logs`
4. If `--dry-run`: emits discovery JSON and exits
5. Orders `ses_*/` dirs pending-marker-first then newest-mtime (filtered by `--since` if given), probes top 5 in
   parallel via `ThreadPoolExecutor` (order-preserving `executor.map`), accepting the first header in that order
   whose `session.id` parses; warns on stderr when multiple sessions have in-flight turns
6. Runs `sort-by-mtime.py` on `.opencode/logs/` with glob `*.yaml` and `--limit 1`
7. Parses JSON Lines output to get the newest file path
8. Runs `extract-field.py` twice: once for `session.id`, once for `title`
9. Checks for `.opencode/logs/<sid>.state.json`
10. Applies `--state` gate (exit 2 on mismatch; `--json` still prints payload)
11. Prints results (incl. the pending-marker flag)

## Composition by Lower-Level Skills

| Primitive | Composition Mechanism |
| ----------- | ---------------------- |
| `file-glob-sort-by-mtime` | `sort-by-mtime.py --dir .opencode/logs --glob *.yaml --limit 1` → newest path |
| `yaml-field-extract` | `extract-field.py --file <path> --key session.id` → session ID |

## Related Skills

- [`opencode-installed-plugin-lookup`](../opencode-installed-plugin-lookup/SKILL.md) — consumer of the logger-location
  convention (.opencode/logs/)
