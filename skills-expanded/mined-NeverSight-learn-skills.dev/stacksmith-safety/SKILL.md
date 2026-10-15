---
name: stacksmith-safety
version: 1.0.0
description: "Safety controls for any software project. Subcommands: careful on (enable confirmation gates before risky actions), freeze (lock file or scope boundaries), guard (validate preconditions before destructive ops), off (disable active guards). Trigger before bulk edits, migrations, destructive operations, or any change where accidental scope creep would be costly."
---

## Command routing

Parse the user's invocation:

- `/stacksmith-safety careful on` -> careful mode
- `/stacksmith-safety freeze [path]` -> freeze mode
- `/stacksmith-safety guard [path]` -> guard mode
- `/stacksmith-safety off` -> remove all restrictions

If the user says "be careful" or "careful mode", treat it as `careful on`.

All timeline logs in this skill use:
- `skill: "stacksmith-safety"`
- `mode: "careful" | "freeze" | "guard" | "unfreeze"`

---

## Subcommand: `careful on`

Active when:
- user ran `/stacksmith-safety careful on`
- user said "be careful" or "careful mode"
- `guard` is active

Deactivate with `/stacksmith-safety off`.

### Intercepted commands

Before executing any of these, stop and show a warning:

| Command | Risk | Warning |
|---------|------|---------|
| `rm -rf` | Permanent deletion | List exactly what will be deleted |
| `DROP TABLE` | Permanent DB deletion | Name the table and estimated row count |
| `DELETE FROM` without `WHERE` | All rows | Confirm it is intentional |
| `TRUNCATE` | All rows | Same as above |
| `git push --force` / `-f` | Rewrites remote history | Who else is on this branch? |
| `git reset --hard` | Discards uncommitted work | List what will be lost |
| `git clean -fd` | Deletes untracked files | List what will be deleted |
| `chmod -R 777` or `chmod 777` | World-writable permissions | Why is this needed? |

### Warning format

```text
CAREFUL MODE

Command: [exact command]
Risk: [what this will do]

A) Proceed - run it
B) Abort
C) Show me a safer alternative
```

Wait for explicit confirmation before proceeding. Do not warn twice for the same command in the same session if the user already confirmed it.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-safety\",\"mode\":\"careful\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Subcommand: `freeze [path]`

Usage: `/stacksmith-safety freeze [path]`

Default path with no argument: current directory `.`

```bash
FREEZE_PATH="${1:-.}"
mkdir -p ~/.mystack
echo "$FREEZE_PATH" > ~/.mystack/freeze.txt
echo "Freeze active: edits restricted to $FREEZE_PATH"
echo "Run /stacksmith-safety off to remove."
```

When freeze is active:
- reads are always allowed
- writes outside the boundary are blocked

Blocked edit prompt:

```text
FREEZE ACTIVE - edit blocked

File: [path]
Boundary: [frozen path]

A) Edit anyway (one-time override for this file)
B) Abort
C) Expand boundary to include this path
D) /stacksmith-safety off - remove all restrictions
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-safety\",\"mode\":\"freeze\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Subcommand: `guard [path]`

Usage: `/stacksmith-safety guard [path]`

Default path: current directory `.`

```bash
GUARD_PATH="${1:-.}"
mkdir -p ~/.mystack
echo "$GUARD_PATH" > ~/.mystack/freeze.txt
echo "GUARD ACTIVE"
echo "Freeze boundary: $GUARD_PATH"
echo "Destructive commands: confirmation required"
echo "Run /stacksmith-safety off to remove all restrictions."
```

All rules from `careful on` and `freeze` are now active simultaneously.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-safety\",\"mode\":\"guard\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Subcommand: `off`

```bash
rm -f ~/.mystack/freeze.txt
echo "All restrictions removed."
echo "Careful mode: off"
echo "Freeze boundary: none"
echo "All edits and commands permitted."
```

This subcommand turns off careful mode, freeze, and guard together.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-safety\",\"mode\":\"unfreeze\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
