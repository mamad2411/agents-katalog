---
name: pe-dd-checklist
version: 1.0.0
description: Build and run the full private-equity due-diligence checklist across commercial, financial, legal, tax, tech/IT, HR, ESG, and insurance/environmental workstreams, tagging each finding as red-flag or confirmatory with an owner, status, and data-room reference.
author: matrixx0070
tags: [private-equity, due-diligence, quality-of-earnings, commercial-dd, data-room, workstreams, red-flags]
capabilities: []
---

## When to use

Use this once a deal is past screening and into confirmatory diligence — you have signed an LOI or exclusivity, a data room is open (or about to be), and you need a single instrument that scopes every workstream, assigns owners, and tracks findings to close. It is the control tower for the whole DD phase: it tells you what evidence each workstream must produce, who runs it (internal deal team vs external advisor), what has come back, and which findings are deal-breakers versus items to price or paper. Reach for it when you must brief the IC on diligence coverage, when advisor scopes are being negotiated, or when you need to know at a glance which stones are still unturned before signing.

**Not for:** modeling entry/exit, leverage, or the value-creation bridge that DD feeds (use pe-returns-analysis); dissecting LTV/CAC, contribution margin, or cohort curves inside the commercial workstream (use pe-unit-economics); the quick pre-LOI go/no-go filter that happens *before* this checklist exists (use pe-deal-screening); building the origination pipeline that surfaces the target (use pe-deal-sourcing); preparing the question banks and logistics for management and expert calls the checklist schedules (use pe-dd-meeting-prep); assessing the target's AI maturity and data assets as a value lever (use pe-ai-readiness); writing up the diligence conclusions for the committee (use pe-ic-memo); drafting the 100-day and full-hold plan the findings inform (use pe-value-creation-plan); or tracking KPIs, covenants, and board reporting after close (use pe-portfolio-monitoring).

This skill is deal-support, not legal, tax, or accounting advice. Named advisors (QoE accountants, counsel, tax, environmental) must confirm their own workstream findings before you rely on them for signing, pricing, or the SPA.

## Method

1. Set the deal frame: target, sector, deal size, structure (control buyout, minority growth, carve-out, add-on), and timeline to signing. **Decision:** a carve-out or platform buyout demands the full workstream set plus standalone-cost and TSA analysis; a bolt-on onto an existing platform can run a lighter, integration-focused scope. Right-size before you staff.
2. Instantiate the workstreams: commercial (CDD), financial (QoE), legal, tax, tech/IT, HR/management, ESG, and insurance/environmental. For each, name the **owner** and whether it runs internally or through an external advisor — and confirm the advisor is engaged before the data room opens, not after.
3. Build the information request list (IRL) per workstream and map it to the data-room folder structure so every request has a home and every document has a workstream. Track outstanding vs received.
4. Run each workstream to its evidence bar: CDD proves the market and the revenue's durability; QoE normalizes EBITDA and proves working capital and net debt; legal reads contracts, corporate records, litigation, IP, and change-of-control; tax proves the structure and exposures; tech assesses architecture, scalability, security, and tech debt; HR reads management, comp, retention, and org; ESG and environmental screen liabilities and reputational risk.
5. Classify every finding: **Decision:** tag each as **red-flag** (threatens thesis, price, or the ability to sign) or **confirmatory** (validates the model, no action needed). A red flag routes to one of three exits — kill, re-price, or paper it (indemnity, escrow, holdback, condition precedent). Never let a red flag sit unrouted.
6. Reconcile findings back to the model and thesis: every QoE adjustment, contract risk, or churn signal must flow to the returns model and the IC memo. Diligence that does not change the model or the price is decoration.
7. Maintain the tracker as a living document with status, dates, and owners, and hold a standing findings review so the IC sees coverage and open items in real time, not a data dump at the end.

## Example

A sponsor is buying a $180M-revenue industrial-services business at a 9.0x EBITDA multiple ($95M reported EBITDA, ~$855M EV). The checklist stands up eight workstreams. QoE (external accountants) normalizes EBITDA down by $7M — stripping a non-recurring insurance recovery and a related-party rent below market — landing adjusted EBITDA at $88M, which at the agreed 9.0x cuts EV by ~$63M and becomes the lead re-price argument. CDD (external strategy firm) confirms the top-10 customers are 55% of revenue but flags one at 18% with a contract expiring in 14 months and no renewal signed — a red flag routed to "paper it" via a price holdback tied to renewal. Legal finds a change-of-control clause in the largest supply agreement (red flag → condition precedent: obtain consent before close). Tech DD rates the field-scheduling system as end-of-life with ~$4M of deferred replacement cost — confirmatory of a known value-creation item, folded into the 100-day plan rather than the price. HR flags the CFO as a retention risk (no equity rollover) — papered with a new incentive plan. Environmental screens two owned sites as low risk after Phase I. The tracker shows 6 red flags, 3 routed to price, 2 to SPA protections, 1 to the VCP, closing the diligence with a defensible ~$792M revised EV.

## Pitfalls

- **Crediting management's numbers as diligenced.** Reported EBITDA is a starting point, not a finding. Until QoE has normalized for one-offs, run-rate adjustments, accounting policy, and quality of the number, the model rests on the seller's math.
- **Leaving red flags unrouted.** A finding that is not tagged kill / re-price / paper is not diligenced — it is noted. Every red flag needs an exit and an owner, or it resurfaces at signing as a surprise.
- **Confusing customer concentration disclosure with customer risk analysis.** Knowing the top customer is 18% is disclosure; knowing the contract expires in 14 months with no renewal is the risk. CDD must test durability, not just tabulate.
- **Under-scoping carve-outs.** A division separating from a parent carries standalone costs, stranded overhead, and TSA dependencies that reported financials hide. Missing dis-synergies is how carve-out models overstate day-one EBITDA.
- **Advisor scope gaps.** Between the QoE accountants, CDD firm, and counsel there are seams — cyber, insurance adequacy, pension exposure — that no one owns unless explicitly assigned. Map the whole surface and name an owner for every inch, or the seam becomes the post-close claim.

## Output format

```
# DD Checklist & Findings Tracker — <target> — <deal type> — <date> — v<n>
Deal: <EV / multiple / structure>   Signing target: <date>   Deal lead: <name>

## Workstream coverage
| Workstream | Owner | Internal/Advisor | Status | % complete | Key open items |
|-----------|-------|------------------|--------|-----------|----------------|
| Commercial (CDD) | | | | | |
| Financial (QoE) | | | | | |
| Legal | | | | | |
| Tax | | | | | |
| Tech / IT | | | | | |
| HR / Management | | | | | |
| ESG | | | | | |
| Insurance / Environmental | | | | | |

## Findings register
| ID | Workstream | Finding | Type (red-flag/confirmatory) | Impact | Route (kill/re-price/paper/VCP) | Owner | Status |

## Red-flag summary → deal impact
- <finding> → <$ impact / SPA protection / condition> — <owner>

## Information request status
| Workstream | Requests open | Requests received | Data-room folder |

## QoE bridge (reported → adjusted EBITDA)
| Reported EBITDA | +/- adjustment (reason) | Adjusted EBITDA | Effect on EV at <x> multiple |

Advisor workstream findings are PROVISIONAL until each advisor confirms in its final report.
```

## Reference

Substantive overview of the PE diligence process below — accurate to common market practice, not legal, tax, or accounting advice. Scope and findings for regulated workstreams must be confirmed by the responsible advisor.

### The deal timeline — where diligence sits

Diligence is the confirmatory phase between a non-binding indication and a binding commitment:

| Stage | What happens | This checklist's role |
|-------|-------------|----------------------|
| Sourcing / screening | Origination, first look, go/no-go | Not yet — see pe-deal-screening |
| IOI / NBO | Non-binding indicative offer on limited info | Frames what diligence must prove |
| LOI / exclusivity | Selected bidder, exclusivity granted | Checklist stands up; data room opens |
| Confirmatory DD | Full workstreams run to evidence bar | **Core use** |
| SPA negotiation | Findings → price, reps, indemnities | Red-flag routing feeds terms |
| Signing → close | Conditions precedent satisfied | Open items tracked to close |

### The eight workstreams

| Workstream | Core question | Typical owner | Key evidence |
|-----------|--------------|---------------|--------------|
| **Commercial (CDD)** | Is the market attractive and the revenue durable? | Strategy advisor + deal team | Market sizing/growth, competitive position, customer concentration, win/loss, pipeline, pricing power |
| **Financial (QoE)** | Is reported EBITDA real, and what is true net debt / working capital? | External accountants | Quality of earnings, normalizations, revenue recognition, working-capital normalization, net-debt bridge |
| **Legal** | What obligations, risks, and consents attach to the business? | Counsel | Corporate records, material contracts, change-of-control, litigation, IP, employment, real estate, regulatory |
| **Tax** | Is the structure sound and are there historical exposures? | Tax advisor | Historical filings, transfer pricing, VAT/sales tax, structuring, tax attributes |
| **Tech / IT** | Does the technology scale, and what is the debt/security posture? | Tech DD advisor / internal | Architecture, scalability, security, tech debt, key-person dependency, roadmap cost |
| **HR / Management** | Is the team capable and retainable? | Deal team + HR advisor | Org structure, management assessment, comp, retention, culture, pensions |
| **ESG** | What sustainability and governance risks exist? | ESG advisor / deal team | Environmental footprint, governance, social/labor, reputational exposure |
| **Insurance / Environmental** | What insurable and site liabilities exist? | Insurance broker / env consultant | Coverage adequacy, claims history, Phase I/II environmental, contamination liability |

### Red-flag vs confirmatory findings

Every finding resolves to one of two types, and every red flag to one of three exits:

| | Definition | Action |
|--|-----------|--------|
| **Confirmatory** | Validates a thesis assumption or the model | Log; no price/term change |
| **Red flag** | Threatens thesis, price, or ability to sign | Must be routed |
| → Kill | Fundamental, un-mitigable | Walk away |
| → Re-price | Quantifiable value impact | Adjust EV/offer |
| → Paper it | Manageable via contract | Indemnity, escrow, holdback, CP, R&W insurance |

### Quality of Earnings — the financial workstream's core output

QoE reconstructs a defensible earnings base and balance sheet from reported figures:

- **EBITDA normalization** — remove non-recurring items (litigation settlements, one-off gains), owner/related-party adjustments (above/below-market rent, personal expenses), run-rate adjustments (full-year effect of new contracts or headcount), and accounting-policy effects. The output is *adjusted (normalized) EBITDA* — the number the multiple is actually applied to.
- **Net-debt bridge** — move from equity value to enterprise value by identifying all debt-like items: funded debt, capital leases, unfunded pensions, deferred consideration, and debt-like provisions.
- **Working-capital normalization** — establish a normalized working-capital level (peg) so the buyer neither over- nor under-pays for working capital delivered at close; seasonality and quality of receivables matter.

A QoE EBITDA adjustment flows straight to price: at a purchase multiple *m*, a ΔEBITDA changes enterprise value by roughly *m × ΔEBITDA*.

### Data-room organization

A well-run data room mirrors the workstreams. Discipline here is what makes diligence auditable:

| Folder | Contents |
|--------|----------|
| 1. Corporate | Cap table, org chart, board minutes, constitutional docs |
| 2. Financial | Audited/management accounts, budgets, QoE support |
| 3. Commercial | Customer/supplier contracts, pipeline, market data |
| 4. Legal | Material contracts, litigation, IP, permits |
| 5. Tax | Filings, correspondence, structuring memos |
| 6. HR | Org, comp, employment agreements, pensions |
| 7. Tech / IT | Architecture, security, systems inventory |
| 8. ESG / Environmental | Reports, Phase I/II, policies |

Track each information request against its folder so nothing is both "requested" and homeless.

### Provider vs advisor roles

Diligence is run by the deal team but executed largely through advisors, and the split matters for accountability:

- **Deal team (internal):** owns the thesis, sets scope, integrates findings into the model, and makes the buy/pass call. Typically runs management assessment and light commercial work directly.
- **External advisors:** QoE accountants, CDD/strategy firm, legal counsel, tax advisor, tech DD, environmental consultant, insurance broker. Each owns its workstream's evidence and signs its own final report — the buyer relies on the advisor's confirmation, not the deal team's summary, for regulated conclusions.
- **Reliance:** where a bank or co-investor will rely on advisor reports, reliance letters must be arranged; findings marked PROVISIONAL until the advisor's final report is issued.
