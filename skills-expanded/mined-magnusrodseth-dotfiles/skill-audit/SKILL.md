---
name: skill-audit
description: Audit installed Claude Code skills for context-budget cost and real usage. Inventories ~/.claude/skills, estimates the always-loaded token cost of each description, and mines ~/.claude/projects transcripts for actual invocations to find unused skills. Use when the user asks to "audit skills", "clean up skills", "find unused skills", "skill budget", "too many skills", or wonders what their skills cost in context.
---

# Skill Audit

Every installed skill's name + description is loaded into context in every
session. This skill finds which ones earn that cost.

## Workflow

1. Run the analyzer:

```bash
bash ~/dotfiles/.claude/skills/skill-audit/scripts/skill-audit.sh
```

Add a project's skills to the inventory with `--root` (repeatable):

```bash
bash ~/dotfiles/.claude/skills/skill-audit/scripts/skill-audit.sh \
  --root ~/dev/personal/vault/.claude/skills
```

2. Read the report:
- Header: total skills and the always-loaded token cost per session.
- Main table: used skills, most-used first, with last-used date and source.
- `UNUSED IN WINDOW`: removal candidates, most expensive first.

3. Suggest removals; delete only when the user confirms. Removal mechanics
depend on the `SOURCE` column:

| Source | Managed by | Remove with |
|---|---|---|
| `skills-cli` | skills.sh lock file | `npx skills remove <name>`, then `bash ~/dotfiles/scripts/skills/packages.sh export` and commit the lock file |
| `dotfiles` | authored in dotfiles | delete `~/dotfiles/.claude/skills/<name>/`, run `bash ~/dotfiles/scripts/skills/link-dotfiles-skills.sh` (prunes the global link), remove a leftover `~/.agents/skills/<name>` symlink if present, commit |
| `local` | nothing (untracked real dir in `~/.claude/skills`) | delete the dir; or move keepers into `~/dotfiles/.claude/skills/` so they become tracked and validated |

## Caveats

- Usage evidence is heuristic: Skill tool calls, slash commands, and
  SKILL.md reads found in transcripts. A skill invoked another way (or on
  another machine) can look unused.
- The window is bounded by transcript retention; the report prints the
  oldest transcript date. Roughly a month of history is typical.
- Zero uses is not automatically removable: reference skills (e.g. runtime
  contracts another skill depends on) and rarely-needed safety skills can
  be worth their tokens. Judge, don't just delete.
- Plugin skills are not scanned; manage those via `/plugin`.
- Cross-machine: skills used only on the other machine look unused here.
  Check before removing lock-file entries that sync via dotfiles.
