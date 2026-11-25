---
name: smart-skill-router
description: Route a user's task to the best currently installed skill or natural combination of skills without requiring skill names. Use for any task where an AI coding agent should inspect its available skills, select matching capabilities, respect confirmation boundaries, and fall back to general capability when no installed skill is suitable.
---

# Smart Skill Router

Apply a universal routing policy before executing a task. This is a skill-selection strategy, not a business-specific tool and not a substitute for the skills it selects.

## Route the task

1. Identify the user's real goal, relevant context, expected outcome, and risk level. Do not rely only on literal wording.
2. Inspect the skills available in the current environment. Do not assume an unlisted or uninstalled skill exists.
3. Compare likely skills by task fit, reliability, simplicity, and required permissions.
4. Prefer the best installed skill when it materially helps. Do not require the user to memorize or explicitly mention its name.
5. Combine multiple installed skills only when the task naturally forms a workflow and each skill has a clear role.
6. Follow every selected skill's instructions and resolve conflicts using the agent's instruction hierarchy and the user's explicit request.
7. If no installed skill fits, or a general approach is simpler and safer, proceed with general capability.

## Avoid forced routing

- Do not invoke a skill merely because it is available.
- Do not add setup, dependencies, or workflow steps without a concrete benefit.
- Do not stop because a specialized skill is missing when ordinary tools can complete the task.
- Do not invent capabilities, permissions, integrations, or installation state.
- Prefer the smallest set of skills that fully supports the goal.

## Respect confirmation boundaries

Proceed with ordinary read-only analysis, drafting, summarization, and scoped local file work when allowed by the host agent and user instructions.

Show the intended action and obtain confirmation before:

- sending messages, email, notifications, or other external writes;
- publishing, uploading, pushing, deploying, merging, approving, or submitting;
- deleting, overwriting, or moving important data;
- changing permissions, authentication, environment settings, or system state;
- accessing or exporting sensitive data beyond the scope the user specified;
- installing a new skill, plugin, dependency, or external integration.

Treat the host agent's stricter safety, approval, and sandbox rules as authoritative. Confirmation does not bypass those rules.

## Communicate the decision

When useful, briefly state which skill or skill combination is being used and why. If no skill fits, continue normally without making skill selection the focus. Report the result, where it is located, and any relevant next step.

## Compatibility

Apply this policy in Codex and in Claude Code, Cursor, OpenClaw, or another AI coding agent that can discover and read `SKILL.md`. Adapt installation and approval mechanics to the host agent; preserve the routing principles.
