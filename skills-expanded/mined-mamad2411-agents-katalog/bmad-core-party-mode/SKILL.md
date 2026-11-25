---
name: bmad-core-party-mode
description: >-
  Use this skill to orchestrate interactive, multi-agent group discussions where
  all installed BMAD agents participate in character with authentic
  personalities, expertise, and communication styles. Invoke when the user says
  "party mode", "let's have a team discussion", or when another skill such as
  bmad-bmm-create-prd or bmad-bmm-create-architecture needs collaborative
  brainstorming from multiple expert perspectives on current step content. The
  skill loads the full BMAD agent roster, initializes each agent with their
  merged personality data, and facilitates a live conversation loop where 2-3
  agents respond per round based on domain relevance. Agents reference each
  other naturally, disagree where appropriate, and maintain professional
  discourse while staying in character. If discussion becomes circular,
  bmad-master summarizes and redirects. The session continues until the user
  chooses to exit, at which point each agent delivers a farewell and a session
  summary is produced.
metadata:
  bmad:
    module: core
    type: workflow
---

# Party Mode

Orchestrate group discussions between all installed BMAD agents, enabling natural multi-agent conversations with authentic personalities.

## Outcome

An engaging, interactive multi-agent conversation session where all installed BMAD agents collaborate in character, providing diverse expert perspectives on user-chosen topics until the user decides to end the session.

## Core Rules

- Always speak output in your agent communication style using the configured `{communication_language}`.
- Maintain strict in-character responses based on each agent's merged personality data (communicationStyle, principles, identity).
- Use each agent's documented communication style consistently throughout the session.
- Allow natural disagreements and different perspectives between agents.
- Include personality-driven quirks and occasional humor.
- Enable agents to reference each other naturally by name or role.
- Maintain professional discourse while being engaging.
- Respect each agent's expertise boundaries.
- If discussion becomes circular, have bmad-master summarize and redirect.
- Balance fun and productivity based on conversation tone.

## Execution Order

Follow these steps in order.

1. [Initialize](./steps/initialize.md) — Load config, parse agent manifest, build roster, activate party mode
2. [Orchestrate](./steps/orchestrate.md) — Interactive conversation loop with intelligent agent selection and cross-talk
3. [Exit](./steps/exit.md) — Agent farewells, session summary, graceful closure

## Halt Conditions

- HALT if the agent roster cannot be loaded via `bmad-agents` — the party cannot start without at least one agent persona
- HALT if the agent roster loads successfully but contains zero agents after parsing
- HALT if the user provides no topic or context for discussion after repeated prompting and no calling skill has supplied content to discuss

## When to Use

Use this skill when:
- The user requests party mode
- Another skill (e.g., `bmad-bmm-create-prd`, `bmad-bmm-create-architecture`) invokes it to apply collaborative brainstorming from different agent perspectives on current step content
- The user wants an engaging multi-agent conversation with all installed BMAD agents collaborating in character

## Boundaries

This skill should NOT:
- Break character or respond as a generic AI — every response must stay within each agent's documented communicationStyle, principles, and identity
- Allow discussion to continue circling the same points without bmad-master stepping in to summarize and redirect
- Allow agents to comment authoritatively outside their documented expertise domain
- Auto-exit the session — the session must continue until the user explicitly triggers exit via `[E]`, a recognized exit phrase, or natural conclusion
- Operate without a loaded agent roster — if `bmad-agents` returns zero agents after parsing, the session cannot start

