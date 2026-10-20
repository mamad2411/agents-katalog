---
name: skill-registry
description: Use to discover which skills exist in a project before delegating to a subagent. Run `ether skill-registry refresh` after adding, removing, renaming, or moving skills; use `ether skill-registry list` to inspect resolution without writing files. Orchestrators should read `.ether/skill-registry.md` to match a task against available skills and pass the exact SKILL.md path to a subagent, rather than rewriting or summarizing skill content.
---

# Skill Registry Harness

An index of every skill available in a project — name, full description, scope, and exact
`SKILL.md` path — so an orchestrator can match a task against skills and hand a subagent the
real file to read, instead of a digested summary.

## When to use it

Run `ether skill-registry refresh` after adding, removing, renaming, or moving skills. Run
`ether skill-registry list` to inspect what would be resolved without writing anything.

## Resolution

Scans project skill roots first (`skills/`, `.claude/skills/`), then the global root
(`~/.claude/skills/`). A skill present in both scopes keeps the project version — project wins.
Skills named `_shared`, `skill-registry`, or matching `ether-*` are never indexed: the first two are
internal plumbing, `ether-*` skills are orchestrator-managed by the SDD workflow itself, not
delegator-selected.

## Skill Loading Contract

Pass exact paths to subagents, not compact rules:

```markdown
## Skills to load before work

Read these exact files before reading, writing, reviewing, testing, or creating artifacts:

- /path/to/skills/go-testing/SKILL.md
- /path/to/skills/docs-writer/SKILL.md
```

The subagent reads those files directly. This keeps the original `SKILL.md` as the source of
truth and avoids losing author intent to automatic summarization — an index costs tokens only
when a subagent actually needs a skill, unlike baking compact summaries into every prompt.

## Command reference

- `ether skill-registry refresh [--force]` — resolves the skill set, writes `.ether/skill-registry.md`
  (a Markdown table: Skill, Trigger / description, Scope, Path) and a cache file.
- `ether skill-registry list [--json]` — same resolution, prints instead of writing; `--json` for
  machine-readable output.
