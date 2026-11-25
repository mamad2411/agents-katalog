---
name: add-on-finder
description: >
  Buy-and-build screener: finds bolt-on / add-on acquisition targets in Italy for a starting
  company or a portfolio, using Syrto. Surfaces similar or complementary companies smaller than
  the starting company, favours geographic proximity, sets distressed ones aside and, by default,
  focuses on family-owned targets whose beneficial owners average over 65 (a succession signal).
  Trigger on "add-on", "bolt-on", "buy and build", "trova add-on per [azienda]", "chi posso
  comprare partendo da [azienda]", "target di acquisizione per [azienda]", "crescere per linee
  esterne", "aziende da aggregare alla piattaforma", or any request for smaller similar companies
  to acquire starting from a company or portfolio. Not for a sell-side buyer universe (use
  buyer-list), a peer or competitor list (use syrto-comparables), or sales prospects (use
  prospects-scout).
---

# Add-on Finder

Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, output, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`: which tool answers each capability, and the metric slugs). If an upstream `SYRTO-HANDOFF` exists, reuse its ids and data before calling Syrto (core §8).

Find **bolt-on / add-on acquisition targets** on the Italian market for a **starting company** (buy-and-build logic): starting from the starting company's own business, surface **smaller, similar or complementary companies** that the starting company could acquire and integrate to grow by external lines.

Syrto is the **exclusive** source for discovery, ownership and financials. Deliverables (Excel and report) are in **Italian** by default; converse in the user's language (core §1).

## What makes a good add-on (the default thesis)

An add-on is not just "a similar company" — it must be **acquirable and integrable**. The defaults below encode that. State them back to the user and let them confirm or override at the start of every run (see Step 0):

1. **Similar / complementary business** — the core of the search. Found via Syrto semantic company search built from the starting company's own activity description (competitors and adjacent players, *not* Ateco codes).
2. **Smaller than the starting company** — a bolt-on, not a merger of equals. Default gate: target revenue **below the starting company's** (a sensible default band is roughly 5%–60% of the starting company's revenue; adjust per user). A company the same size or larger is not an add-on — flag it as a "fusione tra pari", don't put it in the main list.
3. **Geographic proximity preferred, not mandatory** — same region / macro-area eases integration and synergies, so proximate targets rank higher, but a strong out-of-region fit still qualifies.
4. **Not in serious financial distress** — financial health is *not* the selection driver, but companies in real crisis (e.g. persistently negative EBITDA, negative equity, very high leverage / clear distress signals) are **de-prioritized**, not silently dropped: they go to a separate "Da valutare con cautela" list with the reason.
5. **Family-owned with an ageing owner (succession signal) — default focus.** By default prioritise **family-owned** targets whose **average beneficial owner age is over 65**. An old family owner without an obvious successor is a classic exit signal — exactly the target most likely to sell. This is a **default, not a hard requirement**: the user can widen it (all ownership types, no age filter) at the start.

**Crucial behavioural rule:** if the user does **not** specify the criteria, do **not** guess silently. First **state explicitly** what you would search for (the five points above, with the concrete thresholds you'd apply), then ask the user to **confirm or adjust** before running the search. This mirrors how the user works: propose the sensible default, let them correct the aim.

## Two input modes

- **Single starting company (default):** the user gives one company (name or tax id) as the starting company/seed. Its own Syrto business description drives the semantic search; its own revenue sets the "smaller than" gate.
- **Portfolio:** the user gives a **list** of companies that together represent a portfolio (e.g. a fund's holdings, or a group's operating companies). Treat the portfolio as the starting company: build the semantic query from the **union** of the portfolio's activity descriptions (search per-company and merge results, de-duplicated), and set the "smaller than" gate against the **largest** portfolio company (or per-company if the user wants add-ons mapped to each holding). Always **exclude the portfolio companies themselves** from results.

## Syrto data notes (why the search is built this way)

- The owner-age filter of the company search works on the **average** age of the beneficial owners. That is exactly this skill's default (average over 65), so it goes into discovery.
- Ownership type (family, family-owned group, industrial group, financial owner, other) is also a company-search filter, one value per search: the family default plus a family-group widening means two searches, merged.
- Both filters keep only companies that have a value, so a company whose owners are not disclosed never enters the pool. Say so in the counts (Step 5).
- Location filters match the registered headquarters. The company search can also filter by where a company has a registered branch, for "has a site in X".
- Show ownership types by their Italian labels from the capability map, never the raw code.

## Workflow

### Step 0 — Understand the starting company & confirm criteria

1. **Locate the starting company(ies).** Resolve each seed by name or tax ID. If ambiguous, ask the user which match.
2. **Pull the starting company profile.** Read its company profile (activity, target markets, HQ region) and its financial analysis (one call: revenue, EBITDA and the latest filed year, which sets the size gate). For a portfolio, read the profiles in one multi-company call and compare the holdings' revenue and EBITDA in one comparison.
   - If the activity or target-market description is missing (common for small companies), fall back to the company's website from its profile or a web lookup, confirm the site with the user, and write the missing description in Syrto's concise style before proceeding.
   - If the starting company is a holding or a group platform, its individual accounts can be near-empty and the "smaller than" gate would collapse. Propose its consolidated figures for the gate in the confirmation below and record the basis in the Riepilogo; targets stay on their own individual accounts.
3. **Craft the semantic query** from the activity description(s) — a precise, faithful rewrite of what the starting company does. Keep it specific to the real business; don't broaden into an unrelated market.
4. **State the criteria and get confirmation.** Present, in Italian, exactly what you'll search for and ask the user to confirm or change:
   - la query semantica (mostrala) e la soglia di pertinenza (default **0.8**, lo stesso default della ricerca Syrto);
   - **dimensione**: target più piccoli dell'azienda di partenza — proponi la banda di fatturato (default ~5%–60% del fatturato dell'azienda di partenza), da confermare;
   - **geografia**: stessa regione/area preferita ma non obbligatoria (di default nessun filtro rigido, solo bonus nel ranking) — chiedere se vogliono restringere;
   - **proprietà**: di default **solo familiari**; chiedere se aprire a tutte;
   - **età titolare effettivo (media)**: di default **> 65** — chiedere se togliere/cambiare la soglia;
   - **salute finanziaria**: le aziende in forte crisi vengono de-prioritizzate (non escluse) → lista "Da valutare con cautela";
   - **anno di riferimento**: proponi l'ultimo anno depositato dall'azienda di partenza. Tutte le soglie e i KPI usano questo anno, e i target che non l'hanno ancora depositato non entrano nella ricerca;
   - **base di bilancio**: bilanci individuali, salvo il caso holding descritto sopra.

   Ask with a structured choice if your client offers one, otherwise a short numbered question. Only proceed to Step 1 after the user confirms (or adjusts).

### Step 1 - Discovery (semantic company search)

Build one semantic company search with:
- the description query from Step 0 and the confirmed relevance cutoff (default 0.8);
- the owner-age filter (beneficial owners' average age, minimum 65) when that default is on;
- the ownership-type filter set to family when that default is on. If the user also wants family-owned groups, run a second search with that value and merge; if they open to every ownership type, leave the filter out;
- a filter on revenue from sales and services with the confirmed band (max below the starting company, and the confirmed min), on the confirmed reference year;
- geography only if the user chose to restrict it; otherwise leave geo open and use proximity only as a ranking bonus.

Run searches one at a time (core §6). Page through the results until the pool is large enough that ~15–25 will survive (gather somewhat more, e.g. 40–70). For each candidate keep its **semantic match score** (it feeds the Add-on Score), its revenue for the reference year, its ownership type and its owners' average birth year: discovery returns them when you filter on them, so later steps don't re-fetch them. **Always exclude the starting company / portfolio companies themselves.**

**Portfolio:** if targets will be mapped to each holding, run one search per holding, because the match score doesn't say which of several descriptions a company matched. Otherwise the company search accepts several alternative descriptions in one call (the capability map gives the limit), which also removes duplicates for you.

Widen the net (if too few survive) by **reformulating the query** toward adjacent activities, or by adding them as alternative descriptions, not by dropping the cutoff below 0.8 unless the user agrees.

### Step 2 — Screening (L1, cheap): size confirmation

The revenue band is already enforced by the discovery filter, and each discovery result carries its revenue for the reference year, so this step needs no extra calls. Record that revenue and its ratio to the starting company for the output. Nothing larger than the starting company reaches this point; if the user wants to see near-equals too, run discovery once without the upper bound and list the companies above it as "fusione tra pari", outside the main list.

### Step 3 — Ownership & succession enrichment (batched)

Ownership type and average owner age are already filtered **upstream in discovery** (Step 1), and discovery returned both for every candidate, so this step no longer gates on them: it adds the top owners and the successor flag.

For the survivors, read the ownership structure in multi-company calls rather than one company at a time (the capability map gives how many fit one call). A multi-company read shows only each company's largest few owners and officers, and its warning says when a list was cut: when the successor question matters for a top target and its list was cut, read that company alone.

For each company:
- **Ownership detail:** record the top owner(s) for the output. The family/type filter already ran in discovery; no re-gating here.
- **Age context:** record the top owner(s) and their age for the output and note whether a **potential successor** exists (a younger same-surname owner) as useful colour. This is not a gate, just enrichment.
- **Null handling:** ownership/age unresolved (null shares, holding on top, age not disclosed) → route to **"Da verificare"** with the reason, don't drop silently. A list cut short in a multi-company read is not unresolved: read that company alone first.

### Step 4 — Add-on scoring & financial-health check (L2, on survivors only)

For every in-target company, pull the overview. The financial KPIs are the bulk of the work here, so fetch them in bulk rather than company by company:
- **KPIs:** compare the survivors in multi-company comparisons on the reference year: Fatturato, EBITDA, Margine EBITDA %, crescita/CAGR, PFN e leva (net debt / EBITDA). Take the metric slugs from the capability map and confirm them with metric-definition search, as the map asks: an unknown slug returns no data for that metric. Read the comparison's warning before building the table: it names every company or metric that came back empty. **Label the year in the output.** Every survivor passed a revenue filter on that year, so each one has that year's filing.
- **Profile:** read the survivors' company profiles in multi-company calls: legal name, tax ID, sector/NACE, sede, activity and target-market descriptions.
- **Sector benchmark:** where the automatic benchmark genuinely helps the health read, the single-company financial analysis with its automatic benchmark is still fine, but use it as a follow-up on notable cases, not as a per-company loop, since the comparison already covers the KPIs.

Then compute a transparent **Add-on Score (0-100)**. It is this skill's own acquisition score, distinct from the commercial Fit Score in core §4, so core's fixed-weight and no-breakdown rules do not apply here. Explain the weighting to the user; don't present it as a black box. Suggested default weights (tunable): **Similarità di business 40**, **Dimensione 20**, **Segnale di successione 20**, **Prossimità geografica 10**, **Salute finanziaria 10**. See `references/scoring-output-formatting.md` for what each weight captures.

Flag distress explicitly (persistently negative EBITDA, negative equity, leverage clearly out of line) → caution list with the reason. Distress de-prioritises, it does not auto-exclude.

### Step 5 — Validation preview in chat (BEFORE any file)

Do **not** build the Excel straight away. First show the ranked in-target companies **as a table in the chat** so the user can validate: Azienda, Attività (sintesi), Regione, Fatturato, EBITDA, Titolare effettivo (età media), Proprietà, Add-on Score, razionale in una riga. Below it, state the parameters used (query, soglia di pertinenza, banda dimensione, geo, soglia età, proprietà, anno, base di bilancio) and the counts (candidati screenati, in target, in "Da valutare con cautela", in "Da verificare"). Add one line saying that companies with no data on ownership type or owner age are not in these counts, because the discovery filters keep only companies that have a value.

Then **ask the user to confirm**, with a structured choice if your client offers one (e.g. Confermo / Modifica criteri / Stop), otherwise a short numbered question. Only after explicit confirmation proceed to Step 6. If they want changes (different band, wider ownership, different query), re-run the relevant steps first.

### Step 6 — Output (only after confirmation)

**Default deliverables: produce BOTH an Excel and a readable report — always, without asking.** The Excel is the data/scanning tool; the readable report is the presentable version of the same analysis, rendered per `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (not hand-built). Build the Excel first (with your client's spreadsheet capability), then the readable report from the same data so the two never diverge.

→ **Before building the output, read `references/scoring-output-formatting.md`** for the full Add-on Score weighting rubric, the Excel tab/column specs (Add-on Target, Da valutare con cautela, Da verificare, Riepilogo), the readable-report structure, the number formatting, the ownership labels, and the efficiency & robustness checklist.

## Optional helpers

- **Follow an owner:** when an owner or family holding looks worth following, find the person to see the other companies they own or run. That can reveal a family group or a second target. Resolve those companies by tax ID before using them.
- **Proximity beyond the HQ:** registered branches can sharpen the geographic-proximity component of the Add-on Score. They are registry records, not proof of an operating site, a plant or a territory, and an empty list is not evidence of a single-site business. If the user wants "has a site in the region", use the branch-location filter of the company search in discovery.
- This suite never buys contacts.

## Important notes

- Syrto is the exclusive source for discovery, ownership and financials — do not substitute web guesses (web is only for filling a missing activity description, confirmed with the user).
- **The five criteria (similar · smaller · proximate · not distressed · family + ageing owner) are defaults, not laws.** If the user hasn't specified them, state them and ask for confirmation before searching; if they widen or drop any, honour that and record what was used in the Riepilogo.
- **Always validate in chat first (Step 5), build files only after the user confirms.**
- The Add-on Score is a decision aid: always show its weighting so the user can trust and tune it.
- Close the deliverables with the source line from the capability map.

---
_Fonte dati: Syrto_
