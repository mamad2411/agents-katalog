---
description: Save current project task progress to local task state file for cross-session continuity. Use when the user asks to save progress, uses an equivalent localized trigger phrase, the session is interrupted, or the user wants to resume work later. Writes to .claude/project-task-state.json so next session can load it via SessionStart hook.
---

# Save Progress

Saves current task progress to `.claude/project-task-state.json` in the project directory so the next session can automatically load it and resume where you left off.

## What to Save

Before invoking this command, you should know:
- **Current task**: What are you working on RIGHT NOW?
- **Completed tasks**: What has been finished in this session? (Be specific, not "various things")
- **Remaining tasks**: What still needs to be done?

## How to Invoke

```bash
# Detect the Python hook path — it lives in ~/.claude/hooks/
python "$HOME/.claude/hooks/mcp_memory_global.py" \
  --mode save \
  --task "Describe current task in one sentence" \
  --done "Task 1 completed" "Task 2 completed" \
  --remaining "Next task to do" "Another remaining task"
```

Or use the Claude Code hooks path from the user profile if `HOME` is not set:

```cmd
python "%USERPROFILE%/.claude/hooks/mcp_memory_global.py" ^
  --mode save ^
  --task "..." ^
  --done "..." ^
  --remaining "..."
```

## When to Save

Trigger this when:
- User explicitly asks to save progress
- Session is being interrupted (detected via hook or user signal)
- A major milestone is completed
- Before switching to a different project
- End of a work session

## What NOT to Save

- Generic "worked on project" — be specific: "completed dependency license audit for 4 READMEs"
- Session noise — only save meaningful task state
- Duplicate entries — if nothing meaningful changed, don't overwrite

## Output

The command returns JSON with:
- `saved`: boolean
- `file`: path to the state file
- `total_sessions`: number of sessions recorded
- `total_completed`: total completed tasks across all sessions
- `last_session_completed`: how many tasks completed this session
- `last_session_remaining`: remaining tasks as of this save

Show the user a brief summary after saving.

## Example

User says: "save progress"

```bash
python "$HOME/.claude/hooks/mcp_memory_global.py" \
  --mode save \
  --task "Audit Meta_Kim dependencies and update 4 READMEs" \
  --done "Audited npm dependency licenses" "Audited GitHub skill repositories" "Wrote English README dependency section" \
  --remaining "Update localized READMEs" "Push to GitHub" \
  --note "Found CLI-Anything is Apache 2.0, not MIT"
```

Output: show the user a concise progress summary such as "Progress saved: 2 completed, 2 remaining, 5 total sessions."

## Layered Session Context (how it works)

The SessionStart hook outputs context in 3 layers to avoid context explosion:

| Layer | Trigger | Size | Content |
|-------|---------|------|---------|
| **L1 compact** | Always | ~120 chars | Task state: "doing X, N done, M left" |
| **L2 filtered** | Project tag matched | ~400 chars | Project memories with relevance > 0.55 |
| **L3 full** | User queries manually | ~800 chars | Full memories + recent |

**User can query on demand:**

```bash
# Query task state only (no MCP calls)
python mcp_memory_global.py --mode query-project

# Query all memories (full dump)
python mcp_memory_global.py --mode query-memories
```

If the user asks for previous context, history, or remembered notes, use `--mode query-memories`.
If the user asks for project progress or where the previous session stopped, use `--mode query-project`."

## Prompt Acceptance

This helper binds `planning-continuity`, `memory-graph-and-observability`, `runtime-native-surfaces`, and `verification-eval-and-release`. It saves resumable task context; it does not replace the canonical planning files or prove the user goal is done.

## Pass

- Saved state records the current task, completed work, remaining work, and any meaningful note.
- The summary is specific enough for a later session to resume.
- Existing `task_plan.md`, `findings.md`, and `progress.md` remain the active planning continuity source when present.

## Fail

- The command saves generic session noise or duplicates unchanged state.
- It treats memory write success as task completion.
- It overwrites planning files, PRD decisions, or canonical governance state.

## Block

Block or report unavailable when the memory hook script cannot be found, Python is unavailable, the project directory is unknown, or the user asks for credential/private-state writes outside the approved memory boundary.

## Return to stage

Return to Fetch when previous context is needed before saving. Return to Verification when the user asks whether saved state actually matches current project files.

## Verification

Use the JSON output fields `saved`, `file`, `total_sessions`, `last_session_completed`, and `last_session_remaining`. For prompt acceptance, run `npm run meta:prompt:validate`.

## Preserve

Preserve Claude Code native hooks, local memory, project planning files, MCP memory service state, filesystem boundaries, and user privacy. This command must not replace planning-with-files or Meta_Kim run artifacts.
