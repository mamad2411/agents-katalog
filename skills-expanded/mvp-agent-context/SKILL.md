---
name: mvp-agent-context
description: Generate Codex-first agent context files for a Web MVP. Use after the PRD and Technical Blueprint exist when the user needs AGENTS.md, REVIEW-CHECKLIST.md, and agent_docs for project brief, requirements, tech stack, page map, data model, build tasks, testing, and reusable prompts.
---

# MVP Agent Context

Generate the files a coding agent needs before implementation.

## Inputs

Read:

- `docs/BuildablePRD-*.md`
- `docs/TechBlueprint-*.md`
- Optional `docs/EvidencePack-*.md`

## Files

Create or update:

```text
AGENTS.md
REVIEW-CHECKLIST.md
agent_docs/
  project_brief.md
  product_requirements.md
  tech_stack.md
  page_map.md
  data_model.md
  build_tasks.md
  testing.md
  prompts.md
```

Use `templates/` from this repository as the starting point when available. Replace placeholders with project-specific details.

## Rules

- Keep `AGENTS.md` concise.
- Put detailed requirements in `agent_docs/`.
- Include safety rules: no delete, no auto-commit, no deploy, no real secrets, no out-of-scope features.
- Stop after generating context and ask whether to create build tickets.
