---
name: belgium-financial-statements
description: "> Use this skill when preparing, reviewing, or advising on annual financial statements (jaarrekening / comptes annuels) for a Belgian company. Trigger on phrases like \"jaarrekening\", \"comptes annuels Belgique\", \"NBB deposit\", \"Nationale Bank\", \"Banque Nationale de Belgique\", \"BNB\", \"Belgian GAAP\", \"Code des sociétés et associations\", \"WVV\", \"audit Belgium\", \"commissaris\", \"verkort schema\", \"volledig schema\", or any question about preparing and filing statutory accounts under Belgian company law. Covers Belgian GAAP frameworks, size thresholds, required statements, formats, notes, filing deadlines, and audit requirements."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: BE
  category: financial-statements
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/belgium-financial-statements"
  obligation: FS
---

# Belgium Financial Statements Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Belgium (Koninkrijk België / Royaume de Belgique) |
| Currency | EUR |
| Filing authority | Nationale Bank van België / Banque Nationale de Belgique (NBB/BNB) — Centrale des Bilans |
| Primary legislation | Code des Sociétés et des Associations (CSA) / Wetboek van Vennootschappen en Verenigingen (WVV) |
| Supporting legislation | Koninklijk Besluit / Arrêté Royal of 29 April 2019 (chart of accounts and annual account formats) |
| Accounting standards | Belgian GAAP (KB/AR of 29 April 2019 + Advice CBN/CNC) |
| Financial year | Any 12-month period (calendar year most common) |
| Filing deadline | 30 days after AGM approval; at latest 7 months from year-end |
| Filing fee | EUR 71.80–426.40 (depending on model and filing method) |
| Digital filing | XBRL via NBB Filing application (filing.nbb.be) |

---

## Section 2 -- Reporting Framework

| Entity type | Applicable standard |
|---|---|
| Large companies | Belgian GAAP — volledig schema / schéma complet (full model) |
| Small companies | Belgian GAAP — verkort schema / schéma abrégé (abbreviated model) |
| Micro companies | Belgian GAAP — micro schema / schéma micro (micro model) |
| Listed groups (consolidated) | IFRS as adopted by the EU (mandatory) |
| Non-listed groups (consolidated) | Belgian GAAP consolidated rules or IFRS (choice) |

Belgian GAAP is unique to Belgium and differs significantly from IFRS in areas such as extraordinary items, provisions, revaluations, and revenue recognition.

---

## Section 3 -- Size Thresholds

Effective for financial years beginning on or after 1 January 2024 (Art. 1:24, 1:25 CSA/WVV):

### Large company (Art. 1:24)

A company is **large** if it exceeds more than one of:

| Criterion | Threshold |
|---|---|
| Jaaromzet / Chiffre d'affaires (Turnover excl. VAT) | EUR 11,250,000 |
| Balanstotaal / Total du bilan (Balance sheet total) | EUR 6,000,000 |
| Gemiddeld personeelsbestand / Effectif moyen (FTE) | 50 |

If no more than one is exceeded → company is **small**.

### Micro company (Art. 1:25)

A small company is **micro** if it exceeds no more than one of:

| Criterion | Threshold |
|---|---|
| Jaaromzet / Chiffre d'affaires (Turnover excl. VAT) | EUR 900,000 |
| Balanstotaal / Total du bilan (Balance sheet total) | EUR 450,000 |
| Gemiddeld personeelsbestand / Effectif moyen (FTE) | 10 |

Assessment based on the **consistency principle**: exceeding (or no longer exceeding) thresholds has consequences only if it occurs for **two consecutive** years.

---

## Section 4 -- Required Financial Statements

| Document | Micro | Small (verkort) | Large (volledig) |
|---|---|---|---|
| Balans (Balance sheet) | Required (micro model) | Required (abbreviated) | Required (full) |
| Resultatenrekening (P&L) | Required (micro model) | Required (abbreviated) | Required (full) |
| Toelichting (Notes) | Required (minimal) | Required (abbreviated) | Required (full) |
| Sociale balans (Social report) | Required | Required | Required |
| Jaarverslag (Management report) | Not required | Not required | Required |
| Verslag commissaris (Audit report) | Not required | Not required | Required |

The **sociale balans** (social balance sheet reporting employee information) is mandatory for all Belgian companies filing annual accounts.

---

## Section 5 -- Year-End Adjustments Checklist

| # | Adjustment | Belgium-specific notes |
|---|---|---|
| 1 | Afschrijvingen (Depreciation) | Linear depreciation standard; declining balance if justified; minimum fiscal rates often applied |
| 2 | Voorzieningen voor risico's en kosten | CBN/CNC advice; probable and estimable obligations |
| 3 | Overlopende rekeningen (Accruals) | Strict matching; prorata temporis |
| 4 | Waardevermindering op handelsvorderingen (Bad debts) | Case-by-case assessment; tax deductibility requires proof of irrecoverability |
| 5 | Voorraden (Inventory) | Lower of cost (FIFO/weighted average/LIFO allowed) and market value |
| 6 | Uitgestelde belastingen (Deferred tax) | Very limited under Belgian GAAP — only timing differences on grants and capital gains |
| 7 | Wisselkoersverschillen (FX) | Monetary: closing rate; unrealised losses provisioned; unrealised gains not recognised |
| 8 | Vakantiegeld (Holiday pay) | Mandatory provision for holiday pay earned but not yet paid |
| 9 | Herwaarderingsmeerwaarden (Revaluations) | Permitted under Belgian GAAP if durable excess value; credited to revaluation surplus |
| 10 | Eindejaarspremie (13th month provision) | Provision for year-end premium if applicable per CLA |
| 11 | Investeringsaftrek (Investment deduction) | Tax computation item; off-balance sheet |
| 12 | Ontvangen subsidies (Grants) | Capital grants: balance sheet item released over asset life |

---

## Section 6 -- Resultatenrekening Format (P&L)

Belgian GAAP — volledig schema (by nature):

```
I.    Bedrijfsopbrengsten (Operating income)
      A. Omzet (Turnover)
      B. Wijziging in voorraad goederen in bewerking, gereed product
      C. Geproduceerde vaste activa
      D. Andere bedrijfsopbrengsten

II.   Bedrijfskosten (Operating charges)
      A. Handelsgoederen, grond- en hulpstoffen
      B. Diensten en diverse goederen
      C. Bezoldigingen, sociale lasten en pensioenen
      D. Afschrijvingen en waardeverminderingen
      E. Voorzieningen voor risico's en kosten
      F. Andere bedrijfskosten
      G. Als herstructureringskosten geactiveerde bedrijfskosten (-)

III.  Bedrijfswinst / Bedrijfsverlies (Operating profit/loss)

IV.   Financiële opbrengsten (Financial income)
V.    Financiële kosten (Financial charges)

VI.   Winst / Verlies uit gewone bedrijfsuitoefening

VII.  Uitzonderlijke opbrengsten (Exceptional income)
VIII. Uitzonderlijke kosten (Exceptional charges)

IX.   Winst / Verlies van het boekjaar vóór belasting

X.    Belastingen op het resultaat (Income tax)
XI.   Winst / Verlies van het boekjaar (Net profit/loss)

XII.  Onttrekking aan belastingvrije reserves
XIII. Overboeking naar belastingvrije reserves
XIV.  Te bestemmen winst / verlies van het boekjaar
```

---

## Section 7 -- Balans Format (Balance Sheet)

Belgian GAAP — volledig schema:

```
ACTIVA (Assets)

VASTE ACTIVA (Fixed assets)
  I.    Oprichtingskosten (Formation expenses)
  II.   Immateriële vaste activa (Intangible assets)
  III.  Materiële vaste activa (Tangible assets)
        A. Terreinen en gebouwen
        B. Installaties, machines en uitrusting
        C. Meubilair en rollend materieel
        D. Leasing en soortgelijke rechten
        E. Overige materiële vaste activa
        F. Activa in aanbouw
  IV.   Financiële vaste activa (Financial fixed assets)

VLOTTENDE ACTIVA (Current assets)
  V.    Vorderingen op meer dan één jaar
  VI.   Voorraden en bestellingen in uitvoering
  VII.  Vorderingen op ten hoogste één jaar
  VIII. Geldbeleggingen (Short-term investments)
  IX.   Liquide middelen (Cash)
  X.    Overlopende rekeningen (Accrued income/prepayments)

─────────────────────────────────────

PASSIVA (Equity and Liabilities)

EIGEN VERMOGEN (Equity)
  I.    Inbreng (Capital / Contribution)
  II.   Uitgiftepremies (Share premium)
  III.  Herwaarderingsmeerwaarden (Revaluation surplus)
  IV.   Reserves
  V.    Overgedragen winst/verlies (Retained earnings)
  VI.   Kapitaalsubsidies (Capital grants)

VOORZIENINGEN EN UITGESTELDE BELASTINGEN (Provisions)
  VII.  Voorzieningen voor risico's en kosten
  VIII. Uitgestelde belastingen

SCHULDEN (Liabilities)
  IX.   Schulden op meer dan één jaar
  X.    Schulden op ten hoogste één jaar
  XI.   Overlopende rekeningen (Accrued charges/deferred income)
```

---

## Section 8 -- Toelichting (Notes to Accounts)

| # | Disclosure | Micro | Small (verkort) | Large (volledig) |
|---|---|---|---|---|
| 1 | Accounting policies (waarderingsregels) | Simplified | Required | Required |
| 2 | Fixed asset movements | Not required | Required (summary) | Required (full) |
| 3 | Financial fixed assets detail | Not required | Required | Required (full) |
| 4 | Receivables/payables maturity | Required | Required | Required |
| 5 | Results – breakdown | Not required | Simplified | Required |
| 6 | Social balance sheet (sociale balans) | Required | Required | Required |
| 7 | Directors' remuneration | Not required | Not required | Required |
| 8 | Off-balance commitments (rechten en verplichtingen) | Required | Required | Required |
| 9 | Related party transactions | Not required | Not required | Required |
| 10 | Tax regime information | Not required | Simplified | Required |
| 11 | Revaluations detail | Not required | If applicable | Required |
| 12 | Profit appropriation | Required | Required | Required |

---

## Section 9 -- Filing Requirements

| Item | Detail |
|---|---|
| Filing authority | Nationale Bank van België (NBB) — Centrale des Bilans |
| Filing method | XBRL via filing.nbb.be (web application or software interface) |
| AGM approval deadline | Within 6 months from financial year-end |
| Filing deadline | 30 days after AGM; at latest 7 months from year-end |
| Filing fee (2024) | EUR 71.80 (micro XBRL) to EUR 426.40 (full model, paper equivalent) |
| Format | XBRL (mandatory); PDF for additional documents |
| Language | Dutch, French, or German (depending on registered office region) |
| Late filing surcharge | EUR 120 (month 8) increasing to EUR 1,200 (month 12+) — additional cost per month |
| Correction filing | Possible within 2 months of original filing |

### Late filing cost calculation

| Month after 7-month deadline | Additional surcharge |
|---|---|
| 1st month (month 8) | EUR 120 |
| 2nd month | EUR 240 |
| 3rd month | EUR 360 |
| Each subsequent month | EUR 600 (to max EUR 1,200) |

---

## Section 10 -- Audit Requirements

### Mandatory appointment of commissaris (statutory auditor)

Required when the company is classified as **large** (Art. 1:24 CSA/WVV) — exceeds more than one of:

| Criterion | Threshold |
|---|---|
| Turnover (excl. VAT) | EUR 11,250,000 |
| Balance sheet total | EUR 6,000,000 |
| Employees (FTE) | 50 |

Must exceed for **two consecutive** years (consistency principle).

### Always subject to audit

- Listed companies (regardless of size)
- Public interest entities
- Companies forming part of a group that must consolidate (Art. 3:72 CSA)
- Companies with a works council (Ondernemingsraad) employing ≥ 100 employees

### Auditor qualification

Bedrijfsrevisor / Réviseur d'entreprises registered with the Instituut van de Bedrijfsrevisoren (IBR) / Institut des Réviseurs d'Entreprises (IRE).

### Audit mandate

- Duration: 3 renewable years (Art. 3:58 CSA)
- Appointed by AGM
- Cannot be dismissed without just cause

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/belgium-financial-statements) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
