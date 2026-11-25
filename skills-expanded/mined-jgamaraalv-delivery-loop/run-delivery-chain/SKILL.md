---
name: run-delivery-chain
description: Build, run, test, and drive the delivery-chain Claude Code plugin. Use when asked to run delivery-chain, run its tests, exercise the agent-memory hook sidecar, or verify the plugin's runtime works on this machine.
---

`delivery-chain` is a **Claude Code plugin**, not an app — no GUI, no server, no
CLI binary. The deliverable is prose (skills + agent personas under `.claude/`).
The **one executable component** is the stdlib-only Python **agent-memory hook
sidecar** (`scripts/agent_memory_hook.py`), invoked by the harness at
`SubagentStart` (inject per-role memory) and `SubagentStop`/`Stop` (persist an
episode). "Running" this plugin means **driving that sidecar** the way
`hooks/hooks.json` does, and keeping the Python test suite green.

Drive it via **`.claude/skills/run-delivery-chain/driver.sh`** — it feeds the
shipped hook command a live-harness event on stdin and asserts the full
persist → inject round-trip. There is nothing to screenshot.

All paths below are relative to the repo root (`<unit>/`).

## Prerequisites

`python3` (stdlib only — **no pip, no venv, no network**). Verified on 3.14, the
sidecar targets 3.x broadly.

```bash
python3 --version   # → Python 3.14.3 here
```

No `apt-get` line: the sidecar imports only the standard library, and the rest
of the plugin is Markdown.

## Setup

None. No install, no build step. Clone and run.

Optional env (the driver and tests work **without** it):

```bash
# Only Phases 2-3 (OpenAI lesson extraction + embedding retrieval) read this.
# Absent → those phases skip silently; persist + curation + patterns still run.
export OPENAI_API_KEY=...   # optional; NEVER commit it into hooks/hooks.json
```

## Run (agent path)

Drive the runtime end to end — persist an episode from a transcript, inject it
back, plus a prose-only negative case and a malformed-stdin robustness check:

```bash
.claude/skills/run-delivery-chain/driver.sh
# → === ALL CHECKS PASSED — the agent-memory runtime round-trips end to end ===
```

Runs from **any cwd** (it resolves the plugin root from its own location, like
the real `${CLAUDE_PLUGIN_ROOT}`), uses a throwaway `mktemp -d` host repo as
`CLAUDE_PROJECT_DIR`, and unsets `OPENAI_API_KEY` so it stays keyless/offline.
The store it writes/reads lives under `$CLAUDE_PROJECT_DIR/.claude/agent-memory/`
in that temp dir and is deleted on exit. The driver is the harness — it's how
you confirm the runtime works without spinning up a real `claude` session.

What each step asserts:

| step | drives | asserts |
|---|---|---|
| 1 | `subagent-stop` with a `transcript_path` JSONL | exactly **1** episode written, carrying `taskId` |
| 2 | `subagent-start` (episode + a seeded lesson) | output wrapped in **one** `=== AGENT MEMORY ===` envelope; episode under its prior-experience label, lesson under its relevant-lessons label |
| 3 | `subagent-stop` with a prose-only message | episode count **unchanged** (prose carries no `taskId`/`status`) |
| 4 | `subagent-stop` with garbage stdin | exits **0** (exit 2 would block a Stop hook) |

### Drive a single phase by hand

The shipped command reads the hook event JSON on **stdin** and writes the
hook-output JSON on stdout. Subcommand is `subagent-start` or `subagent-stop`:

```bash
echo '{"agent_type":"frontend-engineer"}' | python3 scripts/agent_memory_hook.py subagent-start
# → {"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": ""}}
# (empty context + exit 0 when no store exists — the keyless degradation path)
```

## Test

The full suite — stdlib `unittest`, **no pytest, no deps**:

```bash
(cd scripts/tests && python3 -m unittest discover)
# → Ran 695 tests ... OK   (a few seconds)
```

One file (**must `cd` in first** — see Gotchas):

```bash
(cd scripts/tests && python3 test_memory_store.py)
# → Ran 86 tests ... OK
```

Static secret-scan gate (CI's `static` job also runs this):

```bash
bash scripts/secret_scan.sh; echo "exit $?"   # → exit 0 (clean)
```

## Gotchas

- **Single-file tests fail from the repo root.** `python3 scripts/tests/test_memory_store.py`
  (run from `<unit>/`) fails one assertion: `test_no_getcwd_scatter...` checks
  that no `.claude/` dir exists under cwd — but the repo root *has* one (the
  plugin's own), so it false-positives. Run from inside `scripts/tests/`
  (`cd scripts/tests && python3 test_memory_store.py`) and it's 86 OK. The
  whole-suite `discover` command already `cd`s in, so it's unaffected.
- **The memory envelope only appears when enrichment adds a block.** By the
  byte-identity contract in `agent_memory_hook._enrich_context`, a bare episode
  injects *without* the `=== AGENT MEMORY ===` wrapper when keyless retrieval
  finds nothing and no lesson exists. The driver seeds one lesson (lessons load
  keyless) so the envelope path is exercised — don't expect the envelope around
  an episode-only, no-lesson, no-key store.
- **The hook never exits non-zero.** Malformed stdin, missing `agent_type`, I/O
  errors — all degrade to exit 0. Exit 2 from a `Stop` hook would block the stop
  and risk a recursion loop, so the sidecar is wrapped to always exit 0. Don't
  rely on exit codes to detect failure; inspect the store or stdout instead.
- **A `Stop`/main-thread event with no `agent_type` persists nothing.** Persist
  is per dispatched persona only; an `agent_type` of `""`/`unknown` is skipped so
  the orchestrator's own turn never becomes a spurious `unknown/` episode.

## Troubleshooting

- **`subagent-start` prints `"additionalContext": ""`**: expected when the
  per-role store is empty or `CLAUDE_PROJECT_DIR` is unset/points at a dir with
  no `.claude/agent-memory/<agent>/`. Run `subagent-stop` with a real status
  block first (the driver does this in step 1), then start again.
- **`FAIL: AGENT MEMORY envelope must wrap output exactly once (found 0)`** if
  you adapt the driver and drop the lesson seed — see the envelope gotcha above.
- **`sidecar not found at .../scripts/agent_memory_hook.py`**: the driver is
  being run from a copy detached from the repo. It resolves the plugin root three
  levels up from itself (`.claude/skills/run-delivery-chain/`), so keep it in
  place or run the shipped command directly with `python3 scripts/...`.
