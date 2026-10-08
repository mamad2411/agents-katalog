---
name: shareholder-remedies
description: >
  Advise shareholders on remedies available under Hong Kong company law for corporate misconduct, director breaches, and unfairly prejudicial conduct, including unfair prejudice petitions, derivative actions, and just and equitable winding up.
---
# Shareholder Remedies — Skill

## Purpose

Advise shareholders on remedies available under Hong Kong company law for corporate misconduct, director breaches, and unfairly prejudicial conduct, including unfair prejudice petitions, derivative actions, and just and equitable winding up.

## Scope

- Unfair Prejudice Petition (s.724 Cap 622)
- Statutory Derivative Action (ss.731–738 Cap 622)
- Winding Up on Just and Equitable Grounds (s.177(1)(f) Cap 32)
- Injunctions and interim relief
- Investigation by Financial Secretary (s.143 Cap 622)
- Common law remedies (personal claims, *Foss v Harbottle* exceptions)
- Strategic considerations: choice of remedy, costs, settlement

## Workflow

### 1. Identify the Grievance

- Mismanagement or director self-dealing?
- Exclusion from management (quasi-partnership)?
- Misfeasance, misappropriation, or breach of duty?
- Failure to provide information?
- Unfair dilution or share issuance?
- Oppression of minority?

### 2. Evaluate Available Remedies

#### Unfair Prejudice (s.724 Cap 622)

**Threshold**: Company's affairs conducted in an unfairly prejudicial manner to members (including petitioner).

**Key elements**:
- Legitimate expectation of participation (common in quasi-partnerships)
- Breach of trust or confidence
- Unfairness judged objectively
- Prejudice to petitioner's interests (not necessarily financial)

**Orders available** (s.725):
- Purchase of petitioner's shares (most common — fair value determined by court)
- Regulation of future company conduct
- Injunction or other order

**Typical cases**:
- *Re Chime Corporation Ltd* — leading HK authority
- *Re Tai Lap Investment Co Ltd* — quasi-partnership principles
- *Re Wong Kwok Keong v Goldveon Ltd* — exclusion from management

#### Derivative Action (ss.731–738 Cap 622)

**Threshold**: Member may apply for leave (court permission) to bring proceedings in company's name.

**Court considers**:
- *Prima facie* case
- Good faith of applicant
- Interests of the company
- Alternative remedies available
- Likelihood of success

**Advantages**:
- Company gets the benefit of the judgment
- Costs protection available (s.738 — indemnity for costs)
- Standing where company refuses to pursue wrongdoers

**Disadvantages**:
- Leave hurdle — court controls access
- Company may discontinue if it takes over
- Costs awarded against member if unsuccessful

#### Just and Equitable Winding Up (s.177(1)(f) Cap 32)

**Grounds**:
- Loss of substratum
- Deadlock at board level
- Breakdown of mutual trust (quasi-partnership)
- Justifiable lack of confidence in management

**Important**: Court has discretion to stay winding up if alternative remedy available (s.180(1) Cap 32). Often paired with unfair prejudice petition.

### 3. Strategic Considerations

| Factor | Unfair Prejudice | Derivative Action | Just & Eq. Winding Up |
|--------|------------------|-------------------|----------------------|
| Company continues? | Yes (usually) | Yes | No (liquidation) |
| Petitioner remains? | Often bought out | Yes | No |
| Relief for wrongs? | Indirect | Direct | Limited |
| Cost risk | Moderate | High | Moderate |
| Third-party effect | Members only | Company + wrongdoers | Creditors |
| Time to resolution | 12–24 months | 6–18 months (leave) | 6–18 months |

### 4. Draft and File

- **Unfair Prejudice**: Originating summons + affidavit evidence; seek directions
- **Derivative Action**: Ex parte leave application; evidence of *prima facie* case
- **Winding Up**: Petition to CFI; supporting creditor's or member's evidence

### 5. Settlement and Costs

- Unfair prejudice petitions often settle — share buyout at court-ordered or negotiated valuation
- Derivative actions may settle with costs against or in favour of member
- Court may order company to indemnify member for costs in derivative action
- ADR (mediation) strongly encouraged by HK courts

## Key Provisions

| Section | Remedy | Key Detail |
|---------|--------|------------|
| s.724 Cap 622 | Unfair prejudice | Any member may petition, court may order buyout |
| s.725 Cap 622 | Unfair prejudice orders | Wide discretion (buyout, regulation, injunction) |
| s.731 Cap 622 | Derivative action leave | Member must obtain court permission |
| s.732 Cap 622 | Derivative test | Good faith, company's interests, *prima facie* case |
| s.177(1)(f) Cap 32 | Just & equitable winding up | Courts use petition as drag-along pressure |
| s.180 Cap 32 | Stay of winding up | Court stays if alternative remedy available |

## Key Cases

- **Re Chime Corporation Ltd** — Leading unfair prejudice authority
- **Re Lam Kwai Chung Garment Factory Ltd** — Just and equitable winding up
- **Re Tai Lap Investment Co Ltd** — Quasi-partnership and unfair prejudice
- **Re Grand Field Group Holdings Ltd** — Derivative action leave principles
- **Re Haron International Ltd** — Deadlock and winding up

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





- HKLII (https://www.hklii.hk) — Company law case law
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 622 (ss.724–738), Cap 32 (s.177, ss.180)
- Companies Registry e-Search (https://www.icris.cr.gov.hk) — Company records for valuation evidence


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10

python3 corporate-legal/scripts/check_company.py <BRN_or_name>
```
