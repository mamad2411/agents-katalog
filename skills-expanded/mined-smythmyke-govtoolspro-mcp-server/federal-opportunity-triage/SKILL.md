---
name: federal-opportunity-triage
description: >-
  Use when a user is evaluating a U.S. federal contracting opportunity (a SAM.gov
  notice, RFP/RFQ, solicitation number, NAICS code, or agency) and wants a bid/no-go
  decision, the competitive picture, a pricing benchmark, teaming partners, or a
  recompete pipeline. Drives the GovToolsPro connector tools in the right order so
  Claude returns a synthesized recommendation instead of raw data.
---

# Federal Contract Opportunity Triage

Guide for using the **GovToolsPro** MCP connector to help U.S. federal contractors
make bid/no-bid decisions. GovToolsPro returns synthesized decisions (scores,
incumbents, market structure), not raw SAM.gov/FPDS dumps. Always close with a clear
recommendation and remind the user to verify against the official solicitation.

## When to use this skill
Trigger when the user mentions any of: a SAM.gov notice ID or `sam.gov/opp/...` link,
a solicitation/RFP/RFQ number, a NAICS or PSC code, "should we bid on…", "who's the
incumbent", "is this market competitive", "what should we price labor at", "find a
teaming partner", or "what's expiring / coming up for recompete".

## Core workflow (bid/no-bid triage)
Run only the steps the user's question needs; for a full triage, go in order.

1. **Pull the solicitation** — `get_solicitation` with the notice ID (preferred) or
   solicitation number. This is the entry point; it returns NAICS, PSC, set-aside,
   place of performance, deadline, POCs, and attachment links. Reuse those fields in
   the next steps.
2. **Score the fit** — `score_go_no_go`. Needs the user's company profile (set-asides
   held, NAICS, location, certifications like CMMC, size). If you don't have it, ask
   for it once, then score. Surface hard blockers explicitly.
3. **Identify the incumbent & competition** — `find_incumbents` (NAICS required; pass
   agency/PSC/place-of-performance from step 1 for accuracy). Note the anticipated
   next-award date.
4. **Market & competitive context** — `analyze_market` (5 credits: spend trend, top
   contractors, HHI concentration, set-aside mix, geography) and/or
   `analyze_award_patterns` (3 credits: award sizes, competition mix, bid intensity,
   vehicles, pricing types). Use these to judge how winnable and how concentrated the
   space is.
5. **Pricing benchmark** — `lookup_labor_rates` (free) for the relevant labor
   categories / NAICS (GSA CALC ceilings + BLS loaded wages).
6. **Teaming** — `find_partners_near` with a capability keyword + the place of
   performance from step 1, when the user needs a subcontractor or partner.

## Pipeline building (no specific solicitation yet)
Use `predict_recompete` filtered by NAICS/PSC/state/value to surface expiring
contracts (recompete opportunities), then feed promising ones back into step 2–4.

## Cost & etiquette
- Free tools: `balance`, `get_solicitation`, `score_go_no_go`, `find_incumbents`,
  `find_partners_near`, `predict_recompete`, `lookup_neco_data`, `lookup_labor_rates`.
- Metered tools: `analyze_award_patterns` (3 credits), `analyze_market` (5 credits).
  Mention the cost before running a metered tool if the user is cost-sensitive; check
  `balance` if a call reports insufficient credits.
- Navy-specific: use `lookup_neco_data` for neco.navy.mil solicitations.

## Output guidance
End with a concise recommendation (GO / NO-GO / lean) citing the score, the incumbent,
and the competitive read — then the standard caveat: these are decision-support
estimates from public data; verify against the official solicitation before relying on
them. Never present raw SAM.gov/FPDS records as the answer.
