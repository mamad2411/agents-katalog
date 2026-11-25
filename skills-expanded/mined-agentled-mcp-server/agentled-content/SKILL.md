---
name: agentled-content
version: 0.2.2
description: Use when drafting, revising, or planning content from authenticated AgentLed workspace context or a caller-selected local root.
category: content
allowedApps: kg
allowedActions: kg.read-text, kg.read-list, kg.get-rows-by-ids, kg.upsert-rows
relevanceKeywords: content, draft, editorial, brand, workspace template
---

# AgentLed Content

The user's explicit content goal is the instruction for this turn and takes precedence over starter suggestions. AgentLed supplies authenticated workspace context and allowed tool bindings; no local root is required. Hermes supplies a caller-selected root and its tool bindings.

## AgentLed host boundary

In AgentLed, use only authenticated current workspace context, knowledge, files, and allowed tools or actions. Never borrow context from another workspace. Load only company facts, brand guidance, editorial rules, or a named brief relevant to the explicit content goal; do not require a local root. Tool availability is advisory, not authority, and unavailable tools are not a reason to withhold useful grounded output. Use only tools and actions the host allows, and treat every external or durable action as separately gated.

## Hermes host boundary

Hermes supplies a caller-selected root and its tool bindings. Do not discover a root. Do not load global context. Do not select a nested root. Do not search sibling roots or infer context from another customer, brand, or repository.

Hermes-only optional guidance is available in [references/context.md](references/context.md), [tools.md](tools.md), and [templates/workspace](templates/workspace). AgentLed execution does not require or receive these relative files.

## Request-led path

1. Start from the explicit content goal.
2. Load only context relevant to that goal.
3. Ask at most the smallest necessary clarification when a missing answer prevents a useful result; otherwise produce the useful draft or review now.
4. Research only when it helps the requested result or the user asks for it. Never claim research or source verification that did not run.
5. When the user asked to keep, save, or prepare the result and the AgentLed host grants the existing private Knowledge tools, reuse the relevant workspace list, upsert the result with a stable identity, and read it back. This same-workspace private result save does not require a separate confirmation; never invent a list, schema, saved state, or link.
6. Return the draft or review, material assumptions, any verified private result link, and any evidence gap plainly.

If required context or a tool is missing, begin with `Partial result:`, preserve any useful grounded output, and give one recovery step.

## Optional starters

If no content goal is present, offer this short optional menu without choosing a default:

- Draft or revise an announcement, email, article, or other requested format.
- Turn an existing note or idea into a useful content draft.
- Prepare a LinkedIn draft for review.

## Repeatability boundary

Ordinary drafting or revision creates no workflow. Create or propose a workflow only after the user explicitly asks to make the process repeatable. A possible future cadence is not an explicit repeatability request.

## Separate action boundaries

Private same-workspace persistence of the requested result follows the host's existing Knowledge permission. Publishing, scheduling, sending, provider connection, changing durable preferences, asset generation, and credit spend are separate explicit and approval-gated actions. Approval for one action grants no authority for another. Do not perform any of them automatically while drafting or revising.

Acme and Northstar in the optional Hermes templates are synthetic fixtures, not live accounts. One-off requests remain one-off and do not alter durable brand preferences.
