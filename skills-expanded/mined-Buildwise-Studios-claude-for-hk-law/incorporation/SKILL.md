---
name: incorporation
description: >
  Guide legal practitioners and company secretaries through the process of incorporating a Hong Kong company under the Companies Ordinance (Cap 622), including company structure, constitutional documents, and post-incorporation compliance.
---
# Incorporation — Skill

## Purpose

Guide legal practitioners and company secretaries through the process of incorporating a Hong Kong company under the Companies Ordinance (Cap 622), including company structure, constitutional documents, and post-incorporation compliance.

## Scope

- Company types available under Cap 622
- Memorandum and Articles of Association (M&A)
- Company name registration and restrictions
- Registered office requirements
- Company secretary appointment
- Director and member requirements
- Share capital structure (no par value)
- Post-incorporation filings

## Workflow

### 1. Determine Company Structure

- **Private company limited by shares** — standard choice for commercial operations
- **Public company limited by shares** — for public offerings, stricter compliance
- **Company limited by guarantee** — NPOs, clubs, trade associations
- **Unlimited company** — rare; used for specific regulatory reasons

### 2. Name Reservation and Checks

- Check name availability via Companies Registry e-Search
- Avoid names identical to existing companies (s.100, Cap 622)
- Restricted names: "bank", "insurance", "trust", "securities", "chamber of commerce", etc. require consent
- Offensive or misleading names are prohibited
- Reserve name online via CR e-Services (valid for 60 days)

### 3. Prepare Constitutional Documents

**Memorandum of Association** must include:
- Company name
- Members' limited liability statement (if applicable)
- Share capital clause (optional; no par value)

**Articles of Association**:
- Model Articles (Schedule 2, Cap 622) apply by default
- Custom articles may be adopted — override model articles where inconsistent
- Key provisions to consider: share transfer restrictions, director powers, board meeting procedures, dividend policy, share issuance authority, indemnity provisions

### 4. File Incorporation Documents

Documents to file with the Companies Registry:

1. Incorporation Form (Form NNC1) — includes proposed director(s), secretary, shareholder details
2. Articles of Association (if customised)
3. Statement of Compliance
4. Business Registration Application (handled concurrently)

**Filing Methods**:
- e-Registry (CR e-Services) — same-day processing (approximately HK$1,545)
- Paper filing — 4 working days (approximately HK$1,720)
- Business Registration Fee: HK$250–HK$3,950 (depending on exemption/waiver)

### 5. Post-Incorporation Steps

- Obtain Certificate of Incorporation and Business Registration Certificate
- Open bank account (physical director presence typically required)
- Maintain Statutory Registers:
  - Register of members
  - Register of directors and secretary
  - Register of charges
  - Significant Controllers Register (SCR) — required within 7 days of incorporation
- Issue share certificates to members
- Appoint auditor (within 9 months unless exempt)
- Ensure directors understand their duties (s.465, Cap 622)
- Display company name at registered office

### 6. Ongoing Obligations

- Annual Return (NAR1) — within 42 days of incorporation anniversary
- Annual financial statements and audit (unless exempt small company)
- Annual profits tax return (IRD)
- Business Registration renewal (annually)
- Change notifications to CR (directors, secretary, registered office within 15 days)

## Key Sections

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.67 | Incorporation | Director, secretary, member, registered address |
| s.98–100 | Company name | Prohibition on identical/deceptively similar names |
| s.116 | Default articles | Model articles apply if no alternative |
| s.475 | Directors' interest declaration | Must declare in board meetings |
| s.627 | Register of members | Must be kept at registered office or prescribed place |
| s.653 | SCR | Required under AML Ordinance |

## Common Pitfalls

- **Registered office**: Must be a physical address in HK (not a PO Box)
- **Company secretary**: Individual must be ordinarily resident in HK; corporate secretary must have registered office in HK
- **Minimum director**: At least one natural person; no corporate director for private companies
- **SCR compliance**: Failure to maintain is a criminal offence; many newly incorporated companies miss this
- **Business Registration**: Must be obtained before commencing business

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





- Companies Registry e-Services Portal: https://e-services.cr.gov.hk
- Companies Registry Open Data: data.gov.hk/en-data/dataset/hk-cr-crdata-list-addr
- Hong Kong e-Legislation: https://www.elegislation.gov.hk
- CR Practice Directions and FAQs (cr.gov.hk)
- Model Articles (Schedule 2, Cap 622)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10

python3 corporate-legal/scripts/check_company.py <BRN_or_name>
```
