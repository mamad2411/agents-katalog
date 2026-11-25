---
name: hermes-agent-orchestration
description: |
  How to drive the Hermes Agent CLI (Nous Research) as the
  coding agent inside a loss-function-driven loop. The
  driver (Hermes or any orchestrator) owns the outer loop,
  the loss function, and the verifier runs. The inner
  Hermes session owns the model call, the per-iteration
  context, the file edits, and the test runs. Load this
  skill whenever launching a nested Hermes chat as the
  inner agent, and when building a Hermes wrapper script
  — the verified chat-mode flags, the JSON output shape,
  the parser, and the contract the wrapper must satisfy
  all live here.
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, hermes-agent, nous-research, agent-orchestration, coding-agents]
    related_skills: [cline-orchestration, claude-code-orchestration, codex-orchestration, opencode-orchestration, harness-engineering, loss-function-design]
---

# Hermes Agent Orchestration

This skill describes how to drive **Hermes Agent** (Nous
Research) as the coding agent inside a
loss-function-driven loop. The pattern is
**agent-agnostic at the driver level** — Hermes itself
is the driver in the reference build, but any orchestrator
(a shell script, CI runner, another agent) that can spawn
a subprocess and read JSON can use the same wrapper
contract.

> **Use case:** when the *outer* orchestrator (some other
> process) wants a *nested* Hermes session to act as the
> inner coding agent. If the outer loop *is* Hermes, this
> skill is still useful for understanding what
> `delegate_task` (background subagent) and
> `terminal(hermes chat -q …)` produce on stdout — but you
> don't need a wrapper script for the in-process case.

The split:

- **The outer driver owns:** the loop, the loss function,
  the verifier runs, the human-facing surface, the stop
  criterion, the budget.
- **The inner Hermes session owns:** the model call, the
  tool surface, the per-iteration context, the file edits,
  the test runs.

## Why Hermes-as-inner-agent

- **Provider-agnostic.** Hermes supports 20+ providers
  (OpenRouter, Anthropic, OpenAI, Gemini, DeepSeek, xAI,
  local models, Nous Portal OAuth, etc.). The driver
  never sets the model — Hermes's own config does.
- Native tool surface (file, terminal, browser, web
  search, vision, image-gen, MCP, custom tools).
- `hermes chat -q "<task>"` for non-interactive one-shots
  with `--output-format json` for parseable results.
- Skills are first-class — the loop's candidate skill
  is just a markdown file the inner session picks up
  automatically.
- `--worktree` mode gives the inner session an isolated
  git worktree (the equivalent of Cline's `--worktree`,
  but it carries auth because the Hermes daemon owns the
  credential pool).

## Locating the `hermes` binary

The wrapper resolves the binary at call time. The resolution
order is:

1. The `$HERMES_BIN` environment variable, if set.
2. `$(command -v hermes)` — whatever's on `PATH`.
3. Bail with exit code 3 and a clear error.

Same pattern as the other wrappers. **Do not hardcode an
absolute path** in the wrapper.

## Working invocation (chat mode, JSON output)

```bash
"$HERMES_BIN" chat \
  --query "$TASK" \
  --output-format json \
  --cwd "$ITER_DIR" \
  --max-turns "$MAX_TURNS" \
  --profile "$HERMES_PROFILE" \
  --toolsets "$TOOLSETS" \
  --source lfd-loop \
  --no-session-persistence \
  > "$RAW_OUT" 2>"$STDERR_FILE"
```

Where:

- `--query` is the cycle prompt (note: Hermes uses
  `--query` not a positional arg).
- `--output-format json` makes the result parseable.
  Default is human prose.
- `--cwd` sets the inner session's working directory.
  Per-cycle isolation.
- `--max-turns` caps the agentic loop.
- `--profile` selects a named Hermes profile (e.g.
  `lfd-coder` — a stripped-down profile with only the
  tools a cycle needs). Default to the active profile.
- `--toolsets` whitelists toolsets for this session.
  Comma-separated. Default: `terminal,file`. Add others
  (e.g. `browser`, `web`) only when the cycle needs them.
- `--no-session-persistence` skips writing the session
  to disk. Recommended for loops (no session bloat).

## What we tried and what broke

| Flag                              | Result                                                                  |
|-----------------------------------|-------------------------------------------------------------------------|
| `hermes -p "..."`                 | `-p` is not a Hermes flag. The one-shot entry point is `hermes chat --query ...`. |
| `hermes chat "..."` (positional)  | Hermes CLI expects `--query` for chat mode. The positional form is for the interactive REPL. |
| `hermes chat --query "..."` (no `--output-format json`) | The transcript is human prose. The wrapper's parser needs `--output-format json`. |
| `hermes chat --query "..." --worktree` | Creates an isolated worktree — **fine, and the worktree carries auth** (Hermes owns the credentials). Use when you want stronger isolation than `--cwd`. |
| `hermes chat --query "..." --skills "codex,coder"` | The `--skills` flag preloads skills into the session. The loop-driver doesn't set this; the loop's *candidate* skill is installed at `~/.hermes/profiles/<active>/skills/` and loaded automatically. |
| `hermes chat --query "..." --yolo` | Skip the manual command approval prompts. Required for non-interactive loops unless the cycle is on the `auto-approve` allowlist. |
| `hermes chat --query "..." --model gpt-5` | Don't set `--model` in the wrapper. The user picks the model via `hermes model` or `hermes config set model.default`. |
| `hermes chat --query "..." --provider openai` | Same — the user picks the provider. The loop's drift sub-loss catches unwanted drift. |
| `hermes --bare` (no such flag) | Hermes has no `--bare` mode. Use `--toolsets ""` to disable built-in tools and `--no-session-persistence` to skip session writes. |

## The right pattern

- **`hermes chat --query ...` is mandatory** for
  non-interactive work. The interactive REPL is for
  human-driven exploration.
- **`--output-format json` is mandatory** for the
  wrapper to parse results. Without it the output is
  human prose.
- **`--yolo` (or `approvals.mode: off` in config) is
  required for non-interactive loops.** Without it the
  inner session prompts for approval on shell commands
  and hangs.
- **`--toolsets "terminal,file"` is the minimal
  whitelist** for most code-editing cycles. Add
  `browser` or `web` only when the cycle needs them.
- **`--no-session-persistence` is recommended** for
  loops. Without it the session DB grows by one entry
  per cycle, which is wasteful and pollutes
  `session_search`.
- **Provider config is sacred.** Hermes picks the model
  from its own config (`hermes config set model.default`).
  The wrapper must NEVER pass `--model` / `--provider`
  unless you are specifically testing model drift.
- **Per-cycle isolation** comes from `--cwd $ITER_DIR`.
  Use `--worktree` when you want stronger isolation
  (the inner session gets a fresh git worktree at
  `.hermes-worktrees/<name>/` and the worktree carries
  auth).

## Output schema (verified)

`hermes chat --output-format json` emits a JSON object
on stdout when the task finishes. The schema:

```json
{
  "result": "<final assistant text>",
  "session_id": "20260225_143052_a1b2c3",
  "turns": 3,
  "duration_ms": 10276,
  "usage": {
    "input_tokens": 5,
    "output_tokens": 603,
    "cache_read_tokens": 0,
    "cost_usd": 0.0787
  },
  "model": "anthropic/claude-sonnet-4",
  "provider": "openrouter",
  "finish_reason": "completed"
}
```

Key fields for the loop:

- `result` — the final assistant text. Equivalent to
  Cline's `run_result.text`. The loop's `candidate_text`.
- `session_id` — Hermes session ID. Useful for
  debugging failed cycles.
- `turns` — agentic loop count. Maps to Cline's
  `iterations`.
- `duration_ms` — wall-clock duration.
- `usage` — token + cost accounting.
- `model` / `provider` — what's actually being used.
- `finish_reason` — `"completed" | "max_turns" | "user_cancelled" | "error"`.

The reference parser at
`scripts/parse_hermes_output.py` extracts this shape. As
with the other adapters, if Hermes's output schema
changes, edit the parser, not every wrapper.

## Token accounting caveat

`usage.input_tokens + output_tokens + cache_read_tokens`
is the *total tokens Hermes sent/received in the API*,
including cache hits. The cost is in `usage.cost_usd`
when the provider supports cost reporting; otherwise the
loop's `cost` sub-loss is graded 0.0 (no cost data
available).

## Smoke test

The minimal smoke test:

```bash
hermes chat --query "Respond with exactly: HERMES_SMOKE_OK" \
  --output-format json --no-session-persistence
```

Expected: JSON object on stdout with `"result": "HERMES_SMOKE_OK"`
(or similar). Exit code 0.

If the JSON does not parse, Hermes likely isn't
authenticated — run `hermes auth status` and check
`config.yaml`.

## Drop-in substitution

This skill is a sibling of `cline-orchestration`,
`claude-code-orchestration`, `codex-orchestration`, and
`opencode-orchestration`. The harness-scaffold and
loop-driver skills are **runtime-agnostic**. They invoke
whatever wrapper is at `verifiers/<runtime>-wrapper.sh`.
The user passes `--runtime {cline,claude-code,codex,hermes-agent,opencode}`
to `harness-scaffold` to generate the correct wrapper.

The 4 invariants from `compatibility.md` hold here:

1. `parse_hermes_output.py` emits JSON in the same shape
   as `parse_cline_output.py`.
2. The wrapper accepts a positional `TASK` plus
   `--cwd PATH`, `--timeout N`, `--cycle NAME` and writes
   the parsed JSON to stdout.
3. The `hermes-agent-skills-dir.sh` instrument prints the
   agent's skills directory to stdout.
4. The wrapper exits non-zero on missing binary / bad
   args, exits 0 on successful agent run, never blocks
   longer than `--timeout`.

## Common pitfalls

1. **Forgetting `--yolo` / `approvals.mode: off`.** The
   inner session prompts for approval on shell commands
   and hangs the loop. Either pass `--yolo` on every
   invocation, or set `approvals.mode: off` in the
   profile config.
2. **Forgetting `--output-format json`.** Without it the
   output is human prose, unparseable.
3. **Setting `--model` in the wrapper.** Don't. The user
   picks the model via `hermes model`. The loop's drift
   sub-loss catches unwanted drift.
4. **Running the interactive REPL.** The REPL requires
   `pty=true`; `hermes chat -q` does NOT need pty. Use
   the chat command.
5. **Forgetting `--no-session-persistence`.** The session
   DB grows by one entry per cycle, which is wasteful.
6. **Confusing the wrapper with `delegate_task`.** If the
   outer loop *is* Hermes, you don't need a wrapper
   script — use `delegate_task` (in-process) or
   `terminal(hermes chat -q …)` (out-of-process). This
   skill is for the case where Hermes is the inner agent
   and the outer driver is something else (a shell
   script, CI runner, another coding agent, etc.).

## Verification checklist

- [ ] Wrapper resolves `hermes` via `$HERMES_BIN` →
      `command -v hermes` → bail.
- [ ] Wrapper uses `hermes chat --query ...` and
      `--output-format json`.
- [ ] Wrapper passes `--yolo` (or relies on profile
      config for approvals.mode: off).
- [ ] Wrapper passes `--max-turns` and `--toolsets`.
- [ ] Wrapper writes parsed JSON to stdout, not the
      transcript.
- [ ] Wrapper exits non-zero on missing binary, zero on
      successful agent run.
- [ ] Wrapper is wrapped in `timeout` and kills Hermes
      if it overruns.
- [ ] `hermes-agent-skills-dir.sh` prints the active
      profile's `skills/` path.
- [ ] No absolute paths, no per-user config baked in.
