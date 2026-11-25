---
name: aigov-policy-monitor
version: 1.0.0
description: Run a horizon-scanning cadence over the external AI regulatory and standards landscape and translate each change into a so-what impact and a concrete action for your organization.
author: matrixx0070
tags: [ai-governance, horizon-scanning, regulatory-monitoring, eu-ai-act, standards-tracking, compliance]
capabilities: []
---

## When to use

Use this when the organization needs to stay ahead of a moving regulatory target — new or amended AI laws, phased applicability dates, sector rules, and standards updates — and turn each development into a decision the business can act on rather than a headline. Run it on a recurring cadence, not once. Its output feeds directly into gap analysis.

**Not for:** doing the control-to-requirement gap analysis itself (use aigov-reg-gap-analysis), building the system inventory (use aigov-ai-inventory), classifying a specific use case (use aigov-use-case-triage), writing an impact assessment (use aigov-aia-generation), reviewing vendor terms (use aigov-vendor-ai-review), drafting internal policy (use aigov-policy-starter), the discovery interview (use aigov-cold-start-interview), tailoring artifacts (use aigov-customize), or organizing a single review (use aigov-matter-workspace).

This skill provides decision-support and situational awareness, not legal advice. Dates, thresholds, and applicability change and are frequently amended; a qualified attorney must verify any specific legal obligation before the organization relies on it, changes course, or represents a compliance position.

## Method

1. Define your watch-list: the regimes, sectors, and jurisdictions where the org operates or ships (EU, US federal + relevant states, sector regulators), plus the standards bodies you follow.
2. Set the cadence and sources: pick a scanning rhythm (e.g., weekly light, monthly deep) and authoritative sources for each item on the watch-list. **Decision:** high-exposure jurisdiction or an imminent phased date → tighten cadence and assign an owner.
3. Scan for changes: new/amended laws, enforcement actions, official guidance, and standards revisions since the last run.
4. For each hit, capture the primary source and mark every date/threshold **TO-VERIFY** — never restate a deadline as settled from a secondary summary.
5. Write the "so-what": which of our systems/use cases does this touch, and what is the exposure if we do nothing? **Decision:** material impact → open or update a matter and route the item to aigov-reg-gap-analysis; immaterial → log and close.
6. Assign an action, owner, and due date for each material item; track status to closure.
7. Maintain a rolling register so nothing is scanned-then-forgotten, and so you can show a continuous monitoring trail.

## Example

Scan hit: EU AI Act — GPAI (general-purpose AI model) obligations reportedly applying on a phased date `[TO-VERIFY with counsel]`. So-what: our customer-support bot is built on a third-party foundation model, so provider-passthrough obligations may reach us. Action: confirm the date and scope with counsel, request the vendor's GPAI documentation, and route to aigov-reg-gap-analysis. Owner: Legal Ops. Due: 2 weeks. Status: OPEN. Logged with the official source link, not a news article.

## Pitfalls

- **Restating dates as fact from secondary sources.** Phased timelines get amended; cite the primary text and mark every date TO-VERIFY until counsel confirms.
- **Scanning without a so-what.** A change nobody maps to a specific system produces awareness but no action — always name the affected use case and the exposure.
- **One-and-done monitoring.** A single scan goes stale in weeks. The value is the cadence and the rolling register, not a snapshot.
- **Watching only laws.** Standards updates (NIST, ISO), enforcement actions, and official guidance shift the "reasonable practice" bar even when no statute changes.

## Output format

```
# AI Policy & Regulatory Scan — <period>
Watch-list: <jurisdictions / sectors / standards>   Cadence: <weekly|monthly>

## Changes this cycle
- Item: <law/standard/guidance/enforcement>
  Source: <primary link>
  Date/threshold: <value> [TO-VERIFY with counsel]
  So-what (affected systems): <...>
  Exposure if no action: <...>
  Action / owner / due / status: <...> / <name> / <date> / OPEN

## Routed to gap analysis
- <item> -> aigov-reg-gap-analysis (matter <id>)

## Register (rolling)
<date> | <item> | material? | action | status

Situational awareness only. Verify all dates and obligations with a qualified attorney.
```

## Reference

### EU AI Act — phased applicability (concept, dates TO-VERIFY)

The Act does not switch on all at once; obligations phase in by category, generally in this order. Treat the *sequence* as the stable concept and every specific date as something counsel must confirm — the schedule has been subject to change and delay proposals.

| Phase (relative order) | Scope | Note |
|------------------------|-------|------|
| **Prohibitions** first | Banned "unacceptable-risk" practices (e.g., certain social scoring, some biometric uses) | Earliest to apply |
| **GPAI obligations** next | General-purpose / foundation-model transparency and documentation duties | Provider passthrough can reach deployers |
| **High-risk obligations** later | Full conformity, risk management, documentation for high-risk systems | Longest lead time |

The tiering model itself: **unacceptable** (prohibited), **high-risk** (heavy obligations), **limited-risk** (transparency duties, e.g., disclosing AI interaction), **minimal-risk** (largely unregulated). Use the tier to prioritize which scan hits matter most.

### Moving-target regimes to watch

| Layer | Examples (verify current status) |
|-------|----------------------------------|
| **EU** | AI Act phased dates, GPAI guidance, delegated/implementing acts |
| **US federal** | Executive actions, agency guidance (FTC, EEOC, sector regulators) |
| **US states** | State AI/automated-decision and biometric laws — fast-moving, patchwork |
| **Sector** | Financial, health, employment, insurance rules touching automated decisions |
| **Standards** | NIST AI RMF and profiles, ISO/IEC 42001 (AI management systems), ISO/IEC 23894 (AI risk) |

### NIST AI RMF as a living framework

The AI RMF (functions **GOVERN, MAP, MEASURE, MANAGE**) is voluntary and evolving — NIST publishes **profiles** and companion resources (e.g., generative-AI guidance) over time. Monitor it as a *living* reference: updates shift expected practice and give you defensible, framework-aligned language even where no law has changed. ISO/IEC 42001 similarly formalizes an auditable AI management system and is a certification track worth tracking.

### Running the horizon-scanning cadence

- **Cadence:** a lightweight frequent sweep plus a periodic deep review; tighten around known phased dates.
- **Triage each hit:** material vs immaterial to *your* systems — only material items consume analysis effort.
- **Feed the pipeline:** material items become inputs to aigov-reg-gap-analysis, where controls are mapped to the new requirement; open a matter (aigov-matter-workspace) for anything that needs a tracked decision.
- **Keep the register:** a continuous, dated trail is itself evidence of diligence — showing you were monitoring is part of a defensible posture.
- **Verification discipline:** dates and legal specifics are the most volatile and the most consequential elements; they must be confirmed with counsel before any reliance, because getting a phased date wrong can mean missing a live obligation.
