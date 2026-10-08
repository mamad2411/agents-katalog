---
name: self-augmentation
description: Protocol for discovering, loading, and creating specialized skills at runtime — scan for and load relevant skills before tasks needing domain expertise, pass skills to sub-agents, and capture recurring patterns as new skills.
triggers:
  - "skill discovery"
  - "loading skills"
  - "self-augmentation"
  - "specialized expertise"
  - "how to use skills"
---

# Self-Augmentation Protocol

Discover and load specialized skills when a task needs domain expertise.

## When to act

- **Task mentions any technology/framework/library/tool** (Docker, React, TensorFlow, …) → invoke `scan_skills` with query='that technology' immediately.
- **Delegating to sub-agents** → include `load_skill=[...]` in `call_agent`.
- **You notice a recurring pattern worth capturing** (multi-step procedure, domain knowledge not covered by existing skills, ≥5 tool calls with a coherent workflow) → load the `skill-creator` skill for instructions, then create the new skill via `propose_skill`.
- **You hit an unrelated bug/issue in the harness or project you're working on** (not part of your task) → don't fix it inline; log it via the `bug-tracker-entry-format` skill so it's tracked separately.

## Tool reference

- **`load_skill`**: loads skills into YOUR context. Takes a list of names (e.g. `["docker-best-practices"]`).
- **`call_agent` with `load_skill` param**: loads skills into SUB-AGENT context, same format.
  ```
  call_agent(agent_class="coder", task="Set up Dockerfile", load_skill=["docker-best-practices"])
  ```

## Workflow

1. **Scan** — `scan_skills` with a query matching the requirements.
2. **Load** — `load_skill` to inject expertise.
3. **Execute** — follow loaded guidelines.
4. **Delegate** — pass relevant skills to sub-agents when needed.
5. **Improve** — after using a skill, if you spot issues or gaps, submit a new version under the same name via `propose_skill`.

## Project memories

Skills are cross-project reusable procedures ("how to do X"). Project memories are facts specific to the current project ("what happened with Y", "architecture decision Z") — markdown files in `.agent_lessons/` (the standard per-project memory location).
- **When debugging X** → grep for X and related terms in `.agent_lessons/` before starting fresh.
- **Working on a known component** → check if past investigations exist before reinvestigating (e.g. grep "compression" when fixing compression bugs).
- **You get `[MEMORY HINT]` hits** → actually read the referenced lesson files before proceeding; they usually contain the exact gotcha you're about to hit.
- **Before saving a new memory** → load the `project-memory-writing` skill for formatting guidance.
- Use Obsidian-style backlinks `[[memory-name]]` to connect related memories; they're lightweight and discoverable via plain-text search.

Skills teach you HOW to work; project memories tell you WHAT already happened here.
