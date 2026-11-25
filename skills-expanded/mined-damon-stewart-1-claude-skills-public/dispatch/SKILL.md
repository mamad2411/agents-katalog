---
name: dispatch
description: Dispatch a task to a background Claude Code instance. Use when the user wants to kick off work without blocking the current session. Triggers on "dispatch", "background task", "run in background", "kick off", or "/dispatch".
user_invocable: true
---

# Dispatch: Background Claude Task Runner

The user wants to send a task to a separate Claude Code process running in the background.

## What to do

1. **Confirm the task.** Restate what the user wants done in one sentence. If unclear, ask.

2. **Pick permission tier.** Based on the task:
   - **Read-only** (research, summarize, explain): `"Read,Glob,Grep,Write,WebSearch,WebFetch"` (Write always included so output file can be created)
   - **Code** (fix bugs, write features, refactor): `"Read,Glob,Grep,Edit,Write,Bash(git diff *),Bash(git status *),Bash(npm test *),Bash(npx *)"`
   - **Full** (commits, installs, builds): `"Read,Glob,Grep,Edit,Write,Bash"`
   - **LLM review** (Gemini/ChatGPT): `"Read,Glob,Grep,Write,Bash"` (unrestricted Bash needed for `source ~/.api-keys-cache`)
   - Default to read-only unless the task clearly requires writes. Ask if unsure.

3. **Pick model.** For research, summaries, file searches, and template writes, add `--model sonnet` to reduce cost. Use Opus (default) for architecture, client-facing copy, and multi-step reasoning.

4. **Pick LLM target.** Default is Claude. Ask if the task warrants a different LLM:

| Target | When to use | How it works |
|--------|-------------|--------------|
| Claude | Code tasks, file edits, multi-step work | Direct `claude -p` execution |
| Gemini | Reviews, second opinions, long analysis | `claude -p` calls `gemini-api.sh` |
| ChatGPT | Alternative perspective, copy feedback | `claude -p` calls `chatgpt-api.sh` |

For Gemini/ChatGPT: write the prompt to a temp file first, then pass it via the script. Use unrestricted Bash tier. See `references/multi-llm-dispatch.md` for script paths and model names.

5. **Set timeout.** Timeout is the circuit breaker (`--max-turns` was removed in Claude Code 2.1):
   - Simple (research, summaries): 600s
   - Medium (file edits, multi-step): 1800s
   - Complex (builds, large refactors): 3600s

   Requires `gtimeout` (GNU coreutils). If missing: `brew install coreutils`.

6. **Build and run.** Generate job ID and write the prompt to a temp file, then launch:

```bash
JOB_ID="job-$(date +%Y%m%d-%H%M%S)"
PROMPT_FILE="/tmp/${JOB_ID}-prompt.txt"

# Write full task prompt to file (include file paths, project context, done criteria)
cat > "$PROMPT_FILE" << 'PROMPT'
<the user's task prompt>
PROMPT

# Launch in background
(bash "${CLAUDE_PLUGIN_ROOT}/skills/dispatch/scripts/dispatch.sh" \
  "$JOB_ID" "$PROMPT_FILE" "<TOOLS>" <TIMEOUT_SECS> [MODEL] [ADD_DIR]) &

echo "Dispatched ${JOB_ID} (PID: $!)"
```

Run with `run_in_background: false` since the subshell backgrounds via `&` and returns immediately.

7. **Report back.** Tell the user: job ID, what it's doing, timeout, how to check (`/jobs`).

## Failure detection

The dispatch script writes a `.meta` file with these fields:

```
status: running|complete|failed|timed_out
task: <first 80 chars of prompt>
model: opus|sonnet|haiku
started: YYYY-MM-DD HH:MM:SS
completed: YYYY-MM-DD HH:MM:SS
output: /path/to/output.md
tools: <tool list>
exit_code: <integer>
```

Status logic:
- `exit_code = 0` AND output file exists: `complete`
- `exit_code = 124`: `timed_out` (gtimeout killed the process)
- `exit_code != 0` OR no output file: `failed`

If a job shows `failed`, check `~/.claude/jobs/<JOB_ID>.log` for the last 20 lines.

## Why /tmp/ for output

`~/.claude/` is a sensitive write path. Claude Code blocks the Write tool there even with `--permission-mode bypassPermissions`. The dispatch script writes to `/tmp/` first, then copies to `~/.claude/jobs/` via shell after completion.

For tasks needing multiple output files, direct the spawned Claude to `~/Claude-Stuff/` or a project directory.

## Rules

- If the task involves a specific project directory, pass it as the ADD_DIR argument.
- Never dispatch tasks that need user judgment mid-execution.
- Never dispatch tasks that touch production systems, push code, or send external messages.
- The background Claude has NO access to this conversation's context. Include everything it needs in the prompt.
- Do NOT use `--bare` flag (breaks keychain auth and disables hooks/plugins/CLAUDE.md).
- Tell spawned Claude to target `/tmp/` or `~/Claude-Stuff/` for writes, never `~/.claude/`.
- For tasks that benefit from parallel sub-agents, use `/spawn-agent-team` instead of a single dispatch.
