---
name: regl-cold-start-interview
version: 1.0.0
description: Run a structured intake interview to map a new user's regulatory exposure from scratch, so the watch/diff/comment pipeline starts on real obligations.
author: matrixx0070
tags: [regulatory, legal, intake, onboarding, scoping, exposure-mapping]
capabilities: []
---

## When to use

Use this at the very start, when you know nothing about the user's regulatory landscape and need to build the exposure map that every other regl skill depends on. Reach for it to onboard a new business line, a new user, or a jurisdiction you have never covered.

**Not for:** users whose exposure is already mapped (go straight to regl-reg-feed-watcher), analyzing a specific rule (regl-policy-diff), or customizing an existing setup (regl-customize). If the interview reveals a live legal question or existing violation, route it to an attorney rather than advising.

## Method

1. Establish the business basics: what the organization does, its products/services, jurisdictions of operation, size, and customer types. Regulatory exposure follows activity and geography.
2. Probe for regulated activities directly: data/privacy, financial services, health, employment, environmental, consumer protection, sector-specific licensing. Ask "do you handle X?" rather than "are you regulated for X?"
3. For each hit, identify the likely regulator(s) and the rules already known to bind them.
4. Capture current-state maturity: is there an existing compliance program, prior exams, known open issues, or pending matters?
5. **Decision point:** if the user surfaces an existing violation, active investigation, or a question that needs a legal answer, stop scoping and escalate to an attorney — the interview maps exposure, it does not give legal advice.
6. Turn answers into a prioritized exposure map: agencies, dockets, and topics ranked by risk, ready to hand to regl-reg-feed-watcher and regl-matter-workspace.
7. Record assumptions explicitly so gaps in the user's answers are visible, not silently filled.

## Example

> Intake: fintech, US + Canada, holds consumer financial data, lends. Regulated activities: consumer lending (CFPB, state AGs), data privacy (state laws, PIPEDA), fair-lending (ECOA). Maturity: no formal program, no prior exam. Assumption: no EU customers (user unsure — flagged). Existing issue surfaced: an unresolved consumer complaint pattern → attorney review. Output handed to regl-reg-feed-watcher as a 4-agency watchlist.

## Pitfalls

- Asking "are you regulated?" — users don't know; ask what they do and infer.
- Silently assuming jurisdiction scope instead of recording the unknown as an assumption.
- Continuing to scope after a live violation surfaces, instead of escalating.
- Producing a flat list with no risk ranking, so the feed watcher can't prioritize.

## Output format

```
COLD-START INTAKE — <org>
Business: <activity> | Jurisdictions: <list> | Customers: <type>
Regulated activities detected:
  <activity> → <regulator(s)> → <known binding rules>
Maturity: <program? prior exams? open issues?>
EXPOSURE MAP (risk-ranked):
  1. <agency/topic> — <why high>
Assumptions (unconfirmed): <list>
Attorney escalation: <violations/legal questions surfaced>
Handoff: <to regl-reg-feed-watcher / regl-matter-workspace>
```

## Reference

**Rulemaking lifecycle:** the exposure map should note, per agency, whether relevant rules are settled (final/effective) or in flux (active ANPRM/NPRM dockets), so the watcher knows where change is likely.

**Comment-period mechanics:** flag agencies with active open comment periods during intake — an onboarding user may want to weigh in via regl-comments before a rule finalizes against them.

**Policy-diff method:** intake establishes the "current state" baseline (existing program and controls) that later diffs and gap analyses measure against. Attorney-escalation gate: existing violations, active investigations, and any request for a legal conclusion leave the intake flow and go to counsel — scoping is not legal advice.
