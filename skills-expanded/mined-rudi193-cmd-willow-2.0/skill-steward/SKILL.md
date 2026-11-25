---
name: skill-steward
description: Weekly external skill delta scan → SOIL triage queue → Grove #upstream. Phase 3 of skill surface strategy. Never auto-installs.
---

# Skill steward (phase 3)

**Policy:** Catalog and triage only. External `SKILL.md` trees are untrusted until a human marks `adopt` and phase-4 forks into Fylgja.

## When to use

- Weekly hygiene on `awesome-claude-skills`, Cursor `skills-cursor`, optional `~/.openclaw/skills`
- After pulling a large awesome-claude-skills update
- Before adopting a community skill into `willow/fylgja/skills/`

## Commands

```bash
willow.sh skills steward run-once          # respect 7-day interval
willow.sh skills steward run-once --force  # scan now
willow.sh skills steward run-once --dry-run
willow.sh skills steward status
willow.sh skills steward list
willow.sh skills steward show awesome-claude/foo
willow.sh skills steward dismiss awesome-claude/foo --reason "duplicate"
willow.sh skills steward adopt awesome-claude/foo --note "phase-4 fork"
```

## Weekly cron (local)

```cron
0 9 * * 1 cd ~/github/willow-2.0 && ./willow.sh skills steward run-once
```

Posts to Grove **`#upstream`** when there are new/changed external skills or queued triage items.

## OpenClaw tree (one-time)

```bash
willow.sh skills openclaw-setup              # sparse-clone + copy starter skills
willow.sh skills openclaw-setup --with-cli   # also npm install -g openclaw
```

Creates `~/.openclaw/skills/` with bundled starters (`clawhub`, `github`, `memory`, …).

## Scan roots

| Source | Path |
|--------|------|
| awesome-claude | `~/github/awesome-claude-skills/` (`WILLOW_AWESOME_CLAUDE_SKILLS` override) |
| cursor | `~/.cursor/skills-cursor/` |
| openclaw | `~/.openclaw/skills/` (after openclaw-setup) |

Classifier: `scripts/skill_catalog_scan.py` (execution class A–E, risk heuristics).

## Related

- `docs/SKILL_SURFACE_STRATEGY.md` — phases 0–5
- `agents/hanuman/bin/skill_steward.py` — implementation
- `willow/skill-catalog.jsonl` — phase-1 seed (50 skills)
