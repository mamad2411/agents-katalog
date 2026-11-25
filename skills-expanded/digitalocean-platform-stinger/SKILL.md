---
name: "digitalocean-platform-stinger"
description: "Recommend DigitalOcean App Platform or Droplet fit from supplied workload, data, operator and recovery needs. Prepare dated cost inputs and readiness handoffs; no provisioning."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; accessible official-source reading required."
metadata:
  hive-tier: specialist
  hive-drone: digitalocean-platform-wasp-drone
  pair-drone: digitalocean-platform-wasp-drone
  domain: infrastructure-decision
  mode: research-only
---

# DigitalOcean platform fit

## Purpose

Produce one DigitalOcean topology recommendation or a clearly provisional intake, with workload eligibility, operator duties, recovery gaps and dated cost-owner handoff. Read [README.md](README.md) for the guide map.

## When to use

- "Does DigitalOcean fit this workload?"
- "Should this use App Platform or a Droplet, and which responsibilities remain?"
- "What data, backup, load balancing and transfer inputs must I prepare?"

## Boundaries

Broad multi-provider selection belongs to Infrastructure Fit; cash/labor arithmetic to Operating Cost; actual container/CI work to DevOps, data design to DB, and risk review to Security. This capability performs public-source advisory research. It does not provision, enter credentials, create accounts, install tools, change configuration/settings, spend, deploy, migrate, destroy, publish, commit or run provider API probes.

## Procedure

1. Follow [normalize workload](guides/01-normalize-workload.md) and the [worksheet](references/templates/topology-cost-readiness.md). Preserve unknowns, date/account cohort and workload units. Missing actual workload yields PENDING_WORKLOAD and one compact decisive question.
2. Follow [select topology](guides/02-select-topology.md). Compare current App Platform/Droplet eligibility and separately evaluate managed data. Check state/native/protocol/jobs/region/scaling and operational ownership before price.
3. Read the [digest](references/research/distilled-digitalocean.md) and [responsibility map](references/service-responsibilities.md). Refresh exact current source/rates/edition transition eligibility for the decision date. No universal cheapest, fastest, compliance or recovery guarantee.
4. Follow [cost and readiness handoff](guides/03-cost-and-readiness-handoff.md). Resolve selected owners, send sourced cost rows without introducing another calculator, return one provisional or supported advisory recommendation and explicit unavailable implementation/proof.
5. Review against [fictional fit](references/examples/fictional-fit.md) and [negative cases](references/examples/negative-cases.md). Distinguish manually reviewed examples from unexecuted runtime, provider and native-host checks.

Runtime is research-only. Ship Gate removed: advice does not implement application code. Parent owns source promotion, registration and independent Security then Quality, followed by orchestrator repository-health review before any separately authorized commit.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): resolve selected Infrastructure Fit, Operating Cost, DevOps, DB and Core Security before their handoffs.
