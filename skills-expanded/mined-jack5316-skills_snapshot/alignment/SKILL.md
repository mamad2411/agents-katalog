---
name: alignment
description: Update a skill in a strategic, reflective, purposeful, and systematic way. Analyzes skills through the ALIGNMENT framework (Strategic, Reflective, Purposeful, Systematic) and produces actionable improvement recommendations. Use when you want to refine a skill, improve skill quality, or align a skill with PAI framework.
---

# Alignment Skill (/alignment)

Update skills in a **strategic, reflective, purposeful, and systematic** way. Analyzes existing skills through the ALIGNMENT framework and produces actionable recommendations for improvement.

## ALIGNMENT Framework

| Pillar | Focus |
|--------|-------|
| **Strategic** | Purpose alignment, PAI framework fit, layer coherence, integration with related skills |
| **Reflective** | Effectiveness, gaps, what works, improvement opportunities |
| **Purposeful** | Clear intent, user value, outcomes, success criteria |
| **Systematic** | Completeness, consistency, conventions, documentation, error handling |

## Quick Start

```bash
# Analyze a skill
python3 _scripts/alignment_skill.py rag

# Analyze and save report
python3 _scripts/alignment_skill.py ai-brief --save

# List available skills
python3 _scripts/alignment_skill.py --list
```

## Options

- `skill` — Skill name to align (e.g., rag, ai-brief, clean)
- `--list` — List all available skills
- `--save` — Save alignment report to `Sources/Alignment - Skill - YYYY-MM-DD.md`
- `--context TEXT` — Additional context for analysis (e.g., "User reports slow performance")

## Examples

```bash
# Basic alignment analysis
python3 _scripts/alignment_skill.py rag

# Save report for later reference
python3 _scripts/alignment_skill.py clean --save

# Add context about a specific issue
python3 _scripts/alignment_skill.py filter --context "Output format doesn't match other skills"

# See what skills exist
python3 _scripts/alignment_skill.py --list
```

## Output

- **Terminal**: Full alignment report with Strategic, Reflective, Purposeful, Systematic assessments and prioritized recommendations
- **Saved report** (with `--save`): `Sources/Alignment - Skill Name - YYYY-MM-DD.md`

## What It Analyzes

1. **skills.json** — Registration, description, commands
2. **SKILL.md** — Documentation completeness, accuracy, examples
3. **Python script** — Conventions, error handling, PAI alignment

## Related

- `/meta-skill` — Create new skills from scratch
- `/package` — Analyze overall skill configuration health
- CLAUDE.md — PAI framework and skill creation guidelines
