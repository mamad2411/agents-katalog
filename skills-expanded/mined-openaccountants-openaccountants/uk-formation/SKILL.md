---
name: uk-formation
description: "> Use this skill whenever asked about forming, incorporating, or registering a company in the United Kingdom. Trigger on phrases like \"set up a company in the UK\", \"UK Ltd\", \"Companies House\", \"incorporate in England\", \"UK company formation\", \"register a business UK\", \"limited company UK\", \"LLP formation UK\", \"UK company costs\", \"confirmation statement\", or any question about starting a business entity in England, Wales, Scotland, or Northern Ireland. Covers entity types, registration process, capital requirements, costs, post-formation compliance, and bank account opening. ALWAYS read this skill before advising on UK company formation."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GB
  category: formation
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/uk-formation"
  tax_year: 2025-26
  obligation: FORM
---

# UK Company Formation Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Year applicability:** Rules in this skill apply across **2024-25, 2025-26, and 2026-27** unless a specific section flags a year-dated change. The pack is read alongside the rate-bearing skills (`uk-income-tax-sa100`, `uk-national-insurance`, `uk-dividends`, etc.) which carry full 3-year tables.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | United Kingdom of Great Britain and Northern Ireland |
| Currency | GBP |
| Company registrar | Companies House -- companies-house.gov.uk |
| Key legislation | Companies Act 2006; Economic Crime and Corporate Transparency Act 2023 |
| Typical formation time | 24 hours (online); 8--10 days (paper) |
| Corporate tax rate | 25% (main rate); 19% (small profits, taxable profits ≤ £50,000) |
| Skill version | 1.0 |

---

## Section 2 -- Entity Types Comparison

| Feature | Sole Trader | Private Ltd (Ltd) | Limited Liability Partnership (LLP) | Public Ltd (PLC) |
|---|---|---|---|---|
| Legal personality | No | Yes | Yes | Yes |
| Liability | Unlimited | Limited to share capital | Limited to capital contribution | Limited to share capital |
| Min. members | 1 | 1 shareholder + 1 director | 2 designated members | 2 directors + 1 secretary |
| Min. share capital | N/A | £1 (no minimum prescribed) | N/A (capital contribution) | £50,000 (25% paid up = £12,500) |
| Tax treatment | Income tax + NIC | Corporation tax | Partners taxed individually | Corporation tax |
| Admin burden | Low | Medium | Medium | High |
| Audit required | No | Only if thresholds exceeded | Only if thresholds exceeded | Yes |
| Filing accounts | No | Yes (abbreviated for micro/small) | Yes | Yes (full) |

**Recommended default:** Private company limited by shares (Ltd) for most commercial purposes.

---

## Section 3 -- Registration Process

### Step 1: Choose Company Name
- Check availability on Companies House name checker
- Must not be identical to or "too like" an existing registered name
- Sensitive words (bank, royal, charity) require prior approval
- Must end in "Limited" or "Ltd" (or Welsh equivalents)

### Step 2: Prepare Incorporation Documents
- **Memorandum of association** -- subscribers confirm intention to form a company
- **Articles of association** -- use model articles (SI 2008/3229) or bespoke articles
- **Form IN01** -- application for registration (submitted online as part of digital flow)

### Step 3: Register with Companies House
- Online: via Companies House Web Incorporation Service or software filing
- Fee: £100 (online/software) or £124 (paper); same-day service £156 (software only)
- Provide: company name, registered office address, director(s), shareholder(s), SIC code, articles, share structure

### Step 4: Receive Certificate of Incorporation
- Typically within 24 hours for online filings
- Certificate confirms company number, date of incorporation, and registered office

### Step 5: Register for Corporation Tax with HMRC
- Must register within 3 months of starting to trade
- Obtain Unique Taxpayer Reference (UTR)

### Step 6: Register for VAT (if applicable)
- Mandatory if taxable turnover exceeds £90,000 (2025/26 threshold)
- Voluntary registration permitted below threshold

### Step 7: Set Up PAYE (if employing staff)
- Register as employer with HMRC before first payday

### Step 8: Register for Confirmation Statement
- Annual confirmation statement due at least once every 12 months (£50 online / £110 paper)

---

## Section 4 -- Capital Requirements

| Entity Type | Min. Share Capital | Min. Paid-Up | Payment Timing | In-Kind Contributions |
|---|---|---|---|---|
| Private Ltd | £1 (no statutory minimum) | No minimum paid-up requirement | On or after incorporation | Permitted (no independent valuation required for private companies) |
| PLC | £50,000 | 25% (£12,500) + share premium | Before trading certificate issued | Permitted (independent valuation required) |
| LLP | N/A | Members agree capital contribution | Per LLP agreement | Per LLP agreement |

---

## Section 5 -- Costs Breakdown

| Cost Component | Amount (GBP) | Notes |
|---|---|---|
| Companies House incorporation (online) | £100 | Standard service (~24 hours) |
| Companies House incorporation (same-day) | £156 | Software filing only |
| Companies House incorporation (paper) | £124 | 8--10 working days |
| Annual confirmation statement | £50 (online) / £110 (paper) | Due every 12 months |
| Registered office service | £50--£300/year | If using a service address |
| Accountant fees (annual) | £500--£3,000/year | Varies by complexity |
| Company secretary (optional) | £0--£500/year | Not required for Ltd |
| **Total initial cost** | **£100--£300** | Government fees only; professional fees additional |

### Annual Maintenance

| Item | Cost (GBP) |
|---|---|
| Confirmation statement | £50 |
| Corporation tax filing | Included in accountant fees |
| Annual accounts filing (Companies House) | Free |
| Registered office | £50--£300 |
| Accountancy fees | £500--£3,000 |

---

## Section 6 -- Post-Formation Compliance

| Obligation | Deadline | Authority |
|---|---|---|
| Confirmation statement | Within 14 days of review period end (annual) | Companies House |
| Annual accounts | 9 months after financial year-end (private) | Companies House |
| Corporation tax return (CT600) | 12 months after accounting period end | HMRC |
| Corporation tax payment | 9 months and 1 day after accounting period end | HMRC |
| VAT returns | Quarterly (MTD-compliant software required) | HMRC |
| PAYE/RTI submissions | On or before each payday | HMRC |
| PSC register (People with Significant Control) | Maintain and update within 14 days of changes | Companies House |
| Register of members | Maintain at registered office | Internal |

---

## Section 7 -- Bank Account Opening

### Documents Typically Required
- Certificate of incorporation
- Memorandum and articles of association
- ID and proof of address for all directors and shareholders (25%+)
- Proof of registered office
- Business plan or description of activities

### Typical Timeline
- 1--5 working days (UK digital banks: Tide, Starling, Revolut Business)
- 2--4 weeks (traditional high-street banks)

### Common Banks
- Barclays, HSBC UK, Lloyds, NatWest (high street)
- Tide, Starling Bank, Revolut Business, Monzo Business (digital)

---

## Section 8 -- Foreign Founder Considerations

| Question | Answer |
|---|---|
| Non-resident directors allowed? | Yes -- no residency requirement for directors |
| Minimum UK-resident director? | No (but at least one natural person aged 16+ required) |
| Nominee shareholders permitted? | Yes (PSC register must still disclose ultimate beneficial owners) |
| Apostille requirements | Foreign ID documents may need certified translation |
| Physical presence required? | No -- entire process can be completed remotely |
| Foreign ownership restrictions | None for standard Ltd; FCA-regulated activities require separate authorisation |
| ID verification | From 2024, Companies House requires verified identity for directors and PSCs |

---

## Section 9 -- Common Mistakes and Refusals

**R-UK-F1 -- Shell company for fraud.** "This skill will not assist in forming a company intended as a shell for fraudulent or money-laundering purposes. Under the Economic Crime and Corporate Transparency Act 2023, Companies House has enhanced powers to query and reject suspicious filings."

**R-UK-F2 -- Using a fake registered office.** "The registered office must be a genuine address where documents can be served. PO Boxes are not permitted. Virtual office services are acceptable if they provide a physical address and forward mail."

**R-UK-F3 -- Failure to disclose PSCs.** "Every UK company must maintain a PSC register. Deliberate failure to identify and disclose people with significant control is a criminal offence."

**R-UK-F4 -- Trading without VAT registration.** "If taxable turnover exceeds £90,000, VAT registration is mandatory. Trading above the threshold without registration risks penalties and backdated assessments."

**R-UK-F5 -- Dormant company misconception.** "A dormant company still has filing obligations (annual accounts and confirmation statement). Failure to file leads to penalties and eventual compulsory strike-off."

---

## Section 10 -- Timeline

| Step | Duration | Cumulative |
|---|---|---|
| Name check and document preparation | 1--2 days | Day 1--2 |
| File online with Companies House | 1 day | Day 2--3 |
| Certificate of incorporation received | Same day to 24 hours | Day 2--4 |
| Open business bank account | 1--5 days (digital) / 2--4 weeks (high street) | Day 3--28 |
| Register for corporation tax (HMRC) | 1--7 days | Day 4--35 |
| Register for VAT (if needed) | 1--30 days | Day 5--65 |
| Set up PAYE (if employing) | 1--5 days | Day 6--70 |
| **Ready to trade** | | **As fast as 2--3 days (digital bank)** |

The UK has one of the fastest and cheapest company formation processes globally.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute legal, tax, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/uk-formation) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
