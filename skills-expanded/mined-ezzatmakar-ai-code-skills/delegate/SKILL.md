---
name: delegate
description: Hand a task to a different model's CLI — Codex, OpenCode, Claude Code, Cursor, Gemini, or Aider — headlessly, then capture and summarize its answer. Use when you explicitly name a target — "delegate this to codex", "ask opencode to explain this file", "run this with cursor", "get a second opinion from claude", "have aider make this change" — to build a non-interactive invocation, confirm it, execute it (read-only by default; edit mode only on request), and report the result. Honors model, mode, timeout, and JSON output. Not a router: you must name the target; it never picks or substitutes a model for you.
license: MIT
compatibility: Model-agnostic; runs from Claude Code, Codex, or OpenCode. Plain bash — resolves targets by $DELEGATE_<TOOL>_BIN, PATH, or known install paths (codex is often off-PATH inside ChatGPT.app; gemini may be absent). Degrades gracefully when a target or `timeout`/`gtimeout`/`jq` is missing. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Delegate to another model's CLI

Delegate a single task to a **named** model CLI — Codex, OpenCode, Claude Code, Cursor, Gemini, or
Aider — run it **headlessly**, and bring the result back. This skill is an **explicit dispatcher**: the user names
the target; it never routes, guesses, or substitutes a model. It **defaults to read-only**, and it
**always confirms the exact command before executing**, because delegating spends the target's credits
and — in edit mode — can modify files.

Two helpers do the mechanical work; resolve `<skill-directory>` from the loaded skill path:

- `<skill-directory>/scripts/detect-clis.sh` — which targets are installed and how to invoke each.
- `<skill-directory>/scripts/delegate.sh` — build, preview (`--dry-run`), and run one delegation.

Read [references/TARGETS.md](references/TARGETS.md) for the per-tool adapter matrix (flags, model syntax,
output capture, the codex off-PATH gotcha, gemini-absent handling, and cost notes).

## Non-negotiable output

- **Name the target or stop.** This is not a router. If the user did not name a target, ask which one;
  never choose or substitute a model. If the named target is not installed, stop and report how to
  install it — do not fall back to another CLI.
- **Read-only by default.** Only pass `--mode edit` when the user explicitly asked to allow changes, and
  only after they confirm. Never enable a tool's dangerous bypass flag (`danger-full-access`,
  `--dangerously-*`).
- **Confirm before executing.** Always show the resolved command (via `--dry-run`), the mode, the model,
  the working directory, and that it will spend the target's credits — then get explicit confirmation.
- **Warn on self-delegation.** Delegating to the CLI you are already running in spawns a fresh nested
  session (extra cost, loop risk). Call it out and confirm before proceeding; never chain it.
- **Never put secrets in the prompt.** It is sent verbatim to a third-party CLI on its own billing.
- **Report faithfully.** State the target, model, mode, exit code, and whether output was truncated by a
  timeout. Do not claim success on a non-zero exit. After an edit-mode run, tell the user to review the
  working tree.

## Phase 0: Resolve inputs

Determine these before doing anything, then echo them back:

1. **Target** (required, explicit): one of `codex`, `opencode`, `claude`, `cursor`, `gemini`, `aider`. If
   missing, ask — do not guess.
2. **Prompt**: the task to delegate. Prefer passing it to `delegate.sh` via `--stdin` and a quoted
   heredoc (quote-proof for multi-line prompts with backticks, quotes, or `$`).
3. **Model** (`--model`, optional): pass through to the target. Use `delegate.sh --to <target>
   --list-models` to discover options when the user is unsure.
4. **Mode** (`--mode`, default **read-only**): `edit` only when the user explicitly wants the delegate to
   change files.
5. **Timeout** (`--timeout`, default 600s; `0` disables), **JSON** (`--json`, only if structured output
   is wanted), and **working dir** (`--cwd`, default the current directory).
6. Whether to **save** the delegate's output to a file (optional) or just summarize it in chat.

## Phase 1: Check availability

Run `<skill-directory>/scripts/detect-clis.sh`. Confirm the target is installed and note its resolved
binary path (codex is commonly resolved from inside ChatGPT.app). If the target is not installed, stop
and give the install hint from the table. Do not substitute another model.

## Phase 2: Self-delegation and safety check

If the target is the same CLI you are currently running in (Claude Code → `claude`, Codex → `codex`,
OpenCode → `opencode`), warn that this spawns a fresh nested session with extra cost and loop risk, and
get explicit confirmation. If `--mode edit`, state plainly that the run may modify files and spend
credits.

## Phase 3: Build and confirm (the gate)

Run `delegate.sh` with `--dry-run` to get the exact resolved command. Present to the user: target,
binary, model, mode, working directory, timeout, and the command itself. **Require explicit confirmation
before executing** — especially for `--mode edit` and for self-delegation. Never run on the user's behalf
without it.

```bash
<skill-directory>/scripts/delegate.sh --to <target> [--model M] [--mode read-only|edit] \
  [--json] [--cwd DIR] --dry-run --stdin <<'PROMPT'
<the task>
PROMPT
```

## Phase 4: Execute and capture

After confirmation, re-run the same command **without** `--dry-run`. Capture stdout and the exit code.
`delegate.sh` returns the target's own exit code (or `124` on timeout, `3` if the target vanished). On
failure or timeout, report the error and any partial output — do not silently retry.

A real delegation often runs for **minutes**. If you are invoking `delegate.sh` from a host whose shell
has a short foreground timeout (e.g. an agent Bash tool that caps at ~120s), run it in the **background**
and poll for completion — a foreground shell will otherwise kill the delegate mid-task. Bound the run
with `delegate.sh`'s own `--timeout` rather than relying on the caller's shell limit.

## Phase 5: Summarize back

Present a concise, host-neutral summary: which target and model ran, the mode, the exit status and
duration, then the delegate's final answer (and the raw output or a saved-file path if the user asked
for it). Note explicitly if output was truncated by a timeout. If the run was in edit mode, remind the
user to review the working tree (e.g. `git status` / `git diff`) — this skill does not review or apply
the delegate's changes for you.
