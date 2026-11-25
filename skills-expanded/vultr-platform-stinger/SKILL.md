---
name: "vultr-platform-stinger"
description: "Assess Vultr workload fit, compute forms, operator duties, data/recovery and dated cost inputs. Use for a read-only Vultr recommendation. Read README.md for guides."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; official-source reading required."
metadata:
  hive-tier: specialist
  paired-drone: vultr-platform-wasp-drone
  hive-drone: vultr-platform-wasp-drone
  pair-drone: vultr-platform-wasp-drone
  domain: infrastructure-decision
  mode: research-only
allowed-tools: "Read Glob Grep WebFetch WebSearch"
---

# Vultr platform fit

## Purpose

Select one provisional or documented Vultr compute/service form for a supplied workload. Explain eligibility, operator duties, data/network/recovery gaps and dated cost-owner inputs without claiming availability, performance or a price quote.

## When to use

- "Does Vultr fit this workload?"
- "Which Vultr compute form suits this CPU/GPU worker and storage needs?"
- "What would I operate and recover myself on Vultr?"

## When not to use

- Multi-provider topology comparison: selected Infrastructure Fit.
- Cost calculation: selected Operating Cost; supply its dated rate contract.
- Account/API inspection, provisioning, credentials, purchases, settings, installation, deployment, recovery execution or deletion: no authority in this advisory skill.
- Security/compliance/SLA certification or a claim of customer-cloud proof.

## Procedure

1. Read [README.md](README.md), [classify-workload](guides/01-classify-workload.md) and the [worksheet](references/templates/workload-decision.md). Gather supplied runtime, lifecycle/state, CPU/GPU, storage, network, geography, traffic, RPO/RTO and operator constraints. Missing workload yields provisional status.
2. Check exact compute/service eligibility with fresh official body evidence. Preserve the [digest](references/research/distilled-vultr.md) limits; no unsupported plan or regional inventory inference.
3. Follow [responsibilities](guides/02-review-responsibilities.md). Assign data/network/security and recovery/exit duties; separate instance snapshots, automatic backups, volume recovery and managed database entitlements.
4. Follow [decision and cost handoff](guides/03-deliver-decision.md). Resolve selected owners by name through trusted Core, supply dated units/allowances and leave rate or billing conflicts unpriced. Produce no calculator.
5. Return ONE supported/provisional/unsupported recommendation and its decisive evidence, responsibility map, recovery proposal, cost gaps and review triggers. Check the [fictional scenario](references/examples/fictional-scenario.md) and [negative cases](references/examples/negative-cases.md).
6. Report advisory/static proof only and list unexecuted customer acceptance tests. Return in chat; an authorized orchestrator saves the agreed local Library report. Missing reading/selected-owner capability is a gap, not permission to install or activate it.

## References map

- Raw source ledger: own fetched URLs, timestamps and hashes.
- Raw archive: substantive body provenance and fetch-failure evidence.
- [Paired Drone](../../agents/vultr-platform-wasp-drone.md): bounded read-only delegation.

Runtime is research-only. Ship Gate removed: this advisory workflow produces no application-code or provider changes. Parent owns source promotion, registration, ordered Security, independent Quality and parent Health reviews and any separately authorized commit.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support) - Resolve selected Infrastructure Fit, Operating Cost, Network Boundaries, DB, DevOps and Core Security before handoff.
