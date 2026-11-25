---
name: conference-watch
description: >-
  Watch and report on upcoming AI/ML conferences: submission deadlines (every
  stage), dates, location, special sessions / calls for papers, official links,
  and a 5-year acceptance-rate trend. Use when the user asks about future AI
  conference deadlines, wants to plan submissions, compare venues, or track a
  set of conferences by area/reputation/difficulty. Works in any agent that has
  a web-search / web-fetch capability (Claude Code, Codex, etc.).
license: MIT
metadata:
  version: 0.0.1
---

# ConferenceWatch

Produce an accurate, well-sourced snapshot of the AI/ML conferences a user cares
about — with **every submission deadline stage**, dates, location, special
sessions / CFP, official links, and a **5-year acceptance-rate trend**.

Two artifacts are always produced:
1. A JSON dataset (one object per conference) — the structured source of truth.
2. A human-readable Markdown report with a short summary.

---

## Guiding principles

- **Never invent dates.** A deadline goes into the JSON only if you found it on
  an official/authoritative source. If you infer from historical patterns, mark
  it `approximate` and say so explicitly in the report.
- **Cite everything.** Every edition and every acceptance-rate number carries a
  `source_links` entry. Prefer official conference sites and CFP pages; use
  aggregators (see references) as leads, then confirm on the official page.
- **Timezones matter.** Record the raw deadline text (e.g. "May 22, 2026 AoE").
  Most AI venues use **AoE (Anywhere on Earth, UTC-12)**. Keep the AoE flag.
- **Today is the anchor.** Use the current date to decide which edition is
  "upcoming" vs "past". Do not assume the model's training-cutoff year.

---

## Workflow

### Step 0 — Establish the anchor date
Determine today's date (from the environment/context). All "future vs past"
decisions are relative to it. State the anchor date in the report metadata.

### Step 1 — Analyze input & narrow the scope
Parse the user's request for any of these filters:
- **Area / topic** — e.g. NLP, CV, ML theory, RL, robotics, HCI, systems,
  data mining, speech, multimodal, AI4Science.
- **Reputation / tier** — CORE rank (A*/A/B) or "top-tier only".
- **Difficulty** — proxied by acceptance rate (e.g. "only <25% venues").
- **Named conferences** — if the user already lists venues, skip to Step 2.
- **Region / timing** — e.g. "conferences with deadlines in the next 6 months",
  or "held in Europe".

If the request is under-specified, **ask 1–3 concise follow-up questions** to
narrow it (offer sensible defaults so the user can decline easily). Example:

> To focus the search, which of these should I use?
> 1. **Area** — all AI, or a subfield (NLP / CV / RL / …)?
> 2. **Tier** — top-tier (CORE A*) only, or include A/B venues?
> 3. **Horizon** — only deadlines in the next N months, or the full year?
> (If you'd rather not specify, I'll default to the top AI venues across areas.)

**Default when the user declines or doesn't answer:** the top general AI venues
plus the leading venue(s) for any area they mentioned. See
[references/conference-catalog.md](references/conference-catalog.md) for the
curated tier list to draw from.

### Step 2 — Build the initial conference list (initial JSON)
From the filters, assemble the candidate list and **write the initial JSON**
using the schema in [references/json-schema.md](references/json-schema.md) and
the template [assets/conference-data.template.json](assets/conference-data.template.json).
At this stage only `metadata` + conference names/areas/tier need to be filled;
edition/deadline/trend fields are placeholders to fill in Step 3–4.

Confirm the list with the user briefly ("I'll investigate these N conferences:
…") before the (potentially long) search phase, unless they asked you to just
go.

### Step 3 — Research each conference: the UPCOMING edition first
For each conference, search for the **next (future) edition** relative to the
anchor date. Query patterns that work well:
- `"<CONF> <year> call for papers"`, `"<CONF> <year> important dates"`,
  `"<CONF> <year> submission deadline"`, `"<CONF> <year> paper deadline"`.
- Then **open the official site / CFP page** to confirm; aggregators can be
  stale or wrong.

When exact info is found, record in the conference's `upcoming_edition`:
- `year`, `location` (city, country; note if virtual/hybrid), `venue` if known.
- `dates`: conference start/end.
- `deadlines`: **every stage** — abstract registration, full paper, supplementary,
  rebuttal, author response, notification, camera-ready, workshop/tutorial
  proposals, etc. Keep the raw text + AoE flag + `confirmed: true`.
- `special_sessions`: special tracks, new-this-year themes, datasets & benchmarks
  track, position papers, findings, industry track, journal-to-conference, etc.
- `call_for_papers_url` and `website`.
- `data_confidence: "confirmed"` and `source_links`.

If no future edition is announced yet, leave `upcoming_edition.data_confidence`
as `"approximate"` and fill it via inference in Step 4.

### Step 4 — Historical anchor: last 5 editions → trend + inference
For each conference, gather the **last 5 editions** (most recent past years):
- Populate `acceptance_rate_trend` with `{year, submissions, accepted,
  acceptance_rate, source}` per year — as many of the 5 as are available.
- If the upcoming edition's deadlines were **not** found in Step 3, **infer**
  the approximate deadline window from the historical pattern (e.g. "abstract
  deadline has fallen in the third week of May for the last 4 years → est.
  ~mid-May <next_year>"). Write these into `upcoming_edition.deadlines` with
  `confirmed: false` and set `data_confidence: "approximate"`. **Always flag
  inferred dates clearly** in both JSON and report.

### Step 5 — Finalize JSON
Write the complete JSON to `conferences.<anchor-date>.json` (or a path the
user specifies). Validate it against the schema: every conference has a name,
tier, website; every deadline has a stage + confirmed flag; every trend/edition
row that carries data also carries a source link.

### Step 6 — Produce outputs
1. **Answer directly** in chat: a compact table or list of the most
   time-sensitive items (nearest deadlines first), plus the short summary.
2. **Write the Markdown report** using
   [assets/report.template.md](assets/report.template.md):
   - A 3–5 sentence **summary** synthesizing what you found (nearest deadlines,
     notable new tracks, acceptance-rate direction).
   - A per-conference breakdown (deadlines table, location, special sessions,
     links, acceptance-rate trend).
   - A clearly-labeled **"Approximate / inferred"** section for anything not
     confirmed.
   - A **Sources** list.

---

## Output file naming
- Data: `conferences.<YYYY-MM-DD>.json`
- Report: `conference-report.<YYYY-MM-DD>.md`
(Use the anchor date so successive runs are comparable / diffable.)

## Quality checklist before finishing
- [ ] Anchor date stated; upcoming vs past decided against it.
- [ ] Every confirmed deadline has a source link; timezone/AoE captured.
- [ ] Inferred/approximate items are flagged in **both** JSON and report.
- [ ] Acceptance-rate trend covers up to 5 recent years with sources.
- [ ] JSON validates against the schema; report summary written.
- [ ] Missing data is shown as `null` with a note — never fabricated.
