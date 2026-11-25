---
name: skill-evolver
description: "evolution, evolver, evolve, skills, run, check, status, skill 進化, 跑進化, 進化報告"
version: 0.1.0
tools: Bash, Read
argument-hint: "run [--max-skills N --max-rounds N] | status | ledger | dry-run"
disable-model-invocation: true
io:
  input:
    - mime: "text/plain"
      description: "Subcommand and optional parameters"
  output:
    - mime: "text/markdown"
      description: "Evolution report or status output"
---

# Skill Evolver

AutoResearch-inspired overnight skill evolution engine. Frozen eval metrics
that agents cannot modify + keep/discard loop with git-backed experiment tracking.

## Subcommands

### run — Execute evolution loop

```bash
~/.local/bin/python3 ~/workshop/stations/skill-evolver/cli/skill_evolver.py run \
  --max-skills 5 --max-rounds 10
```

Options:
- `--max-skills N` — Max skills per run (default: 5)
- `--max-rounds N` — Max mutation rounds per skill (default: 10)
- `--json` — Output JSON results
- `--config PATH` — Custom config JSON

### status — Show latest report

```bash
~/.local/bin/python3 ~/workshop/stations/skill-evolver/cli/skill_evolver.py status
```

### ledger — View experiment history

```bash
~/.local/bin/python3 ~/workshop/stations/skill-evolver/cli/skill_evolver.py ledger --last 20
```

### dry-run — Preview without executing

```bash
~/.local/bin/python3 ~/workshop/stations/skill-evolver/cli/skill_evolver.py dry-run
```

## SDK Usage

```python
from sdk_client.skill_evolver import SkillEvolverClient

client = SkillEvolverClient()
targets = client.dry_run()
results = client.run(max_skills=1, max_rounds=2)
report = client.status()
```

## Architecture

- **Frozen evals**: `stations/skill-evolver/frozen_evals/` (quality_judge + scoring_rubric)
- **Golden cases**: `stations/skill-evolver/golden_cases/{skill}/cases.json`
- **Evolution directions**: `stations/skill-evolver/evolution.md` (human-authored)
- **Ledger**: `~/.claude/data/skill-evolver/evolution_ledger.json`
- **Reports**: `stations/skill-evolver/reports/evolution-YYYY-MM-DD.md`
- **Cronicle**: Nightly at 02:00 (event: ws-skill-evolution)

## Adding Golden Cases for a Skill

Create `stations/skill-evolver/golden_cases/{skill-name}/cases.json`:

```json
{
  "skill": "skill-name",
  "cases": [
    {
      "id": "case-01",
      "input": "test input for the skill",
      "expected_traits": ["trait 1", "trait 2"],
      "weight": 1.0
    }
  ]
}
```

## Mutation Themes

Each round applies ONE theme: `simplify` | `clarify` | `restructure` | `example_tune` | `constraint`

## Budget

Default: 5 skills x 10 rounds = 50 eval calls/night. LLM-as-Judge uses Haiku.
