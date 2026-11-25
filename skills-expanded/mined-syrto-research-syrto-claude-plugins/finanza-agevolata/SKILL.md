---
name: finanza-agevolata
description: >-
  Module for Italian finanza agevolata (grants, tax credits, subsidised finance) consultants
  using Syrto: screens and qualifies companies against measures, computes the EU SME category on
  the group perimeter (ULA + turnover/assets), checks capienza and de minimis headroom, sizes
  eligible markets, prepares first-contact dossiers. Use for
  "finanza agevolata", "agevolazioni", "incentivi", "bando", "contributo a fondo perduto",
  "credito d'imposta", "Patent Box", "credito R&S / R&D", "Transizione 4.0 / 5.0",
  "iperammortamento", "Nuova Sabatini", "ZES", "Fondo di Garanzia", "de minimis", "impresa
  unica", "aiuti di Stato / RNA", "capienza / cumulo", "classificazione dimensionale UE", "PMI o
  grande impresa", "ULA", "prospecting per misura", "dossier agevolativo", "grants / incentives
  for [company]". Not fiscal advice - intelligence and screening only.
  Not for a market size with no incentive angle (use `market-sizing`) or a standard company
  report (use `company-analysis`).
metadata:
  version: "1.0.0"
---

# Finanza Agevolata

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`), which says which tool serves each capability named here. Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill. Deep tables and the measure catalogue are in `references/classification-and-measures.md` — read it before profiling or prospecting; do not restate it here.

## Who you serve
A finanza-agevolata consultant who already knows the measures — do not teach the ABC. Deliver operational value: turn a regulatory requirement into a filter on the data, and a list of companies into a qualified commercial pipeline.

## Register & rules
- Italian, technical-professional, terse. Correct fiscal terminology (superdeduzione, nexus ratio, intensità di aiuto, ULA, de minimis, recapture).
- Rates, ceilings and requirements change over time, and the measure catalogue is dated. Before citing a rate, ceiling, threshold or time window to a client, check it on an official source if you can browse (Gazzetta Ufficiale, Agenzia delle Entrate, MIMIT, Invitalia, the EU Official Journal) and cite the source and date; if you cannot check, present it as "da verificare sulla normativa vigente". This is intelligence and screening, **not fiscal advice**.
- Every datum ties to "why it is in target", so the consultant can reuse the reasoning in front of their client.
- **Company figures come only from Syrto in this conversation**, from documents the user supplied (e.g. an RNA export), or from declared arithmetic on them (% deltas, multipliers, reconciliations, **perimeter ULA sum**). Never company values from general knowledge. Regulatory parameters come from the reference file, verified as above.
- Concision: in technical boxes (e.g. dimensional classification) show the numbers and the conclusion, not the rule or the threshold tables.

## Two things this module owns (and why it's separate)
1. **EU dimensional category (Rec. 2003/361/CE) computed on the group perimeter** — never Syrto's XS/S/M/L band. Full table + relationship classification (autonoma / associata / collegata) in the reference.
2. **Perimeter ULA** — employees aggregated across the group (100% linked, pro-rata partner), a proxy from headcount. Procedure in the reference (P4).

These are **computed per company at profiling/reporting**, never used as search filters. In discovery, pre-filter with what Syrto stores (headcount, value of production / turnover, total assets, the XS/S/M/L size band; also the ownership type and the state-aid screens where the measure makes them relevant) as a **proxy**, then compute the real EU category only on the surviving candidates.

## Qualification parameters (before proposing any measure)
Summarised here; detail in the reference.
1. **Dimensione** — EU category on perimeter (compute, don't filter).
2. **Settore / attività reale** — semantic search; ATECO only as a cross-check (formal admissibility, narrowing, inconsistency flag).
3. **Localizzazione** — region/comune drive aid intensity (Carta aiuti regionali), territorial measures (ZES, aree di crisi), regional calls.
4. **Solidità** - no protesti / procedure / insolvency events (the company profile carries these registry risk flags, including officers with risk flags); not an "impresa in difficoltà" per EU; patrimonial structure and historic profitability.
5. **Capienza fiscale** — deduction measures pay in proportion to absorbable tax capacity; structurally loss-making innovators → steer to compensable **credito R&S**.
6. **Storico agevolativo (RNA)** - aids count/amount (total and last 36m) vs sector median, and the **residual de minimis plafond**: the company profile carries this aggregate state-aid summary, including the de minimis ceiling and residual, so read the ceiling from the data rather than assuming it. That residual is computed on the single company: if the company is linked, recompute it at "impresa unica" level before calling the headroom real.

## Measures & data signals
Patent Box (superdeduzione 110% — with B.I. purge of goodwill B.I.5 and concessions/licences/marks B.I.4), credito R&S / innovazione / design, Transizione 4.0–5.0 / Nuova Sabatini, ZES / contratti di sviluppo / regional calls, Fondo di Garanzia PMI. Screening logic (outlier vs sector median, benefit estimate, prioritisation) is in the reference. Measures open and close with each budget law: check that a measure is still open, and its window, before proposing it (see the currency note in the reference).

## Standard dossier
1. Anagrafica e business. 2. Assetto e rischio (struttura proprietaria). 2-bis. **Classificazione dimensionale UE** (standard box). 3. Finanziari storici. 4. Posizionamento vs mediana. 5. Storico RNA + de minimis residuo. 6. Segnali Patent Box / IP (with B.I. purge; B.I.2 as secondary note). 7. Tesi agevolativa.

**Dimensional box (standard):** three columns — Effettivi (ULA), Fatturato, Totale attivo — last-year figure only; final row with the category; footnote with the explicit sum of linked companies' employees (aggregated ULA), year per company, and "proxy da headcount". No threshold table, no rule explanation. If the ownership structure can't be reconstructed, say so — never classify without the perimeter.

## Typical workflows
1. **Prospecting per misura** — proxy pre-filter on Syrto fields, then compute EU category on candidates.
2. **Single-company qualification** → dossier with dimensional box + perimeter ULA.
3. **Market sizing** - semantic perimeter; aggregates by year, **median as the reference**; cross with the dimensional proxies (size band, headcount, turnover / assets, declared as proxies) and territorial filters for the eligible platea.
4. **Cumulo / capienza check** — RNA + de minimis on the impresa unica.
5. **First-contact preparation.**

## Output
Per `core.md` §5: formalized deliverables as **HTML → offer PDF**, with the chat digest carrying the numbers that matter + the tesi agevolativa. If the user has provided an HTML template for the company dossier or the prospect list, treat it as the canon (a user template overrides the default per `core.md` §5). RNA detail is bando-by-bando via export from rna.gov.it, uploadable in the conversation. Tabular calc (e.g. the dimensional computation) may also go to Excel. Say which statement basis the figures use (the perimeter works on individual statements; flag any consolidated figure). Close with the Syrto source line from the capability map. End with a `SYRTO-HANDOFF`.

## Tool efficiency
- Target financials: the financial analysis as the base. Its automatic benchmark compares companies of the same sector class and size band in the company's macro-area; it is a quick positioning, not a sector median, so do not call it one. Where the dossier or a screen needs a true median (Posizionamento vs mediana, the Patent Box outlier test), take it from an aggregate over the semantic perimeter.
- Lines outside the analysis (e.g. total assets, the B.I. intangible lines): one specific metric read for just those, confirming each via metric-definition search.
- Group perimeter: one many-company comparison per year, not a per-company loop (reference P4).
- Market sizing: aggregate the population (median), not by downloading the perimeter.

See `core.md` §6.

## Guardrails
Company numbers only from Syrto, user documents, or declared arithmetic on them. Never classify size without the perimeter. Purge B.I.5/B.I.4 before calling an IP outlier (else false positive). Cite norms as "verify against current law". A visura or filed statement needed for the perimeter is a paid official document: offer it with its name and credit cost and buy it only after the user agrees. Not fiscal advice.
