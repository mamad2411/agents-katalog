---
name: gateway
description: Skill map and integration guide. Tracks existing skills, relationships, and how to integrate new skills. Clarifies Functions, Connections, Limitations, Guidance (FCLG) for each skill. Use when creating a new skill, navigating skills, understanding skill relationships, or /gateway.
---

# Gateway Skill

Generates a full skill map or FCLG analysis (Functions, Connections, Limitations, Guidance) for any skill. Use when creating a new skill to get integration guidance.

## Usage

```bash
python3 _scripts/gateway.py                                          # full skill map
python3 _scripts/gateway.py --skill rag                              # deep dive on one skill
python3 _scripts/gateway.py --integrate my-new-skill "description"  # integration analysis
python3 _scripts/gateway.py --save
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Full skill map with FCLG for all skills |
| `--skill NAME` | FCLG deep dive for one skill |
| `--integrate NAME "desc"` | Integration analysis for a newly created skill |
| `--save` | Save to `Maps/Skill Gateway.md` or `Maps/Gateway - {name}.md` |

## Workflow for New Skills

1. Create skill: implement script + SKILL.md + register in `skills.json`
2. Run: `python3 _scripts/gateway.py --integrate my-skill "description" --save`
3. Use the output to add to pipelines and connect to related skills

## Output

`Maps/Skill Gateway.md` (full map) or `Maps/Gateway - {skill}.md` (single/integration)
