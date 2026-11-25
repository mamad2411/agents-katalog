---
name: opencode-orchestration
description: |
  How to drive the OpenCode CLI (opencode.ai) as the
  coding agent inside a loss-function-driven loop. The
  driver (Hermes or any orchestrator) owns the loop, the
  loss function, and the verifier runs. OpenCode owns
  the model call, the per-iteration context, the file
  edits, and the test runs. Load this skill whenever
  launching, monitoring, or interrupting an OpenCode
  session from inside a loss-function-driven loop, and
  when building an OpenCode wrapper script — the verified
  run-mode flags, the JSON output shape, the parser, and
  the contract the wrapper must satisfy all live here.
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [opencode, coding-agents, agent-orchestration, provider-agnostic]
    related_skills: [cline-orchestration, claude-code-orchestration, codex-orchestration, hermes-agent-orchestration, harness-engineering, loss-function-design]
---

# OpenCode Orchestration

This skill describes how to drive **OpenCode CLI**
(opencode.ai) as the coding agent inside a
loss-function-driven loop. The pattern is
**agent-agnostic at the driver level** — Hermes is the
driver in the reference build, but any orchestrator (a
shell script, CI runner, another agent) that can spawn a
subprocess and read JSON can use the same wrapper
contract.

The split:

- **The driver owns:** the loop, the loss function, the
  verifier runs, the human-facing surface, the stop
  criterion, the budget.
- **OpenCode owns:** the model call, the tool surface, the
  per-iteration context, the file edits, the test runs
  inside its sandbox.

## Why OpenCode

- **Provider-agnostic.** OpenCode works with OpenRouter,
  Anthropic, OpenAI, Google, local models, and any
  OpenAI-compatible endpoint. The driver never sets the
  model — OpenCode's own auth does.
- Native tool surface (file edit, command run, browser,
  MCP).
- `opencode run "<prompt>"` for one-shot non-interactive
  runs. **This is the mode the loop should use.**
- `--format json` for machine-readable single-object
  output. (`--format stream-json` is also available for
  live streaming, but the reference parser handles the
  single-object output.)
- Per-cycle workdir isolation via `--workdir` is supported
  but **the wrapper uses `--cwd`-style isolation** to
  match the other adapters' contract.
- Auth via `opencode auth login` or provider env vars
  (`OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, etc.).

## Locating the `opencode` binary

Shell environments may resolve different OpenCode
binaries. The wrapper resolves the binary at call time.
The resolution order is:

1. The `$OPENCODE_BIN` environment variable, if set.
2. `$(command -v opencode)` — whatever's on `PATH`.
3. Bail with exit code 3 and a clear error.

If the loop driver itself is shell-based, double-check
`which -a opencode` first — Homebrew, npm-global, and
manual installs can coexist on `PATH`.

## Working invocation (run mode, JSON output)

```bash
"$OPENCODE_BIN" run \
  --format json \
  --model "$OPENCODE_MODEL" \
  "$TASK" \
  > "$RAW_OUT" 2>"$STDERR_FILE"
```

Where:

- `run` is the one-shot subcommand. The interactive
  form is `opencode` (TUI), which needs `pty=true`. The
  loop uses `opencode run` (no pty).
- `--format json` makes the result parseable. Default
  is human prose.
- `--model` selects the model. **Set this in the
  loop-driver / wrapper via `$OPENCODE_MODEL` env var,
  not as a hardcoded value** — the user picks the model.
- `$TASK` is the cycle prompt. The wrapper can also
  pass the prompt as the last positional argument.
- The working directory is the wrapper's `ITER_DIR`
  (see "Per-cycle isolation" below).

## What we tried and what broke

| Flag                              | Result                                                                  |
|-----------------------------------|-------------------------------------------------------------------------|
| `opencode -p "..."`               | `-p` is not an OpenCode flag. The one-shot entry point is `opencode run`. |
| `opencode` (interactive TUI)      | Requires `pty=true`. The loop should use `opencode run` instead. |
| `opencode run "..."` (no `--format json`) | Human-readable transcript, not parseable. The wrapper's parser needs `--format json`. |
| `opencode run --format json ...`  | Works. The wrapper's reference invocation. |
| `opencode run --thinking ...`     | `--thinking` is a model-effort hint; some providers ignore it. Default is fine. |
| `opencode run --model openrouter/anthropic/claude-sonnet-4 ...` | `provider/model` format. **Don't hardcode in the wrapper** — user picks. |
| `opencode run --workdir /tmp/foo ...` | `--workdir` sets the agent's working directory. Equivalent to Cline's `--cwd`. The wrapper uses `cd` instead for shell-script consistency. |
| `opencode --exit` (no such flag)  | OpenCode has no `--exit` flag. The TUI exits on Ctrl+C. |
| `opencode --version`              | Works. Useful in the smoke test. |

## The right pattern

- **`opencode run` is mandatory** for non-interactive
  work. The interactive TUI is for human-driven
  exploration and requires `pty=true`.
- **`--format json` is mandatory** for the wrapper to
  parse the result. Without it the output is human
  prose.
- **`--model` is set from `$OPENCODE_MODEL` env var.**
  The user configures this in their shell or in
  `opencode auth login`; the wrapper reads it. **Do not
  hardcode the model in the wrapper.**
- **Provider config is sacred.** OpenCode picks the
  provider from its own auth (`opencode auth list`).
  The wrapper must NEVER pass `--provider` directly
  (the provider is part of the model string).
- **Per-cycle isolation** comes from `cd "$ITER_DIR"`
  in the wrapper, where `ITER_DIR` is a fresh per-cycle
  directory. The verifier scripts also read from
  `ITER_DIR`.
- **Capture duration from the JSON result, not from
  `date`.** OpenCode emits a `duration_ms` field.

## Output schema (verified)

`opencode run --format json` emits a single JSON object
to stdout when the task finishes. The schema:

```json
{
  "result": "<final assistant text>",
  "session_id": "ses_abc123",
  "duration_ms": 10276,
  "usage": {
    "input_tokens": 5,
    "output_tokens": 603,
    "cache_read_tokens": 0
  },
  "model": "openrouter/anthropic/claude-sonnet-4",
  "finish_reason": "completed"
}
```

Key fields for the loop:

- `result` — the final assistant text. The loop's
  `candidate_text`.
- `session_id` — OpenCode session ID. Useful for
  debugging (`opencode session list`).
- `duration_ms` — wall-clock duration.
- `usage` — token accounting.
- `model` — `provider/model` string.
- `finish_reason` — `"completed" | "max_iterations" | "error"`.

The reference parser at
`scripts/parse_opencode_output.py` extracts this shape.
If OpenCode's output schema changes, edit the parser, not
the wrapper.

## Token accounting caveat

`usage.input_tokens + output_tokens + cache_read_tokens`
is the *total tokens OpenCode sent/received in the API*,
including cache hits. Cost is not part of the standard
output — the loop's `cost` sub-loss is graded 0.0
unless the user provides a custom cost function.

## Smoke test

The minimal smoke test:

```bash
opencode run --format json "Respond with exactly: OPENCODE_SMOKE_OK"
```

Expected: JSON object on stdout with `"result": "OPENCODE_SMOKE_OK"`
(or similar). Exit code 0.

If the JSON does not parse, OpenCode likely isn't
authenticated — run `opencode auth list` and check
provider env vars are set.

## Drop-in substitution

This skill is a sibling of `cline-orchestration`,
`claude-code-orchestration`, `codex-orchestration`, and
`hermes-agent-orchestration`. The harness-scaffold and
loop-driver skills are **runtime-agnostic**. They invoke
whatever wrapper is at `verifiers/<runtime>-wrapper.sh`.
The user passes `--runtime {cline,claude-code,codex,hermes-agent,opencode}`
to `harness-scaffold` to generate the correct wrapper.

The 4 invariants from `compatibility.md` hold here:

1. `parse_opencode_output.py` emits JSON in the same
   shape as `parse_cline_output.py`.
2. The wrapper accepts a positional `TASK` plus
   `--cwd PATH`, `--timeout N`, `--cycle NAME` and writes
   the parsed JSON to stdout.
3. The `opencode-skills-dir.sh` instrument prints the
   agent's skills directory to stdout.
4. The wrapper exits non-zero on missing binary / bad
   args, exits 0 on successful agent run, never blocks
   longer than `--timeout`.

## Common pitfalls

1. **Forgetting `--format json`.** Without it the output
   is human prose, unparseable.
2. **Hardcoding the model in the wrapper.** Read
   `$OPENCODE_MODEL` env var instead. The user picks.
3. **Running the TUI in non-pty mode.** The TUI requires
   `pty=true`; `opencode run` does NOT need pty.
4. **PATH mismatch selecting a different OpenCode
   binary.** If the loop driver and the user shell have
   different `PATH` orderings, they may run different
   binaries. Pin via `$OPENCODE_BIN` env var.
5. **Setting `--provider` directly.** OpenCode uses
   `provider/model` strings; set the whole string via
   `$OPENCODE_MODEL` instead.

## Verification checklist

- [ ] Wrapper resolves `opencode` via `$OPENCODE_BIN` →
      `command -v opencode` → bail.
- [ ] Wrapper uses `opencode run` and `--format json`.
- [ ] Wrapper reads `$OPENCODE_MODEL` for the model
      string, not a hardcoded value.
- [ ] Wrapper writes parsed JSON to stdout, not the
      transcript.
- [ ] Wrapper exits non-zero on missing binary, zero on
      successful agent run.
- [ ] Wrapper is wrapped in `timeout` and kills OpenCode
      if it overruns.
- [ ] `opencode-skills-dir.sh` prints the agent's skills
      directory.
- [ ] No absolute paths, no per-user config baked in.
