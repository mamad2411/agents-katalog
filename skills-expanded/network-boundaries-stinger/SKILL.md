---
name: network-boundaries-stinger
description: "Choose firewall, WAF and rate-limit placement from actual network flows. Return one sourced control recommendation with owner and proof gaps. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; official-source reading required."
metadata:
  hive-tier: specialist
  hive-drone: network-boundaries-wasp-drone
  pair-drone: network-boundaries-wasp-drone
  domain: network-boundaries
  mode: research-only
---

# Network Boundaries

## Purpose

Map a supplied topology to firewall, WAF, edge rate and application admission controls, then return one provisional or supported recommendation with actual boundary, identity, limits and owner/proof gaps.

## When to use

- "Which firewall, WAF and rate-limit layers fit this app?"
- "Where should public, private and admin traffic be controlled?"
- "Can clients bypass the proxy or spoof the identity used for limits?"

## When not to use

Hosting topology belongs to Infrastructure Fit; actual provider/WAF/ACL/OS changes to selected implementation owners; authorization/risk audit to Core Security; prices to Operating Cost. This pair does not configure, test traffic or certify enforcement.

## Procedure

1. Read [README.md](README.md), then [map flows](guides/map-flows.md); retain UNKNOWN listeners/ports and material questions when no topology is supplied.
2. Fill the [worksheet](references/templates/flow-control-worksheet.md) for ingress, egress, returns, operator/service paths and actual trusted proxies.
3. Apply [select layers](guides/select-layers.md): one justified placement per boundary; authenticated tenant authority stays separate from IP/proxy metadata.
4. Apply [handoff](guides/prepare-proof-handoff.md): plan eligibility, bursts, costs, per-control outage semantics, selected owners and target-specific NOT_RUN proof.
5. Return one recommendation, sources/dates/limits and unresolved questions in chat. Only an authorized orchestrator saves the report. Review the [synthetic scenario](references/examples/fictional-scenario.md) and [negative cases](references/examples/negative-cases.json) without claiming execution.

## References map

- [Distillation](references/research/distillation.md) and raw ledger: current primary captures and evidence gaps.
- [Paired Drone](../../agents/network-boundaries-wasp-drone.md): exact advice scope.

Runtime is research-only. Ship Gate removed: advice produces no application code or provider configuration. Parent owns source promotion, registration and ordered forge gates before any separately authorized commit.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): resolve trusted Core and selected Infrastructure Fit, Security, Vercel, Tailscale, runtime and Operating Cost owners.
