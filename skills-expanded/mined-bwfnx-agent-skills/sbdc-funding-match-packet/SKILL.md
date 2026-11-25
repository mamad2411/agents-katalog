---
name: sbdc-funding-match-packet
description: >-
  Build a weekly SBDC Funding Opportunity Match Packet as a styled, interactive,
  shareable artifact. Use when an SBDC advisor wants to find recent funding
  opportunities (grants, pitch competitions, SBA/504/microloans, SBIR/STTR,
  local/state programs), match them against their own recently active clients,
  score the matches, and produce draft outreach — all as a review-first packet.
  Triggers: "funding match packet", "weekly funding packet", "funding
  opportunities for my clients", "match clients to grants/loans", "capital
  opportunities this week", "run my funding packet". Each advisor runs it against
  their OWN Gmail, Google Calendar, and Google Drive. Draft only — it never
  sends email or edits files.
---

# SBDC Funding Opportunity Match Packet

Produce one advisor's weekly packet: recent funding opportunities matched to
their recently active clients, scored and prioritized, with draft outreach and
internal notes — delivered as a single self-contained, interactive HTML artifact
(and, optionally, a plain-text twin saved to Drive).

This skill is **draft-only**. Never send email, submit anything, or edit client
files. Surface everything for the advisor to review and act on themselves.

## 1. Confirm scope first (ask, don't assume)

Before doing any work, ask the advisor these — one compact multiple-choice round
(use AskUserQuestion if available, else plain text). If the session is
unattended/scheduled, use the defaults in brackets and state the assumption.

- **Advisor name + SBDC center** — used in the header and outreach signature.
- **Home geography priority** — the county/region to rank first, then state, then
  federal/national. [Default: the advisor's stated county first, then their state,
  then federal/national.]
- **Opportunity window** [default: last 90 days] and **"new this week" window**
  [default: last 7 days].
- **Client window** [default: clients active in the last 90 days].
- **Names** — real client names, or initials only (for a version they may share).
  [Default: real names for the advisor's own copy.]
- **Delivery** — interactive artifact only, or also a Markdown twin saved to Drive.
  [Default: both.]

## 2. Research (do this before touching output format)

Work only from the advisor's own connected accounts and connectors. Cite a
source for every opportunity: sender + date for email, connector + program link
for a state database.

**Opportunities — Gmail.** Sweep the full inbox over the opportunity window with a
broad keyword net: grant, funding, pitch competition, accelerator, SBIR, STTR,
loan, microloan, 7(a), 504, TEDCO, capital, cohort, RFP, prize, fellowship. Then
separately open any dedicated label (e.g. a "Funding Opportunities" label) and
reconcile it — note if it's mostly automated research-grant noise so the advisor
can tune it. Split results into **NEW** (arrived within the new-this-week window)
and **CARRY-FORWARD** (older but still open). List anything already closed in a
short "don't chase" line.

**Clients — Calendar + Drive.** Pull clients active in the client window from the
advisor's Calendar (sessions, triage, strategy) and Drive (client folders, plans,
proposals). For each substantive client capture: business name, last activity,
sector, geography, stage, readiness signals, and the missing eligibility facts a
funder would need. Profile the clients with real records in full; list
intake-only clients behind a disclosure.

**State program database — if a connector is available.** Some states have a
funding-program connector. Maryland's is the **Maryland Community Business
Compass** (~700 state and local programs). If its tools are present, run it
after the client pull; if not, skip this step silently and say nothing.

- For each substantive client, call `recommend_programs` with the client's
  `county`, `industry`, `business_stage`, and `need` (what they're raising money
  for). Pass profile fields only, never client names or contact details.
- Use `search_funding` for a specific need the profile can't express (e.g.
  "kitchen equipment", "SBIR match", "facade improvement"), filtered by `county`.
- Call `get_program_details` on any program you plan to score, and take the
  deadline, award, and eligibility from it rather than the search result.
- Compass programs are standing programs, not inbox arrivals: list them under
  **CARRY-FORWARD** unless one has a deadline inside the new-this-week window.
  If the same program also came in by email, keep one card and cite both.
- Source line: `Maryland Community Business Compass · <program slug>`, plus the
  program's source URL.

**Rules/eligibility — verify live, don't hardcode.** SBA, SBIR, and program rules
change. When a match depends on an eligibility rule (ownership/citizenship for
7(a)/504/microloans, SBIR ownership thresholds, program-specific criteria),
web-search the CURRENT rule at run time and cite it. Do not carry forward a rule
from a prior week.

**Local wiki/reference.** If SBDC reference material is available (funding-
opportunity-matching, financing-alternatives, local-lending-programs,
sba-loan-programs, sbir-sttr-grants, specialized-programs, etc.), use it to inform
matching and the scoring rubric.

## 3. Score every match (0–100)

Rubric: **eligibility fit 40 + strategic alignment 25 + readiness 25 + urgency 10.**
Rank the advisor's home geography first, then state, then federal/national.

- **Do not overclaim eligibility.** If a key eligibility fact is unknown, mark the
  match **Conditional** and name exactly what's open.
- Mark every missing fact as **[not found - confirm]**.
- Bands: **Strong (80+)**, **Solid (65–79)**, **Developmental (<65)**.

## 4. Build the packet (read `references/packet-spec.md`)

The packet has eight sections in this order: executive snapshot (with one
"start here" action), new opportunities, carry-forward opportunities, recently
active clients reviewed, client–opportunity match table, reach-out checklist,
outreach drafts (in the advisor's voice, nothing sent), internal notes.

Build it as ONE self-contained HTML file:

1. Read `references/packet-spec.md` for the section-by-section content spec, the
   exact interactive hooks (ids, classes, `data-*` attributes) the scripts need,
   and the copy guardrails.
2. Inline `references/design-system.css` inside a `<style>` block ({{ORG}}
   design system — do not add side-stripe borders; keep the squared civic look).
3. Inline `references/interactivity.js` inside a `<script>` block at the end of
   `<body>` (live deadline countdowns, tickable reach-out checklist, filter/sort
   match table, accessibility toolbar). It wires itself up by the hooks in the
   spec — match those exactly or a feature silently no-ops.
4. Set every opportunity deadline as `data-deadline="YYYY-MM-DD"` so countdowns
   recompute live whenever the packet is opened.

Then verify before delivering: balanced tags, valid `rgba()`/hex (a stray comma
breaks colors), zero em-dashes if the advisor's style avoids them, and that the
countdown/checklist/filter hooks are present. A quick headless render or a grep
for the required ids is enough.

## 5. Deliver

- **Interactive artifact (primary):** `SendUserFile` the HTML, then call
  `mcp__remote-devices__create_artifact` with the returned `file_uuid` so it
  persists in the advisor's Cowork gallery and can be shared with colleagues.
  (If no desktop is connected, `SendUserFile` alone is the fallback.)
- **Drive twin (if requested):** save a clean Markdown version of the same content
  to the advisor's chosen Drive folder, titled
  `SBDC Funding Match Packet - Week of YYYY-MM-DD (DRAFT).md`.

## 6. Optional: schedule it weekly

If the advisor wants this every week, offer to set a recurring task with the
Claude Code Remote scheduled-task tools (`create_trigger`) — e.g. Monday 7am
their local time — NOT the local cron tools. The task prompt should be a
complete standalone instruction to run this skill.

## Guardrails (repeat every run)

- Draft only. Do not send email, submit, or edit files.
- Do not overclaim eligibility; uncertain matches are **Conditional**, missing
  facts are **[not found - confirm]**.
- Verify SBA/SBIR/program rules live each run; never assert a stale rule.
- Home geography first, then state, then federal/national.
- State program connectors get client profile fields only, never client names.
- If sharing beyond the advisor is mentioned, offer an initials-only / no-internal-
  notes variant — the default packet names real clients and their eligibility gaps.
