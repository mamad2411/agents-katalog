---
name: org-weekly
description: Run weekly automation scripts (weekly synthesis, self-reflection). Use when user asks for weekly synthesis or /org-weekly.
---

# Weekly Organization Skill

Runs weekly synthesis and self-reflection scripts.

## Usage

```bash
python3 _scripts/org_skill.py --weekly
```

## Options

- `-s, --skip s1,s2`: Skip specific scripts

## Scripts

weekly_synthesis.py (self_reflection.py run separately via /skill reflect)
