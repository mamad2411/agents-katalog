---
name: push-claude
version: 1.0.0
description: |
  Push all Claude Code configuration, skills, memory, and settings to the
  RobotFlow-Labs/claude git repo for backup and cross-machine sync.
  Auto-commits with a timestamped message and pushes to origin/main.
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Push Claude — Backup & Sync

## What This Does
Commits and pushes the entire `~/.claude` configuration to `github.com/RobotFlow-Labs/claude.git`.
This keeps skills, memory, settings, agents, and project configs backed up and synced across all your Macs.

## What Gets Synced
- **Skills** — All custom skills (gstack, ethskills, robotflowlabs, etc.)
- **Memory** — All project memory files (MEMORY.md + individual memories)
- **Settings** — settings.json, settings.local.json
- **Agents** — Custom agent definitions
- **Commands** — Custom slash commands
- **Hooks** — Git/event hooks
- **Plans** — Saved plans
- **Project configs** — CLAUDE.md files per project
- **Scripts** — Helper scripts

## What Does NOT Get Synced
- Credentials (.credentials.json)
- Conversation transcripts (*.jsonl)
- Telemetry, caches, sessions
- node_modules (install per-machine)
- Generated DD output (data-for-*/ — regenerate per-machine)
- Machine-specific state (IDE, statusline)

## Execution

### Step 1: Status Check
```bash
cd ~/.claude
git status --short
```

Show the user what changed since last push.

### Step 2: Stage All Changes
```bash
cd ~/.claude
git add -A
```

### Step 3: Commit with Timestamp
Generate a commit message that includes:
- Current date/time
- Summary of what changed (new skills, updated memory, settings changes, etc.)

```bash
cd ~/.claude
git commit -m "$(cat <<'EOF'
sync: [DATE] — [brief summary of changes]
EOF
)"
```

### Step 4: Push to Remote
```bash
cd ~/.claude
git push -u origin main
```

### Step 5: Confirmation
Report:
```
  ✓ Pushed to RobotFlow-Labs/claude
  ✓ [N] files changed, [N] insertions, [N] deletions
  ✓ Commit: [hash]
  ✓ Last sync: [timestamp]
```

## Cross-Machine Setup
On a new Mac, clone and you're ready:
```bash
git clone https://github.com/RobotFlow-Labs/claude.git ~/.claude
cd ~/.claude/skills/robotflowlabs && npm install
cd ~/.claude/skills/gstack && npm install
```

## Edge Cases
- If there are merge conflicts from another machine, show them and ask the user how to resolve
- If nothing changed, say "Already up to date — nothing to push"
- If the remote is ahead, pull first: `git pull --rebase origin main` then push
