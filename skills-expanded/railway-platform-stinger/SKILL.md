---
name: railway-platform-stinger
description: "Select Railway from supplied workload, state, jobs, networking, cost inputs and recovery duties. Return one sourced recommendation or provisional choice and owner gaps."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; official-source reading required."
metadata:
  hive-tier: specialist
  paired-drone: railway-platform-wasp-drone
  hive-drone: railway-platform-wasp-drone
  pair-drone: railway-platform-wasp-drone
  domain: infrastructure-decision
  mode: research-only
allowed-tools: Read Glob Grep WebFetch WebSearch
---

# Railway platform fit

## Purpose

Recommend Railway only against supplied runtime, storage, job, network, region, budget and recovery requirements. Produce a reviewable decision and cost-owner payload with operator duties and unresolved proof.

## When to use

Use for "Does this workload fit Railway?", "Choose Railway for our API and workers", "Can Railway volumes and replicas satisfy this topology?", or "What must we price and operate before selecting Railway?"

## Boundaries

No supplied workload means provisional choice or a batched question. This is read-only advice: no installation, accounts, credentials, provider writes, paid resources, settings, provisioning, deployment or publication. Deployment belongs to the selected authorized implementation owner, or is reported as a precise owner gap.

## Procedure

1. Read [README.md](README.md) and [qualify workload](guides/01-qualify-workload.md). Fill the [worksheet](references/templates/fit-worksheet.md) with supplied facts and unknowns.
2. Apply the sourced runtime, volume/replica, job cadence/exit, private-network and region constraints. Trace disputed facts to the [digest](references/research/distilled-railway.md), ledger and raw archive. Refresh sources for a real task.
3. Follow [cost envelope](guides/02-cost-envelope.md). Preserve units, scenarios and aggregate plan-floor semantics; resolve selected Operating Cost for arithmetic. Unknown costs remain unpriced.
4. Follow [decision and handoff](guides/03-decision-and-handoff.md). Give one supported or provisional recommendation, operator responsibilities, RPO/RTO/export proof, reassessment triggers and actual implementation-owner gap.
5. Review the [fictional case](references/examples/fictional-case.md) and [negative cases](references/examples/negative-cases.md). Return report text; the authorized caller saves it. Source review proves no native/customer behavior.

## Related drones and stingers

- [Paired Drone](../../agents/railway-platform-wasp-drone.md) - Read-only Railway research and decision report.
- [Owner resolution](README.md#ownership-and-host-scope) - Infrastructure Fit, Operating Cost, Network Boundaries, DB/security and authorized deployment owners.

Runtime is research-only. Source changes go through ordered Security, Quality and Health review.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Owner resolution](README.md#ownership-and-host-scope) - Resolve selected specialists through trusted Core/catalog rather than assuming a cached installation.
