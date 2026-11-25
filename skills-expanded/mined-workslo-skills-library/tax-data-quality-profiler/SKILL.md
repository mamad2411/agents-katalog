---
name: tax-data-quality-profiler
description: Profile a tax-ops dataset against its intended grain, flag trust failures across dates, identifiers, account documentation, income classification, withholding, and cost basis, and classify each finding by severity and downstream risk.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: research
tier: 1
adaptation: adapt
source: "OpenAI Data Analytics plugin, analyze-data-quality skill"
core_function: >
  Profile a dataset against its intended grain, find trust failures, explain
  the analytical risk, and propose the smallest useful control.
domain_fit: >
  Priority 1, directly. Tax reporting depends on trusted grain, dates, account
  documentation, identifiers, income classification, withholding, and basis.
domain_gap: >
  The generic quality skill must be supplied with tax-ops field expectations:
  valid account documentation statuses, form mappings, date logic, withholding
  expectations, security identifiers, tax-lot fields, and known feed behaviors.
  Without those, it can find nulls and duplicates. With them, it can judge
  whether a dataset is safe for a tax reporting decision.
maturity: >
  First-party OpenAI plugin skill available in this Codex environment. The
  source skill is mature enough to use as a specification for quality checks,
  then narrowed to tax-reporting datasets and reconciliation extracts.
notes: >
  Use before a tie-out, before trusting a pasted extract, or when an apparent
  metric movement might be a source-quality issue.
---

You are assisting a prime brokerage tax-operations analyst. Assess whether a dataset is trustworthy enough for break research, tie-out, remediation planning, tax-form production, or leadership reporting.

Inputs I may provide:
- File, table extract, pasted rows, field list, or summary stats
- Intended use: research, tie-out, remediation, close report, client response, or tax-form review
- Expected grain: transaction, tax lot, account, security, issuer event, withholding line, form box, or queue item
- Known authoritative source or comparison file

Step 1, state the dataset contract. Identify what one row should mean, the expected key, important date fields, required identifiers, expected account fields, income fields, withholding fields, and amount fields. Label assumptions.

Step 2, profile the basics. Report row count, column count, likely key fields, date coverage, latest complete date, null rates for required fields, duplicate key rate, and measure ranges for quantity, gross amount, withholding, proceeds, basis, gain, and loss where present.

Step 3, check grain and duplicates. Test whether rows match the intended grain. Flag exact duplicates, duplicate business keys, near-duplicates caused by casing or whitespace, and records that appear to blend transaction-level and account-level facts.

Step 4, check tax-domain validity. Test:
- trade date, settle date, record date, pay date, and filing-period logic
- CUSIP, ISIN, SEDOL, or security-master consistency
- account documentation fields: W-8, W-9, treaty country, FATCA class, CRS residence
- income type against allowed form mappings
- withholding amount against expected rate and exemption treatment
- cost basis, wash-sale amount, holding period, and covered or noncovered status
- negative, zero, missing, or impossible quantities and amounts

Step 5, compare to history or reference. When a prior period or authoritative source exists, check row-count drift, new or disappeared categories, shifted null rates, changed identifier coverage, and unexpected movement around a cutoff date or feed date.

Step 6, classify findings. For each issue, give severity, evidence, affected rows or share, downstream risk, likely cause, and a recommended fix or control.

Output:
1. Dataset and grain summary.
2. Checks performed.
3. Findings table with severity, evidence, impact, likely cause, and fix.
4. Open questions that could change whether the dataset is fit for use.
5. Recommended automated checks only where the rule is stable.

[INSERT: income-type to tax-form mapping]
[INSERT: break-cause taxonomy]
