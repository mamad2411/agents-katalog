---
name: ambient
description: Use for ambient-library operations in Codex. Triggers on setting up ambient-library in a project, configuring project skills, updating or managing skills, code review, making a folder ambiently intelligent (stamping .aai or creating an ambient folder for a purpose), and any project-specific task covered by a canonical domain skill such as writing a project brief or summarizing a project.
---

# ambient

You are the Codex adapter for ambient-library.

ambient-library is a canonical library of agents, skills, and reusable
capabilities. This Codex skill is only a thin runtime wrapper. The canonical
router, subskills, and domain skills live outside this wrapper at:

```text
../../
```

Resolve that path relative to this `SKILL.md` file. Then read and follow the
canonical router:

```text
../../.aai/instructions.md
```

## Codex Adapter Rules

- Treat `../../` as the canonical library root.
- When the canonical instructions mention `${CLAUDE_PLUGIN_ROOT}`, translate it to
  the canonical library root above.
- When the canonical instructions say to use the `Read` tool, use normal Codex
  file-reading tools.
- Route to exactly one canonical subskill per request.
- For domain skill selection, read only
  `../../library/catalog.yaml` first.
- Load at most one domain skill body:
  `../../library/<skill-name>/instructions.md`.
- Never load the whole library to decide relevance.
- Merge project instructions from `AGENTS.md`, `CLAUDE.md`, or equivalent local
  project guidance before acting.
- Do not mention adapter internals, path translation, or routing mechanics unless
  the user asks how the system works.

The objective is runtime agnosticism: Codex gets one registered skill, while the
capability logic stays canonical and shared.
