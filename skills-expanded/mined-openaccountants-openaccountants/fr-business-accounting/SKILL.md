---
name: fr-business-accounting
description: "> French business accounting, VAT declarations, invoicing, and e-invoicing 2026 reform. Trigger on phrases like \"comptabilité française\", \"expert-comptable\", \"TVA France\", \"déclaration CA3\", \"déclaration CA12\", \"TVA intracommunautaire\", \"facturation France\", \"facture électronique\", \"e-invoicing France\", \"Factur-X\", \"UBL\", \"CII\", \"plateforme agréée\", \"PDP\", \"PPF\", \"réforme facturation 2026\", \"e-reporting\", \"PEPPOL France\", \"mentions obligatoires facture\", \"avoir facture\", \"numérotation factures\", \"franchise en base TVA\", \"autoliquidation TVA\", \"régime réel simplifié TVA\", \"régime réel normal TVA\", \"FEC\", \"fichier des écritures comptables\", \"Plan Comptable Général\", \"PCG\", \"liasse fiscale\", \"bilan France\", \"compte de résultat\", \"clôture annuelle\", \"amortissements comptables\", \"IS France\", \"impôt sur les sociétés\", \"taux réduit PME 15%\". Covers TVA regimes and rates, e-invoicing/e-reporting reform timeline, mandatory invoice mentions, IS computation, annual closing, and FEC generation."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: FR
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/fr-business-accounting"
  tax_year: 2025
  obligation: OTHER
---

# France — Business Accounting, VAT & E-Invoicing v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Based on work by [Romain Simon (@romainsimon)](https://github.com/romainsimon/paperasse)**, licensed under MIT. Adapted for the OpenAccountants format.

> **Disclaimer:** This skill is for informational purposes only and does not constitute tax advice. All positions must be reviewed and signed off by a qualified expert-comptable before filing. Get this reviewed at **openaccountants.com**.

---

## Section 1 — Quick Reference

| Field | Value |
|---|---|
| Country | France |
| Scope | Business accounting (IS/IR entities), TVA, invoicing |
| Currency | EUR only |
| Accounting framework | Plan Comptable Général (PCG) |
| Tax authority | DGFiP |
| Key legislation | CGI (art. 38-39, 219, 293 B, 242 nonies A), Code de Commerce |

---

## Section 2 — VAT (TVA) Regimes and Rates

### Standard rates (2025)

| Rate | Application |
|---|---|
| 20% (taux normal) | Most goods and services |
| 10% (taux intermédiaire) | Restaurants, certain renovation works, public transport |
| 5.5% (taux réduit) | Food staples, books, energy, accessibility works |
| 2.1% (taux super-réduit) | Press, certain medicines, live performances |

### TVA regimes

| Regime | Condition | Declaration |
|---|---|---|
| Franchise en base (art. 293 B CGI) | Services CA ≤ EUR 36,800 (tolerance EUR 39,100); Sales CA ≤ EUR 91,900 (tolerance EUR 101,000) | No TVA collected or deducted. Mandatory mention: "TVA non applicable, art. 293 B du CGI" |
| Régime réel simplifié | CA < EUR 840,000 (goods) or EUR 254,000 (services) | CA12 annual + quarterly advances |
| Régime réel normal | Above simplified thresholds | CA3 monthly (or quarterly if TVA < EUR 4,000/year) |

### Intra-EU / international services

| Scenario | Treatment |
|---|---|
| Service purchased from EU provider | **Autoliquidation** (art. 283-2 CGI) — buyer self-assesses TVA |
| Service sold to EU business (B2B) | Reverse charge — invoice without TVA, mention "Autoliquidation" |
| Service sold to EU consumer (B2C) | French TVA unless OSS threshold exceeded |
| Import of goods from outside EU | TVA at customs or autoliquidation (since 2022) |

---

## Section 3 — E-Invoicing Reform (Réforme Facturation Électronique 2026)

### Timeline

| Date | Obligation | Scope |
|---|---|---|
| **1 September 2026** | **Reception** of e-invoices | All TVA-liable entities (including franchise en base) |
| **1 September 2026** | **Emission** of e-invoices | Grandes Entreprises (GE) and ETI |
| **1 September 2027** | **Emission** of e-invoices | PME and micro-entreprises |

### Key concepts

| Concept | Description |
|---|---|
| PA (Plateforme Agréée) | Certified platform for transmitting/receiving e-invoices. Mandatory for all. |
| PPF (Portail Public de Facturation) | Since Oct 2024, **no longer handles emission/reception**. Only serves as central directory + e-reporting concentrator. |
| e-Reporting | Transmission of B2C, international, and payment data. Does **NOT** cover domestic B2B between TVA-liable entities (already transmitted via e-invoicing). |
| Formats | Factur-X (CII), UBL, CII — structured XML embedded in or alongside PDF |
| PEPPOL | European e-invoicing network — accepted delivery channel |

### New mandatory mentions (from 1 September 2026, B2B domestic invoices)

| Mention | Notes |
|---|---|
| Client SIREN | Required on all domestic B2B invoices |
| Transaction category | "Biens" / "Services" / "Mixte" — separate from line descriptions |

### E-reporting scope

| Transaction type | E-reporting required? |
|---|---|
| B2B domestic (both TVA-liable) | No — covered by e-invoicing |
| B2C | Yes |
| International (export, intra-EU) | Yes |
| Payment data | Yes (for TVA-on-payments regime) |

---

## Section 4 — Invoice Requirements (Mentions Obligatoires)

### Mandatory mentions on every invoice

| Mention | Legal basis |
|---|---|
| Invoice date | Art. 242 nonies A CGI |
| Sequential invoice number (no gaps) | Art. 242 nonies A CGI |
| Seller: name, address, SIREN/SIRET | Art. 242 nonies A CGI |
| Buyer: name, address | Art. 242 nonies A CGI |
| Buyer SIREN (B2B domestic, from Sept 2026) | Réforme 2026 |
| VAT identification numbers (seller + buyer for intra-EU) | Art. 242 nonies A CGI |
| Description of goods/services | Art. 242 nonies A CGI |
| Quantity | Art. 242 nonies A CGI |
| Unit price (HT) | Art. 242 nonies A CGI |
| TVA rate(s) applied | Art. 242 nonies A CGI |
| Total HT, TVA amount, Total TTC | Art. 242 nonies A CGI |
| Payment terms (due date) | Art. L441-9 Code de Commerce |
| Late payment penalties rate | Art. L441-10 Code de Commerce |
| Fixed recovery fee (EUR 40) | Art. D441-5 Code de Commerce |
| Early payment discount or "Escompte: néant" | Art. 242 nonies A CGI |

**If franchise en base:** "TVA non applicable, art. 293 B du CGI" instead of TVA amounts.

### Credit notes (avoirs)

Must reference the original invoice number and clearly state the reason for the credit.

### Numbering

Sequential, chronological, no gaps. Common format: annual reset (e.g., F-2025-001, F-2025-002… F-2026-001).

### Retention

Invoices must be retained for **10 years** (art. L123-22 Code de Commerce). Digital archival with integrity guarantees.

---

## Section 5 — Corporate Tax (Impôt sur les Sociétés — IS)

### Rates (2025)

| Bracket | Rate | Condition |
|---|---|---|
| First EUR 42,500 of profit | **15%** (taux réduit PME) | CA < EUR 10M, capital fully paid up, ≥75% held by individuals |
| Above EUR 42,500 | **25%** (taux normal) | |

**Short financial year:** the EUR 42,500 threshold is prorated: EUR 42,500 × (days / 365).

### IS is not deductible

IS itself (account 695) is **not deductible** from taxable profit (art. 39-1-4° CGI). It must be added back in the fiscal result.

### Non-deductible charges (common traps)

| Charge | Rule |
|---|---|
| Fines and penalties | Not deductible |
| Luxury expenses (chasse, yacht) | Not deductible |
| Personal expenses of shareholder | Not deductible — risk of "acte anormal de gestion" |
| IS itself | Not deductible |
| Excessive management fees | Excess not deductible |

### Deductibility conditions (art. 39-1 CGI)

All charges must satisfy four conditions:
1. Incurred in the interest of the business
2. Reflect normal management
3. Supported by documentation (invoices)
4. Result in a decrease of net assets

---

## Section 6 — Annual Closing (Clôture Annuelle) — Summary

### 12-step workflow

1. Collect all transactions for the financial year
2. Categorise expenses (vendor → PCG account)
3. Bank reconciliation
4. Inventory entries (amortisation, PCA/CCA, provisions)
5. IS calculation
6. Generate journal entries (`data/journal-entries.json`)
7. Generate financial statements (bilan, compte de résultat, balance)
8. Generate the FEC (Fichier des Écritures Comptables)
9. Prepare liasse fiscale (2033 for simplified, 2050 for normal)
10. Prepare 2065-SD (IS declaration)
11. Prepare PV d'approbation / déclaration de confidentialité
12. Generate PDFs

### FEC (Fichier des Écritures Comptables)

Mandatory file with **18 columns**, pipe-separated (`|`). Must include all journal entries for the financial year.

**Conformity checks:**
- Total debits = total credits (global balance)
- Each entry (EcritureNum) is balanced
- Sequential numbering (no gaps)
- Dates within the financial year
- No negative amounts
- PieceRef populated for every entry
- CompteNum consistent with PCG roots

**Non-compliant FEC → comptabilité non probante** (art. L. 192 LPF) → burden of proof shifts to the taxpayer.

---

## Section 7 — Shareholder Current Account (Compte Courant d'Associé — 455)

**High fiscal risk zone**, especially for SASU/EURL.

| Check | Rule |
|---|---|
| Pre-incorporation expenses | Must be assumed within 6 months of registration; annexed to statuts or PV |
| Home office (bureau à domicile) | Pro-rata of surface area; plan required; non-deductible: mortgage principal, personal utilities |
| Interest on current account | Deductible only up to TMPV BCE rate; capital must be fully paid up (art. 212 CGI) |
| Mixed-use expenses | Only professional portion deductible |
| Currency conversion | BCE rate per transaction or monthly average accepted |

---

## Section 8 — Fiscal Calendar (Key Deadlines)

| Deadline | Obligation |
|---|---|
| Monthly 19th–24th | CA3 (TVA mensuelle) |
| Quarterly | CA3 (TVA trimestrielle if < EUR 4,000/year) |
| May (2nd business day after 1 May) | CA12 annual TVA return |
| 15 March, 15 June, 15 September, 15 December | IS quarterly advances |
| Within 3 months of year-end + 1 month extension | Liasse fiscale + 2065-SD |
| Within 6 months of year-end | AGO (approbation des comptes) |
| 1 month after AGO | Dépôt au greffe |

Check the official calendar: `https://www.impots.gouv.fr/professionnel/calendrier-fiscal`

---

## Section 9 — Conservative Defaults

| Ambiguity | Default |
|---|---|
| TVA regime unknown | Franchise en base (if CA permits) |
| Charge deductibility doubtful | Non-deductible (conservative) |
| Mixed-use proportion unclear | 0% professional (flag for reviewer) |
| IS rate applicable unclear | 25% (no PME reduced rate) |
| Immobilisation vs charge threshold | EUR 500 HT (capitalise above) |

---

## Section 10 — Key Legal References

| Rule | Article |
|---|---|
| Taxable profit | art. 38-1 CGI |
| Net asset variation | art. 38-2 CGI |
| Deductible charges | art. 39-1 CGI |
| IS rates | art. 219-I CGI |
| PME reduced rate | art. 219-I-b CGI |
| IS non-deductible | art. 39-1-4° CGI |
| Franchise en base TVA | art. 293 B CGI |
| Autoliquidation | art. 283-2 CGI |
| CCA interest cap | art. 39-1-3° and 212 CGI |
| Invoice mentions | art. 242 nonies A CGI |
| FEC obligation | art. L. 47 A-I LPF |
| Document retention | art. L123-22 Code de Commerce |

---

*OpenAccountants — open-source accounting skills for AI*
*This output must be reviewed by a qualified professional before filing or acting upon.*
*Latest verified skills: **openaccountants.com** | Report errors: **github.com/openaccountants/openaccountants***

---

_Source: [OpenAccountants](https://openaccountants.com/skills/fr-business-accounting) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
