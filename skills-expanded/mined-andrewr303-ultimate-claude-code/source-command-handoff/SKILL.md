---
name: "source-command-handoff"
description: "Preserve and update authored session notes when the migrated handoff command is requested"
argument-hint: "[session notes or REQ-n/TASK-k]"
---

# source-command-handoff

Requires the full installed Ultimate SDD plugin, including `skills/`, `references/`, `commands/`, and `scripts/`; this wrapper is not self-contained. Resolve `<plugin>` from installed metadata or an explicit installation path, then the target `<repo>` / `<root>` via `<plugin>/references/model.md`. Stop if supporting files are missing.

Read and follow `<plugin>/commands/handoff.md`, `<plugin>/skills/plan-handoff/SKILL.md`, and `<plugin>/references/recovery.md`.

Input: $ARGUMENTS

Read the entire existing `<root>/HANDOFF.md` and preserve authored decisions, constraints, questions, and next-session warnings. Obtain only a read-only draft from the target repository cwd:

```text
python "<plugin>/scripts/plan.py" handoff --root "<root>"
```

Append or make targeted edits after reading; create a concise handoff if absent. Do not regenerate authored notes with the base command's `--write` flag. Use live resume state, not saved Next. No lifecycle advancement, automatic tests, or git mutations.
