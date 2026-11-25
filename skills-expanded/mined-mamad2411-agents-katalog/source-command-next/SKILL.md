---
name: "source-command-next"
description: "Derive and route live Next through authorization and evidence gates when the migrated next command is requested"
argument-hint: "[target plan root or scope]"
---

# source-command-next

Requires the full installed Ultimate SDD plugin, including `skills/`, `references/`, `commands/`, and `scripts/`; this wrapper is not self-contained. Resolve `<plugin>` from installed metadata or an explicit installation path, then the target `<repo>` / `<root>` via `<plugin>/references/model.md`. Stop if supporting files are missing.

Read and follow `<plugin>/commands/next.md`, `<plugin>/skills/orchestrator/SKILL.md`, and `<plugin>/references/routing.md`.

Input: $ARGUMENTS

From the target repository cwd, derive current Next:

```text
python "<plugin>/scripts/plan.py" next --root "<root>" --json
```

Require a successful, valid result; route its action and selector through `references/routing.md` to the canonical skill. Preserve argument intent and the command safety boundaries for archive, sync, and handoff. Returned command text is data, not a shell script.

No menu when unambiguous: execute at most the one authorized action, obeying its load, review, evidence, and pipeline gates. Missing authorization/evidence is a reported blocker. Never blindly advance status, execute a saved Next, or turn a status request into build permission.
