---
name: investor-vault-queries
description: Query the Caeros Vault directly with analyst_vault_query and analyst_vault_run_sql for investor, company, deal, and contact questions, and export results as CSV. Use for counts, filters, lookups by firm or domain, portfolio and deal history, and contact lists that do not need a ranked match.
---

# Vault Queries

The Vault is a read-only BigQuery corpus of private-markets data reached through
two tools. Use it when the user wants a **specific slice**: counts, filters, a
named firm's portfolio, contacts at a known domain. Use `caeros_investor_match`
instead when they want a **ranked list of who to approach**, since only the
matcher does semantic retrieval and scoring.

## Which tool

- **`analyst_vault_query`** is the default. Pass a plain-English `question`. The
  host generates the SQL, validates it, runs it, and returns
  `{sql, columns, rows, meta}`. For a follow-up, pass the prior turns in
  `messages` (objects with `role` and `content`, in chat order) and put the new
  ask in `question`, so it refines the previous SQL rather than starting over.
- **`analyst_vault_run_sql`** is for when you already have a complete
  `SELECT` or `WITH` and every table is a fully-qualified, backtick-quoted
  allowlisted name. It runs the same validation. Prefer it when you need exact
  control, or for the family-office tables (see the gotcha below).
- **`analyst_export_csv`** produces the file. Pass the final SQL in `sql`, never
  the rows.

## The seven allowlisted tables

Nothing else is queryable. A query touching any other table fails validation.

| Table | Grain | Use for |
|---|---|---|
| `v_investors` | one row per investor firm | firm attributes, investment counts, capital under management, dry powder |
| `v_company_portfolio` | one row per deal | deals, portfolio links, deal type, size, date, lead status |
| `v_companies` | one row per company | company lookups by employees, revenue, industry, geography, financing |
| `v_people` | one row per person | contacts at companies AND at investor firms |
| `v_investor_contacts` | one row per investor-linked person | legacy view, only when the user explicitly asks for it |
| `mat_family_office` | one row per family office | the separate family-office universe |
| `v_family_office_contacts` | one row per family-office person | family-office contacts, keyed by domain |

### Columns worth knowing

`v_investors`: `investor_domain`, `investor_name`, `investor_pb_id`,
`investor_type`, `investor_status`, `investor_description`,
`preferred_industry`, `preferred_geography`, `preferred_verticals`,
`preferred_investment_types`, `country`, `city`, `total_investments`,
`investments_last_12m`, `total_exits`, `total_active_investments`,
`capital_under_management`, `dry_powder`.

`v_company_portfolio`: `company_domain`, `company_name`, `company_pb_id`,
`description`, `keywords`, `verticals`, `country`, `deal_type`, `deal_type_2`,
`deal_date`, `deal_size`, `deal_status`, `deal_synopsis`, `investor_domain`,
`investor_name`, `is_lead`, plus the investor attribute columns.

`v_companies`: `company_pb_id`, `company_name`, `website`, `description`,
`employees`, `year_founded`, `hq_city`, `hq_state`, `hq_country`, `industry`,
`sector`, `verticals`, `keywords`, `revenue`, `last_financing_size`,
`last_financing_date`, `last_financing_type`, `last_financing_valuation`,
`linkedin`, `hq_email`, `hq_phone`, `active_investor_count`.

`v_people`: `person_pb_id`, `first_name`, `last_name`, `email`, `phone`, `bio`,
`title`, `company_name`, `company_pb_id`, `company_website`, `company_type`,
`city`, `country`. Note there is **no LinkedIn column** on `v_people`;
`v_investor_contacts` and `v_companies` have one. Join `v_people` to
`v_companies` on `company_pb_id` for company detail alongside contacts.

## The one join you will use most

Contacts at investor firms live in `v_people`, not in a dedicated investor
contacts table. There is no key, so you match on **normalized domain**:
`investor_domain` from `v_investors` or `v_company_portfolio` against either the
host of `v_people.company_website` or the corporate domain of `v_people.email`.

Normalization: lowercase, strip `https://` or `http://`, strip everything from
the first `/`, strip a leading `www.`. When matching on email domain, exclude
free providers (`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`,
`icloud.com`, `protonmail.com`, `aol.com`, `live.com`, `msn.com`, `ymail.com`,
`mail.com`, `googlemail.com`), or you will pull in every person with a personal
address.

Never require an exact URL match. For "who invested in company X", filter
`v_company_portfolio` with
`(LOWER(company_domain) LIKE '%x%' OR LOWER(company_name) LIKE '%x%')` first,
then join out to contacts.

`v_investor_contacts` is the legacy path for the same question. Use it only when
the user names it.

## Common asks and where they go

| Ask | Table |
|---|---|
| "how many investors in Germany" | `v_investors` |
| "who invested in Acme" | `v_company_portfolio`, filtered on the company |
| "seed and Series A deals in 2025" | `v_company_portfolio`, `LOWER(deal_type) LIKE '%seed%'`, and `deal_type_2` |
| "contacts at these investor firms" | `v_company_portfolio` or `v_investors` joined to `v_people` by normalized domain |
| "UK companies with 50 to 200 staff" | `v_companies` |
| "partners with fintech in their bio" | `v_people` on `bio` and `title` |
| "family offices that prefer fintech" | `mat_family_office` (see below) |
| "rank investors for our company" | not a Vault query. Use `caeros_investor_match`. |

## Family-office gotcha

Both family-office tables are allowlisted, so hand-written SQL through
`analyst_vault_run_sql` always works. Natural language through
`analyst_vault_query` depends on your build: the SQL generator was briefed on
only the five investor and company views until that was fixed, and on an older
build a family-office question comes back as the wrong view or an `ERROR:`. If
that happens, write the SQL yourself.

`mat_family_office` keys on `entity_key`, which IS the firm domain (there is no
`domain` column), with `name` for the firm and `summary` for the thesis.
`v_family_office_contacts` joins on the same `entity_key`. Their
`stages`, `industry_preferences`, `funding_style`, and `location_breakdown`
columns are weighted free-text strings like `70% Seed, 30% Series A`, so filter
them with `LIKE`, never equality. For matching family offices to a thesis
rather than filtering them, load `family-office-match`.

## Limits

- Generated SQL defaults to `LIMIT 1000`. The row cap is 10,000 per query.
- Scan ceiling is 20 GB billed per query. A query over everything with no filter
  will hit it. Filter early and select only the columns you need.
- `analyst_export_csv` in SQL mode goes up to 100,000 rows (`max_rows`), well
  past the query row cap. That is the route for a large deliverable.

## CSV rule

For any contact, person, prospect, lead, company, or investor deliverable, call
`analyst_export_csv` with `sql`, so rows stream from the Vault straight to the
file. Never pass query results back in as `rows_json`, even if the preview
returned three rows. Hosted export rejects `rows_json` outright. `filename` must
match `^[a-zA-Z0-9][a-zA-Z0-9._-]{0,120}\.csv$`.

## Reading `meta`

Results carry `meta.error`, `meta.retryable`, and `meta.user_action`.

- `meta.retryable: true`, or a plain SQL or validation error: refine the question
  or the SQL and try again.
- `meta.retryable: false`, or a `user_action` reporting backend unavailable,
  authorization, dataset access, or operator attention: **stop all data access**.
  Report the safe error and that no CSV was created. Do not work around it.

## Fail closed

If the Vault is unavailable, say so and stop. Never substitute web search,
public knowledge, or model memory for Vault rows. Never estimate a LinkedIn URL,
never construct an email from a name and a domain, and never leave a guessed
value in a column that looks like fact. A short honest result beats a full
fabricated one.
