---
name: annual-compliance
description: >
  Guide legal practitioners and company secretaries through Hong Kong's annual corporate compliance obligations under the Companies Ordinance (Cap 622), including annual returns, financial statements, audit requirements, significant controllers register (SCR), and tax filings.
---
# Annual Compliance — Skill

## Purpose

Guide legal practitioners and company secretaries through Hong Kong's annual corporate compliance obligations under the Companies Ordinance (Cap 622), including annual returns, financial statements, audit requirements, significant controllers register (SCR), and tax filings.

## Scope

- Annual Return (Form NAR1) — content, timing, penalties
- Financial statements preparation and audit
- Annual General Meeting (AGM) requirements
- Significant Controllers Register (SCR) maintenance
- Business Registration renewal
- Profits Tax Return filing (IRD)
- Late filing penalties and rectification
- Directors' compliance obligations

## Workflow

### 1. Annual Return (NAR1)

**Timing**: Within 42 days of the anniversary of incorporation (s.662 Cap 622)

**Contents**:
- Registered office address
- Shareholders (members) list
- Share capital details
- Directors and company secretary details
- Register of members location

**Filing**: Via CR e-Services or paper Form NAR1

**Penalties for Late Filing**:
| Delay | Penalty |
|-------|---------|
| Up to 42 days | HK$870 |
| 42 days – 3 months | HK$1,740 |
| 3–6 months | HK$2,610 |
| 6–9 months | HK$3,480 |
| Over 9 months | HK$4,350 |

**Consequences**: Company may be struck off the register for persistent default.

### 2. Financial Statements

**Preparation**: Must comply with HKFRS / HKFRS for Private Entities

**Key requirements**:
- True and fair view of financial position
- Directors' report
- Auditor's report (unless exempt)
- Notes to accounts

**Filing**: Private companies file with CR — abridged accounts (small company) or full accounts; public companies file full accounts

**Exemptions** (s.373 Cap 622):
- Small private company: turnover ≤ HK$100M (2 of 3 criteria) → exempt from audit
- Eligible private company meeting size criteria → simplified reporting

### 3. Significant Controllers Register (SCR)

**Requirement**: Since 1 March 2018, all HK companies must maintain an SCR

**Contents**:
- Name, address, identity document of significant controller
- Nature of control (25%+ shares/votes, control of board)
- Date of entry in register
- Contact details

**Timeline**: Must be established within 7 days of incorporation; updated within 7 days of any change

**Access**:
- Law enforcement — full access
- Public — upon request to CR (limited access: name and nature of control)
- Company — must allow inspection by specified officers

**Penalties**:
- Company: HK$50,000 + HK$1,000/day continuing default
- Director/officer: HK$50,000 + HK$1,000/day

### 4. AGM Requirements

**Private companies**: No AGM required unless articles require (members may opt out by written resolution)
**Public companies**: AGM required annually; notice period: 21 days

### 5. Business Registration Renewal

**Timing**: Annually (within one month of expiry)

**Fee**: HK$250 (standard) / HK$2,150 (non-exempt)

**Method**: Online with IRD or paper form

**Consequences of non-renewal**: Late fee of up to HK$3,000; prosecution

### 6. Profits Tax Return (IRD)

**Filing**: Within one month of IRD issue (extensions available via tax representative)

**Deadline**:
- Standard: April–May each year
- New companies: ~18 months after incorporation
- Extension available for group companies and NPOs

**Who files**: Tax representative (usually auditor or tax accountant)

### 7. Compliance Calendar

| Obligation | Frequency | Deadline | Filing To |
|------------|-----------|----------|-----------|
| Annual Return | Annual | 42 days after anniversary | CR |
| SCR update | As needed | Within 7 days of change | Internal (CR on request) |
| Profits Tax Return | Annual | 1 month from IRD issue | IRD |
| Business Registration | Annual | Before expiry | IRD |
| Financial Statements | Annual | 9 months after year-end (first: 18 months) | CR / Members |
| AGM (public only) | Annual | Within 15 months of last AGM | Minutes to CR |
| Director changes | As needed | Within 15 days | CR |
| Registered office change | As needed | Within 15 days | CR |

## Common Pitfalls

- **Late NAR1**: Most common compliance failure — set calendar reminders
- **SCR omissions**: New incorporations often miss SCR setup
- **No registered agent**: Non-resident companies must have a registered agent
- **Forgotten dormant filings**: Even dormant companies must file returns
- **Audit exemption lost**: Company may lose exemption if it exceeds two of three criteria for two consecutive years
- **Director resignation not filed**: Remains on CR record until Form ND2A filed

## Live Data Lookup



You can look up live company data using the built-in script:



```bash

# Search by Business Registration Number

python3 scripts/check_company.py C1234567



# Search by company name

python3 scripts/check_company.py "Acme Trading"

```



The script uses the Companies Registry public open data API (data.cr.gov.hk — no auth required).

Returns: company name, BRN, type, status, incorporation date, and registered office address.





- Companies Registry e-Search (https://www.icris.cr.gov.hk) — e-Search, e-Registry, NAR1 filing
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 622 (ss.662, 373, SCR provisions)
- CR Practice Directions on Annual Return and SCR
- IRD Guide for Profits Tax


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10

python3 corporate-legal/scripts/check_company.py <BRN_or_name>
```
