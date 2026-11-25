---
name: winding-up-review
description: >
  Advise on winding-up processes under the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Cap 32), including members' voluntary liquidation (MVL), creditors' voluntary liquidation (CVL), and compulsory winding up. Covers liquidator powers, antecedent transactions, director liability, and creditor strategies.
---
# Winding Up Review — Skill

## Purpose

Advise on winding-up processes under the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Cap 32), including members' voluntary liquidation (MVL), creditors' voluntary liquidation (CVL), and compulsory winding up. Covers liquidator powers, antecedent transactions, director liability, and creditor strategies.

## Scope

- Members' Voluntary Liquidation (MVL) — solvent companies
- Creditors' Voluntary Liquidation (CVL) — insolvent companies
- Compulsory Winding Up by court
- Provisional liquidation
- Official Receiver's role
- Liquidator powers and duties
- Antecedent transactions (unfair preferences, undervalue transactions, floating charges)
- Director liability (wrongful trading, fraudulent trading, misfeasance)
- Proof of debt and distribution
- Disqualification of directors
- Cross-border insolvency (UNCITRAL Model Law adoption in HK)

## Workflow

### 1. Determine Winding-Up Route

| Factor | MVL | CVL | Compulsory |
|--------|-----|-----|------------|
| Solvency | Solvent | Insolvent | Usually insolvent |
| Initiation | Directors + Members | Directors + Members | Creditor/Member/Official |
| Liquidator | Members appoint members' liquidator | Creditors appoint liquidator | Official Receiver → private |
| Court involvement | Minimal | Limited | Full |
| Timeframe | 6–12 months | 6–24 months | 12–36 months |

### 2. MVL — Members' Voluntary Liquidation

**Requirements**:
- Directors make a statutory declaration of solvency (s.233 Cap 32) — must include statement of assets and liabilities
- Solvency declaration valid for 5 weeks before resolution
- Members pass a special resolution for winding up (s.228)
- Liquidator appointed by members (s.235)

**Process**:
- Declaration lodged with CR
- Notice published in Gazette
- Liquidator collects assets, pays debts, distributes surplus
- Final meeting of members called
- Liquidator files return; company dissolved after 3 months (or as directed)

### 3. CVL — Creditors' Voluntary Liquidation

**Requirements**:
- Directors fail to make solvency declaration (or declaration invalid)
- Members pass special resolution (s.228)
- Creditors' meeting conducted (s.241) — liquidator nominated by creditors prevails

**Process**:
- Directors prepare statement of affairs (s.242)
- Creditors' meeting within 28 days of resolution
- Committee of inspection formed (optional)
- Liquidator investigates, collects assets, challenges antecedent transactions
- Proofs of debt adjudicated
- Distribution in statutory order
- Final meeting; dissolution

### 4. Compulsory Winding Up

**Petition Grounds** (s.177 Cap 32):
- Inability to pay debts (most common — s.178)
- Just and equitable (s.177(1)(f))
- Public interest
- Court order in unfair prejudice or derivative action

**Procedure**:
- Petition to CFI
- First hearing (directions)
- Winding-up order made or dismissed
- Official Receiver becomes provisional liquidator
- Public examination of directors possible (s.222)
- Private liquidator appointed by creditors/members on OR recommendation

### 5. Liquidator's Powers

- Collect and realise assets (s.199, s.251)
- Examine directors and officers (s.221, s.222)
- Apply to examine third parties (s.224)
- Challenge antecedent transactions:
  - **Unfair preferences** (s.266B) — 6-month relation-back period (2 years for connected persons)
  - **Transactions at undervalue** (s.265A) — 5-year relation-back period
  - **Floating charges** (s.267) — void if created within 12 months of winding up (2 years for connected persons)
  - **Extortionate credit transactions** (s.264B) — open-ended review
- Seek contribution from directors:
  - **Wrongful trading** (s.168E) — personal contribution to assets
  - **Fraudulent trading** (s.168B) — criminal + civil liability
  - **Misfeasance** (s.276) — director/officer breach

### 6. Distribution Priority

| Rank | Class | Notes |
|------|-------|-------|
| 1 | Fixed charge holders | Realisation of secured assets |
| 2 | Liquidator's expenses | Costs of liquidation, remuneration |
| 3 | Preferential creditors | Employees (wages, leave pay — capped) |
| 4 | Floating charge holders | From circulating assets |
| 5 | Unsecured creditors | Rateable distribution (dividend) |
| 6 | Deferred debts | Subordinated debt, shareholder loans |
| 7 | Members | Surplus (if any) |

### 7. Director Disqualification

**Grounds** (s.168G–168R Cap 32):
- Wrongful trading
- Fraudulent trading
- Misfeasance
- Breach of directors' duties
- Persistent default under Cap 622

**Duration**: Up to 15 years
**Consequences**: Cannot be director, liquidator, or involved in company management without court leave

## Key Provisions

| Section (Cap 32) | Subject | Key Detail |
|------------------|---------|------------|
| s.177 | Grounds for winding up | Among others: inability to pay debts, just and equitable |
| s.178 | Inability to pay debts | Statutory demand, unsatisfied execution, balance sheet test |
| s.228 | Resolution for winding up | Special resolution (75%) required |
| s.233 | Solvency declaration | Directors must declare solvency within 5 weeks |
| s.168B | Fraudulent trading | Intent to defraud creditors; criminal + civil |
| s.168E | Wrongful trading | No reasonable prospect of avoiding liquidation |
| s.265A | Transaction at undervalue | 5-year review period |
| s.266B | Unfair preference | 6-month review (2 years connected) |
| s.267 | Avoidance of floating charges | Void if created within 12 months (2 years connected) |
| s.276 | Misfeasance | Summary remedy against directors/officers |

## Key Cases

- **Re Ciro Citterio Menswear plc (in liquidation)** — Wrongful trading, director knowledge
- **Re Beijing Enterprises Holdings Ltd** — MVL and distribution
- **Re UDL Holdings Ltd** — Set-off in liquidation
- **Re Lam Kwai Chung Garment Factory Ltd** — Just and equitable winding up
- **Securities and Futures Commission v Stock Exchange of Hong Kong Ltd** — Director liability

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





- HKLII (https://www.hklii.hk) — Winding-up case law
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 32 provisions
- Companies Registry e-Search (https://www.icris.cr.gov.hk) — Gazette notices, company winding-up status
- Official Receiver's Office — Practice directions, forms, and guidelines


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10

python3 corporate-legal/scripts/check_company.py <BRN_or_name>
```
