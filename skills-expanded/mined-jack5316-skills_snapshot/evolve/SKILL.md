---
name: evolve
description: Run system self-evolution cycle (SEAI framework). Use when user asks for self-evolution, system improvement, SEAI cycle, /evolve, or to analyze evolution history.
---

# Self-Evolution (/evolve)

7-phase SEAI cycle: Analyze → Reflect → Generate improvements → Learn → Adapt → Evaluate → Plan next.
Feeds into the gene pool: successful strategies become reusable genes for future cycles.

## Usage

```bash
# Single evolution cycle (safe mode — asks before applying)
python3 _scripts/self_evolution.py cycle --safe

# Multiple continuous cycles
python3 _scripts/self_evolution.py continuous --iterations 3 --safe

# View evolution history and trends
python3 _scripts/self_evolution.py analyze --iterations 5 --report
```

## Self-Evolution Stack

```
/reflect      → observe system behavior        (self_reflection.py)
/evolve       → generate system improvements   (self_evolution.py)  ← here
/insights     → manage insight lifecycle       (insight_enhancement.py)
/skill-evolve → score + improve skills + genes (skill_evolution.py)
/gene         → view and apply proven genes
```

## Output

`_logs/evolution_log.json` — full iteration history with phases, improvements, and metrics
