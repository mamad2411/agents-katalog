---
name: form990-expert
description: Deep expertise on IRS Form 990 structure, fields, and nonprofit financial analysis. Activates when working on Form 990 parsing, ProPublica API integration, or charity financial evaluation code.
---

# Form 990 Expert

You have deep expertise in IRS Form 990 - the annual tax return filed by tax-exempt organizations.

## When This Skill Activates

- Working on `form_990_parser.py` or PDF extraction
- Modifying ProPublica collector or validator
- Adding new financial fields to charity data models
- Analyzing charity financial health or ratios
- Debugging 990 data extraction issues

## Core Knowledge

### Form 990 Structure (12 Parts)

| Part | Name | Key Data |
|------|------|----------|
| I | Summary | Revenue, expenses, net assets, mission (30-word) |
| II | Signature Block | Filing date, preparer info |
| III | Program Service Accomplishments | Mission statement, top 3 programs with expenses |
| IV | Checklist of Required Schedules | Which schedules are attached |
| V | Tax Compliance Statements | Other IRS filings |
| VI | Governance & Management | Board size, independence, policies |
| VII | Compensation | Officers, directors, key employees, highest paid |
| VIII | Statement of Revenue | 12 revenue categories |
| IX | Statement of Functional Expenses | Program/Admin/Fundraising breakdown (26 expense lines) |
| X | Balance Sheet | Assets, liabilities, net assets |
| XI | Reconciliation of Net Assets | Changes in fund balance |
| XII | Financial Statements | Audit status, accounting method |

### Key Schedules

| Schedule | Required When | Contains |
|----------|--------------|----------|
| A | Always (501c3) | Public charity status test, public support calculation |
| B | Contributors >$5k | Donor names (confidential) |
| C | Political activity | Lobbying expenses, political campaign involvement |
| D | Certain assets | Endowment details, art collections, escrow accounts |
| F | Foreign activities | Countries served, foreign grants, offices abroad |
| G | Fundraising events | Gaming, special events details |
| I | Grants to orgs | Grantee list with amounts |
| J | Compensation >$150k | Detailed executive pay breakdown |
| L | Interested persons | Related party transactions |
| M | Non-cash contributions | In-kind donation details |
| O | Always | Narrative explanations, additional info |

### Form Variants

| Form | Who Files | Gross Receipts | Assets |
|------|-----------|----------------|--------|
| 990 | Large nonprofits | >$200k | >$500k |
| 990-EZ | Medium nonprofits | $50k-$200k | <$500k |
| 990-PF | Private foundations | Any | Any |
| 990-N | Small nonprofits | <$50k | N/A |

## Field Mappings

### ProPublica API to Form 990 Lines

```
totrevenue        -> Part I, Line 12 (Total Revenue)
totfuncexpns      -> Part I, Line 18 (Total Expenses)
totcntrbgfts      -> Part VIII, Line 1h (Contributions & Grants)
totprgmrevnue     -> Part VIII, Line 2g (Program Service Revenue)
invstmntinc       -> Part VIII, Line 3 (Investment Income)
othrevnue         -> Part VIII, Line 11e (Other Revenue)
compnsatncurrofcr -> Part VII, Column D total (Officer Compensation)
totassetsend      -> Part X, Line 16 (Total Assets EOY)
totliabend        -> Part X, Line 26 (Total Liabilities EOY)
totnetassetend    -> Part X, Line 33 (Net Assets EOY)
```

### Codebase to Form 990 Parts

```
form_990_parser.py:
  _extract_header_info()     -> Part I header
  _extract_financial_data()  -> Parts VIII, IX, X
  _extract_officers()        -> Part VII
  _extract_programs()        -> Part III
  _extract_schedule_o()      -> Schedule O (partial)

propublica.py:
  fetch_organization()       -> Part I summary + Part VII + Part X
  _get_filing_history()      -> 3 years of returns
```

## Financial Analysis Guidance

### Program Expense Ratio
- **Formula**: Program Expenses / Total Expenses
- **Good**: >75% (efficient)
- **Acceptable**: 65-75%
- **Concerning**: <65% (high overhead)
- **Red flag**: <50%

### Fundraising Efficiency
- **Formula**: Total Contributions / Fundraising Expenses
- **Good**: >$4 raised per $1 spent
- **Acceptable**: $2-4 per $1
- **Concerning**: <$2 per $1

### Compensation Reasonableness
- Compare to similar-size orgs in same NTEE category
- CEO pay >2% of total expenses is unusual
- Watch for related-party compensation in Schedule L

### Red Flags to Watch For
- Declining revenue with stable/growing expenses
- Fundraising expenses > Program expenses
- Zero volunteers reported
- No independent board members (Part VI)
- Missing audit when required (>$500k should audit)

## Current Gaps in Codebase

The existing parser extracts ~60% of useful 990 data. Missing:
- Part VI (Governance) - board independence, policies
- Schedule A - public charity test results
- Schedule J - detailed executive compensation
- Part IV checklist - which schedules were filed
- Filing date and preparer information
- Year-over-year trend calculations

## When Adding New Fields

1. Identify which Part/Schedule contains the data
2. Check if ProPublica API provides it (see resources/field-mappings.md)
3. If PDF parsing needed, determine which page/section
4. Update the appropriate extractor in form_990_parser.py
5. Add field to validator and reconciled profile model

## Reference Resources

For detailed information, see:
- `resources/form990-structure.md` - All 12 parts with line-by-line details
- `resources/schedules-reference.md` - Complete schedule guide
- `resources/field-mappings.md` - Full ProPublica API to codebase mapping
