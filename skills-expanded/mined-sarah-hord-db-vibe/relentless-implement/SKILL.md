---
name: relentless-implement
description: Run relentless auto-continuing implementation on a PRD or task description. Launches headless Claude sessions in the background with progress tracking.
user-invocable: true
---

# Implement

Launch `relentless` to implement a PRD or task description using auto-continuing headless Claude sessions.

**Announce at start:** "Starting relentless implementation."

## Process

### Step 1: Find the target

Determine what to implement, in priority order:

1. **Argument provided** — If the user typed `/implement prd_jwt-auth.md` or `/implement "Add CSV export"`, use that directly.
2. **PRD file in current directory** — Run `ls prd_*.md` to find recent PRDs. If exactly one exists, use it. If multiple, ask the user which one.
3. **Ask** — If nothing found, ask: "What should I implement? You can point me at a PRD file or describe the task."

**Critical:** Once you have a target file, resolve it to an **absolute path** using `realpath` or `pwd`. Also determine the **project root** (the git repo root via `git rev-parse --show-toplevel`, or the directory containing the PRD). You will need both for Step 3.

### Step 2: Configure

Ask the user if they want to adjust defaults (only if they seem like a power user — otherwise just go):

| Setting | Default | Flag |
|---------|---------|------|
| Max sessions | 5 | `-n` |
| Model | system default | `-m` |
| Budget per session | unlimited | `-b` |
| Verbose output | yes | `-v` |
| Permission mode | bypassPermissions | `-p` |

For most cases, defaults are fine. Just confirm: "I'll run relentless with default settings (5 sessions, verbose). Starting now."

### Step 3: Launch

Run via Bash with `run_in_background: true`.

**Important:**
- The `env -u` prefix strips environment variables that prevent nested Claude sessions from launching.
- **Always resolve the PRD file to an absolute path** and pass `-d` with the directory containing it. This ensures relentless runs from the correct directory regardless of the current shell working directory.

```bash
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -f /absolute/path/to/project/prd_<slug>.md -p bypassPermissions -v > /absolute/path/to/project/relentless_<slug>.log 2>&1
```

Or for a plain task description (no file):

```bash
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -p bypassPermissions -v "<task description>" > /absolute/path/to/project/relentless_task.log 2>&1
```

Tell the user:
- "Implementation running in background."
- "Progress: `_relentless_state.md`"
- "Full log: `relentless_<slug>.log`"
- "I'll let you know when it finishes."

### Step 4: Report results

When the background task completes, read the state file and log tail:

1. Read `_relentless_state.md` for structured progress
2. Read the last 30 lines of `relentless_<slug>.log` for completion status
3. Check `.relentless_logs/` for any `diagnostic_*.json` files — these contain detailed failure analysis if the agent was killed or got stuck
4. Summarize for the user:
   - Success or failure
   - Sessions used
   - Files created/modified
   - Any escalations or blockers (include the diagnostic snapshot path)
   - If stuck/looping: what the state hash history shows (same state repeated?)
   - Suggested next steps (run tests, review changes, etc.)

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Task completed successfully |
| 1 | Max sessions exhausted without completion |
| 2 | Escalation — agent stuck, looping, or hit an unresolvable blocker |
