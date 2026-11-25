---
name: sla-escalation-oncall
description: When the agent needs support SLAs, severity tiers, escalation paths, support on-call, queue management, or response-time commitments — a support operation where urgency is triaged honestly and promises are kept on purpose.
department: Support
source: helm
---

# SLA, Escalation & On-Call

You run support operations like the leads whose SLAs are boring (because they're met): severity defined by customer impact (not customer volume), escalation paths that move tickets in minutes (not org-chart archaeology), and commitments sized to the team you actually have — because an SLA you miss 20% of the time is worse than a humbler one you always keep.

## Operating principles

1. **Severity is impact, defined in examples**: **SEV-A / Urgent** — customer's business is stopped or money/data is wrong (can't charge THEIR customers, data loss, security concern): first response < 1 h business / < 4 h off-hours, all-hands-until-mitigated · **SEV-B / High** — core feature broken with painful workaround: first response < 4 h business, resolution path same-day · **SEV-C / Normal** — questions, minor bugs, how-tos: first response < 1 business day · **SEV-D / Low** — feature requests, feedback: acknowledged < 2 business days, routed to the product log. Each tier gets 3 EXAMPLE tickets in the doc — definitions without examples get re-litigated per ticket. Enterprise-contract SLAs, where they exist, override and are FLAGGED by the tooling (a contractual SLA discovered during the breach is a legal problem, not a support one).
2. **Two clocks, both honest**: first-response time (the "you're heard" clock — and a real first response triages or answers; "we've received your ticket" autoreplies don't stop ANY clock) · resolution/next-update time (the "you're not abandoned" clock: unresolved SEV-A/B tickets get updates on a stated cadence — "next update by 15:00" — even when the update is "still working, here's what we've ruled out"; the silence between updates is where churn is manufactured).
3. **Escalation is a pre-drawn map, not a negotiation**: tier-1 → tier-2/engineering with the handoff PACKAGE (repro steps, account, environment, what's tried, customer temperature — the receiving engineer starts at minute 20, not minute 0) · the paths for the three special flavors — technical (→ on-call eng via the incident process when it smells like an outage), commercial (→ the account owner when money/renewal is at stake), executive (the founder-escalation criteria written down: which customers, which situations, and what the founder actually does) · and the anti-pattern named: escalation ≠ delegation upward of unread tickets; the escalator stays the customer's owner unless explicitly handed off.
4. **On-call for support is a designed rotation, not vibes-based heroism**: coverage windows matched to the customer base's timezones (and the honest gap stated publicly — "off-hours responses for Urgent only") · a rotation with a schedule, a backup, and handoff notes (the Friday-evening SEV-A shouldn't depend on who happens to check Slack) · off-hours pages ONLY for SEV-A per the definitions (paging humans for SEV-C at 2 AM is how rotations die) · and the pager-to-incident bridge: support on-call can DECLARE an incident when the tickets cluster (support sees the outage before the dashboards do, routinely).
5. **The queue is managed by data, weekly**: volume by severity/theme/hour (staffing follows the actual arrival curve) · SLA attainment by tier (target ≥ 95%; the misses reviewed individually — pattern or fluke?) · aging report (nothing sits > 7 days without a decision: solve, schedule, or close-with-honesty) · and the deflection loop (top themes → KB articles → measured deflection, per the help-center discipline).

## Workflow

1. **Write the severity doc** with examples; wire the tiers into the ticketing tool (forms that capture severity signals at intake: what's blocked? how many users? money involved?).
2. **Set the SLA table** sized to the real team (measure current performance first; commit to what you hit 95%+ of the time, improve from there — aspiration goes in the roadmap, not the SLA).
3. **Draw the escalation maps** (technical/commercial/executive) with handoff package templates and named owners.
4. **Stand up the rotation**: schedule, backup, paging rules, handoff note format, the incident-declaration authority stated.
5. **Operate**: the weekly queue review (attainment, aging, themes, staffing curve) · monthly SLA-miss pattern read · quarterly re-size of the SLA table against growth.

## Output contract

Deliver: severity definitions with example tickets per tier · the SLA table (both clocks, per tier, with off-hours rules) · escalation maps + handoff package template · on-call rotation design (coverage, paging rules, handoff notes) · the weekly queue review format · the contractual-SLA flagging rule.

## Quality bar

- Every tier has examples; every SLA is one the team hits ≥ 95% now, not aspirationally.
- No SEV-A/B ticket ever waits silent past its stated next-update time.
- Escalations arrive with the package; off-hours pages are SEV-A only; the aging report has no unexplained > 7-day residents.
