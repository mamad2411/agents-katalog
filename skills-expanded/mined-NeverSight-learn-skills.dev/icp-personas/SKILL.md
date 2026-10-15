---
name: icp-personas
description: >
  Define the ICP, size and tier an ABM target-account list, and map the buying committee — the
  strategy layer before list-building and enrichment. Use when defining an Ideal Customer Profile
  and scoring criteria, deciding how many accounts to target for a revenue goal, tiering accounts
  (A/B/C/D), mapping personas/buying committee (champion, economic buyer, end user, technical
  evaluator), or planning persona-based messaging. Triggers on "ICP", "ideal customer profile",
  "who to target", "scoring criteria", "ABM accounts", "how many accounts", "account tiering",
  "buying committee", "persona mapping", "champion", "economic buyer", "revenue reverse-engineering".
  Do NOT use for actually sourcing companies/contacts (see apollo-search / coldiq-search-enrich),
  scoring math on an export (see tam-scoring), or writing copy (see crawford-method / cold-email-copy).
---

# ICP, Accounts & Personas

The strategy layer: decide WHO to target, HOW MANY, and WHICH people inside each account — before
you spend credits sourcing and enriching. Mostly methodology; a few steps source data from ColdIQ.

## ColdIQ Marketplace Endpoints (where strategy touches data)

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Validate filter values (ICP criteria) | POST | `/v1/limadata/references/autocomplete` | free | `limadata.references.autocomplete` | Confirm titles/industries exist |
| Size the addressable market | POST | `/v1/ai-ark/companies` | per result | `ai_ark.companies.search` | How many fit the ICP |
| Layer intent for prioritization | GET | `/v1/signalbase/funding-signals` | unknown | `signalbase.funding_signals` | Bump in-market accounts |
| Map the buying committee | POST | `/v1/limadata/prospect/employees` | 25 | `limadata.prospect.employees` | Find personas at an account |

## 1. Define the ICP (3 layers + scoring)

- **Firmographic:** industry, employee size, revenue, geography, growth, funding stage.
- **Technographic:** tech stack, CRM, marketing automation, competitor tools.
- **Behavioral/intent:** hiring, funding, leadership changes, content engagement, website visits.

Reverse-engineer from your best 10–20 closed-won customers. Score 100 pts (example weights):
industry 20 · size 15 · revenue 15 · geography 10 · tech fit 15 · growth 10 · intent 15.
Tiers: **A** 90–100 (1:1 ABM) · **B** 70–89 (1:few) · **C** 50–69 (programmatic) · **D** <50 (exclude).

Validate your criteria translate to real filter values before sizing:
→ **POST** `/v1/limadata/references/autocomplete` · free · `limadata.references.autocomplete`

(Hand the scoring rules to [tam-scoring](../tam-scoring/SKILL.md) to run on an actual export.)

## 2. Size & select the account list (ABM)

Revenue reverse-engineering — work backward from the target through funnel benchmarks:
Identified→Aware 55% · Aware→Interested 32% · Interested→Considering 18%.
(e.g. $1M ARR target ≈ ~3,367 accounts identified.)

Check how many companies actually fit before committing:
→ **POST** `/v1/ai-ark/companies` · per result · `ai_ark.companies.search`

4-layer selection: firmographic fit · technographic indicators · CRM intelligence (closed-lost,
lost-to-competitor, churned) · lookalike modeling from best customers. Then prioritize the
in-market ones:
→ **GET** `/v1/signalbase/funding-signals` · ? cr · `signalbase.funding_signals` (unverified)

Track stage progression: Identified → Aware → Interested (5+ clicks / 10+ engagements) → Considering
(site visits, content, demo interest).

## 3. Map the buying committee

| Role | Function | Budget priority |
|------|----------|-----------------|
| Champion | Internal advocate driving evaluation | 40–50% |
| Economic Buyer | Signs the check; cares about ROI | 20–30% |
| End User | Daily user; cares about UX/workflow | 15–20% |
| Technical Evaluator | Integration, security, compliance | 5–10% |
| Blocker/Gatekeeper | Can veto, rarely initiates | monitor |

For each persona capture: title patterns + seniority, function, jobs-to-be-done, pains, success
metrics, content preference, buying role. Find the actual people once you've defined the personas:
→ **POST** `/v1/limadata/prospect/employees` · 25 cr · `limadata.prospect.employees`

Messaging matrix: per persona, different JTBD + pain + stage-appropriate content + role-appropriate
CTA (champion → demo/ROI, end user → trial/ease-of-use). Hand off to
[crawford-method](../crawford-method/SKILL.md) / [cold-email-copy](../cold-email-copy/SKILL.md) to write it.

## Where this hands off

ICP scoring rules → [tam-scoring](../tam-scoring/SKILL.md) · sourcing companies/contacts →
[apollo-search](../apollo-search/SKILL.md) / [coldiq-search-enrich](../lima-data-api/SKILL.md) ·
personas-into-ads → [ad-audiences](../ad-audiences/SKILL.md) · the full build order →
[campaign-delivery](../campaign-delivery/SKILL.md).
