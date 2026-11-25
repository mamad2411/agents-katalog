---
name: prospects-scout
description: >
  Build a fresh, ranked list of NEW prospect companies using Syrto semantic search: from
  criteria you describe, from a seed of your best clients (lookalikes), or from a client list
  in a connected CRM or an uploaded file. Use whenever the user says "trova prospect", "trova
  clienti", "cerca aziende target", "lista prospect", "aziende simili ai miei clienti",
  "lookalikes", "espandi la pipeline", "nuovi target in [settore/regione]", "find new
  prospects", "lookalikes of my clients", "new targets", "who else looks like this", or wants
  a target-company list in a sector/region. Profiles companies only: no contact finding, no
  campaign push. Outputs a scored, tiered top-prospect list plus a SYRTO-HANDOFF for
  downstream skills. Not for ranking a list the user already has (use priority-ranker),
  growing existing clients (use upsell-potential-scout), the peers or competitors of one
  company (use syrto-comparables), or acquisition targets (use add-on-finder).
metadata:
  version: "1.0.0"
---

# Prospects Scout

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`). Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill.

Produce a screened, ranked list of candidate companies to pursue. Companies only — this skill does not find people or push campaigns.

## Read your context first
Read the commercial context (core §3): target revenue band, target sectors/geographies (used as plain-language semantic queries), hard exclusions, spend hook + capture rate, and any portfolio/reference clients. Any field the user states this turn overrides the saved context. If a field the search needs is missing, ask once and offer to save it. NACE/ATECO is used only for hard exclusions or an explicit narrowing — never as a default gate.

## Three entry modes
Detect the mode from the request; ask only if ambiguous.

- **(a) From criteria / from scratch** — the user describes the target (sector, activity, size, geo) or you take it from the saved commercial context. Build semantic queries from that description.
- **(b) Seed list of best clients (lookalikes)** — the user names clients or points to a portfolio. Take the top clients, read each one's activity description in the company profile, and derive semantic queries from what they actually do.
- **(c) Client list from a CRM or a file** - read it from a CRM connector if one is available, otherwise from the spreadsheet or CSV the user uploads. Use it both to seed lookalike queries and to dedup (never re-surface an existing client).

## Steps
1. **Assemble the queries.** One or more semantic queries in the company's language (Italian by default). For lookalikes, one query per distinct client archetype, so each prospect can be traced back to the client it resembles.
2. **Search Syrto.** Run one company search per query. Use a slightly more permissive relevance cutoff than the server default, about 0.75, because a good prospect often sits in an adjacent trade that a peer-discovery cutoff would drop; raise it if the results are noisy. Add the revenue band and geography from the context as filters (the search-filter documentation lists them). Add a sector-code filter only for a hard exclusion or an explicit narrowing.
3. **Screen out.** Remove companies already in the portfolio/CRM (match on tax ID where the list has one, since names are written many ways), anything hitting a configured exclusion, and obvious holding/retail shells (find the operating entity through the ownership structure and resolve it by tax ID instead). State how many were removed and why.
4. **Quick-score survivors.** Read the company profiles of the top candidates, then their Fit Score inputs in one many-company comparison per batch, for one fiscal year: the year the chain already fixed, else the latest year most of them have filed. Compute an abbreviated Fit Score, spend-capacity estimate, and verdict tier per `core.md`.
5. **Suggested angle.** One line per kept prospect: for lookalikes, which client it resembles and why it scored well; for criteria mode, the main driver.

## Output
Per core §5, the full scored list is a file and the chat carries a digest. Columns: company, sector (Syrto), revenue, match score, Fit Score, spend-capacity estimate, coloured verdict tier, and suggested angle; the chat digest is a table of the top ~10 with the same columns. Above it, how the seeds/queries were chosen, the screening summary (excluded N for reason X), and the fiscal year and statement basis the scores use. Offer the list also as a spreadsheet, with your client's spreadsheet capability. End with a `SYRTO-HANDOFF` (chain `prospects-scout→company-analysis→outreach-writer`) carrying resolved ids, filters used, anagraphic and the metrics/fit already gathered, so `company-analysis` and `outreach-writer` start from there.

## Guardrails
Relevance over size — don't let big-but-irrelevant matches top the list. Quick-score is provisional; recommend full profiling before outreach on the top names. Rationale mandatory per prospect. Call out distress signals explicitly. Respect exclusions from the commercial context.
