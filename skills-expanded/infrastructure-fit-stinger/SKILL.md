---
name: "infrastructure-fit-stinger"
description: "Recommend one infrastructure topology from workload, budget and operator skills. Compare managed hosting and VPS with sourced constraints and cost-owner handoff. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; accessible official-source reading required."
metadata:
  hive-tier: specialist
  hive-drone: infrastructure-fit-wasp-drone
  pair-drone: infrastructure-fit-wasp-drone
  domain: infrastructure-decision
  mode: research-only
---

# Infrastructure fit

## Purpose

Recommend one infrastructure topology from a normalized workload, budget and operator capacity. Explain the decisive fit, retained responsibilities, unknown costs, recovery/exit and expansion triggers. Provider preference is a constraint to test, not a universal ranking.

## When to use

- "Which infrastructure fits my app and budget?"
- "Should this run on managed hosting or a VPS?"
- "Does my worker/native backend fit Vercel, Cloudflare or container hosting?"
- "What operations and recovery work will this architecture need?"

## When not to use

- Provisioning, configuring, migrating or deploying: selected implementation owners need separate action authority.
- Full rate arithmetic: resolve selected Operating Cost and reuse its model.
- Product/framework decisions not yet supplied: resolve Builder Readiness/Web Stack Selection as applicable.
- Security/compliance/SLA certification: identify constraints and evidence gaps; use actual review owners.

## Procedure

1. Read [README.md](README.md) and [normalize-workload](guides/normalize-workload.md). Confirm runtime/lifecycle, data, geography, budget, operator and recovery constraints. Ask only missing facts that change eligibility.
2. Use the [intake worksheet](references/templates/workload-intake.md) for all candidates. Preserve estimates, units, CPU/wall distinctions, native requirements and continuous versus completion workers.
3. Apply [hosting comparison](guides/compare-hosting.md) and [discriminators](references/fit-discriminators.md). Retrieve current exact plan/runtime/region evidence. Missing source excludes an unsupported claim; Vultr is unqualified until applicable evidence exists.
4. Follow [data/network](guides/choose-data-network.md). Separate app compute from DB/storage, public/private access, secrets, backup/restore and security ownership. Defer layers without a product need.
5. Follow [cost handoff](guides/estimate-operations.md). Resolve selected Operating Cost with common workload, dated rate units and operator-time inputs. If unavailable, leave totals unresolved rather than duplicating a calculator or guessing prices.
6. Use [review-triggers](guides/review-triggers.md) and the [decision memo](references/templates/decision-memo.md). Give ONE supported or clearly provisional recommendation, operator duties, recovery/exit, missing proof and measured/owner-approved reassessment triggers.
7. Review against the [worked cases](references/examples/cases.md). State unpriced/untested limits. Selection is advisory and does not authorize accounts, credentials, purchases, configuration, provisioning or production effects.

## References map

- [Research digest](references/research/distilled-infrastructure-fit.md), raw ledger: factual grounding and fetch limits.
- [Envelope checker](scripts/check-envelope.py): archive/link and encoded contract checks; no current-cost calculation or runtime qualification.
- [Paired Drone](../../agents/infrastructure-fit-wasp-drone.md): delegation scope.

Runtime is research-only. Ship Gate removed: this workflow produces infrastructure advice rather than application-code changes. Source changes and commits receive ordered Security, Quality and Health review gates. A source checkout is not a selected installation.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): use selected Operating Cost, Launch Assets, DB/security/deployment owners through trusted Core rather than cached cross-pack paths.
