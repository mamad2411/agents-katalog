---
name: briefing
description: >
  Prepare a conversation: a fast, compact commercial briefing on the companies the user is
  about to meet, lighter and quicker than company-analysis. Two input modes: (a) CALENDAR, the companies in a day's external
  meetings when a calendar connector is available, also run by the scheduled daily briefing;
  (b) SPOT, one or more named companies. Combines Syrto data (anagrafica, struttura, analisi
  finanziaria, Fit Score) with web intelligence on person, services and relevant news (deal,
  M&A, investimenti), then talking points. Trigger: "briefing di oggi", "briefing di domani",
  "prepara le call", "profila le call di oggi" (calendar) and "briefing di [azienda]",
  "briefing compatto su X", "prepara la call con X", "prepara il meeting con X", "brief me on
  today's meetings", "prep my call with X" (spot), or a scheduled run. Se l'azienda non è su
  Syrto, produce comunque un profilo web-only. Not for a plain question about the agenda, or
  for deciding on a company and documenting it (use company-analysis).
metadata:
  version: "2.0.0"
---

# Briefing (fast lane)

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`). Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill. Calendar mode needs a calendar connector (whichever the user has connected, e.g. Outlook or Google Calendar); without one, see "Without a calendar, or without anyone to ask".

This is the **fast lane** — a quick, compact commercial profile, lighter than `company-analysis`.
Use it to prepare a conversation (a call or a meeting). When the user needs to decide on a company
and document it, route to `company-analysis` (its **taglio commerciale** dial gives the same
commercial reading in a richer report).

## Input modes
- **Calendar** — profile the companies in the day's meetings for a target date (auto, and schedulable as a routine via `/setup-briefing`). Triggers: "briefing di oggi", "prepara le call", "profila le call di oggi", or a scheduled task.
- **Spot** — one or more named companies, no calendar. Triggers: "briefing di [azienda]", "briefing compatto su X", "prepara la call con X". Skip Steps 1–2 (calendar) and go straight to Syrto + web enrichment for the named company; ask the meeting person's name only if relevant and not given; produce a single card.

## Without a calendar, or without anyone to ask
- **No calendar connector available**: say so in one line and switch to spot mode (ask which companies the user is meeting). In a scheduled run, stop with that line rather than guess the meetings.
- **Scheduled run**: nobody is there to answer, so ask nothing and offer no choices. Use the defaults in this skill, list any assumption in the chat digest, and produce the HTML only; the PDF can be offered in the next conversation.

## Read your context first

Read the seller's context (core §3), never from a hardcoded file:
- **commercial context** — what the user sells, ICP / target, products-services catalogue,
  target revenue band, spend hook + capture rate, exclusions. Serve per generare i talking
  points e la logica "cosa proporgli" coerente con `company-analysis` (taglio commerciale).
- **profile** — tone and numeric depth (calibration of the deliverable).

If a needed field is missing, **proceed with a lighter briefing** (company read + web
intelligence, generic talking points) and note the gap **once**, inviting the user to complete
their saved profile. Do not invent products, ICP or pricing.

## Workflow

### Step 1 — Read the calendar (calendar mode only)

Read the day's meetings from the user's connected calendar (e.g. Outlook or Google Calendar) using its calendar search/list tool, for the **target date**:
- Scheduled run → the date its saved prompt names (`setup-briefing` writes it: the **next working day** for an evening run, **today** for a morning run; after a Friday the next working day is **Monday**).
- Manual run (`/briefing-now`, or "briefing di oggi") → **today** (unless a different date/argument is given)

The target date comes from the request or from the command that invoked the skill; if absent, default = today. In **spot mode** (a named company is given), skip this step.

Keep only meetings with **external participants** (the user's own domain is internal).
Infer the internal domain from the profile / commercial context (or the organizer's
address); do not hardcode a specific company domain.

### Step 2 — Extract company and person from each meeting (calendar mode only)

For each meeting, extract:

**Company name** — parse the subject with these patterns (in priority order):
1. `"<Host> <> NomeAzienda"` (host = the user's company, from the profile)
2. `"<Host> x NomeAzienda"`
3. `"Meeting con NomeAzienda"` / `"Call con NomeAzienda"` / `"Intro NomeAzienda"`
4. `"NomeAzienda — topic"` or `"NomeAzienda | topic"`
5. **Fallback**: take the email domain of the first external participant, strip the TLD,
   capitalize → candidate company name. Personal-mail and PEC domains (gmail, outlook,
   hotmail, libero, icloud, pec.it and similar) name no company: mark the meeting "azienda non
   identificata" instead of looking the domain up.

**Person name** — the display name of the first external participant on the invite. If absent,
use the email prefix (nome.cognome → Nome Cognome).

**Time and type** — start time, duration, and whether it is a first call or follow-up (subject
keywords: "intro", "demo", "follow-up", "allineamento", "recap").

Build a list of meeting objects:
```
{ ora, durata, tipo, nome_azienda, nome_persona, email_persona, subject_originale }
```

### Step 3 — Syrto enrichment (per company)

Follow the robustness and efficiency rules in `core.md`.

For each unique company:
1. **Resolve the company** by name, or by tax ID when a P.IVA/CF is available (unambiguous).
2. If found:
   - **Company profile** → sede, ATECO, real activity, sito, dimensione, dipendenti, mercato di riferimento (the business model comes from here, never the web).
   - **Financial analysis with its automatic benchmark** → the pre-grouped read (profitability, liquidity, solvency, structure + radar + 2-year trajectory), each metric set against companies of the same sector class and size band in the company's area. It does not carry the spend-hook cost line or net worth: read those two with a specific metric read.
   - **Ownership structure** → tipo di controllo, soci, titolari effettivi — quando conta per capire chi controlla il budget (gruppo / holding).
3. If **not found** on Syrto → mark `syrto_missing: true` and proceed web-only (Step 4).

### Step 4 — Web enrichment (per company/meeting)

Three web searches per meeting, with your client's web search (web adds commercial colour only; it never
classifies the business or judges the finances):

- **4a. Person** (calendar mode / when a person is known) — query `"Nome Cognome" "Nome Azienda"`: current role, seniority, professional
  background, public statements/articles/events. Synthesize in 3–5 lines. Professional information only, nothing about private life.
- **4b. Company services (detail)** — query `"Nome Azienda" servizi OR services OR solutions`:
  which practices, industries, deliverables. If Syrto has the activity overview, use it as the
  base and enrich; if the company is not on Syrto, this is the primary source.
- **4c. News & deals** — query `"Nome Azienda" news OR acquisizione OR M&A OR deal OR investimento OR round`
  (last 12 months): closed corporate-finance deals, acquisitions, funding rounds, strategic
  partnerships. If none, fall back to a sector trend — still a good talking point.

### Step 5 — Fit read (same backbone as company-analysis, taglio commerciale)

For each company found on Syrto, produce the fit read with `core.md`:
the **same Fit Score (0–100)**, the **same spend-capacity estimate** (spend-hook
metric × capture rate from the commercial context) and the **same verdict tier** (Strong fit / Qualified /
Monitor / Out of target / Insufficient data). A company briefed here and later analysed by
`company-analysis` (taglio commerciale) must show the same score and info. Never a bare score — follow it
with the 1–2 sentence narrative naming the main drivers and the main drag. First time a score
appears in a conversation, briefly explain its composition per the method.

### Step 6 — Talking points

For each meeting/company, from all data gathered (Syrto + fit read + web + saved context), produce
3–4 **concrete** talking points:
- **Specific** — tie a Syrto datum or a news item to a concrete need.
- **Product-fit ("cosa proporgli")** — draw on the products/services catalogue in
  the commercial context, the same logic `company-analysis`'s commercial cut uses for its "Cosa proporgli"
  block: map which offering this company is in target for and the hook, tied to a finding
  (growth, margin headroom, leverage, size, supplier base). If no catalogue is saved, skip
  the product mapping (do not invent products) and keep the points generic.
- **Actionable** — what to say, what to ask, which pain point to touch.
Respect exclusions from the commercial context; flag distress signals (negative equity, current ratio < 1,
losses + decline) explicitly even if other dimensions look good.

### Step 7 — Deliverable

Render the briefing as a **formalized deliverable per `${CLAUDE_PLUGIN_ROOT}/shared/core.md`**:
default **HTML** built from the canon tokens (from the saved preferences, core §3, else the neutral
default), then offer the **PDF** ("vuoi anche il PDF?"), plus a **chat digest** carrying the
essentials (meetings/companies, fit verdicts, key talking point) so value lands without opening
the file. Keep it compact — this is the fast lane. Keep the look of core §5 (or the saved brand
canon) rather than inventing a style of your own.

Each meeting/company is one **card** with this content/structure, ordered by meeting time (calendar mode):
- **Person** — name, role, 3–5 line bio from web (or "Profilo non disponibile pubblicamente"). Omit in spot mode when no person is given.
- **Company profile** — ragione sociale, sede, sector/activity, size + employees (from Syrto
  anagraphic), enriched with the web detail on services. If not on Syrto, show a "profilo
  web-only" note and build the profile from the web.
- **Key financials + fit read** — the recent-year figures that matter (e.g. Ricavi + YoY,
  EBITDA margin, D/E, efficiency/size scores, ownership) and the **Fit Score + verdict**
  from Step 5. Omit the financial block entirely when the company is not on Syrto.
- **Web intelligence** — recent news (deals, M&A, investments) or the sector trend fallback.
- **Talking points** — the 3–4 points from Step 6.

Numbers follow the house style in core §5. Use the most recent year the company has filed, and
say which year and statement basis the figures are on.

At the **end** of the deliverable, emit a `SYRTO-HANDOFF` block (per `core.md`,
chain `briefing→company-analysis`) listing the profiled companies with resolved ids,
anagraphic, metrics and the fit result, so downstream skills (`company-analysis`, `outreach-writer`) reuse the same data.

### Step 8 — Save and present

Save the HTML as `briefing-YYYY-MM-DD.html` (the target date) where your client keeps generated
files, share it the way your client allows, offer the PDF (not in a scheduled run), and report in chat: companies/meetings profiled, verdicts, any company not
found on Syrto.

## Edge Cases

**No meetings** (calendar mode): minimal deliverable / chat note — "Nessun meeting con esterni in agenda per la
data. Buona giornata!" — and suggest a spot briefing ("briefing di [azienda]") or `/briefing-now` to profile a specific company. In a scheduled run, produce no file: that one line at most.

**Internal-only meetings**: skip — the briefing is for external calls.

**Cancelled / declined meetings**: skip; include only confirmed or tentative.

**All-day events**: skip (typically reminders, not calls). Include only timed meetings.

**Same company in several meetings**: profile the company once, but show a separate card per
meeting (different people = different talking points).

**Ambiguous company**: if resolving the company returns several candidates and you cannot
disambiguate, prefer the one whose sede + ATECO best fits the context; if still ambiguous, show
the best match with a "Possibile omonimia — verificare" note. When a P.IVA/CF is available,
resolve by tax ID for an unambiguous match.

**Person not findable online**: "Profilo non disponibile pubblicamente"; still show name, email
and any role inferable from the invite.

**Web search fails / times out**: proceed with Syrto data only; note "Ricerca web non disponibile".

## Efficiency

Web searches carry no Syrto cost; every Syrto read counts toward the user's usage, so fetch only
what each card needs.
