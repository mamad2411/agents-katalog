---
name: fe-quarterly-checkin
description: Generate quarterly check-in bullets for an SA or manager at their specific ladder level (L3–L7, M3–M5) by reading their Google Doc template, gathering work signals via Glean, and producing level-appropriate content for each expectation row.
---

# fe-quarterly-checkin

## Purpose
Generate a quarterly check-in for an SA or manager at their specific ladder level by reading their Google Doc template, gathering work signals via Glean, and producing level-appropriate bullets for each expectation row.

**Supported levels:** L3, L4, L5, L6, L7, M3, M4, M5

---

## Step 1 — Collect inputs

Before doing anything else, collect these inputs if not already provided:

**Ask as plain conversational questions** — do NOT use a structured multiple-choice prompt for the Google Doc URL, since it requires the user to paste a URL directly.

| # | What to ask | How to ask | Notes |
|---|---|---|---|
| 1 | **Google Doc URL** — their personal copy of the template | Plain text: "Please paste the URL of your Google Doc check-in template." | Never modify the master template |
| 2 | **Time period** — e.g. `FY27 Q1`, date range, or "current quarter" | Use `AskUserQuestion` with quarter options | Infer dates using the Databricks fiscal calendar (see below) |

**Fiscal calendar:** Databricks fiscal year starts **February 1**. FY27 = Feb 2026 – Jan 2027.

| Quarter | Dates |
|---|---|
| Q1 | Feb 1 – Apr 30 |
| Q2 | May 1 – Jul 31 |
| Q3 | Aug 1 – Oct 31 |
| Q4 | Nov 1 – Jan 31 |
| H1 | Feb 1 – Jul 31 |
| H2 | Aug 1 – Jan 31 |

When the user says "current quarter", calculate the correct FY quarter from today's date using this calendar.

| 3 | **Write-back?** — generate text here only, or also update the doc | Use `AskUserQuestion` with two options: "Display here only" and "Also update the Google Doc" | Default: text only. Do NOT write to the doc unless explicitly requested |

**Do NOT ask for level.** The level is auto-detected from the doc in Step 2.

---

## Step 2 — Read the Google Doc and detect level

Use `google-docs` to fetch the doc. **Ignore any "Instructions" or "How to Use" section at the top of the doc** — this contains setup guidance for the user and is not check-in content.

Scan all headings to find which check-in section exists. Look for headings matching the pattern `FY2x Hx Check-In - <Role Title> (<Level>)`:

| Heading pattern | Level |
|---|---|
| `Check-In - Solutions Engineer (L3)` | L3 |
| `Check-In - Sr. Solutions Engineer (L4)` | L4 |
| `Check-In - Solutions Architect (L5)` | L5 |
| `Check-In - Sr. Solutions Architect (L6)` | L6 |
| `Check-In - Lead Solutions Architect (L7)` | L7 |
| `Check-In - Manager (M3)` | M3 |
| `Check-In - Sr. Manager (M4)` | M4 |
| `Check-In - Director (M5)` | M5 |

**Auto-detection rules:**
1. If exactly **one** check-in section exists with empty "How I Demonstrated…" cells, use that level automatically. Confirm the detected level to the user (e.g., "I detected your doc is for **M4 (Sr. Manager)** — proceeding with that level.").
2. If **multiple** check-in sections exist with empty cells, ask the user which one to fill.
3. If **no** recognized heading is found, ask the user to confirm their level and that the doc uses the standard template.

---

## Step 3 — Gather signals via Glean

Search Glean for the specified time period. Pull the most relevant:

Use Glean MCP to search across the user's activity for the specified time period, including but not limited to:

- Google Docs / Sheets / Slides
- Confluence pages
- Jira tickets and epics
- GitHub PRs / repos (for builder-heavy IC work)
- Slack threads (especially customer, SE, pod, and LT channels)
- Salesforce artifacts (ASQs, opportunity notes) if indexed
- Google Calendar events and meeting transcripts / notes

**For ICs (L3–L7), favor signals such as:**

- POCs, notebooks, demos, design docs, runbooks, customer-facing assets.
- QBR / forecast / customer strategy / architecture review meeting notes where they contributed materially.
- Significant Jira work and PRs tied to customer solutions or reusable assets.

**For managers (M3–M5), favor signals such as:**

- Coverage / org design docs, 2x2 directories, territory / patch plans.
- Risk / optimization trackers, to‑and‑through plans, QBR decks.
- LT / SLT / regional forecast notes, partner exec call notes.
- Hiring / calibration artifacts, interview feedback, performance management or bar‑raising docs.

Treat these as **examples, not hard filters**. Prioritize any artifacts (of any type) where:

- The **scope** is meaningful (team / account / region / segment), and
- The **outcome** clearly maps to one or more of:
  - **Impact**
  - **Complexity**
  - **Influence**
  - **Consumption / execution strategy**
  - **Technical bar**
  - **Leadership / culture**

Ignore low‑signal activity (minor edits, routine admin tasks) even if they match the file types above.

---

## Step 4 — Generate bullets

### Mapping signals into the ladder expectations

After you fetch signals via Glean MCP:

1. **Cluster by theme**
   For each signal, decide which dimensions it best represents:
   - Impact
   - Complexity
   - Influence
   - Consumption / execution strategy
   - Technical bar
   - Leadership / culture

2. **Pick the strongest few per dimension**
   Do **not** try to use every signal.
   Select the 1–3 highest‑impact signals per dimension (scope + outcome) for the quarter.

3. **Map into the correct expectation rows**
   For the user's level, look at the left‑most column in each table (expectations).
   For each row, choose the signals that best fit that expectation and synthesize them into bullets.

4. **Synthesize into bullets**
   For each expectation row you fill, write 1–2 bullets in **third person, past tense** with a link to the source artifact:
   - "Did X (signal), which led to Y outcome for Z scope. [Source](URL)"
   - Never use "I" or "my". Write as if describing the person's contributions.

#### IC levels (L3–L7)

Use IC‑type signals (POCs, notebooks, demos, customer assets, design docs, Jira/PRs, meeting notes):

- **IMPACT / Workstream Ownership / Impact Beyond Immediate Scope**
  Map signals where they independently drove a use case, POC, or asset that changed a customer outcome, enabled a new workload, or created reusable value.

- **COMPLEXITY / Engagement Complexity / Problem Solving**
  Map signals showing multi‑workstream juggling, cross‑domain work (DE + ML + governance), or diagnosing and resolving tricky issues.

- **INFLUENCE**
  Map signals where they shaped architecture, shifted a customer's direction, or aligned AEs/DSAs/PS around a better technical approach.

- **DRIVES CONSUMPTION / EXECUTION STRATEGY**
  Map signals that clearly connect to DBU: workload activation, usage growth, risk/attrition recovery, migrations.

- **TECHNICAL BAR**
  Map signals that show stronger product / cloud / governance mastery or a builder + AI‑first mindset (prototypes, live builds, smart use of AI tools).

- **LEADERSHIP & CULTURE**
  Map signals for mentoring, onboarding, sharing assets, running enablement, or modeling culture principles.

#### Manager levels (M3–M5)

Use manager‑type signals (coverage/org docs, 2x2s, risk trackers, QBR decks, LT notes, partner calls, hiring/performance docs):

- **IMPACT (Team / Organizational Revenue & Consumption Impact)**
  Map signals where their decisions or mechanisms changed DBU, coverage, or portfolio health (e.g., coverage model changes, big usage saves, to‑and‑through plans).

- **COMPLEXITY (Team & Patch / Multi-Team / Segment Complexity)**
  Map signals that show balancing multiple districts/verticals, resolving escalations across teams, or restructuring coverage/org for scale.

- **INFLUENCE (Executive Internal / External)**
  Map signals where they influenced RDs/RVPs/PS leadership on strategy, headcount, or investments, and where they engaged VP/CIO‑level customers or key partners to unlock outcomes.

- **LEADERSHIP (STEER)**
  - Spark: signals where they set or re‑articulated vision/mission and energized teams.
  - Target: defining #1 priorities, OKRs, and clear focus areas.
  - Elite Teams: hiring, calibration, performance management, successor planning.
  - Execution: building/operating mechanisms (2x2, QBR, forecast, coverage reviews) that actually changed behavior.
  - Culture: enforcing standards, addressing misalignment, modeling Builder + AI‑first.

- **TECHNICAL BAR**
  Map signals where they used technical depth to guide managers/SAs, shape architecture decisions, or represent Databricks credibly in senior technical conversations.

Always prefer fewer, stronger bullets that clearly link **signal → expectation → outcome**, rather than trying to mention every activity.

---

## Step 5 — Output format

Always produce this in the chat, regardless of write-back preference.

Output the content as **regular flowing text** — do NOT wrap in a code block, as that causes line-break artifacts when pasted into Google Docs.

FY27 H1 Check-In – <Role Title> (<Level>)

IMPACT
• ...
• ...

COMPLEXITY
• ...
• ...

INFLUENCE
• ...
• ...

DRIVES CONSUMPTION / EXECUTION STRATEGY
• ...
• ...

TECHNICAL BAR
• ...
• ...

LEADERSHIP & CULTURE  [or STEER for managers]
• ...
• ...

**Style rules:**
- 2–4 bullets per section
- **Third person, past tense** — never use "I" or "my". Write as if describing the person's work (e.g., "Designed and led the Q1 forecasting process…" not "I designed and led…")
- Lead with scope and outcome (DBU, risk reduction, coverage clarity, hiring bar)
- Emphasize repeatable patterns, not one-off heroics
- Use Databricks terminology naturally (DBU, to-and-through, Built On, Vector Search, FINS, PS) — avoid unexplained internal acronyms
- **No markdown syntax in bullets** — no `**bold**`, no `[text](url)` links. Plain text only so it pastes cleanly.
- **Write bullets as single unbroken sentences** — do not hard-wrap long bullets across multiple lines. Let the text flow naturally so it copies without line-break artifacts.
- **Include source URLs inline as plain text** — append `(Source: URL)` at the end of each bullet. If a bullet draws from multiple sources: `(Sources: URL1, URL2)`

---

## Step 6 — Write-back (only if requested)

If the user explicitly asked for doc updates, use `google-docs` to write the same bullets into the correct table cells ("How I Demonstrated This This Quarter" / "Evidence / Outcome" columns) under the matched ladder section. Keep language identical to what was printed in the chat.
