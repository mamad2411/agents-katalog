---
name: build-buy-analysis-stinger
description: "Compare build, buy and partner approaches for one defined function using requirements, dated evidence, lifecycle costs, ownership and exit constraints."
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork. Advisory analysis; no runtime dependencies.
metadata:
  hive-drone: build-buy-analysis-wasp-drone
  pair-drone: build-buy-analysis-wasp-drone
  domain: product sourcing
---

# Build, buy or partner analysis

## Purpose and triggers

Prepare one conditional sourcing recommendation for a defined functional slice. Use when a user asks whether to build a feature internally, license an existing product or engage a delivery partner, or wants to compare lifecycle cost, integration, operating responsibility and exit constraints.

## Procedure

1. Read [README](README.md), [topic](references/topic.md), [distillation](references/research/distillation.md) and all three linked guides. Ask a compact batch for missing requirements and owner inputs.
2. Use [scope guide](guides/01-bound-the-decision.md) to define one job and shared mandatory acceptance IDs across the approaches.
3. Use [comparison guide](guides/02-compare-lifecycle-and-exit.md) and [worksheet](references/templates/decision-worksheet.md) to separate documented capability, supplied contract/quote, sales statement, assumption and observed proof. Keep unknowns visible.
4. Use [decision guide](guides/03-recommend-and-handoff.md) for one conditional recommendation or one decision-changing evidence task. Check the [fictional example](examples/completed-decision.md) and [negative cases](examples/negative-cases.md); neither proves actual execution.
5. Deliver the local advisory report with evidence dates, required unknowns, partial costs, responsibilities, exit constraints, reversibility and specialist review status.

## Scope and selected owners

Demand validation belongs to Discovery; public market discovery to Competitive Research; staffing to Capacity Planning; pricing and quotes to economics owners; contract/license/security applicability to their specialists; implementation to runtime owners. This skill does not author a PRD, negotiate or sign contracts, select a real vendor without buyer inputs, promise ROI/security/license rights, implement applications, create accounts, enter credentials, execute trials or spend.

Load Pest Controller before dispatch. Source uses plugin-catalog.json; installed work resolves the explicit selected owner through trusted Core. Report missing capabilities before dependent conclusions. Respect other agents' file ownership. Write only the requested advisory output; a read-only Drone returns report content for the authorized parent to save.

## Evidence map

Primary source hashes, raw archive and [paired Drone](../../agents/build-buy-analysis-wasp-drone.md) support review. Harness formats reuse Queen's research; current installed-session availability requires separate proof.

<!-- Ship Gate removed: research-only runtime, produces no application code or provider writes. Source component construction requires parent Security then Quality and orchestrator repository health before authorized commit/push. -->

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [guide map](README.md) - Resolve related selected owners through Pest Controller before dispatch; unavailable owners remain explicit gaps.
