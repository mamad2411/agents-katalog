---
name: ib-precedent-transactions
description: Build a precedent transactions analysis — comparable M&A deals with multiples, from Caeros' private-markets vault. Use when the user asks for precedents, deal comps, M&A multiples, or "what have similar companies sold for".
---

# Precedent Transactions

Build a precedent M&A transaction set from the Caeros vault (full PitchBook
deal, company, and investor data in BigQuery).

## Data access

- Primary: `analyst_vault_query` — describe what you need in plain language
  (it plans and runs the SQL). For precise follow-ups use
  `analyst_vault_run_sql`.
- Discover the schema before assuming table or column names: ask
  `analyst_vault_query` what deal tables exist, or run an
  `INFORMATION_SCHEMA.TABLES` query.
- Export result sets with `analyst_export_csv` when the user wants a file.
- If the vault tools are unavailable in this session, say so and offer the
  public-sources fallback (news search) instead of guessing numbers.

## Workflow

1. **Scope the screen.** Confirm sector or keywords, geography, deal size
   range, and lookback window (default: 5 years). State the criteria back in
   one line before querying.
2. **Pull the deal set.** Query completed M&A / buyout deals matching the
   screen: target, acquirer, close date, deal size, and any disclosed
   valuation fields (EV, revenue or EBITDA at deal time, implied multiples).
   Aim for 8-15 usable precedents; widen or tighten the screen until there.
3. **Clean.** Drop deals with no disclosed economics from the multiples math
   (keep them in an appendix list); flag outliers (>3x the median multiple)
   rather than silently dropping them.
4. **Summarize.** Deliver a table: target, acquirer, date, size, EV/Revenue,
   EV/EBITDA where available; then min / median / mean / max multiple rows,
   and a 2-3 sentence read (where the market clears, trend over time,
   strategic vs sponsor mix).
5. **Apply (when the user named a subject company).** Multiply the median and
   quartile multiples against the subject's metrics for an implied valuation
   range. Label every input as vault data, user-provided, or estimate.
6. **Hand off.** Offer to build the sheet via the spreadsheets skill, or
   export CSV.

## Rules

- Never invent a deal, a price, or a multiple. Missing is missing — say so.
- Cite counts honestly ("12 precedents matched; 7 disclosed economics").
- Vault data is licensed for internal analysis: keep outputs in-session,
  no bulk data dumps beyond the user's request.
