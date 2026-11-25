---
name: "launch-assets-stinger"
description: "Prepare launch accounts, assets and owners for web, desktop, mobile or integrations. Produce a dated readiness ledger with costs, prerequisites and blockers. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; source-reading tools, Python 3 for optional ledger checks."
metadata:
  hive-tier: specialist
  hive-drone: launch-assets-wasp-drone
  pair-drone: launch-assets-wasp-drone
  domain: launch-readiness
  mode: research-only
---

# Launch assets

## Purpose

Prepare the minimum accounts, assets and accountable owners needed for the user's intended launch. Deliver an editable readiness ledger, immediate blockers, deferred services and selected-owner handoffs. Keep documentation requirements, owner claims and observed account readiness distinct.

## When to use

- "What assets and accounts do I need before building or launching this?"
- "Help me prepare for a desktop, mobile or web release."
- "What is missing before my integration can serve customers?"
- "Are my existing accounts ready for this launch milestone?"

## When not to use

- Picking a product/market or full architecture: resolve Builder Readiness or Infrastructure Fit.
- Implementing hosting, databases, OAuth, payments or signing: route to selected specialists under their authorized task.
- Creating accounts, entering credentials, paying fees, modifying provider settings, deploying or publishing: this workflow only prepares the evidence and owner actions.
- Certifying production/security/store approval from a checklist: require actual scoped evidence and appropriate reviewers.

## Procedure

1. Read [README.md](README.md). Confirm product/platform, intended milestone, release route, payment model, existing assets, accountable owner and read/output scope. Ask only unresolved material questions; an account inventory does not authorize account access.
2. Load the applicable web, desktop, mobile or integration guide. Use the [selection reference](references/asset-selection.md) to include capabilities justified by actual product needs and explicitly defer unused providers.
3. Research current official requirements within the authorized read scope. Record source URL/date, retrieval date, region, fee unit and limits. Unknown price or approval time stays unknown. An observed rate is not approval to spend.
4. Fill the [editable ledger](references/templates/readiness-ledger.csv) according to its [contract](references/ledger-contract.md). Separate environments and track owner, access boundary, dependencies, evidence class, status, blocking and next action. Never place secrets, identity documents or payment details in it.
5. Apply [qualify-assets](guides/qualify-assets.md). Keep owner statements reported and provider docs as requirement evidence. Observed-ready requires authorized observation and reviewer evidence for the exact milestone; no script establishes that state.
6. Review minimum assets, source freshness, missing prerequisites, cycles, unknown fees/waits and TLS-versus-signing distinctions. Run the optional [checker](scripts/check-ledger.py) on an authorized saved ledger for structure only.
7. Deliver editable rows and a concise blocker summary, deferred assets with triggers, dated cost limits and selected-owner handoffs. Account setup, billing, credentials and release actions remain separate explicit authority.

## References map

- [Web](guides/prepare-web.md), [desktop](guides/prepare-desktop.md), [mobile](guides/prepare-mobile.md), [integration](guides/prepare-integration.md): preparation procedures.
- [Worked scenarios](references/examples/scenarios.md) and [fictional CSV](references/examples/fictional-ledger.csv): conditional inclusions and readiness failure cases.
- [Research digest](references/research/distilled-launch-readiness.md) and source ledger: current official captures, dates and fetch limits.
- [Paired Drone](../../agents/launch-assets-wasp-drone.md): delegation contract.

Runtime is research-only. Ship Gate removed: this workflow prepares readiness documents and does not implement application code. Source-component forging and any later commits receive separately authorized ordered review gates.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): use selected Core and platform/infrastructure/identity/distribution owners through the trusted resolver. Never infer availability from sibling caches or turn a handoff into authorization for provider changes.
