---
name: claude-subagent
description: Run Claude Code CLI as a subagent for code tasks, review, validation, and implementation. Supports sync, async, parallel, and resume workflows with tiered output management.
---

# Claude Code CLI Subagent

Run Claude Code (`claude -p`) as a subagent for code-related tasks.

## When to Use

- **Implementation** — code changes, bug fixes, feature work
- **Validation** — second opinion on specs, code, architecture
- **Code review** — focused review in a fresh Claude session
- **Cross-agent workflows** — when Codex or Copilot should call Claude as an external worker
- **Parallel work** — fan out independent tasks across multiple agents
- **Fresh context** — use a separate Claude CLI session instead of built-in subagent/task tools

Avoid for:
- Tiny tasks faster to do inline
- Work requiring constant back-and-forth inside one shared context
- Machines where `claude` is not installed or not authenticated

## Prerequisites

- `claude` CLI installed and authenticated
- `jq` installed
- Session persistence enabled (default)

## Current Config Defaults

Unlike the other two skills, this one deliberately does **not** hard-code expected model or effort defaults.

Claude Code settings can vary by machine, auth path, and local config, and hard-coded claims drift fast.
Treat the installed Claude CLI as the source of truth and pass flags explicitly when you need a specific model,
effort level, agent, permission mode, or tool profile.

## Claude-Specific Quirks

- Prefer `claude-result exec "prompt" ...` over calling `claude -p` directly.
- `--allowedTools` is variadic. If you pass flags directly to `claude`, place the prompt after `--` or pipe it on stdin. The helper handles this safely for you.
- `--allowedTools` should be treated as a runtime preference, not a hard security boundary. In testing, Claude still reached for tools outside the requested set in some runs.
- Do **not** default to `--bare`. It can disable the auth path used by a normal Claude Code install and may fail with `Not logged in`.
- Claude's final JSON result goes to stdout, but richer inspection comes from the saved session log under `~/.claude/projects/...`.
- If multiple Claude sessions share the same cwd, `claude-result session-id` can resolve to the wrong one. For automation, always carry the explicit `session_id` returned by `--json exec`.

## Output Strategy (Tiered)

**Default behavior: print the final result to stdout, then inspect the saved session on demand.**

Claude already persists each session under `~/.claude/projects/.../<session-id>.jsonl`, so the helper focuses on:

1. running `claude -p --output-format json`
2. returning only `.result` by default
3. extracting deeper details from the persisted session log only when needed

### Tier 1 — Final result only (default)

```bash
cd /path/to/project && claude-result exec "your prompt"
```

### Tier 2 — Session-aware follow-up

```bash
claude-result session-id
claude-result summary
claude-result last
```

### Tier 3 — Inspect internals on demand

```bash
claude-result thinking
claude-result reasoning
claude-result commands
claude-result tools
claude-result usage
claude-result session-file
```

## Extraction Helper

Use `~/.claude/skills/claude-subagent/scripts/claude-result`:

```bash
claude-result exec "prompt"
claude-result --json exec "prompt"
claude-result last [session-id]
claude-result messages [session-id]
claude-result thinking [session-id]
claude-result reasoning [session-id]
claude-result commands [session-id]
claude-result tools [session-id]
claude-result usage [session-id]
claude-result summary [session-id]
claude-result session-id [session-id]
claude-result session-file [session-id]
```

For automated callers, prefer `claude-result --json exec ...` and carry the returned `session_id`
forward explicitly. Treat `claude-result session-id` as a convenience for human workflows.

## Execution Patterns

### 1) Synchronous (blocking, result inline)

```bash
cd /path/to/project && claude-result exec "Review src/auth for security issues"
```

### 2) Read-only review / analysis

```bash
cd /path/to/project && claude-result exec \
  "Review the recent changes and report real issues only." \
  --permission-mode default \
  --allowedTools Read,Grep,Glob
```

### 3) Asynchronous (background, poll later)

```bash
cd /path/to/project && claude-result exec \
  "Review src/auth and summarize the main risks." \
  --permission-mode default \
  --allowedTools Read,Grep,Glob \
  > /tmp/claude-async.txt 2>/dev/null &
echo "PID=$!"
```

Check completion and retrieve result:

```bash
jobs -l
cat /tmp/claude-async.txt
claude-result last
```

### 4) Parallel (multiple simultaneous agents)

```bash
cd /path/to/project
claude-result exec "task A" --permission-mode default --allowedTools Read,Grep,Glob > /tmp/claude-a.txt 2>/dev/null &
PID_A=$!
claude-result exec "task B" --permission-mode default --allowedTools Read,Grep,Glob > /tmp/claude-b.txt 2>/dev/null &
PID_B=$!
wait $PID_A $PID_B

cat /tmp/claude-a.txt
cat /tmp/claude-b.txt
```

### 5) Implementation / file edits

```bash
cd /path/to/project && claude-result exec \
  "Implement the requested fix in src/auth and update tests." \
  --permission-mode acceptEdits \
  --allowedTools Read,Write,Edit,Bash,Grep,Glob
```

### 6) Higher-autonomy execution

```bash
cd /path/to/project && claude-result exec \
  "Run the failing tests, fix the issue, and summarize the change." \
  --permission-mode bypassPermissions \
  --allowedTools Read,Write,Edit,Bash,Grep,Glob
```

### 7) Resume (continue a prior session)

```bash
cd /path/to/project && claude-result exec \
  "Continue from the prior result and tighten the summary." \
  --resume "$(claude-result session-id)"
```

## Useful Claude Flags

Pass these after the prompt when using `claude-result exec`:

```bash
# Different model
claude-result exec "prompt" --model claude-opus-4-1

# Higher effort
claude-result exec "prompt" --effort high

# Named session
claude-result exec "prompt" --name review-pass

# Use a built-in Claude agent
claude-result exec "prompt" --agent Explore

# Run in another working tree without changing your shell cwd
claude-result --cwd /path/to/project exec "prompt"
```

## Content Passing

### Inline prompt (simple)

```bash
claude-result exec "your prompt here"
```

### Heredoc (complex/multi-line prompts)

```bash
claude-result exec "$(cat <<'EOF'
Task: Review authentication module
Scope: src/auth/
Constraints: No changes, analysis only

Report issues with severity [P1], [P2], [P3].
EOF
)"
```

### File reference (preferred for code tasks)

Let Claude read files itself:

```bash
claude-result exec "Read src/auth/login.ts and identify security issues" --permission-mode default --allowedTools Read,Grep,Glob
```

## Session Storage

Claude persists sessions at:

```text
~/.claude/projects/<cwd-with-slashes-replaced-by-dashes>/<session-id>.jsonl
```

The helper resolves the latest session for the current working directory by default, or you can pass a specific session ID.

For automation, prefer explicit session IDs captured from `--json exec` instead of resolving the latest session by cwd.

## Session Event Reference

The saved session JSONL contains enough structure to inspect:

| Need | Source |
|------|--------|
| Final text | assistant message content items of type `text` |
| Reasoning | assistant message content items of type `thinking` |
| Tool calls | assistant message content items of type `tool_use` |
| Tool results | user messages containing `tool_result` items |
| Usage | final `result` event when present, otherwise assistant message usage |

## Prompt Discipline

- One goal per agent. Narrow scope gives better results.
- Provide exact file paths when possible.
- Specify the output format if you want structured results.
- Use constrained tools for review and validation.
- Use `acceptEdits` or `bypassPermissions` only when you actually want the subagent to modify files.

## Quick Reference

| Need | Command |
|------|---------|
| Sync exec | `claude-result exec "prompt"` |
| Raw JSON result | `claude-result --json exec "prompt"` |
| Async exec | `claude-result exec "prompt" > out.txt 2>/dev/null &` |
| Resume latest | `claude-result exec "prompt" --resume "$(claude-result session-id)"` |
| Read-only review | `claude-result exec "prompt" --permission-mode default --allowedTools Read,Grep,Glob` |
| Implementation | `claude-result exec "prompt" --permission-mode acceptEdits --allowedTools Read,Write,Edit,Bash,Grep,Glob` |
| Extract last message | `claude-result last` |
| Extract thinking | `claude-result thinking` |
| Extract reasoning | `claude-result reasoning` |
| Extract commands | `claude-result commands` |
| Extract tool calls | `claude-result tools` |
| Extract usage | `claude-result usage` |
