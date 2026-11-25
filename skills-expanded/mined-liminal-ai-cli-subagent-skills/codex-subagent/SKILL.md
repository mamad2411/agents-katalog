---
name: codex-subagent
description: Run OpenAI Codex CLI as a subagent for code tasks, review, validation, and implementation. Supports sync, async, parallel, and resume workflows with tiered output management.
---

# Codex CLI Subagent

Run Codex CLI (`codex exec`) as a subagent for code-related tasks.

## When to Use

- **Implementation** — code changes, bug fixes, feature work
- **Code review** — give Codex a review prompt via `codex exec`
- **Validation** — second opinion on specs, code, architecture
- **Parallel work** — fan out independent tasks across multiple agents
- **Large context tasks** — offload work that benefits from Codex's reasoning

Avoid for:
- Tiny tasks faster to do inline
- Work requiring tight back-and-forth in a single context

## Prerequisites

- `codex` CLI installed (`codex-cli v0.104.0+`)
- Authenticated (`codex login`)
- Working directory must be a git repo (or use `--skip-git-repo-check`)

## Current Config Defaults (~/.codex/config.toml)

These are already set — no need to pass flags for default behavior:

| Setting | Value |
|---------|-------|
| Model | `gpt-5.4` |
| Reasoning effort | `high` |
| Service tier | `fast` |
| Sandbox | `danger-full-access` |
| Web search | `live` |
| Multi-agent | `true` |

Plain `codex exec` inherits these defaults automatically unless a command explicitly overrides them.

Override any default with `-c key=value` (e.g., `-c model_reasoning_effort=medium`, `-c service_tier=flex`).

## Output Strategy (Tiered)

**Always write full JSONL to a file. Only read into context what you need.**

Use `--json` on every exec. It sends structured JSONL to stdout, works for exec and resume.

### Tier 1 — Last message only (default, ~90% of tasks)

```bash
cd /path/to/project && codex exec --json "prompt" > /tmp/codex-out.jsonl 2>/dev/null
codex-result last /tmp/codex-out.jsonl
```

### Tier 2 — All agent messages (when final message needs context)

```bash
codex-result messages /tmp/codex-out.jsonl
```

### Tier 3 — Inspect specific details on demand

```bash
codex-result session-id /tmp/codex-out.jsonl   # Thread ID for resume
codex-result usage /tmp/codex-out.jsonl         # Token counts
codex-result commands /tmp/codex-out.jsonl      # Commands + exit codes + output
codex-result reasoning /tmp/codex-out.jsonl     # Thinking summaries (often empty with current CLI builds)
codex-result summary /tmp/codex-out.jsonl       # Session ID + tokens + last message
```

### Extraction Helper

Use `~/.claude/skills/codex-subagent/scripts/codex-result` for quick extraction:

```bash
codex-result last /tmp/codex-out.jsonl      # Last agent message (default)
codex-result messages /tmp/codex-out.jsonl   # All agent messages
codex-result session-id /tmp/codex-out.jsonl # Thread/session ID
codex-result usage /tmp/codex-out.jsonl      # Token counts
codex-result commands /tmp/codex-out.jsonl   # Commands + exit codes
codex-result summary /tmp/codex-out.jsonl    # Session ID + usage + last message
```

## Execution Patterns

### 1) Synchronous (blocking, result inline)

```bash
cd /path/to/project && codex exec --json "your prompt" > /tmp/codex-out.jsonl 2>/dev/null
codex-result last /tmp/codex-out.jsonl
```

Full JSONL saved to file, only last message enters context.

### 2) Asynchronous (background, poll later)

**IMPORTANT: Do NOT combine `&` (shell backgrounding) with `run_in_background` on the Bash tool.
When the Bash tool backgrounds a command, the outer shell exits immediately — any `&`-backgrounded
child process gets orphaned/killed before it finishes. Use ONE backgrounding mechanism, not both.**

**Option A — Use Bash tool's `run_in_background` (preferred):**
Run codex synchronously inside the command. The Bash tool handles backgrounding.

```bash
cd /path/to/project && codex exec --json "your prompt" > /tmp/codex-async.jsonl 2>/dev/null
```

Set `run_in_background: true` on the Bash tool call. Poll or wait for the task notification.

**Option B — Use shell `&` (only when shell stays alive):**
Only works inside a single Bash call where `wait` keeps the shell alive.

```bash
cd /path/to/project && codex exec --json "your prompt" > /tmp/codex-async.jsonl 2>/dev/null &
PID=$!
wait $PID
```

Check completion and retrieve result:

```bash
codex-result last /tmp/codex-async.jsonl
```

### 3) Parallel (multiple simultaneous agents)

**To run multiple agents in parallel, use separate Bash tool calls each with `run_in_background: true`.**
Do NOT use `&` inside the commands. Each Bash call runs one codex synchronously; the Bash tool
handles parallelism.

```bash
# Call 1 (run_in_background: true)
cd /path/to/project && codex exec --json "task A" > /tmp/codex-a.jsonl 2>/dev/null

# Call 2 (run_in_background: true)
cd /path/to/project && codex exec --json "task B" > /tmp/codex-b.jsonl 2>/dev/null
```

Harvest results after both complete:

```bash
codex-result last /tmp/codex-a.jsonl
codex-result last /tmp/codex-b.jsonl
```

**Alternative — Single shell with `wait` (keeps shell alive):**

```bash
cd /path/to/project
codex exec --json "task A" > /tmp/codex-a.jsonl 2>/dev/null &
PID_A=$!
codex exec --json "task B" > /tmp/codex-b.jsonl 2>/dev/null &
PID_B=$!
wait $PID_A $PID_B

# Harvest results
codex-result last /tmp/codex-a.jsonl
codex-result last /tmp/codex-b.jsonl
```

### 4) Resume (continue a prior session)

**Important:** `exec resume` does not support `-C`. You must `cd` to the project directory first.

```bash
cd /path/to/project && codex exec resume --json <SESSION_ID> "follow-up prompt" > /tmp/codex-resume.jsonl 2>/dev/null
codex-result last /tmp/codex-resume.jsonl
```

Resume the most recent session:

```bash
cd /path/to/project && codex exec resume --json --last "follow-up prompt" > /tmp/codex-resume.jsonl 2>/dev/null
codex-result last /tmp/codex-resume.jsonl
```

Get the session ID from a previous run:

```bash
codex-result session-id /tmp/codex-out.jsonl
```

## Overriding Defaults

Only pass flags when you need something different from config.toml defaults.

```bash
# Different model
codex exec --json -m o3 "prompt"

# Lower reasoning effort (faster, cheaper)
codex exec --json -c model_reasoning_effort=medium "prompt"

# Disable fast tier for a run
codex exec --json -c service_tier=flex "prompt"

# Read-only sandbox (safe for untrusted repos)
codex exec --json -s read-only "prompt"

# Workspace-write sandbox (implementation without full access)
codex exec --json -s workspace-write "prompt"

# Full auto convenience flag (workspace-write + on-request approval)
codex exec --json --full-auto "prompt"

# With web search explicitly enabled
codex exec --json --search "prompt"

# Additional writable directories
codex exec --json --add-dir /other/dir "prompt"

# With image input
codex exec --json -i screenshot.png "What's wrong with this UI?"
```

## Content Passing

### Inline prompt (simple)

```bash
codex exec --json "your prompt here"
```

### Heredoc (complex/multi-line prompts)

```bash
codex exec --json - <<'EOF'
Task: Review authentication module
Scope: src/auth/
Constraints: No changes, analysis only
Depth: Deep review

Report issues with severity [P1], [P2], [P3].
EOF
```

### Stdin pipe

```bash
cat prompt.md | codex exec --json -
```

### File reference (preferred for code tasks)

Let Codex read files itself — it has full filesystem access:

```bash
codex exec --json "Read src/auth/login.ts and identify security issues"
```

## JSONL Event Types Reference

| Event | Key Fields | Use |
|-------|-----------|-----|
| `thread.started` | `thread_id` | Session ID for resume |
| `turn.started` | — | Turn boundary marker |
| `item.completed` (reasoning) | `item.text` | Thinking summary |
| `item.completed` (agent_message) | `item.text` | Codex's response text |
| `item.started` (command_execution) | `item.command` | Command about to run |
| `item.completed` (command_execution) | `item.command`, `item.exit_code`, `item.aggregated_output` | Command result |
| `turn.completed` | `usage.input_tokens`, `usage.output_tokens`, `usage.cached_input_tokens` | Token accounting |

## Session Storage

Codex persists sessions at `~/.codex/sessions/YYYY/MM/DD/<session-id>.jsonl`. These contain the full conversation history and can be read directly if needed. Use `--ephemeral` to skip session persistence for throwaway tasks.

## Prompt Discipline

- One goal per agent. Narrow scope = better results.
- Provide exact file paths when possible, not "look through the codebase."
- For structured output, specify the format in the prompt.
- Keep prompts concise — Codex has high reasoning, it doesn't need hand-holding.

## Quick Reference

| Need | Command |
|------|---------|
| Sync exec | `cd /project && codex exec --json "prompt" > out.jsonl 2>/dev/null && codex-result last out.jsonl` |
| Async exec | `codex exec --json "prompt" > out.jsonl 2>/dev/null &` |
| Resume session | `cd /project && codex exec resume --json <ID> "prompt"` |
| Resume latest | `cd /project && codex exec resume --json --last "prompt"` |
| Extract last msg | `codex-result last out.jsonl` |
| Extract session ID | `codex-result session-id out.jsonl` |
| Lower effort | `-c model_reasoning_effort=medium` |
| Disable fast tier | `-c service_tier=flex` |
| Read-only sandbox | `-s read-only` |
| Skip git check | `--skip-git-repo-check` |
