---
name: compabase-company-research
description: Research Polish companies with Compabase - find companies, check KRS registry data, financial statements, management, beneficial owners, public tenders, EU funds, insolvency and sanctions records.
---

# Polish company research with Compabase

Use the Compabase tools when the user asks about a Polish company, wants to verify a business partner, or needs a list of Polish companies matching criteria.

## Workflow

1. Identify the company with `search_companies` (name, NIP, KRS, REGON, city, PKD code or revenue range). Use the KRS number from the result in the next calls. If several companies match, ask the user which one they mean.
2. `get_company` for the registry profile and headline financials.
3. Add detail only as needed:
   - `get_financials` for full statements by year, `get_company_rankings` for its position in its industry or region, `get_financial_stats` for sector benchmarks.
   - `get_company_people` (management and supervisory boards, shareholders) and `get_company_beneficiaries` (beneficial owners).
   - Public money: `get_company_public_tenders`, `get_company_eu_tenders`, `get_company_eu_funds`, `get_company_public_aid`, `get_company_eu_grants`.
   - Risk checks: `get_company_debt_registry` (insolvency and restructuring), `get_company_court_gazette`, `get_company_sanctions`, `get_company_financial_supervision`, `get_company_secured_liabilities`.
   - Other registers: `get_company_stock_market`, `get_company_energy_licenses`, `get_company_waste_registry`, `get_company_articles_of_association`.
4. `count_companies` answers "how many" questions without listing companies.

## Answering

- Quote the company name with its KRS or NIP, and give the reporting period and currency for financial figures.
- State clearly when a register has no records for the company, rather than implying a problem or a clean record beyond what the data shows.
- Do not guess figures that are missing from the results.

## Account

The tools use the user's connected Compabase account. `get_usage` shows the remaining query quota. The plugin cannot change the account, keys, watchlist or billing.
