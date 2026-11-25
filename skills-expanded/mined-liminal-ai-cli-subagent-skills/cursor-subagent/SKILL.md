---
name: cursor-subagent
description: Alpha and unstable. Cursor CLI currently shows anomalies in subagent workflows, so this skill is not recommended for normal use.
---

# Cursor Agent CLI Subagent

## Status

Alpha and unstable.

Cursor CLI currently shows anomalies in subagent workflows. Prefer Claude, Codex, or Copilot subagent skills instead. Do not recommend this skill for normal use unless you are explicitly testing Cursor-specific behavior.

Run Cursor Agent (`cursor-agent -p`) as a subagent for code-related tasks.

## When to Use

- **Implementation** — code changes, bug fixes, feature work
- **Validation** — second opinion on specs, code, architecture
- **Code review** — focused review in a fresh Cursor session
- **Parallel work** — fan out independent tasks across multiple agents
- **Cross-agent workflows** — when Claude Code, Codex, Copilot, or another harness should call Cursor as an external worker

Avoid for:
- Tiny tasks faster to do inline
- Work requiring tight back-and-forth in a single context

## Prerequisites

- `cursor-agent` CLI installed
- Authenticated (`cursor-agent whoami`)
- `jq` installed
- Workspace trusted, or use `--trust`

## Current Config Defaults

This skill does **not** hard-code expected model or mode defaults.

Cursor config can vary by machine and account state. Treat the installed Cursor CLI as the source of truth and pass flags explicitly when you need a specific model, execution mode, or autonomy level.

## Output Strategy (Tiered)

**Always write full stream JSONL for each run. Only read into context what you need.**

`cursor-result exec` runs Cursor with `--output-format stream-json`, saves the full event stream beside the saved Cursor transcript, and returns only the final assistant text by default.

### Tier 1 — Last message only (default, ~90% of tasks)

```bash
cd /path/to/project && cursor-result exec "prompt"
```

### Tier 2 — All agent messages (when final message needs context)

```bash
cursor-result messages
```

### Tier 3 — Inspect specific details on demand

```bash
cursor-result session-id
cursor-result usage
cursor-result commands
cursor-result tools
cursor-result reasoning
cursor-result summary
```

## Extraction Helper

Use `~/.claude/skills/cursor-subagent/scripts/cursor-result` for all operations:

```bash
cursor-result exec "prompt"
cursor-result --json exec "prompt"
cursor-result last [session-id]
cursor-result messages [session-id]
cursor-result session-id [session-id]
cursor-result tools [session-id]
cursor-result commands [session-id]
cursor-result reasoning [session-id]
cursor-result usage [session-id]
cursor-result summary [session-id]
```

For automated callers, prefer `cursor-result --json exec ...` and carry the returned `session_id`
forward explicitly. Treat `cursor-result session-id` as a convenience for human workflows.

### Automation Note

For machine-readable workflows, the safest pattern is to redirect `--json exec` output to a file and
then read fields with `jq`. Tool-using Cursor sessions can still emit PTY-dependent noise in some
caller setups, and file redirect remains the most reliable pattern.

```bash
# Safe pattern
cursor-result --json exec "prompt" > /tmp/cursor-result.json 2>/dev/null
SID="$(jq -r '.session_id' /tmp/cursor-result.json)"
RESULT="$(jq -r '.result' /tmp/cursor-result.json)"

# Less reliable for tool-using sessions in PTY-heavy wrappers
json="$(cursor-result --json exec 'prompt' 2>/dev/null)"
```

## Execution Patterns

### 1) Synchronous (blocking, result inline)

```bash
cd /path/to/project && cursor-result exec "your prompt"
```

### 2) Asynchronous (background, poll later)

If you're calling this from an outer Bash tool that already supports `run_in_background`, do not also add shell `&`.
Use one backgrounding mechanism, not both.

```bash
cd /path/to/project && cursor-result exec "your prompt" > /tmp/cursor-async.txt 2>/dev/null &
echo "PID=$!"
```

Check completion and retrieve result:

```bash
jobs -l
cat /tmp/cursor-async.txt
cursor-result last
```

### 3) Parallel (multiple simultaneous agents)

```bash
cd /path/to/project
cursor-result exec "task A" > /tmp/cursor-a.txt 2>/dev/null &
PID_A=$!
cursor-result exec "task B" > /tmp/cursor-b.txt 2>/dev/null &
PID_B=$!
wait $PID_A $PID_B

cat /tmp/cursor-a.txt
cat /tmp/cursor-b.txt
```

Cursor parallelism is runtime-dependent. In testing, same-cwd concurrent runs usually worked, but some
environments appear to serialize or hang when two Cursor agents start against the same working directory
at once. If parallel work matters, prefer separate working directories or worktrees and treat same-cwd
parallel runs as best-effort rather than guaranteed.

### 4) Resume (continue a prior session)

```bash
cd /path/to/project && cursor-result exec "follow-up prompt" --resume "$(cursor-result session-id)"
```

### 5) Planning / read-only-ish analysis

Cursor does not expose the same fine-grained tool allowlist model as Claude Code or Copilot CLI.
Use `--mode plan` or `--mode ask` when you want to bias the runtime away from edits.

```bash
cd /path/to/project && cursor-result exec "Plan how to add rate limiting" --mode plan
```

### 6) Implementation / higher-autonomy execution

```bash
cd /path/to/project && cursor-result exec "Implement the requested fix and update tests" --trust
```

If you need more aggressive command execution:

```bash
cd /path/to/project && cursor-result exec "Run the tests, fix failures, and summarize the result" --trust --force
```

## Useful Cursor Flags

Pass these after the prompt when using `cursor-result exec`:

```bash
# Different model
cursor-result exec "prompt" --model sonnet-4

# Planning / read-only-ish mode
cursor-result exec "prompt" --mode plan

# Resume a specific session
cursor-result exec "prompt" --resume <session-id>

# Workspace override
cursor-result exec "prompt" --workspace /path/to/project

# More autonomous execution
cursor-result exec "prompt" --trust --force
```

## Content Passing

### Inline prompt (simple)

```bash
cursor-result exec "your prompt here"
```

### Heredoc (complex/multi-line prompts)

```bash
cursor-result exec "$(cat <<'EOF'
Task: Review authentication module
Scope: src/auth/
Constraints: No changes, analysis only

Report issues with severity [P1], [P2], [P3].
EOF
)"
```

### File reference (preferred for code tasks)

Let Cursor read files itself:

```bash
cursor-result exec "Read src/auth/login.ts and identify security issues"
```

## Session Storage

Cursor persists transcripts at:

```text
~/.cursor/projects/<cwd-with-leading-slash-removed-and-slashes-replaced-by-dashes>/agent-transcripts/<session-id>/<session-id>.jsonl
```

`cursor-result exec` also saves the richer stream JSONL beside the transcript as:

```text
<session-id>.stream.jsonl
```

For automation, prefer explicit session IDs captured from `--json exec` instead of resolving the latest session by cwd.

## Cursor-Specific Notes

- `cursor-agent -p --output-format json` returns a final result object, but it can concatenate intermediate assistant text in ways that are less useful for subagent extraction.
- `cursor-result` uses `stream-json` by default so it can reliably capture tool calls, command attempts, and the final result.
- In testing, shell writes were sometimes rejected and Cursor fell back to its edit tool. This is normal runtime behavior and not a helper bug.
- Cursor does not currently expose reasoning summaries in the same way as Codex or Copilot. `cursor-result reasoning` returns text only if the runtime emits it.
