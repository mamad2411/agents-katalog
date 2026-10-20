---
name: ib-deal-screening
description: Screen acquisition targets, buyers, or sponsors from the private-markets vault — target lists, acquirer activity, investor mapping, pipeline briefs. Use when the user wants target lists, "who could buy X", "who is acquiring in Y", or sponsor coverage.
---

# Deal Screening

Build target lists, buyer lists, and activity maps from the Caeros vault
(PitchBook companies, deals, investors, and funds in BigQuery).

## Data access

`analyst_vault_query` (natural language) first; `analyst_vault_run_sql` for
precise follow-ups; `analyst_export_csv` for files. Discover schema before
assuming table names. If vault tools are unavailable, say so — do not
substitute guesses.

## Screens this skill covers

- **Target screen**: companies matching sector, geography, size (revenue or
  headcount), ownership status (founder-owned, PE-backed, corporate-owned),
  and last-round vintage. Output: ranked list with the fields that matched.
- **Buyer screen**: who could acquire a given company — strategic acquirers
  active in the sector (from deal history) plus sponsors with relevant
  platform investments. Output: two lists (strategics, sponsors) with recent
  relevant deals each.
- **Acquirer activity**: most active acquirers or investors in a sector and
  window, with deal counts and notable transactions.
- **Sponsor coverage**: a fund's portfolio, dry-powder signals (fund
  vintages), and add-on patterns.

## Workflow

1. Confirm the screen criteria in one line (sector, geo, size, window,
   ownership). Default window: 24 months.
2. Query the vault; iterate until the list is 10-30 names (widen or tighten
   with the user).
3. Enrich the top names: one line each on why they fit (deal history,
   ownership, scale).
4. Deliver as a ranked table; offer CSV export, a spreadsheet, or an
   investment-committee-style brief of the top 3-5.

## Rules

- Ranked lists must state the ranking basis (fit score inputs), not imply a
  data field that doesn't exist.
- Ownership and size data can lag reality — note the vault's as-of nature
  when a user plans outreach on it.
- Keep outputs to the user's request; no bulk vault dumps.
