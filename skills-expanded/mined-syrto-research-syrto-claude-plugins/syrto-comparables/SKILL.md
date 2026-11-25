---
name: syrto-comparables
description: >
  Find the direct competitors (peer group) of an Italian company with Syrto: a semantic search
  on the company's real activity (not ATECO codes), within a revenue range the user chooses,
  narrowed to the 5 closest by activity and target market, with an optional Excel table.
  Trigger when the user types "comparables [company name]" or "comparables [partita iva/codice
  fiscale]", or asks for aziende simili, peer group, comparable, competitor, analisi comparativa,
  confronto con aziende simili, "find peers / competitors of [company]".
  Trigger examples: "comparables Enel", "comparables 00484960588", "peer group di Luxottica",
  "chi sono i competitor di Ferrari", "trova aziende simili a Mutti".
  Not for a company against its sector aggregate (use `market-benchmark`), sizing a market (use
  `market-sizing`) or a single-company report (use `company-analysis`, which calls this skill at
  livello 3-4).
---

# Syrto Comparables Finder

This skill finds comparable companies to a target company using Syrto's semantic search, filtered by a user-specified revenue range, then narrows down to the 5 most direct competitors.

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`), which says which tool serves each capability named here. Reuse any upstream `SYRTO-HANDOFF` (the resolved target, its revenue, its descriptions) before calling Syrto.

When `company-analysis` runs this skill (livello 3-4), the top 5 go into that report: skip the Excel question in Step 7, and ask the revenue range in the same message as the livello question if it was not given.

End with a `SYRTO-HANDOFF` (per `core.md` §8) listing the target and the five peers with their resolved ids, tax ids and relevance scores.

## Workflow

### Step 1: Find the Target Company

Resolve the target by tax ID when the user gives one, otherwise by name. If several candidates match, pick the best one or ask the user (core.md §6). Keep its resolved id.

Default to the target's own (individual) statement: peers found by the search are individual filings too, so the revenue range compares like with like. If the target is a group the user wants read on its consolidated statement, see the note in Step 3.

### Step 2: Fetch Target Company Data

Make these two reads one after the other (core.md §6):

1. **The company profile** → its short activity description (what the company does), its target-market description (who their customers are), and the sede/regione.
2. **A specific metric read** of its revenue from sales and services for the latest filed year → the revenue figure, useful context for suggesting a range to the user.

If an upstream skill already fetched these, reuse them.

### Step 2b: Fallback — Missing Description Data

Small companies on Syrto may not have the activity description and/or the target-market description. If either is empty after Step 2:

1. **Look up the company online.** Use the website in the company profile (if available), or search the web for the company name.
2. **Show the website to the user** and ask them to confirm it's the right company (e.g., "Ho trovato il sito dell'azienda: https://www.example.com — è corretto?").
3. **Once confirmed, read the website** and generate the missing descriptions yourself, matching the style and format of Syrto's own descriptions.

This is the one place the suite lets the web describe what a company does (core.md §2 otherwise keeps the business model to Syrto): only when Syrto has no description, only after the user confirms the website and approves the generated text, and the output says the peer search started from a description written from the website.

When generating these descriptions, follow Syrto's style closely. Here are real examples to use as reference:

**Activity description examples from Syrto:**
- "Management and strategy consulting for Italian SMEs: M&A, organization, digitalization, compliance, sustainability, sector-focused integrated solutions."
- "Designs, engineers, and builds high-performance and luxury sports cars, runs motorsport teams, and delivers brand experiences."
- "Produces and distributes premium frozen and chilled ready meals, sauces, and pasta for retail and foodservice channels."
- "Develops and operates cloud-based ERP and management software for Italian SMEs, with modules for accounting, invoicing, warehouse, and CRM."

**Target-market description examples from Syrto:**
- "Primarily targets SMEs and mid-market enterprises seeking growth and transformation across multiple sectors."
- "Targets B2C consumers and enthusiasts of luxury sports cars, racing experiences, and premium lifestyle products."
- "Serves large-scale retail chains, independent grocery stores, and professional foodservice operators across Italy and Europe."
- "Targets micro-enterprises, freelancers, and small businesses needing affordable, easy-to-use management tools."

The pattern: the activity description is a concise, factual description of what the company does (products, services, core activities), typically one sentence. The target-market description says who they sell to (customer type, segments, channels), also one sentence.

Generate both descriptions and show them to the user for confirmation before proceeding.

### Step 3: Ask the User for Revenue Range

Do NOT assume a revenue range. Instead, present the target company's revenue to the user and ask them what range they want to search in. This is important because different use cases require different ranges — an M&A advisor might want companies half the size, while a benchmarking exercise needs companies of similar scale.

Ask the user something like:

```
L'azienda ha un fatturato di XX,X Mln €. In che range di fatturato vuoi cercare le comparabili?
- Inserisci min e max (es. "5M - 50M")
- Oppure solo un massimo (es. "fino a 100M")
- Oppure un range relativo (es. "±40%")
```

Use the user's answer to set the `min` and `max` for the revenue filter in the next step. If the user gives a relative range like "±40%", calculate it from the target's revenue. If they give only a max, set min to 0.

If the target is read on its group's consolidated statement, the peers will still be single companies: suggest the range from the target's individual revenue, or tell the user that the comparison sets a group against single companies.

### Step 4: Build the Semantic Search Prompt

Take the activity description from Syrto (the short description) and craft a prompt that describes **specifically** the type of business this company does. The goal is NOT to broaden or generalize into a wider market: it's to write a precise, well-structured description of the same business activity.

**How to build the prompt:**
1. Read the activity description from Syrto
2. Rewrite it as a clear, specific description of what this type of company does
3. Keep it faithful to the original — don't add adjacent sectors or unrelated specializations
4. Structure it as a natural sentence that works well as a semantic search query

**Example:**
- Syrto activity description: "Management and strategy consulting for Italian SMEs: M&A, organization, digitalization, compliance, sustainability, sector-focused integrated solutions."
- Your crafted prompt: `"Management and strategy consulting firms advising small and medium-sized enterprises (SMEs), specializing in one or more of the following: mergers and acquisitions (M&A), organizational design, digital transformation, regulatory compliance, ESG and sustainability."`

**Another example:**
- Syrto activity description: "Progettazione e fornitura di sistemi di illuminazione naturale, ventilazione e evacuazione fumi, software, consulenza e manutenzione."
- Your crafted prompt: `"Aziende che progettano, forniscono e supportano sistemi di illuminazione naturale, sistemi di ventilazione naturale e sistemi di evacuazione fumi, incluse le relative soluzioni software, consulenza tecnica e servizi di manutenzione."`

The prompt stays specific to what the company actually does — it just restructures the short description into a clean query that works well for Syrto's semantic matching engine.

Show the crafted prompt to the user before searching, so they can adjust it if needed. You can put it in the same message as the range question in Step 3, so the user answers both at once.

### Step 5: Search for Comparable Companies

Run one company search, building the filter object from the search-filter documentation:
- **Activity:** a semantic search on the **prompt crafted in Step 4**, with a permissive relevance cutoff of about 0.5 (well below the server default). Breadth is the point here: results come back ranked by relevance, and Step 6 does the real selection.
- **Revenue:** revenue from sales and services within the `min` and `max` from Step 3.
- **Year:** the latest fiscal year the target has filed, so the target's revenue and the peers' revenue bound refer to the same year.

This should return companies that do similar things AND are in the user's desired revenue bracket.

If fewer than 10 results come back, consider widening the revenue range slightly or lowering the relevance cutoff to about 0.4, and tell the user you widened. If still too few, note this to the user: some niches are small.

**Keep, for each result, what you'll reuse:** its resolved id, its relevance score (you'll show it in the final top 5) and its activity summary (every semantic-search result carries one). Holding on to the activity summary here is what lets Step 6 skip a batch of extra calls.

### Step 6: Select the Top 5 Direct Competitors

The first page of results (the most relevant companies) is your candidate pool; you rarely need a second page. Similarity alone doesn't guarantee they're direct competitors, and this step filters for the most relevant ones.

The good news: the semantic search already handed you each candidate's activity summary in Step 5. That is the same information as the activity description you'd otherwise fetch, so **do not read the company profile of the candidates just to read their activity**: reuse the activity summary you already saved. Reading ~10 profiles to re-fetch data you already have is wasted time and Syrto usage.

You only need a candidate's company profile in two situations:
- its activity summary came back empty or missing from the search, or
- the activity comparison is a genuine toss-up and you want the target-market description (which the search does not return) to break the tie.

In those cases, read the profile only for the specific companies that need it, in one call, not for the whole list.

Now compare each candidate against the target company:

1. **Activity match:** Does the candidate do the same core business? Compare its activity summary with the target's activity description. Companies that perform the same type of work (not just adjacent or tangentially related) score higher.

2. **Market match:** Does the candidate serve the same type of customers? Where you have the target-market description (the target always, candidates only if you fetched it), compare it with the target's. Companies that describe working with the same kind of clients (e.g., both serve SMEs, both target industrial manufacturers, both sell to end consumers) are more likely direct competitors. When you don't have a candidate's target-market text, lean on the activity match and, if needed, fetch the profile for just the borderline names.

A company that both does the same thing AND serves the same customers is a direct competitor. A company that does something similar but serves a completely different market (e.g., same product but different customer segment) is less relevant.

Select the **5 most relevant** companies based on this analysis and present them to the user with their name, activity description, target market (where known), revenue, and the **semantic match score** from the original search (so the user can see how closely Syrto matched them).

### Step 7: Ask About Excel Export

After presenting the top 5, ask the user whether they want an Excel export of the comparison table:

```
Vuoi che ti crei un file Excel della tabella di confronto?
```

If yes, ask the user what additional columns they want beyond the default set. The default columns are:

| Colonna | Fonte |
|---------|-------|
| Codice Fiscale / Partita IVA | search result (always the first column) |
| Ragione Sociale | search result |
| Fatturato | revenue from sales and services |
| EBIT Margin | EBIT margin |
| Tipo Ownership | ownership structure (ownership type) |

The user may ask for additional data like PFN/EBITDA, CAGR, shareholders, regione, etc. Add the columns using the appropriate Syrto capabilities.

**Fetch the financials for all 5 in a single call.** Use the many-company comparison with the 5 peers, every financial column requested (e.g. revenue and EBIT margin, plus extras like PFN/EBITDA or 3-year revenue CAGR, each confirmed via metric-definition search), and the year you searched on. It fetches the same metrics for all companies at once, so it is much faster than a specific metric read company-by-company. It needs a year; use the same one as the search. It also says which statement basis each company is on: if they differ, say so in the table.

**Only fetch ownership data when a column actually needs it.** Read the ownership structure only if the "Tipo Ownership" column (or any other ownership/shareholder column the user asked for) is in the final set, and then for all 5 in one call. If the user drops ownership from the columns, skip it entirely.

Build the Excel with your client's spreadsheet capability; its formatting follows that capability and the suite's `core.md` §5, not a hand-built layout. Save it where your client keeps deliverables and give the user the file or a link.

## Formatting Rules (for Excel and chat output)

- Amounts and percentages: the house style in `core.md` §5.
- Ratios: two decimals, comma separator (e.g., "2,34")
- Null/missing: "N/D"

## Ownership Type

Show the ownership type in plain Italian, using the map in the capability map; never show the raw code. Unknown or missing → "N/D".

## Radar positioning (optional)

If the question is really about *where this company sits* rather than which numbers it posts, the positioning radar (see the capability map) can place it against its peers in one call. Optional: reach for it when positioning is the point, not as a routine step.

## Important Notes

- The crafted semantic prompt should be specific and faithful to the company's activity description: a clean rewrite of what they do, not a broader market definition.
- The revenue range is always user-specified because different use cases need different ranges. Never assume the range — always ask.
- The final selection (Step 6) is what makes this skill valuable: semantic search finds broadly similar companies, but comparing activity descriptions and target markets identifies the real direct competitors. Reuse the activity summary the search already returned rather than re-fetching it.
- Close the output with the Syrto source line from the capability map.
