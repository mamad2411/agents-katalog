---
name: claude-code-orchestration
description: |
  How to drive the Claude Code CLI (Anthropic) as the coding
  agent inside a loss-function-driven loop. The driver
  (Hermes or any orchestrator) owns the loop, the loss
  function, and the verifier runs. Claude Code owns the model
  call, the per-iteration context, the file edits, and the
  test runs. Load this skill whenever launching, monitoring,
  or interrupting a Claude Code session from inside a
  loss-function-driven loop, and when building a Claude Code
  wrapper script — the verified print-mode flags, the JSON
  output schema, the parser, and the contract the wrapper
  must satisfy all live here.
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [claude-code, anthropic, agent-client-protocol, agent-orchestration, coding-agents]
    related_skills: [cline-orchestration, codex-orchestration, hermes-agent-orchestration, opencode-orchestration, harness-engineering, loss-function-design]
---

# Claude Code Orchestration

This skill describes how to drive **Claude Code CLI** (Anthropic)
as the coding agent inside a loss-function-driven loop. The
pattern is **agent-agnostic at the driver level** — Hermes is
the driver in the reference build, but any orchestrator (a
shell script, CI runner, another agent) that can spawn a
subprocess and read JSON can use the same wrapper contract.

The split:

- **The driver owns:** the loop, the loss function, the
  verifier runs, the human-facing surface, the stop
  criterion, the budget.
- **Claude Code owns:** the model call, the tool surface, the
  per-iteration context, the file edits, the test runs
  inside its sandbox.

## Why Claude Code

- Native tool surface (file edit, command run, MCP, browser,
  web search).
- Provider-locked: Claude Code is Anthropic-only (Claude
  Opus / Sonnet / Haiku and their variants). The driver
  never sets the model — Claude Code's own auth does.
- Print mode (`-p`) for clean non-interactive one-shots.
  **This is the mode the loop should use.**
- Structured JSON output (`--output-format json`) and
  streaming JSON (`--output-format stream-json`) for
  headless integration.
- Per-task budget caps (`--max-turns`, `--max-budget-usd`).
- `--bare` mode strips hooks / plugins / CLAUDE.md loading
  for fast deterministic CI runs.
- `--allowedTools` whitelists exactly the tools a cycle
  needs (Read, Edit, Write, Bash).
- Auth via OAuth (`claude auth login`) or
  `ANTHROPIC_API_KEY`.

## Locating the `claude` binary

The wrapper resolves the binary at call time. The resolution
order is:

1. The `$CLAUDE_BIN` environment variable, if set.
2. `$(command -v claude)` — whatever's on `PATH`.
3. Bail with exit code 3 and a clear error.

Same pattern as the Cline wrapper. **Do not hardcode an
absolute path** in the wrapper — the user installs Claude Code
wherever they want.

## Working invocation (print mode)

```bash
"$CLAUDE_BIN" "$TASK" \
  --print \
  --output-format json \
  --bare \
  --cwd "$ITER_DIR" \
  --max-turns "$MAX_TURNS" \
  --allowedTools "Read,Edit,Write,Bash" \
  --append-system-prompt-file "$SYSTEM_PROMPT_FILE" \
  > "$RAW_OUT" 2>"$STDERR_FILE"
```

Where:

- `TASK` is the cycle prompt (positional, NOT `-q`).
- `ITER_DIR` is a fresh per-cycle directory (the wrapper
  seeds it from the project root).
- `MAX_TURNS` defaults to 30, override per project.
- `--bare` skips hooks / plugins / CLAUDE.md discovery for
  deterministic runs. **Drop it if you want the user's
  CLAUDE.md to load.**
- `--allowedTools` is the safety net. List exactly the
  tools the cycle needs; the loop's safety sub-loss still
  greps the transcript for `rm -rf`, `chmod 777`, secret
  patterns.

`--thinking` is the equivalent of Cline's reasoning effort.
In Claude Code v2.x it is `--effort low|medium|high|max|auto`.
Default to `low` or omit it; `high`/`max` noticeably slow
cycles and burn budget without proportional quality gains
on most cycles.

## What we tried and what broke

| Flag                              | Result                                                                  |
|-----------------------------------|-------------------------------------------------------------------------|
| `claude -q "..."`                 | `-q` is a chat-mode flag, not a print-mode flag. Use `-p` / `--print`. The task is a **positional arg**. |
| `-p` (without `--bare`)           | Loads user's `~/.claude/CLAUDE.md` and any project `CLAUDE.md`. **Predictable cycles need `--bare`** unless you want user-level context. |
| `--output-format text` (default)  | The transcript is human-readable prose, not JSON. The wrapper's parser needs `--output-format json` or `--output-format stream-json`. |
| `--max-turns 0`                   | Rejected; `--max-turns` is at least 1. Pass a real number. |
| `--max-budget-usd 0.01`           | Rejected; the system-prompt cache creation alone costs ~$0.05. Minimum is ~$0.05. |
| `--dangerously-skip-permissions`  | The non-interactive `-p` mode already skips ALL permission dialogs. Adding this flag is a no-op (and prints a warning in some versions). |
| `claude --worktree feature-x`     | Creates `.claude/worktrees/feature-x` — fine, but the worktree dir doesn't carry the auth, and the loop already isolates via `--cwd $ITER_DIR`. Drop the worktree. |

## The right pattern

- **`-p` / `--print` is mandatory** for non-interactive work.
  The interactive REPL is for human-driven exploration, not
  loops.
- **`--bare` is recommended** for loss-function loops. It
  strips plugin / hook / CLAUDE.md discovery and gives
  predictable, reproducible cycles. Drop it only if your
  loop intentionally depends on the user's CLAUDE.md
  (e.g. a "follow the project's coding rules" skill).
- **`--allowedTools` is a whitelist, not a blacklist.**
  Pick the smallest set the cycle needs. Common minimal
  set: `Read,Edit,Write,Bash`.
- **Provider config is sacred.** Claude Code picks the
  model from its own auth (`claude auth status`). The
  wrapper must NEVER pass `--model` unless you are
  specifically testing model drift. The driver layer is
  the right place to set `expected_model` for the drift
  sub-loss.
- **Capture duration from the JSON result, not from
  `date`.** Claude Code emits `duration_ms` and
  `total_cost_usd` in the JSON result object. Use both.
- **Per-cycle isolation** comes from `--cwd $ITER_DIR`
  where `ITER_DIR` is fresh per cycle, not from
  `--worktree`. The verifier scripts must also read from
  `$ITER_DIR`.

## Output schema (verified)

When you pass `--output-format json`, Claude Code prints
**one** JSON object to stdout when the task finishes. The
schema (v2.x):

```json
{
  "type": "result",
  "subtype": "success",
  "result": "<final assistant text>",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "duration_ms": 10276,
  "duration_api_ms": 8400,
  "stop_reason": "end_turn",
  "terminal_reason": "completed",
  "is_error": false,
  "usage": {
    "input_tokens": 5,
    "output_tokens": 603,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  },
  "modelUsage": {
    "claude-sonnet-4-6": {
      "inputTokens": 5,
      "outputTokens": 603,
      "cacheReadInputTokens": 0,
      "cacheCreationInputTokens": 0,
      "costUSD": 0.078,
      "contextWindow": 200000
    }
  }
}
```

Key fields for the loop:

- `type` — always `"result"` for the single-object output.
- `subtype` — `"success" | "error_max_turns" | "error_budget" | "error_tool"`.
- `result` — the final assistant text. Equivalent to
  Cline's `run_result.text`. The loop's `candidate_text`.
- `session_id` — UUID for resumption (rarely needed in a
  loop; useful for debugging failed cycles).
- `num_turns` — agentic loop count. Maps to Cline's
  `iterations`.
- `total_cost_usd` — actual spend. Cheaper proxy for cost
  than raw tokens.
- `duration_ms` — wall-clock duration including all tool
  calls. Use this for budget enforcement.
- `usage.input_tokens` + `usage.output_tokens` — token
  accounting.
- `modelUsage` — per-model breakdown (only present if the
  task used more than one model, e.g. `--fallback-model`
  kicked in).

The reference parser at
`scripts/parse_claude_output.py` extracts this shape. Like
the Cline parser, the wrapper owns nothing — if Claude
Code's output schema changes, you patch the parser, not
every wrapper.

## Token accounting caveat

`usage.input_tokens + output_tokens` is the *total tokens
Claude Code sent/received in the API*, including cached
reads. The actual cost is in `total_cost_usd` — use that
for budget-aware loss functions. `usage.cache_read_input_tokens`
is the prompt cache hit count; high values are a good sign
(the prompt is being reused across cycles, so
`--append-system-prompt` is doing its job).

## Smoke test

The minimal smoke test:

```bash
claude --print --output-format json --bare \
  --max-turns 1 \
  "Respond with exactly: CLAUDE_CODE_SMOKE_OK"
```

Expected: JSON object on stdout with `"result": "CLAUDE_CODE_SMOKE_OK"`
(or similar). Exit code 0.

If the JSON does not parse, Claude Code likely isn't
authenticated — run `claude auth status` and check
`ANTHROPIC_API_KEY` is set.

## Drop-in substitution

This skill is a sibling of `cline-orchestration`. The
harness-scaffold and loop-driver skills are
**runtime-agnostic**. They invoke whatever wrapper is at
`verifiers/<runtime>-wrapper.sh`. The user passes
`--runtime {cline,claude-code,codex,hermes-agent,opencode}`
to `harness-scaffold` to generate the correct wrapper.

The 4 invariants from `compatibility.md` hold here:

1. `parse_claude_output.py` emits JSON in the same shape as
   `parse_cline_output.py`.
2. The wrapper accepts a positional `TASK` plus
   `--cwd PATH`, `--timeout N`, `--cycle NAME` and writes
   the parsed JSON to stdout.
3. The `claude-code-skills-dir.sh` instrument prints the
   agent's skills directory to stdout.
4. The wrapper exits non-zero on missing binary / bad
   args, exits 0 on successful agent run, never blocks
   longer than `--timeout`.

## Common pitfalls

1. **Forgetting `--print`.** Without it Claude Code starts
   the interactive REPL and the wrapper hangs. Always
   pass `-p` / `--print`.
2. **Not setting `--max-turns`.** Print mode without a
   turn cap is a runaway risk. Default to 30; lower for
   tight cycles.
3. **Forgetting `--allowedTools`.** Without it Claude
   Code uses the default tool set, which can include
   things the cycle shouldn't touch (e.g. WebFetch on
   a cycle that should be local-only).
4. **Assuming `--bare` is a no-op.** `--bare` skips OAuth
   in some configurations and **requires**
   `ANTHROPIC_API_KEY`. If you set `--bare` and rely on
   OAuth, the loop will fail with a confusing auth error.
   Use OAuth mode without `--bare`, or set
   `ANTHROPIC_API_KEY` with `--bare`.
5. **Parsing `text` output.** The default
   `--output-format text` is prose, not JSON. The wrapper
   must pass `--output-format json` (or stream-json).
6. **Ignoring `subtype`.** `subtype == "error_max_turns"`
   is a real failure even if the assistant text looks
   reasonable. The wrapper's `finish_reason` should map
   these to the right sub-loss gates.
7. **Setting `--model` in the wrapper.** Don't. The user
   picks the model via `claude auth status` /
   `--model sonnet|opus|haiku`. The loop's drift
   sub-loss catches unwanted model drift.

## Verification checklist

- [ ] Wrapper resolves `claude` via `$CLAUDE_BIN` →
      `command -v claude` → bail.
- [ ] Wrapper uses `--print` and `--output-format json`.
- [ ] Wrapper passes `--max-turns` and `--allowedTools`.
- [ ] Wrapper writes parsed JSON to stdout, not the
      transcript.
- [ ] Wrapper exits non-zero on missing binary, zero on
      successful agent run.
- [ ] Wrapper is wrapped in `timeout` and kills Claude
      Code if it overruns.
- [ ] `claude-code-skills-dir.sh` prints the user's
      `~/.claude/skills/` path (or the project-local
      `.claude/skills/`).
- [ ] No absolute paths, no per-user config baked in.
