---
name: copilot-subagent
description: Run GitHub Copilot CLI as a subagent for code tasks, validation, review, and implementation. Works with enterprise Copilot subscriptions. Multi-model access including Claude, GPT, and Gemini.
---

# GitHub Copilot CLI Subagent

Run GitHub Copilot CLI as a subagent for code-related tasks.

## When to Use

- **Implementation** — code changes, bug fixes, feature work
- **Validation** — second opinion on specs, code, architecture
- **Code review** — structured review in a fresh Copilot session
- **Parallel work** — fan out independent tasks across multiple agents
- **Enterprise environments** — Copilot may be the only approved AI coding tool
- **Multi-model access** — switch between Claude, GPT, Gemini via one CLI

Avoid for:
- Tiny tasks faster to do inline
- Work requiring tight back-and-forth in a single context

## Prerequisites

- `copilot` CLI installed (`npm install -g @github/copilot@latest`)
- Authenticated (`copilot login`)
- Working directory must be a git repo (or use `--allow-all-paths`)
- If not installed globally, use `--npx` flag on `copilot-result` commands

## Current Config Defaults (~/.copilot/config.json)

These are already set — no need to pass flags for default behavior:

| Setting | Value |
|---------|-------|
| Model | `gpt-5.4` |
| Reasoning effort | `high` |

Override model with `--model <name>`. No flag exists for reasoning effort — it's config-only.

## Output Strategy (Tiered)

**Always use `copilot-result` for extraction. Only pull what you need into context.**

Copilot stores structured JSONL in `~/.copilot/session-state/<id>/events.jsonl` for every session. The `copilot-result` helper extracts specific fields so you don't blow out the driving agent's context.

## Tool Profile Defaults

`copilot-result exec` now applies a Codex-like constrained tool profile by default:

- `--disable-builtin-mcps`
- `--available-tools report_intent bash apply_patch view rg glob`

Use `--raw-tools` to disable this and run with Copilot's default full tool surface.

### Tier 1 — Last message only (default, ~90% of tasks)

```bash
copilot-result exec "prompt" --allow-all 2>/dev/null
```

Or capture to file for later:

```bash
copilot-result exec "prompt" --allow-all > /tmp/copilot-out.txt 2>/dev/null
cat /tmp/copilot-out.txt
```

### Tier 2 — All agent messages (when final message needs context)

```bash
copilot-result messages
```

### Tier 3 — Inspect specific details on demand

```bash
copilot-result session-id             # Latest session ID (convenience)
copilot-result tools                  # Tool calls with names and arguments
copilot-result reasoning              # Thinking summaries
copilot-result summary                # Session ID + model + last message
```

All extraction commands can target a specific session ID:

```bash
copilot-result last <session-id>
copilot-result tools <session-id>
```

For automated callers, prefer `copilot-result --json exec ...` and carry the returned `session_id`
forward explicitly. Treat `copilot-result session-id` as a convenience for human workflows.

### Automation Note

For machine-readable workflows, the safest pattern is to redirect `--json exec` output to a file and
then read fields with `jq`. Tool-using Copilot sessions can still emit PTY-dependent progress noise in
some caller setups, and file redirect remains the most reliable pattern.

```bash
# Safe pattern
copilot-result --json exec "prompt" --allow-all > /tmp/copilot-result.json 2>/dev/null
SID="$(jq -r '.session_id' /tmp/copilot-result.json)"
RESULT="$(jq -r '.result' /tmp/copilot-result.json)"

# Less reliable for tool-using sessions in PTY-heavy wrappers
json="$(copilot-result --json exec 'prompt' --allow-all 2>/dev/null)"
```

### Extraction Helper

Use `~/.claude/skills/copilot-subagent/scripts/copilot-result` for all operations:

```bash
copilot-result exec "prompt" --allow-all   # Run copilot (Tier 1)
copilot-result --json exec "prompt" --allow-all  # Normalized machine-readable result
copilot-result --raw-tools exec "prompt" --allow-all   # Full/default Copilot tools
copilot-result last [session-id]           # Last agent message
copilot-result messages [session-id]       # All agent messages
copilot-result session-id                  # Latest session ID (convenience)
copilot-result tools [session-id]          # Tool calls + arguments
copilot-result reasoning [session-id]      # Thinking summaries
copilot-result summary [session-id]        # Session ID + model + last message
```

## Execution Patterns

### 1) Synchronous (blocking, result inline)

```bash
cd /path/to/project && copilot-result exec "your prompt" --allow-all 2>/dev/null
```

Response goes to stdout. Session JSONL saved automatically for later extraction.

### 2) Asynchronous (background, poll later)

If you're calling this from an outer Bash tool that already supports `run_in_background`, do not also add shell `&`.
Use one backgrounding mechanism, not both.

```bash
cd /path/to/project && copilot-result exec "your prompt" --allow-all > /tmp/copilot-async.txt 2>/dev/null &
echo "PID=$!"
```

Check completion and retrieve result:

```bash
# Is it done?
jobs -l

# Get result when done
cat /tmp/copilot-async.txt

# Or extract from session JSONL
copilot-result last
```

### 3) Parallel (multiple simultaneous agents)

```bash
cd /path/to/project
copilot-result exec "task A" --allow-all > /tmp/copilot-a.txt 2>/dev/null &
PID_A=$!
copilot-result exec "task B" --allow-all > /tmp/copilot-b.txt 2>/dev/null &
PID_B=$!
wait $PID_A $PID_B

# Harvest results
cat /tmp/copilot-a.txt
cat /tmp/copilot-b.txt
```

### 4) Resume (continue a prior session)

Resume works in non-interactive mode. Use `copilot-result exec` so default tool constraints still apply.
For automation, prefer an explicit session ID captured from `copilot-result --json exec ...`:

```bash
cd /path/to/project && copilot-result exec "follow-up prompt" --resume <session-id> --allow-all 2>/dev/null
```

Resume the most recent session:

```bash
cd /path/to/project && copilot-result exec "follow-up prompt" --resume $(copilot-result session-id) --allow-all 2>/dev/null
```

Resume a specific session:

```bash
copilot-result exec "follow-up prompt" --resume <session-id> --allow-all 2>/dev/null
```

Get the session ID from a previous run:

```bash
copilot-result session-id
```

## Permission Levels

### Full access (default for subagent use)

```bash
--allow-all    # or --yolo — enables tools + paths + URLs
```

### Read-only (analysis, review, validation)

```bash
--allow-tool read --allow-tool 'shell(cat)' --allow-tool 'shell(grep)'
```

### Write files, no shell

```bash
--allow-tool read --allow-tool write
```

### Git but no push

```bash
--allow-tool 'shell(git:*)' --deny-tool 'shell(git push)'
```

### Permission syntax

| Pattern | Matches |
|---------|---------|
| `shell(command)` | Specific shell command |
| `shell(git:*)` | All git subcommands |
| `write` | File creation/modification |
| `read` | File reading |
| `MCPServer(tool)` | Specific MCP server tool |

## Models

Available via `--model`:

### Primary models (high reasoning configured by default)

| Model | Use case |
|-------|----------|
| `gpt-5.4` | **Default on this machine.** Strongest general coding performance in current tests |
| `gpt-5.2` | General, strong. Good for non-code tasks |

### All available models

| Model | Strengths |
|-------|-----------|
| `claude-opus-4.6` | Most capable Claude |
| `claude-sonnet-4.6` | Balanced Claude |
| `claude-sonnet-4.5` | Previous gen Claude |
| `claude-haiku-4.5` | Fast, cheap Claude |
| `gpt-5.4` | Current default on this machine |
| `gpt-5.3-codex` | Code-optimized |
| `gpt-5.2-codex` | Code-optimized |
| `gpt-5.2` | General |
| `gpt-5.1-codex-max` | Maximum reasoning |
| `gpt-5.1-codex` | Code-optimized |
| `gpt-5.1` | General |
| `gpt-5.1-codex-mini` | Fast, cheap |
| `gpt-5-mini` | Fast, cheap |
| `gpt-4.1` | Legacy, stable |
| `gemini-3-pro-preview` | Google, 1M context |

### Overriding the default model

```bash
copilot-result exec "prompt" --model gpt-5.2 --allow-all
copilot-result exec "prompt" --model claude-opus-4.6 --allow-all
```

## Content Passing

### Inline prompt (simple)

```bash
copilot-result exec "your prompt here" --allow-all
```

### Heredoc (complex/multi-line prompts)

```bash
copilot-result exec "$(cat <<'EOF'
Task: Review authentication module
Scope: src/auth/
Constraints: No changes, analysis only

Report issues with severity [P1], [P2], [P3].
EOF
)" --allow-all
```

### File reference (preferred for code tasks)

Let Copilot read files itself — it has filesystem access:

```bash
copilot-result exec "Read src/auth/login.ts and identify security issues" --allow-all
```

## Portable Invocation (--npx)

If `copilot` is not installed globally, use `--npx` to run via `npx`:

```bash
copilot-result --npx exec "your prompt" --allow-all
```

This runs `npx -y @github/copilot` under the hood. Useful on machines where you've authenticated with Copilot but haven't installed the CLI globally.

If you run `copilot-result exec` without `--npx` and `copilot` is not found, the script will tell you:

```
Error: copilot CLI not found.
Install:  npm install -g @github/copilot@latest
Or use:   copilot-result --npx exec "your prompt"
```

## Session Storage

Copilot persists sessions at `~/.copilot/session-state/<session-id>/`. Each session contains:

| File | Contents |
|------|----------|
| `events.jsonl` | Structured event log (messages, tool calls, reasoning) |
| `workspace.yaml` | Session metadata (ID, cwd, git info, timestamps) |
| `checkpoints/` | Session state checkpoints |

### JSONL Event Types Reference

| Event | Key Fields | Use |
|-------|-----------|-----|
| `session.start` | `.data.sessionId`, `.data.context` | Session ID, git context |
| `session.model_change` | `.data.newModel` | Model used |
| `user.message` | `.data.content` | User input |
| `assistant.message` | `.data.content`, `.data.reasoningText`, `.data.toolRequests` | Response + thinking |
| `tool.execution_start` | `.data.toolName`, `.data.arguments` | Tool call |
| `tool.execution_complete` | `.data.success`, `.data.result` | Tool result |
| `assistant.turn_start/end` | `.data.turnId` | Turn boundaries |

## Prompt Discipline

- One goal per agent. Narrow scope = better results.
- Provide exact file paths when possible, not "look through the codebase."
- For structured output, specify the format in the prompt.
- Keep prompts concise — gpt-5.4 at high reasoning doesn't need hand-holding.

## Quick Reference

| Need | Command |
|------|---------|
| Sync exec | `copilot-result exec "prompt" --allow-all 2>/dev/null` |
| Sync exec (full tools) | `copilot-result --raw-tools exec "prompt" --allow-all 2>/dev/null` |
| Async exec | `copilot-result exec "prompt" --allow-all > out.txt 2>/dev/null &` |
| Resume session | `copilot-result exec "prompt" --resume <ID> --allow-all 2>/dev/null` |
| Resume latest | `copilot-result exec "prompt" --resume $(copilot-result session-id) --allow-all` |
| Extract last msg | `copilot-result last` |
| Extract session ID | `copilot-result session-id` |
| Different model | `--model gpt-5.2` |
| Read-only | `--allow-tool read` |
| Portable (no install) | `copilot-result --npx exec "prompt" --allow-all` |
