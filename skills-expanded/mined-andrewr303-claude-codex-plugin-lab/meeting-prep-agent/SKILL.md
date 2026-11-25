---
name: meeting-prep-agent
description: Run a Codex meeting-prep workflow that combines CRM and market context with reviewed client materials to produce an advisor briefing memo and slide deck.
---

# Meeting Prep Agent Task Pack

Use this task pack when the user needs an internal briefing pack ahead of a client or prospect meeting.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/wealth-management/` and `codex/skills/financial-analysis/`
- use [`docs/runtime/presentations.md`](../finance-modeling-office-pro/references/runtime-presentations.md) for deck production discipline

## Inputs

Minimum inputs:

- client or prospect name
- meeting date
- objective of the meeting

Optional inputs:

- local account statements or inbound materials
- agenda or CRM notes
- preferred deck template

## Output Contract

Primary artifacts:

- `./out/briefing-<client>.pptx`
- `./out/briefing-<client>.md`

Supporting scratch files are allowed under:

- `./out/tmp/meeting-prep-agent/`

## Connector Gate

Preferred connectors:

- `crm`
- `capiq`

If one or both connectors are unavailable, continue with local notes and public context only if that fallback is acceptable for the meeting. State the reduced confidence explicitly.

## Task-Pack Flow

1. Scope the meeting and participants.
2. Pull the structured profile and account context.
3. Review untrusted external materials and current news.
4. Draft the advisor briefing.
5. Build the deck and stop for advisor review.

## Phase 1: Scope The Meeting

- Confirm whether the meeting is a review, prospect pitch, or issue-management conversation.
- Confirm whether the output is advisor-internal only.
- Label client-provided files and inbound emails as untrusted inputs.

## Phase 2: Pull Structured Profile

Target artifact:

- `./out/tmp/meeting-prep-agent/profile-packet.md`

Use:

- `client-review`
- `client-report`
- `investment-proposal` when the meeting is a prospect or re-allocation pitch

Capture:

- relationship context
- account status
- current holdings or proposal scope
- outstanding actions

If delegation is available and explicitly authorized, this phase maps to `briefing-profiler`.

## Phase 3: Review External Materials And News

Target artifact:

- `./out/tmp/meeting-prep-agent/news-and-materials.md`

Rules:

- summarize only facts relevant to the meeting
- keep raw client-provided materials out of the final deck unless validated
- separate sourced facts from inferred talking points

If delegation is available and explicitly authorized, this phase maps to `briefing-news-reader`.

## Phase 4: Draft The Advisor Briefing

Write:

- `./out/briefing-<client>.md`

The memo should cover:

- meeting objective
- client profile summary
- recent portfolio or proposal context
- current market context
- recommended talking points
- open questions

## Phase 5: Build The Deck And Stop

Write:

- `./out/briefing-<client>.pptx`

Use `pptx-author` conventions and verify the deck visually per [`docs/runtime/presentations.md`](../finance-modeling-office-pro/references/runtime-presentations.md).

If delegation is available and explicitly authorized, the final memo and deck phase maps to `briefing-pack-writer`.

Stop after the memo and deck are complete. This pack is for internal meeting preparation, not for direct client distribution without human review.
