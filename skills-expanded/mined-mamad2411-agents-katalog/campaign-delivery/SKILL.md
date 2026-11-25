---
name: campaign-delivery
description: >
  Build an outbound campaign end-to-end with a proven 9-phase system, orchestrating the other
  skills and their ColdIQ endpoints at each phase. Use when running a full campaign from scratch,
  planning the build order, knowing what comes before what (copy before list), or coordinating
  TAM → scoring → enrichment → copy → load. Triggers on "build a campaign", "campaign from
  scratch", "full outbound pipeline", "9-phase", "campaign checklist", "what order", "kick off a
  campaign". Do NOT use for a single sub-step in isolation (use the specific skill: apollo-search,
  tam-scoring, contact-enrichment, cold-email-copy, instantly-api) or pure copy frameworks
  (see crawford-method / cold-email-copy).
---

# Campaign Delivery

Build outbound campaigns with a 9-phase system (based on Jordan Crawford / Blueprint GTM).
This is the orchestrator — each phase points to the skill and ColdIQ endpoint that does the work.

> Golden rule: **write the perfect email FIRST, then build the list that makes it true.** Copy
> (Phases 2–3) comes BEFORE list building (Phase 5).

## The 9 phases

**Phase 0 — Kick-off (free).** Define the tension triangle for the segment
(see [crawford-method](../crawford-method/SKILL.md)). No spend yet.

**Phase 1 — Context.** Pull background on the ICP and a flagship customer.
→ **POST** `/v1/limadata/research/ai-search` · 0.3 cr · `limadata.research.ai_search`

**Phases 2–3 — Copy (free).** Write 5–10 angles, pick PQS/PVP, draft the perfect email + sequence
(see [crawford-method](../crawford-method/SKILL.md), [cold-email-copy](../cold-email-copy/SKILL.md)).
QA against the 7-component + benchmark checklists.

**Phase 4 — Targeting criteria (free).** Translate the email into list criteria (company +
contact + signal + exclusion filters). Validate filter values for free:
→ **POST** `/v1/limadata/references/autocomplete` · free · `limadata.references.autocomplete`

**Phase 5 — List building (costs credits).** Build the TAM from the criteria.
→ **POST** `/v1/ai-ark/companies` · per result · `ai_ark.companies.search`
→ **POST** `/v1/apollo/organizations/search` · 1 cr · `apollo.organizations.search`
Layer in signals (see [signal-detection](../signal-detection/SKILL.md)):
→ **GET** `/v1/signalbase/funding-signals` · ? cr · `signalbase.funding_signals` (unverified)

**Phase 5b — Score & tier** (see [tam-scoring](../tam-scoring/SKILL.md)), then **dedup**
(see [list-dedup](../list-dedup/SKILL.md)) BEFORE paying to enrich.

**Phase 6 — Contacts & enrichment.** Pull contacts for T1/T2, find + verify emails
(see [contact-enrichment](../contact-enrichment/SKILL.md)).
→ **POST** `/v1/limadata/prospect/employees` · 25 cr · `limadata.prospect.employees`
→ **POST** `/v1/limadata/find/work-email` · 1 cr · `limadata.find.work_email`
→ **POST** `/v1/findymail/verify` · 1 cr · `findymail.verify`

**Phase 7 — Personalization & QA.** Generate per-segment opening lines / ideas, QA the merge
fields against real lead data.

**Phase 8 — Deploy.** Create the campaign with ColdIQ defaults, load leads, verify, then activate
(see [instantly-api](../instantly-api/SKILL.md) — **always confirm with the user before activating**).
→ **POST** `/v1/instantly/campaigns` · free · `instantly.campaigns.create`
→ **POST** `/v1/instantly/leads` · free · `instantly.leads.create`
→ **POST** `/v1/instantly/campaigns/{id}/activate` · free · `instantly.campaigns.activate`

**Phase 9 — Learn.** Pull performance, compare to benchmarks, log what worked.
→ **GET** `/v1/instantly/campaigns/analytics` · free · `instantly.campaigns.analytics`

## Timeline & principles

Copy + targeting (Phases 0–4) ≈ 2.5 hours of thinking before a single credit is spent. Spend
nothing until the email is written. Dedup before enrichment. Test on a sample before the full
send. Each follow-up must add new information (max 2–3 touches).

## Per-campaign file structure

```
campaigns/{name}/  →  brief.md · copy/ · targeting.md · leads/ · report.md
```
