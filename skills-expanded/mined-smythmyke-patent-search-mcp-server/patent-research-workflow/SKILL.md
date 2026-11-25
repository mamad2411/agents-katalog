---
name: patent-research-workflow
description: >-
  Use when a user asks about a US patent — what it covers, whether it's still
  in force, who owns it, whether it survived PTAB challenges or was litigated,
  what happened during examination, or whether it's risky to a product. Drives
  the AI Patent Search Generator connector tools in the right order (cheap
  free lookups first → dossier for depth → risk_profile for a verdict) so
  Claude returns synthesized patent intelligence instead of raw records.
---

# Patent Research Workflow

Guide for using the **AI Patent Search Generator** MCP connector to turn a US
patent number into legal intelligence: bibliography, claims, prosecution
history, PTAB validity challenges, district-court litigation, ownership chain,
legal status, examiner statistics, and an AI risk verdict. All data is live
from USPTO Open Data (US patents; file-wrapper coverage from 2001).

## When to use this skill
Trigger when the user mentions: a US patent number (e.g. "US10867416B2",
"patent 8,724,622"), "is this patent valid/alive/expired", "who owns this
patent", "has this patent been challenged/litigated/sued over", "patent due
diligence", "freedom to operate" (with the not-legal-advice caveat), "what are
the claims of", "prosecution history / file wrapper", or "the examiner for
this application".

## Core workflow (patent number → intelligence)

1. **Normalize the number.** Tools accept loose input ("10,867,416",
   "us10867416") and normalize to canonical form (US10867416B2). US patents
   only — say so if the user asks about EP/WO/CN numbers.

2. **Start with the question's cheapest sufficient tool** (don't open with the
   dossier if a free lookup answers it):
   - "Still in force? When does it expire?" → `legal_status` (free)
   - "Who owns it? Chain of title?" → `assignments` (free)
   - "Was it attacked at the PTAB? Did it survive?" → `challenges` (free)
   - "What happened during examination?" → `prosecution` (free)
   - "Who sued whom over it?" → `litigation` (2 credits)
   - "How tough was the examiner?" → `examiner` (2 credits)

3. **Go deep with `dossier`** (3 credits fresh, free from 24h cache) when the
   user wants the full picture: title, assignees, inventors, dates, status,
   independent claims, citations, family, CPC classes, similar documents.
   Use `claims` (1 credit cold, free cached) instead when they only need
   claim language — it's cheaper and returns every claim in full.

4. **One-shot verdict with `risk_profile`** (40 credits fresh, free from 24h
   cache) when the user asks "how risky is this patent?" or wants due
   diligence: aggregates legal status + PTAB + litigation + ownership + term
   and returns Low/Moderate/High with a plain-English rationale and the
   underlying signals. Mention the cost before running it; repeat calls within
   24 hours are free.

5. **Interpret, don't dump.**
   - PTAB outcomes: "Institution Denied" / "terminated without adverse
     finding" → the patent survived that challenge; a Final Written Decision
     finding claims unpatentable is the serious one.
   - Litigation coverage is the USPTO Patent Litigation Dataset: comprehensive
     2003–2016, partial to 2020, nothing after 2020. An empty result means "no
     suit on record in that window," not "never litigated."
   - Examiner allowance rate: compare against the ~60-70% USPTO average;
     pendency is reported in months from a sample of the examiner's cases.
   - `inForce: false` with a lapse event usually means unpaid maintenance fees
     — cheap to confirm via the maintenance-fee history in `legal_status`.

## Cost & etiquette
- Free: `challenges`, `legal_status`, `assignments`, `prosecution`, `balance`.
- Metered (prepaid credits, 1 credit ≈ $0.10): `claims` 1 (cold only),
  `litigation` 2, `examiner` 2, `dossier` 3 (fresh only), `risk_profile` 40
  (fresh only). Cached repeats within 24h are free for dossier/claims/
  risk_profile. New accounts include free starter credits.
- Check `balance` when a call reports insufficient credits; mention costs
  before the 40-credit `risk_profile` run.

## Output guidance
Lead with the direct answer (in force or not, survived or not, owner, risk
label), then the supporting record in a compact list. Always close patent
legal questions with the standard caveat: this is factual public-record
reporting and machine-generated summary — not legal advice; validity,
infringement, and freedom-to-operate conclusions need a registered patent
attorney.
