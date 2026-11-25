---
name: easyskillz-reference
description: Use when managing project skills, agent targets, migrations, or owned instruction files with Easyskillz 0.5.1.
---
# Easyskillz 0.5.1 reference

Easyskillz keeps canonical skills in `.easyskillz/skills/<name>/` and materializes complete native directories for configured agent surfaces.

## Safety contract

- Preview every mutation with `--dry-run`.
- Apply explicit document, migration, format, and repair operations with `--write`.
- Never edit generated targets; edit the canonical skill directory and sync again.
- Invalid YAML is diagnosed, never silently repaired.
- Cleanup requires local ownership state and an unchanged artifact identity.
- `project sync` does not manage instruction files.

## Canonical commands

### skill

- `easyskillz skill add`
- `easyskillz skill remove`
- `easyskillz skill activate`
- `easyskillz skill deactivate`
- `easyskillz skill list`
- `easyskillz skill validate`
- `easyskillz skill format`
- `easyskillz skill repair`

### tool

- `easyskillz tool register`
- `easyskillz tool unregister`
- `easyskillz tool list`

### project

- `easyskillz project sync`
- `easyskillz project doctor`
- `easyskillz project export`
- `easyskillz project migrate`

### docs

- `easyskillz docs adopt`
- `easyskillz docs sync`
- `easyskillz docs restore`
- `easyskillz docs list`

## Common workflows

```bash
easyskillz skill validate
easyskillz skill add review-pr --dry-run
easyskillz project sync --dry-run
easyskillz project doctor --strict
easyskillz project migrate --dry-run
easyskillz docs adopt docs/AGENTS.source.md --target AGENTS.md --dry-run
easyskillz docs sync --dry-run
```

Human aliases `sync`, `doctor`, and `add <name>` remain deprecated compatibility shims through 0.5.x. Prefer canonical commands.
