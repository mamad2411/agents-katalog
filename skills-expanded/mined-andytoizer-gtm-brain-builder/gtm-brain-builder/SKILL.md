---
name: gtm-brain-builder
description: Orchestrate the creation or maintenance of a source-backed GTM brain for a company, including tool connection, section routing, Grill-me questions, session relay, section-agent sequencing, and recurring freshness workflows. Use when a user wants to build a GTM Brain or make one shareable/useful for sales, marketing, CS, support, and operators.
---

# GTM Brain Builder

Use this as the orchestrator. The goal is a usable operating brain, not a generic notes repo.

## Required First Moves

1. Read or create `README.md`, `AGENTS.md`, `systems/mvp-checklist.md`, `systems/sources.md`, `systems/tools.md`, `systems/grill-me.md`, and `projects/{operator}/building-the-brain/README.md`.
2. Set or refresh the MVP checklist before section work so the agent stays in "build the brain" mode until the MVP is complete.
3. Invoke or follow `$source-connector-inventory` before filling strategy sections.
4. Keep `$grill-me` always on for interpretation decisions.
5. Use `$session-relay` for long builds and handoffs.

## MVP Checklist Discipline

The orchestrator owns `systems/mvp-checklist.md`.

That file must make the current boundary obvious:

- `Current phase`: usually `Build the brain MVP`.
- `In scope`: source inventory, canonical docs, proof/ICP/messaging/tone/sales memory, relay, refresh design.
- `Out of scope until MVP complete`: launching campaigns, building operating dashboards, running GTM tasks, creating downstream website/deck/campaign assets, or adding automations that assume the brain is finished.
- `MVP checklist`: the concrete items required before the brain is usable.
- `Next checklist`: what the following session should do next.

At the start of each session, read the MVP checklist before doing work. Before handoff, update it with completed items and the next recommended checklist.

## Section-Agent Order

Run section work in this order unless the user has a sharper priority:

1. `$source-connector-inventory`
2. `$company-core-agent`
3. `$customer-icp-agent`
4. `$messaging-market-agent`
5. `$brand-voice-agent`
6. `$design-system-agent` when the user needs a brand kit, design-system brief, Claude.ai/design workflow, or Codex import instructions
7. `$sales-memory-agent`
8. `$freshness-automation-agent`

If actual subagents are available and the user explicitly asks for parallel agents, use the plugin-level agent definitions in `../../agents/` and split work by section with disjoint write scopes. Otherwise, act as the relevant specialist yourself and load only the relevant skill.

## Agent Hierarchy

- `../../agents/gtm-brain-orchestrator.md`: owns sequencing, MVP checklist, and handoff.
- `../../agents/source-connector-agent.md`: owns source coverage.
- `../../agents/company-core-agent.md`: owns company/product truth.
- `../../agents/customer-icp-agent.md`: owns customers, proof, and ICP.
- `../../agents/messaging-market-agent.md`: owns messaging and market.
- `../../agents/brand-voice-agent.md`: owns brand and speaker tone.
- `../../agents/design-system-agent.md`: owns design-system briefs, design tool workflows, and import guidance.
- `../../agents/sales-memory-agent.md`: owns sales memory.
- `../../agents/freshness-automation-agent.md`: owns refresh design.

## Decision Protocol

Before promoting interpretation into durable context, ask:

```text
Question:
My current best hypothesis:
Why this matters:
What changes depending on your answer:
```

Ask one question at a time. Use source work to make the question sharper.

## References

- Read `../../references/build-lessons.md` for distilled GTM Brain build lessons.
- Read `../../references/brain-section-map.md` before changing repo structure.
- Read `../../references/output-quality-rubric.md` before marking a section complete.

## Done State

A first usable GTM Brain has:

- MVP checklist with explicit non-goals and next checklist.
- Connected-source inventory and access gaps.
- Source priority and update rules.
- Company/product truth with approved and working claims separated.
- Customer/proof/ICP docs grounded in commercial, CRM, usage, and customer evidence.
- Messaging and market docs grounded in buyer language and proof.
- Brand and speaker-tone profiles separated from sales copy.
- Design-system brief and import notes when visual systems are in scope.
- Sales memory with campaign lessons and caveats.
- Session relay handoff and transcript archive policy.
- Proposed refresh cadence.
