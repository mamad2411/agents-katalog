---
name: ma-einvoice
description: "> Use this skill whenever asked about Morocco e-invoicing, the DGI's mandatory electronic-invoicing roadmap, or invoice-conformity rules for a self-employed person or micro-business. Trigger on phrases like \"Morocco e-invoicing\", \"facturation électronique Maroc\", \"e-facture DGI\", \"facture électronique obligatoire\", \"invoice rules Morocco\", \"mentions obligatoires facture Maroc\", \"ICE sur facture\", \"فاتورة إلكترونية المغرب\", \"CGI 145-IX\". Covers the current paper/PDF invoice mentions (ICE, IF, numérotation séquentielle, ventilation TVA), the announced continuous-transaction-control (pre-clearance) model under CGI Art. 145-IX, the SIMPL télédéclaration obligations already in force, the penalty exposure for non-conforming invoices, and what a freelancer should do now. The go-live roadmap is UNCONFIRMED — the implementing decree was still pending as of mid-2026. Reply in the user's language (English, French, or Moroccan Arabic / Darija). Cross-reference morocco-vat, ma-auto-entrepreneur, and ma-bookkeeping."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: MA
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ma-einvoice"
  tax_year: 2026
  obligation: EINV
---

# Morocco — E-Invoicing / Facturation Électronique (DGI)

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

Morocco is moving towards **mandatory electronic invoicing** (facturation
électronique / la facture électronique / الفوترة الإلكترونية), administered by the
**Direction Générale des Impôts (DGI)**. The legal hook is **Article 145-IX of the
Code Général des Impôts (CGI)**, which empowers the administration to require an
IT-based invoicing system meeting technical criteria set by regulation. The
operative detail — formats, thresholds, the platform, and the go-live dates — is to
be fixed by an **implementing decree (décret d'application)** that, as of the last
research update, had **not yet been published in the Bulletin Officiel**.

This skill replies in the user's language. Moroccan users mix English, French, and
Darija — keep the native terms (DGI, ICE, IF, TVA, SIMPL, facturation
électronique, CTC) and explain them once.

> **READ THIS FIRST.** Mandatory B2B/B2C e-invoicing in Morocco is an **announced
> roadmap, not a regime in force**. Do not tell a user they "must e-invoice from
> [date]" — the start dates, scope thresholds, and even the final clearance model
> are **pending the décret d'application**. What *is* already binding is (a) the
> paper/PDF invoice-conformity rules under CGI Art. 145, and (b) the SIMPL
> télédéclaration/télépaiement obligations. Anchor advice on those.

---

## 1. Quick Reference

| Field | Value |
|---|---|
| Topic | E-invoicing / facturation électronique |
| Authority | Direction Générale des Impôts (**DGI**), tax.gov.ma |
| Currency | **MAD** (dirham) |
| Legal basis | **CGI Art. 145-IX** (e-invoicing enabling provision); CGI Art. 145 (invoice mentions); Art. 146, 192, 198 ter (sanctions) |
| Status | **Roadmap — pending.** Implementing decree NOT yet published; go-live dates UNCONFIRMED |
| Announced model | Continuous Transaction Control (**CTC**) / pre-clearance — *verify in final decree* |
| Announced formats | UBL / CII (e.g. UBL 2.1) — *verify* |
| Platform | DGI national platform built by **xHub**, integrated with **Simpl-TVA**; public brand name (e.g. *fatourati.gov.ma*) **NOT confirmed** — verify |
| Already in force | SIMPL télédéclaration & télépaiement (mandatory for enterprises since 2017); ICE on invoices |
| Sequencing (announced) | Large companies (B2B) first → SMEs → small enterprises → B2C — *verify dates* |
| Quality tier | **Research-verified — pending sign-off by a Moroccan expert-comptable** |
| Tax year | 2026 |
| Version | 1.0 |
| Last research update | Mid-2026 |

### Conservative defaults

- **Default to "pending / verify."** If a user asks "when does it start" or "what
  format," answer with the *announced* position and immediately flag that the
  décret d'application is not yet published. Never present a date as settled law.
- **Default to current-law conformity.** Whatever happens with e-invoicing, an
  invoice that already satisfies CGI Art. 145 (ICE, IF, sequential numbering, TVA
  breakdown) is the safe baseline. Advise the user to fix paper/PDF conformity
  first.
- **Default to escalation for go-live decisions.** Onboarding to a clearance
  platform, choosing an OD/PDP-style provider, or changing the invoicing workflow
  is a reviewer decision once the decree lands — flag to an expert-comptable.
- **Never invent thresholds.** The turnover/headcount cut-offs for each wave are
  decree-defined and not yet public. Do not guess MAD figures.

---

## 2. Current Invoicing Rules (in force today)

These apply **now**, on paper or PDF, regardless of the e-invoicing roadmap. A
"regular invoice" (**facture régulière**) is the precondition for the customer's
right to deduct TVA and expenses (CGI Art. 146 / Art. 106). A missing or defective
mention is the single most common reason the DGI rejects deductible TVA on audit.

### Mandatory mentions (mentions obligatoires) — CGI Art. 145

The seller must show:

1. **Seller identification** — raison sociale / name, address, and the seller's
   **Identifiant Fiscal (IF)**, **Taxe Professionnelle (TP)** number, **Registre
   de Commerce (RC)** number where applicable, and the **ICE**.
2. **ICE — Identifiant Commun de l'Entreprise.** A **15-digit** common business
   identifier. The **seller's ICE** has been mandatory on invoices since 2016
   (CGI Art. 145-VIII). The **client's ICE** is mandatory in **B2B** transactions
   (since January 2019). Both ICEs on a B2B invoice is the rule.
3. **Customer identification** — name/raison sociale, address, and (B2B) the
   customer's ICE.
4. **Sequential invoice number** (numérotation chronologique et continue) — no
   gaps; a single uninterrupted series.
5. **Date** of issue.
6. **Description** of goods/services, **quantity**, **unit price HT** (hors taxe).
7. **Total HT**, the **TVA rate(s)** and **TVA amount broken down by rate**
   (ventilation de la TVA par taux), and the **total TTC** (toutes taxes
   comprises).
8. **Terms / mode of payment** (modalités de paiement) where required.

> Native-term note: **HT** = hors taxe (net of VAT); **TTC** = toutes taxes
> comprises (VAT-inclusive); **TVA** = taxe sur la valeur ajoutée. Rates from 2026
> are principally **20%** and **10%** (7% and 14% phased out — see `morocco-vat`).

### Self-employed / auto-entrepreneur note

An **auto-entrepreneur** (statut AE) still issues conforming invoices and carries
an **ICE**. AE invoices are typically out of scope for TVA where the person is not
TVA-registered, but the Art. 145 identification and numbering rules still apply.
See `ma-auto-entrepreneur` for the regime and `morocco-vat` for TVA treatment.

---

## 3. The E-Invoicing Roadmap (status: UNCONFIRMED)

> Everything in this section is **announced / expected**, drawn from DGI
> communications, the PLF (projet de loi de finances) 2026 process, and Big-4 /
> vendor commentary. None of it is settled until the **décret d'application** is
> published in the **Bulletin Officiel**. Treat all dates as provisional.

### Legal mechanism

- **CGI Art. 145-IX** is the enabling provision: it lets the DGI mandate an
  IT-based invoicing system meeting technical criteria, with the specifics
  delegated to a regulatory text.
- As of the last research update, the **draft implementing decree** had been
  transmitted within government (reported as sent to the Secrétariat Général du
  Gouvernement) but was **not yet published**. **Until publication, no mandatory
  e-invoicing obligation is legally effective.** *(verify current status against
  the Bulletin Officiel and tax.gov.ma before advising.)*

### Expected model — Continuous Transaction Control (CTC / pre-clearance)

- Commentary points to a **clearance / CTC** model: each invoice would be
  **validated by the DGI platform before it is legally valid**, rather than a
  post-audit model where invoices are exchanged freely and checked later.
- The DGI was reported to have considered **both** post-audit and CTC; CTC /
  pre-clearance is the most-cited expectation but is **not formally confirmed** in
  a published text. *(verify.)*

### Expected platform

- A **national DGI platform**, developed by Moroccan firm **xHub** (Casablanca
  Technopark), integrated with the existing **Simpl-TVA** environment.
- A confirmed public-facing brand/URL (some sources speculate names such as
  *fatourati.gov.ma*) is **NOT verified**. Do not state a platform URL as fact.

### Expected formats

- Structured formats aligned to international standards — **UBL** (e.g. UBL 2.1)
  and/or **CII** — for interoperability. *(verify exact format and version in the
  technical spec / decree.)*

### Expected sequencing (waves)

- A **phased rollout** by size/type is expected: **large companies (B2B) first**,
  then **SMEs**, then **small enterprises**, then **B2C** last. **Specific dates
  and the turnover/headcount thresholds for each wave are decree-defined and not
  yet public** — do not quote figures.

### What this means for a freelancer

A typical self-employed person or micro-business sits in the **later waves** (small
enterprise / B2C), so even on the most aggressive announced timeline they are
**unlikely to be in the first cohort**. The honest position: *the obligation is
coming, the exact date for your tier is unknown, prepare but do not panic.*

---

## 4. Penalties

Two layers: **invoice-conformity penalties that exist today**, and **future
e-invoicing-specific penalties** that the decree may add.

### In force today (CGI)

- **Missing / wrong ICE** — penalty reported as **MAD 100 per omission**, capped
  around **MAD 5,000 per fiscal year** (CGI Art. 198 ter). *(verify amounts
  against current Loi de Finances.)*
- **Insufficient / irregular invoicing** — sanction reported in the range **MAD
  2,000 to MAD 50,000** (CGI Art. 146). *(verify.)*
- **Fictitious / fake invoices (factures fictives)** — **MAD 5,000 to 50,000** and
  potential criminal exposure (imprisonment) under CGI Art. 192. Serious; escalate.
- **Practical worst case: loss of deduction.** On audit the DGI routinely
  **rejects the customer's TVA and expense deduction** on a non-conforming invoice
  (no ICE/IF, broken numbering). This is usually costlier than the fixed fine.

### Future (e-invoicing-specific) — NOT yet set

- The implementing decree is expected to introduce **specific sanctions** for
  failure to issue cleared e-invoices, use of a non-compliant format, or
  non-transmission to the platform. **These do not exist as published, quantified
  penalties yet.** Do not state amounts. *(verify on decree publication.)*

> All penalty figures above are from secondary/research sources and require
> confirmation against the live CGI and the latest Loi de Finances by a Moroccan
> expert-comptable before being relied on.

---

## 5. What To Do Now

Practical, low-regret steps for a self-employed person — none of which depend on
the decree landing:

1. **Get and use your ICE.** Confirm your 15-digit **ICE** is obtained and printed
   on every invoice. Verify it (and your B2B clients' ICEs) where possible.
2. **Make invoices Art. 145-conforming today.** Seller IF/TP/RC/ICE, client ICE
   (B2B), **continuous sequential numbering with no gaps**, dates, descriptions,
   **HT / TVA-by-rate / TTC** breakdown. This is the baseline that survives any
   reform.
3. **Use structured invoicing software, not loose Word/Excel.** Pick a tool that
   keeps an unbroken numbering series and can export structured data. Vendors are
   already marketing "DGI 2026 ready / e-facture" software — treat such claims as
   **marketing, not certification**, until the DGI publishes conformity criteria.
4. **Keep your SIMPL access live.** Télédéclaration/télépaiement via **SIMPL**
   (portail.tax.gov.ma) is already mandatory for enterprises. Ensure credentials,
   email, and bank mandate work — the e-invoicing platform is expected to sit
   alongside this environment.
5. **Watch the Bulletin Officiel and tax.gov.ma** for the **décret d'application**
   and the **DGI technical specification**. The decree is the trigger event;
   nothing is mandatory before it.
6. **Identify your likely wave.** Large B2B is first; a freelancer is almost
   certainly later. Don't onboard to a clearance platform prematurely.
7. **Escalate the go-live decision** to a Moroccan **expert-comptable** once the
   decree is published — format choice, provider selection, and workflow change
   are professional-review items.

---

## 6. Reference + Test Suite

### Reference

- **CGI Art. 145** — mandatory invoice mentions (incl. Art. 145-VIII ICE).
- **CGI Art. 145-IX** — e-invoicing enabling provision (decree pending).
- **CGI Art. 146 / Art. 106** — regular-invoice precondition for deduction.
- **CGI Art. 192, 198 ter** — invoice-related sanctions.
- **Décret d'application (CGI 145-IX)** — *PENDING publication in the Bulletin
  Officiel; verify.*
- **PLF / Loi de Finances 2025–2026** — roadmap context; verify final wording.
- **SIMPL** — DGI télédéclaration/télépaiement portal (portail.tax.gov.ma).
- DGI: tax.gov.ma. Cross-skills: `morocco-vat`, `ma-auto-entrepreneur`,
  `ma-bookkeeping`, `ma-income-tax`.

### Test suite

**T1 — "When is e-invoicing mandatory for me?"** → State it is an announced
roadmap, decree pending, dates UNCONFIRMED; freelancers are in later waves; do not
quote a date. PASS only if no date asserted as fact.

**T2 — "Is fatourati.gov.ma the official platform?"** → Platform is a DGI/xHub
build integrated with Simpl-TVA; the public brand/URL is **not confirmed**. Do not
assert the name.

**T3 — "What must be on my invoice today?"** → ICE (seller, + client if B2B), IF,
TP/RC, sequential number, date, description, HT, TVA per rate, TTC, payment terms.

**T4 — "I forgot my client's ICE on a B2B invoice."** → Non-conforming; risks
client's TVA/expense deduction on audit + ICE-omission penalty (~MAD 100/omission,
verify). Reissue correctly.

**T5 — "Which format — UBL or CII?"** → Announced UBL/CII; exact format/version
**verify** in the DGI technical spec; not yet binding.

**T6 — Auto-entrepreneur asks if e-invoicing applies.** → Same roadmap; AE still
must issue Art. 145-conforming invoices with ICE now; later wave for clearance.
Cross-ref `ma-auto-entrepreneur`.

**T7 — "What's the penalty for a fake invoice?"** → CGI Art. 192: MAD 5,000–50,000
plus possible imprisonment; serious; escalate. Verify amounts.

**T8 — Vendor says software is "DGI 2026 certified."** → No published conformity
criteria yet; treat as marketing; verify after decree.

---

## PROHIBITIONS

- **NEVER assert an unconfirmed go-live date as fact.** The décret d'application is
  pending; all dates are provisional until published in the Bulletin Officiel.
- **NEVER state the clearance model (CTC/pre-clearance) as legally settled** — it
  is the expected model, not confirmed in a published text.
- **NEVER assert a platform name/URL** (e.g. *fatourati.gov.ma*) as official — not
  confirmed.
- **NEVER quote wave thresholds** (turnover/headcount) — decree-defined, not public.
- **NEVER state e-invoicing-specific penalty amounts** — not yet published.
- **NEVER accept an invoice without IF/ICE** as conforming.
- **NEVER tell a freelancer to onboard to a clearance platform before the decree** —
  that is a reviewer decision.
- **NEVER compute amounts** — defer arithmetic to the engine; this skill states
  rules and status only.

---

## Disclaimer

This skill is **research-verified** from DGI communications, the Loi de Finances /
PLF 2025–2026 process, and Big-4 / vendor commentary, and is **pending sign-off by
a qualified Moroccan expert-comptable**. Morocco's mandatory e-invoicing regime is
an **announced roadmap**: the implementing decree was still pending at the last
research update, so dates, scope, formats, the platform, and e-invoicing-specific
penalties are **subject to change and must be verified** against the Bulletin
Officiel and tax.gov.ma before being relied on.

Outputs are for informational and computational purposes only and do not
constitute tax, legal, or financial advice. All outputs must be reviewed and signed
off by a qualified professional before filing or acting upon. The most up-to-date,
verified version of this skill is maintained at
[openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ma-einvoice) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
