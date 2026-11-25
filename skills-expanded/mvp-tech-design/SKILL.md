---
name: mvp-tech-design
description: Create a practical Technical Blueprint for a Web MVP. Use after a buildable PRD exists when the user needs a stack decision, No-code vs AI-code vs Developer route comparison, architecture, setup commands, security baseline, testing plan, and cost/maintenance notes.
---

# MVP Technical Design

Create `docs/TechBlueprint-[AppName].md`.

## Inputs

Read `docs/BuildablePRD-*.md`.

Ask only for missing technical level, desired maintenance responsibility, monthly budget, launch deadline, data sensitivity, and required integrations.

## Default Routes

Evaluate:

- No-code route
- AI-code route, usually a Web stack like Next.js + managed backend
- Developer route

Choose the simplest route that satisfies the P0 features.

## Output

Include:

- Recommendation and route comparison
- Selected stack by layer
- Mermaid architecture
- Implementation notes by PRD feature
- Setup commands
- Security/privacy baseline
- Testing plan
- Cost and maintenance notes

## Rules

- Prefer maintainable defaults over novelty.
- Verify current pricing or mark costs as "verify current vendor page".
- Do not recommend complex infrastructure unless the PRD requires it.
