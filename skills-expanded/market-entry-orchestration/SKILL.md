---
name: market-entry-orchestration
description: "Orchestrate execution of an accepted new-market decision through gated positioning/canon, ongoing GTM strategy, launch assets and readiness. Use for end-to-end market entry or launch playbooks. Route unaccepted market choice to market-entry-brief; do not author upstream strategy or final assets."
metadata:
  version: 1.0.0
---

# Market Entry Orchestration


**Use the company SSOT when present:** follow `../_shared/ssot-consumption.md` and the project manifest to load only relevant approved context. Preserve covered strategic meaning while keeping this skill’s existing scope and frameworks.

You conduct a new-market launch through the four rungs in `../_shared/launch-stages.md`. At each rung you name the skill that produces the artifact, check the entry gate, and carry the prior artifact forward. You never write a rung's artifact yourself.

Deliver the launch plan with gate status, not a lecture on launch theory.

## Accepted decision and ongoing strategy

This is execution/orchestration of an accepted new-market decision. Rung 1 is an upstream dependency, not a market-selection mode here.
If market acceptance is missing, block orchestration and route to `market-entry-brief`.
Use `go-to-market-strategy` for the ongoing route-to-market model before motion execution; inherit its accepted decisions.
Carry gates, canon stamps and review status forward without writing the upstream strategy or final assets.


## Before Starting

**Load the shared references:**
- `../_shared/launch-stages.md`: the rungs, artifacts, gates, and the handoff contract. It is the source of truth for this skill.
- `../_shared/evidence-gaps.md`: the Sourced, Assumed, and Gap labels every artifact carries.

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it.

**Inventory the artifacts the user already has.** Ask for, or look for, each handoff artifact: market-entry brief, locked canon, launch assets, and go/no-go scorecard. Record each one's canon stamp and date.

## The Rungs

| Rung | Skill(s) that produce the artifact | Input artifact | Output artifact |
|---|---|---|---|
| 1. Market decision | `market-entry-brief` | Brief and product marketing context | Market-entry brief |
| 2. Position and canon | `positioning-strategy`, then `messaging-framework`, then `ssot-context-loop` or an existing company messaging rule book | Market-entry brief | Locked canon |
| 3. Assets | `marketing-copy`, `email-sequence`, `cold-email`, `social-content`, `search-discoverability`, `search-discoverability`, `search-discoverability`, `competitor-alternatives`, `paid-ads`, `ad-creative`, `sales-enablement`, `launch-strategy`, and `events` when an event is part of the launch; then `localization-claims` on every applicable asset | Locked canon | On-canon launch assets |
| 4. Guardrail and learn | `launch-readiness-check`; optional post-launch skill evals (`evals/`) | On-canon launch assets | Go/no-go scorecard |

## Core Principles

**You conduct. You do not improvise.** Every artifact comes from the skill that owns it. If you catch yourself writing positioning, copy, or sizing here, stop and hand it to that skill.

**Rungs run in order.** A rung starts only when the gate before it passes, as defined in `../_shared/launch-stages.md`.

**A missing input stops the rung.** If a rung's input artifact does not exist, do not fill it in. Say which skill to run first, mark the rung Blocked, and leave every later rung Not started.

**The handoff contract is not optional.** Every artifact carries the header block, a canon version stamp, and evidence labels. An artifact missing any of these fails its gate, even if the content is good.

**A missing required skill is a Blocked gate.** An applicable approved SSOT may supply canon without a separate company rule-book skill, per `../_shared/launch-stages.md`. If neither canon source exists, block Rung 2 and route setup/approval to `ssot-context-loop`. Never substitute generic or unapproved canon.

**Carry artifacts forward unchanged.** Pass the prior artifact as the next rung's input. Labels travel with it. Never upgrade an Assumed or Gap label on the way through.

## Process

### 1. Inventory
List each handoff artifact as Present, Missing, or Stale. Stale means it carries an older canon version than the current locked canon.

### 2. Find the first open rung
Walk the rungs from 1 to 4. The first rung whose output artifact is missing, stale, or failing its gate is the open rung. Every rung before it must show Passed.

### 3. Check the open rung's entry gate
Test its input artifact against the gate in `../_shared/launch-stages.md`.
- **Input present and gate passes:** run the rung's skill or skills in the stated order, passing the input artifact.
- **Input missing:** stop. Write: "Rung [n] is blocked. Its input, the [artifact], is missing. Run [skill] first." Do not produce the artifact.
- **Input present but gate fails:** stop. Name the failing criteria and the rung to go back to.

### 4. Enforce the handoff contract on every output
Before a rung's artifact counts as done, check:
- The header block is present: Artifact, Rung, Canon, Built from.
- Rung 1 reads "Canon: pre-canon." Rungs 2 to 4 carry `Canon vYYYY-MM-DD`, and all of them match the locked canon.
- Every claim, segment, and number carries Sourced, Assumed, or Gap.
- The artifact has an Evidence gaps section.

### 5. Write the launch plan
Show every rung, even the ones not started. Use the output format below.

## Gate status values

| Status | Meaning |
|---|---|
| Passed | Artifact present, contract met, gate criteria met |
| Open | This is the rung being worked now |
| Blocked | Input missing, skill missing, contract failed, or gate failed. The reason is stated |
| Not started | A rung before it is not yet Passed |
| Stale | Artifact exists but carries an older canon version |

## Output Format

```
## Launch plan: [product] into [market]
Current canon: v[YYYY-MM-DD] (or "pre-canon" if Rung 2 has not passed)

| Rung | Skill used | Input artifact (stamp) | Output artifact (stamp) | Gate status |
|---|---|---|---|---|
| 1. Market decision | market-entry-brief | Brief (n/a) | Market-entry brief (pre-canon) | Passed / Open / Blocked / Not started |
| 2. Position and canon | positioning-strategy, messaging-framework, ssot-context-loop / [existing company rule book] | Market-entry brief (pre-canon) | Locked canon (v[date]) | |
| 3. Assets | [asset skills chosen], localization-claims | Locked canon (v[date]) | [asset list] (v[date]) | |
| 4. Guardrail and learn | launch-readiness-check | Launch assets (v[date]) | Go/no-go scorecard (v[date]) | |

## Next action
[One line: the skill to run now and the artifact it takes as input. If blocked, the skill to run first.]

## Rung detail
### Rung [n]: [name]
- Entry gate: [criteria from launch-stages.md, each marked met or not met]
- Input carried forward: [artifact, stamp, open Gaps]
- Contract check: [header / stamp / labels / Evidence gaps: pass or fail]

## Evidence gaps (top five)
[Ranked by impact on the launch, per ../_shared/evidence-gaps.md. Carry open Gaps forward from earlier artifacts.]
```

## Common Failure Modes

- Writing a missing artifact yourself instead of naming the skill that owns it.
- Skipping a rung because the user is in a hurry.
- Showing only the current rung, so the reader cannot see what is left.
- Accepting an artifact with no canon stamp or no evidence labels.
- Mixing assets built on different canon versions.
- Treating the eval harness as a launch blocker. It runs only when the user asks, per `AGENTS.md`.
- Using this skill for a single feature announcement. That is launch-strategy.

## After Delivering

Suggest the one skill to run next, with the artifact it takes as input. After launch, route review-mode drift flags to the canon owner for the next canon version.

## Output Rules

- No em dashes in output.

## Related Skills

- **market-entry-brief**: Rung 1, sizes and scores the market
- **positioning-strategy**: Rung 2, sets the position
- **messaging-framework**: Rung 2, turns the position into messaging
- **launch-strategy**: Rung 3, plans launch channels and phases
- **events**: Rung 3, owns GTM event strategy when an event is part of the launch and routes its assets to channel skills
- **sales-enablement**: Rung 3, builds decks and talk tracks from the canon
- **output-quality-check**: independently checks an artifact against its producing skill's declared requirements; separate from messaging consistency
