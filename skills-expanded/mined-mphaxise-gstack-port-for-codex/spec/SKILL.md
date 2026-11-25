---
name: spec
description: Turn vague intent into a precise, executable spec, issue, or implementation brief for Codex work.
---

# Spec

Use this skill when the user asks to spec something out, write a ticket, create an issue, or turn an idea into an executable implementation brief.

This port is adapted from `garrytan/gstack` at commit `11de390be1be6849eb9a15f91ff4922dd16c589a`.

## Workflow

1. Define the outcome:
   - user-visible goal
   - success criteria
   - non-goals
   - expected artifact or code surface
2. Ground the spec in current context:
   - read relevant files
   - inspect existing patterns
   - identify constraints, owners, and dependencies
3. Write the executable spec:
   - problem
   - proposed behavior
   - acceptance criteria
   - implementation notes
   - validation plan
   - rollout or migration notes when needed
4. If the user asked for an issue, create issue-ready Markdown. If they asked for implementation, proceed into the work after the spec is clear.
5. Preserve open questions separately from decisions so the next agent can act without re-discovering context.

## Codex Adaptation

- Codex does not need Claude plan-mode handoffs; use the current conversation, repo reads, and normal Codex planning/tooling instead.
- Do not spawn a separate worktree or GitHub issue unless the user explicitly asks.
- Prefer a compact spec that can become a commit plan, PR description, or tracker item.

## Guardrails

- Do not turn uncertainty into fake requirements.
- Do not write a marketing brief when the user needs an engineering spec.
- Do not over-spec implementation details that the codebase already constrains.
- Do not create or mutate remote issues without explicit approval.
