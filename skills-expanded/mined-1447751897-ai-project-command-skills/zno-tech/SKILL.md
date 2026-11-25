---
name: zno-tech
description: Use when the user writes /zno-tech or the work involves a major technical decision - frameworks, databases, cache, queues, auth, storage, payment, deployment, CI/CD, monitoring, or any heavy dependency. Presents 2-3 compared options, waits for user confirmation, records the decision in docs/engineering/04-tech-decisions.md, then implements.
---

# Zno-Tech — Technical Selection Gate

Never silently pick major technology. This command runs the selection gate explicitly; other commands invoke the same gate when they hit a major choice.

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Read `<skills-root>/zno-init/references/tech-gate.md` for the gate scope, the required recommendation format, and performance-aware design rules.
2. State the technical need and constraints, then present 2-3 viable options with purpose, pros, cons, performance impact, cost, maintenance complexity, risks, and rollback — in the format from the reference.
3. Recommend one option and explain why.
4. Wait for user confirmation, unless the user explicitly specified the technology and explicitly waived comparison. (In `--super` goal mode, decide autonomously and record in `docs/development/14-decision-log.md`.)
5. After confirmation, record the decision in `docs/engineering/04-tech-decisions.md`. If that doc does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold tech
   ```

6. Implement, then satisfy the verification gate in `references/verification.md` before marking the work complete.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/tech-gate.md` — gate scope, recommendation format, performance-aware design.
- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
