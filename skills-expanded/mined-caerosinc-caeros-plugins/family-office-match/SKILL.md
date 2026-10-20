---
name: family-office-match
description: Match a company or investment thesis to family offices with caeros_family_office_search, and filter or count them with Vault SQL. Use whenever the user asks about family offices, single or multi family offices, or private wealth investors.
---

# Family Office Match

Family offices are a **separate universe** from the PitchBook investors in
`v_investors`, with their own tables and their own search tool. They never
appear in `caeros_investor_match` results.

The most common failure here is answering a family-office question from
`v_investors`. That returns real rows, so it looks correct, and it is completely
wrong. Check which universe the question is about before you touch a tool.

## Which tool

| The user wants | Use |
|---|---|
| "find / match / which family offices fit us" | `caeros_family_office_search` |
| "how many prefer fintech", "list the UK ones", any count or field filter | SQL over `mat_family_office` |
| contacts for specific family offices | `v_family_office_contacts`, keyed on domain |

## caeros_family_office_search

Semantic retrieval over the family-office dataset (roughly 4,900 firms), with
Vault detail and contacts attached to every hit.

Arguments:

| Field | Default | Notes |
|---|---|---|
| `query` | required | Free-text company or thesis description. Reuse the `company-brief` description verbatim if one exists. |
| `top_k` | 20 | Max firms, ceiling 100. |
| `country` | none | Geography hint, appended to the query text. |
| `max_contacts` | 3 | Max contacts per firm. |

Each result carries `rank`, `domain`, `firm_name`, `score`,
`location_breakdown`, `industry_preferences`, `funding_style`, `stages`,
`thesis`, `has_portfolio`, `portfolio_summary`, and `contacts` (name and email).
The envelope carries `query`, `count`, `results`, and, on failure, `status`,
`message`, `failure_code`, `failure_phase`, `retryable`, and
`safe_backend_action`.

Two behaviours worth knowing:

- If the Vault detail fetch fails, the whole search fails rather than handing
  back bare domains with no substance. Treat a failure as a failure.
- If only the contact fetch fails, results still come back, with firms but no
  contacts. Say that contacts were unavailable rather than reporting the firms
  as having none.

`thesis` is truncated to 400 characters and `portfolio_summary` to 600, so quote
them as summaries, not as complete statements.

## Vault SQL for family offices

`mat_family_office` is firm-level, 4,906 rows: `entity_key`, `entity_domain`,
`name`, `contact_count`, `location_breakdown`, `industry_preferences`,
`funding_style`, `stages`, `summary`, `portfolio_summary`, `has_portfolio`.
`v_family_office_contacts` holds the people, 24,537 rows and every firm has at
least one: `entity_key`, `first_name`, `last_name`, `email`, `firm_name`.

Three things that will otherwise cost you a wrong query:

- **`entity_key` is the key and it IS the firm domain** (identical to
  `entity_domain` on every row). There is no `domain` column. The firm name is
  `name`, not `investor_name`. The thesis text is `summary`, not `thesis`.
- **`location_breakdown`, `industry_preferences`, `funding_style`, and `stages`
  are free-text weighted breakdown strings**, not enums. A real `stages` value
  reads `70% Seed, 30% Series A`, and `industry_preferences` reads
  `Retail 40%, Commercial Insurance 30%`. Filter them with
  `LOWER(col) LIKE '%value%'`. Equality returns zero rows, every time.
- **Only 197 firms have `portfolio_summary` content.** Gate on `has_portfolio`
  before selecting it, or most rows come back blank.

Both tables are allowlisted, so hand-written SQL through
`analyst_vault_run_sql` validates and runs. Whether plain-English questions
work through `analyst_vault_query` depends on your build: the SQL generator was
briefed on only the five investor and company views until that was fixed. If a
natural-language family-office question comes back as the wrong view or an
`ERROR:`, you are on an older build. Write the SQL yourself and use
`analyst_vault_run_sql`.

Contacts join, matching how the search tool does it:

```sql
SELECT c.entity_key, c.first_name, c.last_name, c.email
FROM `<project>.<dataset>.v_family_office_contacts` AS c
WHERE c.entity_key IN UNNEST(@domains)
  AND c.email IS NOT NULL AND c.email != ''
```

Use lowercase, trimmed domains as the keys. Filter out empty emails, or you will
report contacts that cannot be reached.

## Procedure

1. Confirm the user means family offices, not VC or PE firms. If they want both,
   run them as two separate steps and label the outputs, since the scores are not
   comparable across universes.
2. Build or reuse the brief from `company-brief`. The description becomes `query`
   unchanged.
3. Call `caeros_family_office_search` once. Set `country` when the user gave a
   geography, and raise `max_contacts` only when they asked for more names.
4. Report firms with their thesis, stage, and industry preferences, plus the
   contacts. Say plainly when a firm has no contacts in the Vault.
5. For a file, export with `analyst_export_csv` in SQL mode over the family
   office tables. Do not pass search results back through `rows_json`.

## Never do this

- Never answer a family-office question from `v_investors` or from the investor
  matcher.
- Never blend family offices into an investor-match list. They are separate
  result sets with separate scores.
- Never invent a contact for a family office that has none in the Vault.
