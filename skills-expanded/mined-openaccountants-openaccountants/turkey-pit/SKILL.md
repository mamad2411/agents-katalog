---
name: turkey-pit
description: "Use this skill whenever asked to prepare, review, or classify transactions for Turkey Personal Income Tax (Gelir Vergisi), annual tax return (Yıllık Gelir Vergisi Beyannamesi / 0001 kodu), or advise on Turkish PIT deductions and filing. Trigger on phrases like \"gelir vergisi\", \"Turkish income tax\", \"yıllık beyanname\", \"GİB\", \"vergi dairesi\", or any Turkey personal income tax request. ALWAYS read this skill before touching any Turkey PIT work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: TR
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/turkey-pit"
  tax_year: 2025
  obligation: IT
---

# Turkey Personal Income Tax (Gelir Vergisi) Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 — Quick reference

| Field | Value |
|---|---|
| Country | Türkiye (Republic of Türkiye) |
| Tax | Gelir Vergisi (Personal Income Tax) |
| Currency | TRY (Turkish Lira / ₺) |
| Tax year | Calendar year (1 Jan – 31 Dec) |
| Current tax year | 2025 |
| Tax authority | Gelir İdaresi Başkanlığı (GİB — Revenue Administration) |
| Return code | 0001 — Yıllık Gelir Vergisi Beyannamesi |
| Filing portal | https://ivd.gib.gov.tr (İnteraktif Vergi Dairesi) |
| Filing deadline | 1–25 March of following year |
| Payment | 2 equal instalments: March and July |
| Source credit | `ozgurg/vergihesaplayici.com` (AGPL-3.0) + `berkaygure/gelir-vergisi-kesintisi-hesaplama` |
| Contributor | Open Accountants Community |
| Validated by | Pending — requires sign-off by a Turkish SMMM or YMM |
| Skill version | 1.0 |

---

## Section 2 — Progressive tax brackets (Vergi dilimleri) — 2025

Annual income tax brackets for yıllık gelir vergisi:

| Taxable Income (TRY) | Rate | Max tax in bracket |
|---|---|---|
| 0 – 158,000 | 15% | 23,700 |
| 158,001 – 330,000 | 20% | 34,400 |
| 330,001 – 1,200,000 | 27% | 234,900 |
| 1,200,001 – 4,300,000 | 35% | 1,085,000 |
| 4,300,001 + | 40% | — |

### Cumulative withholding brackets (Gelir vergisi kesintisi / Stopaj)

Used for monthly payroll cumulative calculation per §94:

| Cumulative base (TRY) | Rate |
|---|---|
| 0 – 24,000 | 15% |
| 24,001 – 53,000 | 20% |
| 53,001 – 190,000 | 27% |
| 190,001 – 650,000 | 35% |
| 650,001 + | 40% |

---

## Section 3 — Income categories (Gelir türleri)

Per Gelir Vergisi Kanunu (GVK), 7 categories:

| # | Turkish | English | GVK Section |
|---|---|---|---|
| 1 | Ticarî kazançlar | Business income | §37–51 |
| 2 | Ziraî kazançlar | Agricultural income | §52–59 |
| 3 | Ücretler | Employment income (wages) | §61–64 |
| 4 | Serbest meslek kazançları | Self-employment / professional income | §65–68 |
| 5 | Gayrimenkul sermaye iratları (GMSİ) | Rental income | §70–74 |
| 6 | Menkul sermaye iratları | Investment income (interest, dividends) | §75–80 |
| 7 | Diğer kazanç ve iratlar | Other income (capital gains etc.) | §80–82 |

---

## Section 4 — Key exemptions and deductions (İstisnalar ve indirimler)

### Exemptions (2025)

| Item | Amount (TRY) | Notes |
|---|---|---|
| Rental income exemption (kira geliri istisnası) | 33,000 | Annual, residential only |
| Young entrepreneur exemption (genç girişimci) | 230,000 | Under 29, first 3 years |
| Severance pay (kıdem tazminatı) | Exempt | Within legal limits |

### Deductions from income

| Deduction | Limit |
|---|---|
| Education & health expenses | 10% of declared income |
| Life insurance premiums | 50% of salary, max per employee limits |
| Private pension (BES) contributions | State matches 30%, employer deductible |
| Charitable donations (bağış) | Up to 5% of income (10% for certain institutions) |
| Sponsorship expenses | Per related legislation |
| Social security premiums (SGK) | Actual amount paid |

---

## Section 5 — Filing rules

### Who must file annually?

- Self-employed (serbest meslek erbabı)
- Business owners (ticari kazanç)
- Rental income above 33,000 TRY exemption threshold
- Investment income above thresholds
- Capital gains (değer artışı kazancı)
- Multiple employers (if total exceeds threshold)

### Who does NOT file?

- Single-employer wage earners (ücretliler) — tax fully withheld at source
- Those with income below declaration thresholds

### Provisional tax (Geçici vergi)

Self-employed and business owners pay quarterly:

| Quarter | Period | Due date |
|---|---|---|
| Q1 | Jan–Mar | 17 May |
| Q2 | Apr–Jun | 17 August |
| Q3 | Jul–Sep | 17 November |
| Q4 | Oct–Dec | 17 February |

Rate: same brackets as annual. Provisional tax is offset against annual liability.

---

## Section 6 — Computation method

```
Step 1: Total assessable income (all 7 categories)
Step 2: − Exempt income (kira istisnası, genç girişimci, etc.)
Step 3: − Allowable expenses per category
Step 4: = Net taxable income (safi gelir)
Step 5: − Deductions (insurance, donations, BES)
Step 6: = Taxable base (vergi matrahı)
Step 7: Apply progressive brackets (Section 2)
Step 8: = Gross tax
Step 9: − Provisional tax paid (geçici vergi)
Step 10: − Withholding tax (stopaj / tevkifat)
Step 11: = Net tax payable or refund
```

---

## Section 7 — Worked example

**Scenario:** Freelance software developer, 2025 annual income 600,000 TRY, allowable expenses 30,000 TRY, no other deductions. No provisional tax paid.

| Step | Description | Amount (TRY) |
|---|---|---|
| Gross income | Professional income §40(4) | 600,000 |
| − Expenses | Documented business costs | (30,000) |
| **Taxable base** | | **570,000** |

Tax computation on 570,000 TRY:

| Bracket | Taxable in bracket | Rate | Tax |
|---|---|---|---|
| 0 – 158,000 | 158,000 | 15% | 23,700 |
| 158,001 – 330,000 | 172,000 | 20% | 34,400 |
| 330,001 – 570,000 | 240,000 | 27% | 64,800 |
| **Total tax** | | | **122,900 TRY** |

If 50,000 TRY provisional tax was paid during the year:
**122,900 − 50,000 = 72,900 TRY** payable at filing (2 instalments: 36,450 March + 36,450 July).

---

## Section 8 — Conservative defaults

| Situation | Conservative position |
|---|---|
| Income category unclear | Classify as taxable; flag for reviewer |
| Expense documentation incomplete | Do NOT deduct; flag |
| Rental income — mixed use | Apply exemption only to clearly residential portion |
| Foreign income | Include if Turkish resident; flag treaty applicability |
| Crypto / digital asset gains | Classify as "diğer kazanç"; flag pending legislation |

---

## Section 9 — Classification rules for bank statements

| Pattern / Keyword | Classification | Category |
|---|---|---|
| Maaş / Ücret / Salary | Employment income | Ücret §61 |
| Kira / Rent | Rental income | GMSİ §70 |
| Faiz / Interest | Investment income | Menkul sermaye §75 |
| Temettü / Dividend | Investment income | Menkul sermaye §75 |
| Serbest meslek / Freelance | Professional income | Serbest meslek §65 |
| Satış / E-ticaret | Business income | Ticarî kazanç §37 |
| Komisyon / Commission | Professional income | §65 or §37 |
| SGK / Social security | Deductible expense | — |
| BES / Pension contribution | Deductible | — |

---

## Section 10 — Sources

| Source | URL |
|---|---|
| GİB (Revenue Administration) | https://www.gib.gov.tr |
| İnteraktif Vergi Dairesi | https://ivd.gib.gov.tr |
| `ozgurg/vergihesaplayici.com` (AGPL-3.0) | https://github.com/ozgurg/vergihesaplayici.com |
| `berkaygure/gelir-vergisi-kesintisi-hesaplama` | https://github.com/berkaygure/gelir-vergisi-kesintisi-hesaplama |
| Gelir Vergisi Kanunu | GVK No. 193 |

---

*OpenAccountants — open-source accounting skills for AI*
*This is not tax advice. All outputs must be reviewed by a qualified professional before filing.*

---

_Source: [OpenAccountants](https://openaccountants.com/skills/turkey-pit) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
