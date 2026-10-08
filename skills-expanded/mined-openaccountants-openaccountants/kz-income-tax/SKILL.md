---
name: kz-income-tax
description: "> Use this skill whenever asked about Kazakhstan individual income tax (ИПН / IIT / jeke tabys salyğy) for individuals or for individual entrepreneurs (ИП / ЖК) on the GENERAL established regime (общеустановленный режим / ОУР). Trigger on phrases like \"ИПН Казахстан\", \"individual income tax Kazakhstan\", \"Форма 220\", \"форма 240\", \"ИП general regime\", \"ИП на ОУР\", \"общеустановленный режим ИПН\", \"10% 15% Казахстан\", \"налоговый вычет ИП\", \"годовая декларация ИПН\", \"183 days Kazakhstan tax residency\", \"non-resident income tax Kazakhstan\", \"КГД декларация\", \"2026 Tax Code Kazakhstan IIT\", or any request to compute, classify, or advise on Kazakhstan ИПН under the 2026 Tax Code. This skill covers the NEW progressive 10%/15% scale effective 1 Jan 2026, income determination for ИП on ОУР (income minus deductions), allowable deductions and the basic deduction, the annual declaration (Форма 220.00 for ИП / Форма 240.00 for individuals), residency (183-day test) and non-resident rates, and interaction with social…"
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: KZ
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/kz-income-tax"
  tax_year: 2026
  obligation: IT
---

# Kazakhstan Individual Income Tax (ИПН / IIT) — General Established Regime — Self-Employed Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

This skill computes and explains **Kazakhstan individual income tax** (Russian: *индивидуальный
подоходный налог*, **ИПН**; Kazakh: *жеке табыс салығы*; English: **IIT / personal income tax**)
for **individuals** and for **individual entrepreneurs** (Russian *индивидуальный предприниматель*,
**ИП**; Kazakh *жеке кәсіпкер*, **ЖК**) operating on the **general established regime**
(*общеустановленный режим*, **ОУР**). The prose is in English; native Russian and Kazakh terms are
kept inline because the source forms, the State Revenue Committee portal, and bank statements use
them. **The AI must reply in the language the user writes in** (Russian, Kazakh, or English).

> **Scope guard.** This skill is for the GENERAL regime (ОУР) only. If the user is on a special
> tax regime (упрощённая декларация / patent / mobile-transfers regime), route to
> **kz-simplified-regime**. From 2026 special-regime taxpayers cannot be VAT payers and use Форма
> 910.00, not Форма 220.00.

---

## 1. Quick Reference

| Item | Value |
|---|---|
| Tax | Individual income tax — ИПН / IIT / жеке табыс салығы |
| Authority | State Revenue Committee — Комитет государственных доходов (**КГД**), under the Ministry of Finance; portal **kgd.gov.kz**, filing via **cabinet.salyk.kz** / eGov |
| Currency | Kazakhstani tenge — **KZT (₸)** |
| Legislation | **Tax Code of the Republic of Kazakhstan (2026)** — new Code signed 18 Jul 2025, effective **1 January 2026** |
| Tax year | Calendar year (1 Jan – 31 Dec 2026) |
| Annual declaration — ИП on ОУР | **Форма 220.00** |
| Annual declaration — individuals | **Форма 240.00** |
| Filing deadline | by **31 March** of the following year *(verify exact 2026 Code date)* |
| Payment deadline | by **10 April** of the following year |
| MCI / МРП (2026) | **4,325 ₸** (месячный расчётный показатель) |
| MZP / МЗП (2026) | **85,000 ₸** (minimum monthly wage) |
| Quality tier | **Research-verified — pending sign-off by a Kazakhstan accountant** |
| Skill version | **1.0** |

### Rate table (2026 Tax Code)

| Income type | Rate | Threshold |
|---|---|---|
| **ИП on ОУР** (business income minus deductions) | **10%** on income up to **230,000 МРП**; **15%** on the excess | 230,000 МРП ≈ **994,750,000 ₸** (= 230,000 × 4,325) |
| Employment / general personal income | **10%** up to **8,500 МРП**; **15%** on excess | 8,500 МРП ≈ **36,762,500 ₸** annually *(some sources cite ≈33.4m using a different MCI; verify)* |
| Dividends (resident) | **5%** up to **230,000 МРП**; **15%** on excess | 230,000 МРП |
| Private practitioners (нотариусы, адвокаты, частная практика) | **9%** flat *(verify)* | — |
| Non-resident — KZ-source employment | **10%** up to 8,500 МРП; **15%** on excess *(verify; subject to DTT)* | — |
| Non-resident — dividends/interest/royalties | typically **15%** (DTT may reduce) *(verify by income type under 2026 Code)* | — |

> The 15% rate applies **only to the portion above the threshold**:
> `IIT = (threshold × 10%) + ((taxable income − threshold) × 15%)`.

### Conservative defaults (apply when input is missing or ambiguous)

- Assume **resident** only if Kazakhstan presence ≥ 183 days is evidenced; otherwise flag the residency question.
- Treat ambiguous receipts as **taxable income**; treat ambiguous outflows as **non-deductible** until business purpose and documentation are confirmed.
- Assume the **general regime (ОУР)** only if confirmed; otherwise ask whether a special regime applies.
- Apply the **basic deduction (360 МРП/year)** only for individual taxpayers/ИП where eligible; do not double-count.
- If a figure cannot be verified against the 2026 Tax Code, present the **formula** and label it **"verify under 2026 Tax Code"**.

---

## 2. Required Inputs & Refusal Catalogue

### Required inputs
1. Taxpayer type — individual vs **ИП on ОУР** (confirm NOT a special regime).
2. Tax residency — days present in KZ during 2026; citizenship/visa status; presence of a permanent home.
3. Gross business income (выручка/доход) for the year, by source.
4. Documented business expenses (расходы) eligible for deduction.
5. Mandatory contributions paid for self (ОПВ, ВОСМС) and any СО, СН.
6. Other income (dividends, employment, rental, capital gains) and any tax already withheld at source (у источника).
7. Eligibility for the basic deduction (360 МРП) and any social/disability deductions.
8. VAT registration status and annual turnover vs the 10,000 МРП threshold.

### Refusal catalogue
- **R-KZ-1** — Special tax regimes (упрощёнка / patent / self-employed mobile-transfer regime, Форма 910.00). → kz-simplified-regime.
- **R-KZ-2** — Corporate income tax (КПН / CIT) for ТОО/legal entities (Форма 100.00). Out of scope.
- **R-KZ-3** — Full VAT (НДС) return preparation (Форма 300.00). → kazakhstan-vat skill; this skill only flags the registration trigger.
- **R-KZ-4** — Payroll withholding / employer reporting (Форма 200.00) for employees. Out of scope here.
- **R-KZ-5** — Cross-border DTT relief, transfer pricing, CFC, or treaty tie-breaker residency determinations. Refer to a qualified Kazakhstan tax adviser.
- **R-KZ-6** — Pre-2026 tax years (old Tax Code). This skill is 2026-Code only.
- **R-KZ-7** — Filing/submitting returns or making payments on the user's behalf, or anything requiring an ЭЦП (digital signature). Provide preparation support only.
- **R-KZ-8** — Definitive legal opinions; outputs are research-verified and require a licensed Kazakhstan accountant's sign-off before filing.

---

## 3. Transaction Pattern Library

Match bank-statement narratives (Russian / Kazakh / English) to a treatment. Defaults are conservative.

### Income (доход — taxable)
| Keyword (RU / KZ / EN) | Treatment |
|---|---|
| оплата по договору, за услуги, за товар / қызмет ақысы, тауар үшін / payment for services, invoice | Business income |
| выручка, поступление от клиента / түсім / revenue, client receipt | Business income |
| вознаграждение, гонорар / сыйақы / fee, honorarium | Business income |
| аренда получена / жалдау ақысы / rent received | Rental income (taxable) |
| дивиденды / дивидендтер / dividends | Dividend income (5%/15% scale) |

### Deductible expenses (вычеты — reduce ИП taxable income)
| Keyword (RU / KZ / EN) | Treatment |
|---|---|
| закуп товара, материалы, сырьё / тауар сатып алу, шикізат / inventory, materials | Deductible (cost of goods/materials) |
| аренда офиса/склада / кеңсе жалдау / office or warehouse rent | Deductible |
| зарплата сотрудникам / жалақы / employee salary | Deductible (plus employer obligations) |
| коммунальные, связь, интернет / коммуналдық, байланыс / utilities, telecom | Deductible (business portion) |
| банковская комиссия / банк комиссиясы / bank fees | Deductible |
| ОПВ/ВОСМС/СО/СН за себя / өз пайдасына аударымдар / own social payments | Deductible per 2026 Code (see §5) |
| амортизация ОС / тозу / depreciation of fixed assets | Deductible per Code rules |

### Non-deductible (не относится на вычеты)
| Keyword / pattern | Reason |
|---|---|
| штрафы, пени КГД / айыппұл / fines, penalties to the state | Statutorily non-deductible |
| личные расходы, личная карта / жеке шығыс / personal spending | Not a business expense |
| расходы без документов / құжатсыз шығыс / undocumented spend | No primary document → not deductible |
| НДС к зачёту / ҚҚС есепке жатқызу / input VAT | Handled under VAT, not an income-tax deduction |

### Exclusions / non-income (не доход)
| Keyword / pattern | Reason |
|---|---|
| перевод между своими счетами / шоттар арасында аудару / own-account transfer | Not income |
| возврат от поставщика / қайтарым / supplier refund | Reduces expense, not income |
| займ полученный / алынған қарыз / loan received | Financing, not income |
| пополнение счёта собственными средствами / өз қаражатын салу / owner top-up | Capital, not income |

---

## 4. Worked Examples

> МРП (2026) = 4,325 ₸. All figures indicative — confirm under the 2026 Tax Code.

**Example 1 — ИП on ОУР, modest profit (single rate).**
Income 30,000,000 ₸; documented expenses 18,000,000 ₸. Basic deduction 360 МРП = 1,557,000 ₸; own ОПВ/ВОСМС say 600,000 ₸ (deductible).
Taxable income = 30,000,000 − 18,000,000 − 1,557,000 − 600,000 = **9,843,000 ₸**.
Below 230,000 МРП, so flat **10%** → ИПН = **984,300 ₸**. Declared on **Форма 220.00**.

**Example 2 — ИП on ОУР, above the 230,000 МРП threshold (progressive).**
Taxable income (after deductions) = 1,200,000,000 ₸. Threshold = 230,000 × 4,325 = 994,750,000 ₸.
ИПН = 994,750,000 × 10% + (1,200,000,000 − 994,750,000) × 15%
= 99,475,000 + 205,250,000 × 15% = 99,475,000 + 30,787,500 = **130,262,500 ₸**.

**Example 3 — Resident individual with dividends.**
Resident receives dividends of 50,000,000 ₸ (below 230,000 МРП). Rate **5%** → **2,500,000 ₸**, usually withheld at source; report on **Форма 240.00** if a declaration is due.

**Example 4 — VAT registration trigger.**
ИП on ОУР turnover reaches 43,250,000 ₸ (= 10,000 МРП). The taxpayer must apply for VAT registration within **5 working days** of crossing the threshold; VAT then at **16%** (НДС). This is separate from ИПН (route VAT work to kazakhstan-vat).

**Example 5 — Non-resident, KZ-source employment.**
Non-resident (in KZ < 183 days) earns KZ-source salary. Tax only KZ-source income; apply the non-resident rate by income type and check any DTT. Flag for adviser review (R-KZ-5).

---

## 5. Tier 1 Rules (2026 Tax Code — article references to verify)

> Cite the **2026 Tax Code of the Republic of Kazakhstan**. Article numbers below are placeholders to
> be confirmed against the enacted Code; do not assert a number you have not verified.

1. **Taxpayers & object of taxation.** ИПН is levied on the income of resident and non-resident
   individuals; residents are taxed on worldwide income, non-residents on Kazakhstan-source income only.
   *(verify article under 2026 Code)*
2. **Residency — 183-day test.** An individual is a Kazakhstan tax resident if present in KZ for **≥ 183
   calendar days** in any rolling 12-month period ending in the tax year, or has a centre of vital
   interests in KZ. *(verify under 2026 Code)*
3. **Progressive ИПН scale.** **10%** up to the relevant threshold and **15%** above it; thresholds
   differ by income type (employment 8,500 МРП; ИП-ОУР and dividends 230,000 МРП). *(VERIFIED via Big-4
   / PwC 2026 notes; confirm exact wording in the Code.)*
4. **Income determination for ИП on ОУР.** Taxable income = annual business income (доход) minus
   documented, business-related deductions (вычеты), the basic deduction, and own mandatory social
   payments. *(verify deduction articles under 2026 Code)*
5. **Deduction conditions.** Expenses must be incurred to earn income, be documented by primary records
   (первичные документы), and not fall in the non-deductible list (fines, personal spend, etc.). §6
   recordkeeping duties apply.
6. **Basic deduction.** **30 МРП per month, capped at 360 МРП per year** (replacing the former 14 МРП
   standard deduction). Social/disability deductions of 882 МРП or 5,000 МРП apply to qualifying persons.
   *(VERIFIED 2026; confirm eligibility scope.)*
7. **Annual declaration & deadlines.** ИП on ОУР file **Форма 220.00**; individuals file **Форма
   240.00**. Filing by **31 March**, payment by **10 April** of the following year. *(verify exact dates.)*
8. **Withholding at source.** Certain income (e.g., dividends) is taxed by withholding (у источника
   выплаты); the recipient may not need a separate declaration if fully withheld. *(verify.)*

---

## 6. Tier 2 — Judgement Calls & Interactions

- **Regime check first.** Always confirm ОУР vs a special regime before applying §1–7; misrouting is the
  most common error. Special-regime taxpayers from 2026 cannot register for VAT.
- **Social payments (взаимодействие с соцплатежами).** For ИП "for self": **ОПВ** (mandatory pension,
  ~10% of income), **ВОСМС** (medical, 5% of 1.4 МЗП base), **СО** (social contributions, ~5%), and
  **СН** (social tax, ~2 МРП monthly — *verify 2026 rate; social tax base rate was reduced from 11% to
  6%*). These are computed separately from ИПН but several are **deductible** when computing ИПН taxable
  income. Do not conflate the bases.
- **VAT (НДС) interaction.** VAT registration is mandatory above **10,000 МРП (43,250,000 ₸)** turnover;
  rate **16%** from 2026. VAT is excluded from income-tax computations (input/output VAT handled
  separately). Route VAT returns (Форма 300.00) to kazakhstan-vat.
- **Threshold which-MCI.** Employment-income threshold of 8,500 МРП is variously quoted as ≈33.4m or
  ≈36.8m ₸ depending on the MCI used; recompute with the **2026 МРП = 4,325 ₸** and flag if the source
  used a prior-year MCI.
- **Non-residents.** Apply rates by income type and check the relevant Double Tax Treaty; treaty
  tie-breakers and relief are adviser-level (R-KZ-5).

---

## 7. Excel Template (ИПН computation for ИП on ОУР)

| Cell / line | Label | Formula / input |
|---|---|---|
| B1 | МРП 2026 | 4325 |
| B2 | Annual business income (доход) | input |
| B3 | Documented deductible expenses (вычеты) | input |
| B4 | Basic deduction | =360*B1 |
| B5 | Own ОПВ + ВОСМС + СО deductible | input |
| B6 | Taxable income | =MAX(0,B2-B3-B4-B5) |
| B7 | Threshold (230,000 МРП) | =230000*B1 |
| B8 | Tax at 10% band | =MIN(B6,B7)*0.10 |
| B9 | Tax at 15% band | =MAX(0,B6-B7)*0.15 |
| B10 | **ИПН payable** | =B8+B9 |
| B11 | VAT registration check | =IF(B2>10000*B1,"REGISTER for НДС 16%","below threshold") |

---

## 8. Bank Statement Guide

Most KZ self-employed clients bank with **Kaspi Bank**, **Halyk Bank** (Народный банк / Halyk), or
**ForteBank**. Statements (выписка) are in Russian and/or Kazakh.

- **Kaspi Bank** — Kaspi Business / Kaspi Pay statements; QR-payments (Kaspi QR) are common business
  income for ИП. Watch for personal Kaspi Gold transfers mixed with business flows — separate them.
- **Halyk Bank (Народный/Halyk)** — Onlinebank/Homebank business statements; clear "поступление"
  (credit) vs "списание" (debit) columns; payment narratives often include counterparty БИН/ИИН.
- **ForteBank** — ForteBusiness statements; similar credit/debit layout.

Key statement terms: **поступление / түсім** = incoming (credit, usually income); **списание / есептен
шығару** = outgoing (debit, usually expense); **перевод / аудару** = transfer (check if own-account);
**комиссия / комиссия** = bank fee (deductible); **ИИН** = individual ID number; **БИН** = business ID
number; **назначение платежа / төлем мақсаты** = payment purpose (key for classification).

**Caution:** ИП frequently mix personal and business money on one card/account. Always confirm which
account is business and exclude own-account transfers and owner top-ups from income.

---

## 9. Onboarding (questions to ask a new user)

1. Are you an individual or an ИП (ЖК)? If ИП, are you on the **general regime (ОУР)** or a special
   regime? (If special → kz-simplified-regime.)
2. How many days were you in Kazakhstan in 2026? (Residency / 183-day test.)
3. What is your total business income for the year, and which bank(s) — Kaspi, Halyk, ForteBank?
4. Do you have documented expenses to deduct? Can you provide primary documents?
5. Have you paid ОПВ / ВОСМС / СО / СН for yourself this year?
6. Did your turnover exceed **10,000 МРП (43,250,000 ₸)** — i.e., are you (or must you be) VAT-registered?
7. Any other income (dividends, employment, rent) and was tax withheld at source?
8. Do you qualify for the basic deduction (360 МРП) or any social/disability deduction?

---

## 10. Reference & Test Suite

### Reference figures (2026, verify before filing)
- МРП = 4,325 ₸; МЗП = 85,000 ₸.
- ИП-ОУР ИПН: 10% up to 230,000 МРП (≈994,750,000 ₸), 15% above.
- Employment ИПН: 10% up to 8,500 МРП, 15% above.
- Dividends: 5% up to 230,000 МРП, 15% above.
- Basic deduction: 360 МРП/year. VAT threshold: 10,000 МРП; VAT rate 16%.
- Forms: 220.00 (ИП), 240.00 (individuals). Filing 31 Mar; payment 10 Apr.

### Test suite (expected behaviour)
1. "Я ИП на упрощёнке" → refuse/route to kz-simplified-regime (R-KZ-1).
2. ИП-ОУР taxable income below 230,000 МРП → flat 10%, Форма 220.00.
3. ИП-ОУР taxable income above threshold → progressive 10%+15% split.
4. Turnover > 43,250,000 ₸ → flag VAT registration (16%) and route to kazakhstan-vat.
5. User in KZ < 183 days → treat as non-resident, tax KZ-source only, flag DTT (R-KZ-5).
6. Unverifiable figure → present formula + "verify under 2026 Tax Code".
7. Own-account transfer in statement → exclude from income.
8. Pre-2026 year requested → refuse (R-KZ-6).

---

## PROHIBITIONS

- Do **not** file returns, submit via cabinet.salyk.kz/eGov, sign with ЭЦП, or move money on the user's behalf.
- Do **not** apply the old (pre-2026) Tax Code or pre-2026 rates/thresholds.
- Do **not** treat special-regime (упрощёнка/patent) taxpayers under this skill.
- Do **not** assert article numbers, exact deadlines, or rates you have not verified against the 2026 Code.
- Do **not** give definitive cross-border/DTT/residency tie-breaker opinions — refer to a qualified adviser.
- Do **not** conflate the ИПН base with VAT, social tax, or social-contribution bases.
- Do **not** present output as final without a licensed Kazakhstan accountant's sign-off.

## Disclaimer

This skill is **research-verified** against publicly available summaries of the 2026 Tax Code of the
Republic of Kazakhstan (КГД / kgd.gov.kz, PwC Tax Summaries, Big-4 and local advisory 2026 notes,
egov.kz) and is **pending sign-off by a qualified Kazakhstan accountant**. Rates, thresholds, МРП
values, form numbers, and deadlines for the new 2026 Tax Code may be amended; figures marked "verify"
must be confirmed before reliance. This is general information, not tax advice, and does not create a
client relationship. Always have a licensed Kazakhstan tax professional review any computation before
filing. Part of **openaccountants.com** — open-source tax skills for AI agents.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/kz-income-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
