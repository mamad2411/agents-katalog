---
name: find-skills-pro
description: Search, evaluate, and select external agent skills from skills.sh, GitHub repositories, curated lists, and local skill packs. Use when the user asks whether external skills are useful, wants to find professional skills, compare skill repositories, or improve the current skill pack with outside sources.
---

# Find Skills Pro

## Workflow

1. Identify the capability gap: what task needs a better skill?
2. Search trusted sources first: official repositories, known maintainers, skills.sh, GitHub, curated lists.
3. Inspect repository health: license, update activity, stars/forks only as weak signals, structure, and safety.
4. Inspect skill quality: trigger description, workflow, checks, avoid rules, output contract, and bundled resources.
5. Decide: `Add`, `Adapt`, `Merge`, `Skip`, or `Monitor`.
6. If adapting, distill only the reusable method into the local skill style.

## Evaluation Criteria

- Clear trigger and use case.
- Repeated value for current projects.
- Low overlap with existing skills.
- Concise instructions with concrete workflow.
- Safe commands and no suspicious hidden behavior.
- License compatible with local usage.
- Easy to maintain.

## Output

```markdown
判断：Add | Adapt | Merge | Skip | Monitor

理由：
- ...

建议落点：
- ...
```
