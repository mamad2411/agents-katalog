---
name: priority-ranker
description: >
  Score and rank a list of companies the user already has (territory, target accounts,
  pipeline, a spreadsheet of names or tax IDs) by Fit Score, business fit first and then
  ability to pay, so a sales team knows where to focus. Use whenever the user provides or
  points to such a list and says "prioritizza", "ordina questi account", "chi chiamo prima",
  "dividi la pipeline in fasce", "quali di questi vale la pena seguire", "prioritize", "rank
  these accounts", "who should I call first", "score this list", "tier my pipeline", "which of
  these are worth pursuing", or uploads a spreadsheet of company names / tax IDs for
  qualification. Outputs a ranked, tiered table with a Fit Score and one-line rationale per
  company. Not for finding new companies (use prospects-scout), headroom in existing clients
  (use upsell-potential-scout), or a single company (use company-analysis).
metadata:
  version: "1.0.0"
---

# Priority Ranker

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`). Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill.

Turn a flat list of companies into a ranked, tiered call list.

## Read your context first
Read the commercial context (core §3): target revenue band, spend hook + capture rate, exclusions. If the target band or spend hook is missing, ask once and offer to save it. If an upstream `SYRTO-HANDOFF` already carries some of these companies (resolved ids, metrics, fit), reuse it and fetch only what is missing.

## Steps
1. **Get the list.** From the user's message, an uploaded spreadsheet or CSV, or a CRM export. Extract company names and/or tax IDs.
2. **Resolve each** company, by tax ID where the list has one (unambiguous), else by name. Note any that don't resolve — they become "Insufficient data". On a long list, don't stop to ask about every ambiguous name: take the candidate whose location and sector fit the list and mark it "da verificare" in its rationale.
3. **Batch the financials.** Read the Fit Score inputs for the whole group with the many-company comparison (one read per batch) rather than querying each company separately, for one fiscal year: the year the chain already fixed, else the latest year most of the list has filed. The Fit Score needs no sector benchmark, so skip population aggregates unless the user asks how the list compares with its market.
4. **Score & tier.** Compute the Fit Score and verdict tier for each. Apply exclusions and the target band as hard filters (excluded → flagged, not ranked into the top tiers).
5. **Rank.** Sort by score within tier: Strong fit → Qualified → Monitor → (Out of target / Insufficient data listed separately).

## Output
Per core §5, the full ranked list is a file and the chat carries a digest. Columns: company, sector (Syrto), revenue, Fit Score, spend-capacity estimate, coloured tier, and a one-line rationale naming the main driver and main drag. The chat digest: how many in each tier, the top 3 to call first, and a table of the top of the list with the same columns; say which fiscal year and statement basis the scores use. Offer the list also as a spreadsheet, with your client's spreadsheet capability, or as a pipeline PDF. If the ranked companies feed another skill, end with a `SYRTO-HANDOFF` carrying the resolved ids, metrics, and fit.

## Guardrails
One-line rationale per row is mandatory — never a bare column of numbers. Don't drop unresolved companies silently; list them as "Insufficient data — verify tax ID". Distress signals override a high size score: flag credit risk in the rationale. Respect exclusions from the commercial context.
