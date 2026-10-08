---
name: directors-duties
description: >
  Advise on directors' duties under Hong Kong company law, including the codified statutory duties (s.465 Cap 622), continuing common law fiduciary duties, disclosure obligations, consequences of breach, and risk mitigation strategies.
---
# Directors' Duties — Skill

## Purpose

Advise on directors' duties under Hong Kong company law, including the codified statutory duties (s.465 Cap 622), continuing common law fiduciary duties, disclosure obligations, consequences of breach, and risk mitigation strategies.

## Scope

- Codified statutory duties (s.465 Cap 622)
- Common law and equitable duties
- Fiduciary duties: loyalty, no conflict, proper purpose
- Duty of skill, care, and diligence
- Disclosure and declaration of interests
- Directors' duties in insolvency context
- Consequences of breach
- Disqualification proceedings
- D&O insurance and indemnification

## Workflow

### 1. Identify the Duty or Duties Engaged

- Is the director acting in good faith and for the benefit of the company? (s.465(1))
- Is the director exercising power for a proper purpose? (s.465(2))
- Is there a conflict of interest? (s.465(3))
- Has the director accepted a benefit from a third party? (s.465(4))
- Is the director exercising reasonable care, skill, and diligence? (s.465(5))
- Is the director making unauthorised use of company property/information? (s.465(6))

### 2. Analyse the Factual Matrix

- What is the director's role and level of involvement?
- Does the company have independent legal advice?
- Are there other directors who knew or should have known?
- Is the company solvent, borderline, or insolvent?
- What is the nature of the breach (action or omission)?

### 3. Apply the Legal Standard

#### Good Faith / Proper Purpose
- Subjective test — what did the director actually believe?
- Proper purpose — objective test based on constitutional powers
- Mixed purposes: what was the dominant purpose?

#### No Conflict
- Any actual or potential conflict must be disclosed
- Crypto assets, side deals, competing businesses — all engaged
- Remedies: recission, account of profits, equitable compensation

#### Care, Skill, and Diligence
- Objective minimum standard + subjective (director's knowledge and experience)
- Higher standard for executive directors, lower for NEDs (but not negligible)
- Business judgment rule does not apply in HK as a distinct doctrine, but courts are reluctant to second-guess honest decisions

#### Insolvency Context
- Directors' duties shift to creditors when company is insolvent or near-insolvent
- Wrongful trading (s.168E Cap 32) — personal liability for continued trading
- Fraudulent trading (s.168B Cap 32) — criminal and civil liability

### 4. Assess Breach and Consequences

| Breach Type | Remedy | Limitation Period |
|-------------|--------|-------------------|
| Breach of fiduciary duty | Equitable compensation / account of profits | 6 years (court discretion) |
| Breach of duty of care | Damages | 6 years from breach |
| Breach of statutory duty | Various (injunctions, damages) | 6 years |
| Wrongful trading | Personal contribution to company assets | On winding up |
| Fraudulent trading | Criminal liability + civil contribution | No limitation for criminal |

### 5. Recommend Mitigation

- Disclosure: Declare interest at earliest board meeting (s.475)
- Board minutes: Document all decisions with rationale
- Independent advice: Seek where conflict arises
- Ratification: Members may ratify certain breaches by ordinary resolution
- D&O insurance: Permitted under s.466 (but not for dishonest acts)
- Resignation: Consider immediate resignation if fundamental conflict exists

## Key Provisions

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.465(1) | Good faith | In the best interests of the company |
| s.465(2) | Proper purpose | Powers must be exercised for proper constitutional purpose |
| s.465(3) | No conflict | Avoid actual/potential conflicts of interest |
| s.465(4) | No third-party benefits | Not to accept benefits from third parties |
| s.465(5) | Care, skill, diligence | Reasonable care (objective + subjective) |
| s.465(6) | No unauthorised use | Cannot misuse company property/information |
| s.466 | Indemnity / D&O insurance | Permitted except for negligence, default, breach of duty |
| s.475 | Declaration of interest | Must declare nature and extent in board meeting |
| s.488–498 | Loans to directors | Member approval required for loans, quasi-loans, credit |

## Key Cases

- **Re Grand Field Group Holdings Ltd** — Directors' duty and derivative action
- **Re Ciro Citterio Menswear plc (in liquidation)** — Wrongful trading principles
- **SFC v Stock Exchange of Hong Kong Ltd** — Directors' duties and regulatory obligations
- **Re Idap Tchnopark Ltd** — No conflict duty in quasi-partnership
- **Re Lee Kwok Keung v The Hong Kong Polytechnic University** — Skill and care standard for NEDs

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





- HKLII (https://www.hklii.hk) — Directors' duty case law
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 622, Cap 32 provisions
- SFC enforcement database for listed company cases


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10

python3 corporate-legal/scripts/check_company.py <BRN_or_name>
```
