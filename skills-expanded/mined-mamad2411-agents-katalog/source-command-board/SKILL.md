---
name: "source-command-board"
description: "Show the Plan / Build / Published board and live Next when the migrated board command is requested"
argument-hint: "[SPEC-n or REQ-n]"
---

# source-command-board

Requires the full installed Ultimate SDD plugin, including `skills/`, `references/`, `commands/`, and `scripts/`; this wrapper is not self-contained. Resolve `<plugin>` from installed metadata or an explicit installation path, then the target `<repo>` / `<root>` via `<plugin>/references/model.md`. Stop if supporting files are missing.

Read and follow `<plugin>/commands/board.md`, `<plugin>/skills/plan-board/SKILL.md`, and the read-only Board/status boundary in `<plugin>/references/routing.md`.

Input: $ARGUMENTS

From the target repository cwd, derive the board and Next without writing:

```text
python "<plugin>/scripts/plan.py" board --root "<root>"
python "<plugin>/scripts/plan.py" next --root "<root>" --json
```

Display live Next only. No scaffolding, context generation, INDEX writes, lifecycle changes, repairs, implementation, or executing Next. Do not pass the board command's `--write` flag, even if older skill guidance requests it; report that conflict instead.
