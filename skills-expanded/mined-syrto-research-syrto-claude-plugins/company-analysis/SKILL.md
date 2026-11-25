---
name: company-analysis
description: >-
  Formal single-company report on an Italian company from Syrto data, with two dials: a depth
  **livello** (1 solo azienda + benchmark automatico · 2 + mercato · 3 + competitor · 4
  completa) and a **taglio** lens - `normale` (understand the company) or `commerciale`
  (qualify it for sales: Fit Score, spend capacity, cosa proporgli, go/no-go). Livello 1 +
  commerciale is the quick commercial qualification. Use for "analisi azienda", "analizza [azienda]", "report /
  dossier / scheda su [azienda]", "com'è messa [azienda]", "salute finanziaria di [azienda]",
  "qualifica [azienda]", "profila [azienda]", "è un buon fit", "vale la pena", "scheda
  finanziaria", "cosa vendergli", "analyse [company]", "company report on [company]", "is
  [company] a good fit", "should we go after [company]".
  Not for preparing a meeting or call - person, news, talking points, the day's calendar (use
  `briefing`) - nor for a peer list alone (use `syrto-comparables`) or company vs sector
  aggregates alone (use `market-benchmark`).
metadata:
  version: "2.0.0"
---

# Company Analysis

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`), which says which tool serves each capability named here. Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill. This skill **composes** `market-benchmark`, `market-sizing` and `syrto-comparables` as building blocks — reuse their logic, do not re-implement it.

## Read your context first
From the profile (core §3): the user's sector and role. They drive **which numbers to feature** and the language register. The goal each sector's numbers serve is listed in `${CLAUDE_PLUGIN_ROOT}/skills/syrto-onboarding/references/proficiency-model.md` ("Sector overlay"); if the sector-relevant emphasis is unclear, choose it from there yourself rather than asking the user to pick metrics. Also read the preferences (core §3) if present: it stores a default **livello** (a tier, or "ask each time") and a default **taglio** (`normale` / `commerciale`, or "ask each time").

## The two dials (independent)
Every report has two orthogonal dials: **livello** (depth / scope) and **taglio** (lens).

- **`normale`** — understand the company: financial health, market, peers. The formalized report.
- **`commerciale`** - qualify the company for sales on top of the analytical content: Fit Score, spend capacity, "perché è in target", product-fit ("Cosa proporgli"), and a go/no-go verdict. Available at every livello 1-4.

Resolve each dial in this order:

1. **The request itself.** "qualifica X", "è un buon fit", "vale la pena", "cosa vendergli" mean commerciale; "analizza X", "salute finanziaria", "com'è messa" mean normale; "completa", "con il mercato", "con i competitor" name the livello.
2. **The saved default** in the preferences (core §3).
3. **Otherwise ask once, with both dials in one question.** You may suggest the likely taglio from the user's role (commerciale for sales / BD / commercial banking; normale for credit / M&A / due diligence), but let the user choose.

When a dial comes from the request or from a default rather than from the question, say so in one line at the top of the answer, so the choice is visible and easy to change: *"Livello 1, taglio commerciale - dimmi se preferisci altro."* Any request can override either dial: *"stavolta normale"*, *"fammela completa e commerciale"*.

Ask with a structured choice if your client offers one, otherwise as a short numbered question:

> Che analisi vuoi per **[Azienda]**?
>
> **Livello**
> 1. **Solo azienda** - i numeri di [Azienda] con un confronto rapido con le aziende della stessa classe ATECO e della stessa fascia dimensionale nella sua area geografica (benchmark automatico, indicativo).
> 2. **Azienda + mercato** — [Azienda] più un'analisi del mercato in cui opera, costruita su un perimetro pulito basato sulla sua **attività reale** (non sull'ATECO): dimensione, dinamiche e benchmark veri.
> 3. **Azienda + competitor** — [Azienda] a confronto con i suoi **peer diretti** (senza l'analisi di mercato).
> 4. **Completa** — azienda + mercato + competitor, il quadro intero.
>
> **Taglio**: **commerciale** (fit score in alto, perché è in target, cosa proporgli, verdetto) o **normale** (report standard: numeri, e mercato/peer secondo il livello)?

### Persisting the defaults
After the first report built from that question (not from a default), ask **once**:

> Vuoi che questi diventino i tuoi **default** — livello **[N]** e taglio **[normale/commerciale]** — quando chiedi un'analisi azienda (salvo diversa indicazione), oppure preferisci che te lo **chieda ogni volta**?

Save both to the preferences (core.md §3). Thereafter use the defaults, stating them in one line as above, or keep asking, per the user's choice.

## The four levels and the benchmark rule
Internal labels: `solo-azienda` · `azienda-mercato` · `azienda-competitor` · `completa`.

- `solo-azienda` - company financials plus the **automatic benchmark** of the financial analysis (same call, no separate aggregate). This is the only level that shows it.
- `azienda-mercato` - company plus a proper market analysis on a **clean perimeter built from the real activity** (not ATECO); see "Composing the building blocks".
- `azienda-competitor` - company plus direct peers via `syrto-comparables`.
- `completa` - company plus market plus peers.

From livello 2 on, read the financial analysis without its automatic benchmark: next to a real market or peer layer it confuses. The analysis still rates each metric 1-5 against that same automatic benchmark, so at levels 2-4 either leave those ratings out or label them "rating Syrto (benchmark automatico)", so the reader never sees two benchmarks that disagree without explanation. The **taglio** dial is independent of this rule.

When you show the automatic benchmark, describe it as companies of the same sector class and size band in the company's macro-area (country-wide for large companies). It is not a national sector average, not a median and not a mean, and the report does not name the region.

## Composing the building blocks
- `azienda-mercato`: build **one** perimeter from the real activity with `market-sizing`'s calibration, take market size and dynamics from it, then position the company against that same perimeter with `market-benchmark`'s logic. Calibrate once and reuse the perimeter.
- When you run `market-sizing`, `market-benchmark` or `syrto-comparables` inside this report, skip the setup questions this skill has already answered (the company, the real-activity method the level promises, the output format) and do not produce their separate deliverables: their results become sections of this report. Their perimeter checkpoints still apply. Ask only what is still missing (for peers, the revenue range), ideally in the same message as the livello question.

## The commercial cut (taglio = commerciale) — works at ALL levels 1–4
When the lens is `commerciale`, keep everything the chosen **livello** produces and add the commercial reading, per `core.md` §4. It reuses what the level fetched. Some Fit Score inputs are not in the financial analysis (the spend-hook cost line, net worth; the capability map lists them): read those with one specific metric read for just those metrics, the same inputs `briefing` uses, so a company scored by both skills gets the same score. **Layout: the commercial part goes at the TOP of the deliverable**, then the level's analytical content below.

1. **Fit Score (0–100) at the top**, prominent, with — right underneath — a strong **"perché è in target"** narrative (leads with the business-fit reason, then the main drag; first time in a conversation, briefly explain the score's composition).
2. **"Cosa proporgli"** — a section on which of the user's products/services (from the catalogue in the commercial context, core §3) this company is in target for, each tied to a concrete finding. **Include it only if you actually know the catalogue** (it's in memory); otherwise omit the section — never invent products, and at first run invite the user to add their catalogue.
3. **Spend capacity (€)** = spend-hook metric × capture rate (from the commercial context), the rough deal ceiling.
4. **Go/no-go verdict** — one tier (Strong fit / Qualified / Monitor / Out of target / Insufficient data). Respect exclusions from the commercial context.

Then, below, the level's analytical content (the company numbers, plus market/peers at levels 2–4).

**Livello 1 + taglio commerciale = the quick commercial qualification**: company card, Fit Score, key-ratio table with the automatic benchmark, spend capacity, "perché è in target", "Cosa proporgli", and the coloured verdict. At levels 2–4 the same commercial block rides on top of the richer market/peer analysis.

## Routing — this skill vs `briefing`
Both handle a single company; they differ by **purpose**. This skill decides and documents: is the company worth pursuing, how is it doing, at a chosen livello, with the taglio selecting the lens. `briefing` prepares a conversation: person, news and talking points, often from the day's calendar. A request that mentions a call, a meeting or a person goes to `briefing`; a single named company with no meeting context comes here.

## Build steps
1. **Resolve the company and its statement basis.** Resolve by tax ID when you have one, otherwise by name, and confirm the legal entity; watch for holding/retail shells (core.md §7). Reuse an upstream handoff if present. Default to the company's own (individual) statement. Use the group's consolidated statement when the user asks about the group, or when a holding's individual figures look implausibly small next to its known size; if you do not know whether a consolidated statement exists, resolve both and choose. The automatic benchmark and the market and peer layers are built from individual filings, so on a consolidated report say that the comparison sets a group against single companies, and read the gaps as indicative.
2. **Company core.** The company profile, then the financial analysis as the base: pre-grouped (margins, returns, liquidity, solvency, structure, radar, two-year trajectory), with its automatic benchmark only at `solo-azienda`. The sector lens is mostly a **presentation** choice: the analysis already returns a broad set, so feature the sector-relevant numbers from it. Only if a needed figure is genuinely outside it (a raw balance-sheet line, a niche ratio) add **one** specific metric read for just those metrics, confirming each one via metric-definition search. Never loop, never re-fetch what the analysis already has.
3. **Level-specific layer** —
   - `solo-azienda`: the automatic benchmark, already in the analysis call.
   - `azienda-mercato`: see "Composing the building blocks".
   - `azienda-competitor`: run `syrto-comparables`.
   - `completa`: market + peers.
4. **Commercial cut** - only when `taglio = commerciale`: add the Fit Score, spend capacity, "perché è in target", product-fit and go/no-go verdict (see "The commercial cut" above).
5. **Compose** — assemble the report; feature the sector-relevant numbers; keep the register per the proficiency profile.

## Output
Per `core.md` §5: a formalized deliverable (HTML, then offer the PDF); the visual canon comes from the preferences or the neutral default. Structure adapts to the level (company section always; market and/or peer sections as applicable) and to the lens: when `taglio = commerciale` the deliverable **leads with the Fit Score + "perché è in target" at the top, then "Cosa proporgli"** (only if the catalogue is in memory), then the level's analytical content and the verdict. State the statement basis on the cover. Depth and technicality of the prose follow the proficiency profile. Close with the Syrto source line from the capability map. End with a `SYRTO-HANDOFF` whose `chain` is the chain that actually led here, ending in `company-analysis`. It carries the resolved id and statement basis, anagraphic, metrics, any market/peer artifacts and, when the commercial cut ran, the fit result and product-fit mapping, so downstream skills (e.g. `outreach-writer`) reuse them.

## Guardrails
The suite guardrails in `core.md` §7 apply. Specific to this skill:
- The automatic benchmark appears only at livello 1 (see the benchmark rule).
- In the commercial cut a score always comes with its narrative naming the main drivers and the main drag; missing financials give "Insufficient data" with the tax-ID suggestion.
- Do not silently switch level or lens: if you built something other than what was asked or saved, say what you built.

## Radar positioning (optional)
If the question is really about *where this company sits* rather than which numbers it posts, the positioning radar (see the capability map) can place it against its sector or its peers in one call, and can give an SVG for a file. Optional: reach for it when positioning is the point, not as a routine step.
