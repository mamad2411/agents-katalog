---
name: workspace-setup
description: Register or create the user's image operations workspace — a folder on disk where they keep image projects. Use when running for the first time, or when the user says "set up my image workspace", "register my image workspace", "change my image workspace path", or similar. Persists the path so other skills (open-workspace, new-project) can reference it.
allowed-tools: Bash(mkdir *), Bash(test *), Bash(echo *), Bash(realpath *), Bash(date *), Bash(git init:*), Read, Write
---

# Image Workspace Setup

Register the folder the user treats as their image operations workspace. Individual projects live as sub-folders inside it.

## Data store

```
${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops/workspace.json
```

Do **not** write under a coding tool's config directory (`~/.claude/`, `~/.codex/`, `~/.config/opencode/`, and the like).

## Procedure

### 1. Check for existing config

```bash
DATA_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops"
CONFIG="$DATA_DIR/workspace.json"
test -f "$CONFIG" && echo "$CONFIG"
```

If the file exists, open it with the file-reading tool rather than `cat`, which keeps shell use down to the commands that actually do work.

If one exists, show the path and ask whether to keep or change it.

### 2. Ask the user

1. **Existing or new?** — do they already have an image workspace, or should one be created?
2. **Path?**
   - Existing: ask for absolute path; verify with `test -d`.
   - New: propose `~/media-workspaces/images` as the default. Don't auto-create until the user confirms.

### 3. (New only) Version control

Ask whether to `git init` the workspace. Default **no** — image libraries can be large. Only `git init` is in scope; this skill never commits, adds a remote, or pushes.

### 4. Create + persist

```bash
mkdir -p "$DATA_DIR" \
  || { echo "cannot create $DATA_DIR — check permissions" >&2; exit 1; }

# Only if new:
mkdir -p "$CHOSEN_PATH" \
  || { echo "cannot create $CHOSEN_PATH — check the path and permissions" >&2; exit 1; }

WS_PATH=$(realpath "$CHOSEN_PATH")
CREATED=$(date -u +%Y-%m-%dT%H:%M:%SZ)
```

Stop on either failure — persisting a config that points at a directory that does not exist just moves the error to the next skill that reads it.

Write `workspace.json` with the file-writing tool, substituting the two values above:

```json
{
  "path": "<WS_PATH>",
  "created": "<CREATED>",
  "version_controlled": false,
  "type": "image"
}
```

`realpath` canonicalises the path so `open-workspace` and `new-project` resolve the same directory regardless of how the user typed it.

### 5. Confirm

Print the registered path. Remind the user they can now say "open my image workspace" or "create a new image project".
