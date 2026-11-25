---
name: ui-expert-audit-design
description: "AIgile UI Expert workflow — Audit design system compliance and consistency. Run it as the ui-expert agent."
argument-hint: "[context — story id, ticket key, file path, ...]"
disable-model-invocation: true
---

# 🖌️ Audit Design

AIgile workflow owned by the **UI Expert** (`ui-expert`) agent.

**Context for this run:** $ARGUMENTS

## Before you start

1. Adopt the `ui-expert` persona — read `.claude/agents/ui-expert.md` if you are not already that agent, or delegate this whole workflow with the `Agent` tool using `subagent_type: "ui-expert"`, or address it directly with `@agent-ui-expert`.
2. If the context above is empty or ambiguous, ask for what you need with `AskUserQuestion` before doing any work.
3. Track multi-step progress with `TodoWrite`.

## Goal

Audit design system compliance and consistency.

## Resources

Task definitions in `${CLAUDE_PLUGIN_ROOT}/core/tasks/` — follow the matching one exactly:

- `figma-audit-design-system.md`

Templates in `${CLAUDE_PLUGIN_ROOT}/core/templates/`: `front-end-spec-tmpl.yaml`

Checklists in `${CLAUDE_PLUGIN_ROOT}/core/checklists/`: `story-dod-checklist.md`

## Definition of done

- The artifact this workflow produces exists on disk (or the decision is written down), not just described in chat.
- Every applicable checklist item above is satisfied or explicitly waived with a reason.
- You state what you produced, where it lives, and what the next AIgile role should pick up.
