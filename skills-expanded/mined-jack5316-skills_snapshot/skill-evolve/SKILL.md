---
name: skill-evolve
description: Score skill fitness with GDI and auto-improve SKILL.md files using the gene pool (EvoMap) and compounding cycles (BotLearn). Use when user asks to improve skills, audit the skill ecosystem, run skill evolution, check skill health, or /skill-evolve.
---

# Skill Evolution (/skill-evolve)

Full EvoMap + BotLearn self-evolution loop for the PAI skill ecosystem:

**EvoMap GDI scoring** — every skill gets a fitness score:
```
GDI = usage_frequency(35%) + recency(30%) + content_quality(20%) + trigger_clarity(15%)
```

**Gene pool (compounding)** — proven improvement strategies accumulate in `_logs/gene_pool.json`.
Each successful improvement extracts a gene. Future improvements try matching genes first
(free, deterministic) before AI generation. Confidence grows with each application.

**BotLearn loop** — every evolution cycle makes the system smarter and cheaper to run.

## Usage

```bash
# View GDI fitness scores for all 130+ skills
python3 _scripts/skill_evolution.py fitness

# Show only high-priority skills (GDI < 0.3)
python3 _scripts/skill_evolution.py fitness --priority high

# Improve a skill (tries gene pool first, then AI fallback)
python3 _scripts/skill_evolution.py evolve --skill <name>

# Batch-improve all high-priority skills
python3 _scripts/skill_evolution.py evolve --all --priority high --confirm

# View the gene pool (proven strategies)
python3 _scripts/skill_evolution.py gene list
python3 _scripts/skill_evolution.py gene stats

# Find scripts/patterns that need new skills
python3 _scripts/skill_evolution.py synthesize

# Weekly fitness report (also runs automatically via /org-weekly)
python3 _scripts/skill_evolution.py report
```

## Evolution Loop

```
skill_tracker_hook.py → _logs/skill_usage.json
         ↓
skill_evolution.py fitness   (GDI scoring, no AI)
         ↓
skill_evolution.py evolve    (gene pool first → AI fallback)
         ↓
extract gene → _logs/gene_pool.json   (confidence compounds)
         ↓
next cycle: gene pool is smarter
```

## Output

- `_logs/skill_usage.json` — usage events (auto-populated by UserPromptSubmit hook)
- `_logs/gene_pool.json` — compounding library of proven strategies
- `_logs/skill_backups/{skill}/{ts}/SKILL.md` — pre-improvement snapshots
- `_logs/skill_evolution_applied.json` — improvement history
- `Sources/Skill Fitness Report - YYYY-MM-DD.md` — weekly report
