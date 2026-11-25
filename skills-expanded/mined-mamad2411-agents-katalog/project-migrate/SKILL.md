---
name: project-migrate
description: Migrate a project directory to a new path while preserving Claude Code project memory and project-level knowledge. Use this skill when the user wants to move or copy a project to a different directory path — phrases like "/project-migrate", "migrate project to", "move project to new path", "relocate project directory". This skill requires the project-memory skill to be installed separately. It copies the project directory (preserving permissions), migrates Claude Code memory, and persists project knowledge via project-memory so the AI can quickly understand project progress in the new location.
---

# Migrate Project

Copy the current project directory to a new path while preserving Claude Code project memory and persisting project knowledge for continuity.

## Prerequisites

This skill depends on the `project-memory` skill. Before proceeding with any migration step, verify it is installed:

```bash
ls ~/.claude/skills/*/SKILL.md 2>/dev/null | xargs grep -l 'name: project-memory' 2>/dev/null
```

Also check plugin-installed skills:

```bash
find ~/.claude/plugins -name "SKILL.md" -exec grep -l 'name: project-memory' {} \; 2>/dev/null
```

If neither command returns a result, tell the user:

> The `project-memory` skill is not installed. Please install it first:
> ```
> npx skills add spillwavesolutions/project-memory@project-memory -g -y
> ```
> Then run `/migrate-project` again.

Do NOT attempt to search for or install the skill automatically. Stop here and wait for the user.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| target-path | Yes | Destination path for the project. Can be absolute or relative. |

## Workflow

### Step 1: Persist project knowledge

Invoke the `project-memory` skill to persist current project knowledge into `docs/project_notes/`. This ensures the AI in the new location can understand project progress, decisions, bugs, and key facts without session history.

If `docs/project_notes/` already exists with content, update it rather than overwriting.

### Step 2: Confirm target path

Resolve the target path to an absolute path. Compare the basename of the target path with the current project directory name (`basename "$PWD"`).

If they differ, the user may have intended the target as a parent directory. Present both interpretations and ask for confirmation before proceeding:

> The target directory name `misc` differs from the current project name `test`. Which do you mean?
> 1. `/xxx/xxx/misc` — rename the project to `misc`
> 2. `/xxx/xxx/misc/test` — copy into `misc/` keeping the original name
>
> Please confirm (1 or 2):

Wait for the user's response and use the confirmed path as the final target. If the basenames match, proceed without asking.

### Step 3: Validate target path

Verify the resolved target path:

1. **Parent directory exists** — if not, report the error and stop.
2. **Target does not exist, or is an empty directory** — if the target exists and is non-empty, report the error and stop. Do not overwrite existing content.

```bash
TARGET="<resolved-absolute-path>"
PARENT="$(dirname "$TARGET")"

# Check parent exists
if [ ! -d "$PARENT" ]; then
  echo "Error: parent directory $PARENT does not exist."
  exit 1
fi

# Check target is free
if [ -d "$TARGET" ] && [ "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  echo "Error: target $TARGET already exists and is not empty."
  exit 1
fi
```

### Step 4: Copy project directory

Use `cp -rp` to copy the entire project directory, preserving permissions, ownership, and timestamps:

```bash
cp -rp "$PWD" "$TARGET"
```

Report the result to the user, including the size of the copied directory:

```bash
du -sh "$TARGET"
```

### Step 5: Migrate Claude Code project memory

Claude Code stores project-level memory in `~/.claude/projects/<encoded-path>/memory/`. The path encoding replaces every `/` with `-`.

```bash
OLD_ENCODED="$(echo "$PWD" | sed 's|/|-|g')"
NEW_ENCODED="$(echo "$TARGET" | sed 's|/|-|g')"

OLD_MEMORY="$HOME/.claude/projects/${OLD_ENCODED}/memory"
NEW_MEMORY_DIR="$HOME/.claude/projects/${NEW_ENCODED}"
NEW_MEMORY="${NEW_MEMORY_DIR}/memory"

if [ -d "$OLD_MEMORY" ] && [ "$(ls -A "$OLD_MEMORY" 2>/dev/null)" ]; then
  mkdir -p "$NEW_MEMORY"
  cp -rp "$OLD_MEMORY/"* "$NEW_MEMORY/"
  echo "Claude Code project memory migrated."
else
  echo "No Claude Code project memory found to migrate (this is normal for new projects)."
fi
```

### Step 6: Report completion

Output a summary:

```
Migration complete:
  Source: /original/path
  Target: /new/path
  Project memory: migrated (or: none found)
  Project knowledge: persisted in docs/project_notes/

Next steps:
  1. cd /new/path && claude    — start a new session in the new location
  2. Verify everything works as expected
  3. When satisfied, manually remove the old directory:
     rm -rf /original/path
     rm -rf ~/.claude/projects/<old-encoded>/
```

## Constraints

- **Never delete anything.** This skill only copies, never removes.
- **No session history migration.** Session JSONL files are not copied. Start fresh sessions in the new location.
- **No code modification.** Files like `go.mod`, `package.json`, git remotes, etc. are left untouched. The user handles these manually.
- **Language-agnostic.** This skill works for any project regardless of language or framework.
