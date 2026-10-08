---
name: agents-architect:skill
description: Author a single skill from a short brief. Use to add a skill to an existing plugin or iterate on a skill's description/body.
argument-hint: "<skill-name> \"<one-line purpose>\" [--plugin <path>] [--siblings <a,b,c>]"
allowed-tools:
  - Read
  - Write
  - Task
  - AskUserQuestion
---

<objective>
Fast path to a single, well-triggered skill without running full /agents-architect:new.
</objective>

<execution_context>
@${CLAUDE_PLUGIN_ROOT}/agents-architect/templates/skill.template.md
</execution_context>

<context>
Arguments: $ARGUMENTS — name, purpose, optional plugin path and sibling skills for disambiguation.
</context>

<process>
1. Parse args. If plugin path omitted, default to current working directory.
2. `AskUserQuestion` to fill gaps: target trigger phrases (10-30), examples of prompts that should fire it, examples that should NOT.
3. Spawn `agents-architect-skill-author` with the filled brief. It writes `skills/<name>/SKILL.md`, `reference.md` (if needed), `evals/`.
4. Report back the produced files + trigger surface.
</process>

<output>
Paths of produced files + 5-line summary.
</output>
