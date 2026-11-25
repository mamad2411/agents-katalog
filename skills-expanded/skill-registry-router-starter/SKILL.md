# Skill Registry Router Starter

Use this skill to route a free-text scientific task query to the most relevant skills in the local registry.

## What it does

- Loads `registry/skills.jsonl` and `registry/aliases.json`.
- Scores skills by alias phrases, tags, topic paths, and token overlap.
- Returns a ranked list of candidate skills with matched evidence and short rationales.

## When to use it

- You need a lightweight agent-orchestration layer over the skill library.
- You want a deterministic local router before handing control to a larger planning agent.

## Example

```bash
python3 skills/scientific-agents-and-automation/skill-registry-router-starter/scripts/route_skill_query.py \
  --query "single-cell marker ranking" \
  --top-k 3
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/scientific-agents-and-automation/skill-registry-router-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_cross_cutting_domain_skills -v`
