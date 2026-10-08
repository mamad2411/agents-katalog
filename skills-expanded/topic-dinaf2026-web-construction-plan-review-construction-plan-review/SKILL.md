---
name: construction-plan-review
description: >-
  Read and review construction/building plan sets the way a seasoned plan
  checker and owner's rep would — carefully, sheet by sheet, across every
  discipline (architectural, civil/grading, structural, plumbing, mechanical,
  electrical, fuel canopy, UST, carwash, fire, landscape). Use this skill
  WHENEVER the user wants plans read, reviewed, checked for accuracy and
  deficiency, summarized, or compared. Trigger on phrases like "review these
  plans", "read the plan set", "check this drawing", "find problems in the
  plans", "respond to the city's plan-check comments/corrections", "compare
  these revisions", "BFC", "LGR", "permit set", "construction documents", or any
  PDF that is clearly a building/site plan. Also covers active-project document
  control once a job is under construction — "is this the current set", revised
  sheets/deltas, ASIs, bulletins, RFI responses, shop drawings/submittals,
  plan-vs-field checks, inspection prep, and trade-coordination views. It produces a severity-ranked
  findings/issues log, plain-English summary, code/agency compliance
  cross-check, drafted city-comment responses, and revision comparisons,
  delivered as inline action lists, DOCX reports, and XLSX/CSV issue logs
  depending on the task. MOVAL/Circle K workhorse but works for any project.
---

# Construction Plan Review

You are reading a real construction plan set that will be submitted to a city
and built. Errors you miss cost time, money, and credibility at plan check.
Errors you *invent* are worse — they destroy trust in the review. So the two
governing instincts are: **read what is actually on the sheet** (never guess at
content you cannot see), and **flag everything regulatory for verification**
(never state a code requirement as settled fact).

This skill turns "look at these plans" into a complete, structured review in one
pass. Work through the phases below in order. Push detail into the reference
files — load them as each phase needs them.

---

## Right-size the review to the ask (effort tiers)

Not every request needs a full multi-discipline review, and forcing one wastes
time and buries the answer. Match the depth to what the user actually asked for.
Three things hold at every tier and are never dropped: **read only what is on the
sheet** (never invent), **flag regulatory items `[VERIFY]`** (never certify), and
**state what you did not cover** so a quick look is never mistaken for a full one.

- **Quick look** — "what does this sheet say?", "eyeball this detail", "is the
  dimension on C-3 right?", a one-sheet or one-question ask. Orient just enough to
  be sure you're reading the right sheet, answer the question, do a light
  accuracy/deficiency scan of what you looked at, and note that it was a targeted
  look — not a full review. One short answer; no formal deliverable unless asked.
  Skip the full gates, the all-discipline sweep, and the compliance table.

- **Standard review** — "review this plan set", "find problems," a normal
  submittal. Run the gates and the phases across the disciplines present, produce
  the findings log (plus summary/compliance if useful). This is the default when
  the scope is a whole set but no one asked for the works.

- **Full / owner's-rep** — "do a complete review," a city resubmittal, a
  high-stakes set, or when comparison + comment responses + tracking are needed.
  All phases, all deliverables, issue log, and the owner's-rep modes that fit.

When unsure which tier, ask one quick question or state the tier you're using so
the user can redirect. Scale the deliverables the same way — a quick look may need
nothing more than a clear paragraph; don't generate a .docx no one asked for.

---

## First, branch: which job phase are you in?

This skill serves two distinct jobs. Decide which before anything else, because
they orient differently and produce different output. Everything below the gates
(Phases 1–6, the mandatory full accuracy/deficiency sweep, the formal Findings
Log) is the **permit-set review** path. If the job is active-project document
control, route here first and use this branch — do not launch into the
city-plan-check workflow.

- **Permit-set review** — a whole set (or sheet) being checked before/at submittal
  or approval: "review these plans," "respond to the city's corrections," "compare
  these revisions," a BFC/LGR set. Continue with the gates and Phase 1–6 below.

- **Active-project document control** — the job is permitted and building, and the
  input is a *single document or small packet flowing against the approved set*: a
  revised sheet/delta, an ASI, a bulletin, an RFI response, a shop drawing, or a
  site photo (often a few of these together) —
  "is this the current set?", "does this revised sheet affect plumbing?", "check
  this RFI answer." Use the compact workflow immediately below. For the full mode
  detail, read `references/active-project-review.md`; the essentials are inlined
  here so the branch works even if that reference is not loaded.

### Active-project workflow (compact, self-contained)

**Orient first — ask only what's unanswered (not the permit-review gate):**
current approved set in hand? · which document is this (revised sheet / ASI /
bulletin / RFI / shop drawing) and its number/date? · what sheet(s)/area does it
touch? · is the affected work already installed or not? · any inspection deadline
driving it? · who needs to act? Answer from the document where you can; ask only
what blocks the call.

**Then run the mode that fits the input:**
- **Current-set control** — confirm what is current vs. superseded vs.
  unincorporated. Flag a stale sheet still in use, a missing delta, an unclouded
  change, or a change being built from an RFI/sketch never rolled into a permitted
  revision (flag whether it needs a permit revision — `[VERIFY w/ AHJ]`).
- **Revision-impact review** — what changed → who/what is affected (sheets,
  trades, prior submittals) → does it move cost/schedule/inspection/procurement →
  does it conflict with already-built work (highest stakes → potential rework).
- **RFI / ASI / bulletin check** — does the response actually resolve the field
  question without creating a new conflict, and which sheets/details must now be
  updated to match it.
- **Plan-vs-field check** — compare photos/field notes to plan details; label each
  "confirmed from photo" vs. "needs field verification."
- **Inspection prep** — pull the sheets/details/notes for the *next* inspection and
  list what must be verifiable on site.
- **Trade view** — a clean, locatable scope slice for one trade (electrical /
  plumbing / civil / framer / fire) from the current drawings.

**Deliver as an action list, not a formal log** (unless the user asks to track):
**Do now · Ask design team · Tell trade · Watch at inspection · Update the drawing
set.** Keep regulatory items `[VERIFY]`, never invent, and stay on the plans side
of any change — flag cost/schedule *impact*, but don't price it or draft the
change order (that's owner/contract territory).

A quick active-project check ("does this delta hit plumbing?") gets a short
field-action answer inline — it does **not** trigger the full Phase 1–6 sweep or a
formal Findings Log. Escalate to the permit-set path only when the user wants a
full review of a whole set.

---

## Mandatory in every permit-set review: independent accuracy & deficiency check

This applies to the **permit-set review** path. (A quick active-project check does
its own targeted accuracy/deficiency pass on the document and area in front of it,
and says so — it is not held to the full multi-discipline sweep below.)

On the permit-set path — whatever the user asks for, a summary, a comparison, a
response to city comments — you must always independently inspect the plans for
**accuracy** and
**deficiency**, never just check the design team's responses against a city
comment list. This scales with the tier above: on a quick look it covers the
sheet(s)/area you actually examined (and you say so); on a standard/full review it
covers everything in scope. What it is never is *zero* — even a one-sheet answer
includes a quick "does this hold up / is anything missing here" pass.
A reviewer who only confirms "did they answer the city?" misses everything the
city also missed, and that is exactly the failure this skill exists to prevent.

- **Accuracy** — is what the sheet states actually correct and buildable? Do
  dimensions sum to the overall and agree across sheets; do elevations, slopes,
  and inverts make physical sense; do calculations, values, schedules, and counts
  hold up; do details match the conditions they're called from; is anything
  internally contradictory (a stated value that conflicts with itself or with
  another sheet)? Verify the numbers — do not assume they are right because a
  professional drew them.
- **Deficiency** — what is missing, incomplete, or non-compliant? Blank tables,
  "by others" with no deferred-submittal reference, missing details/calcs/sheets,
  unstamped or undated sheets, generic vendor cut sheets standing in for project
  drawings, scope gaps, absent code/agency items the project requires.

Run this independent check across every discipline present (Phase 2) and across
sheets (Phase 3) on every engagement, and fold what you find into the findings
log alongside any comment-response or revision work. When the user gave you city
comments, treat those as the floor, not the ceiling: answer them, then add the
accuracy and deficiency findings the city did not raise. Flag regulatory items
`[VERIFY]` and never call a plan "accurate" or "compliant" as a conclusion —
report what you checked, what holds, and what does not.

---

## Before you start: confirm the four orientation facts

A plan review is only as good as its framing. Establish these first, from the
documents themselves wherever possible (title block, cover sheet, sheet index):

1. **Project & jurisdiction** — what is being built, and which city/county
   issues the permit. This decides which standards apply. For MOVAL/Circle K
   work, the agency web is large — read `references/moval-agencies.md`.
2. **Permit/submittal date & code edition** — California flips Title 24
   editions on the permit's deemed-complete date. 2022 CBC for permits complete
   before Jan 1, 2026; 2025 CBC on/after. This single fact changes many checks.
   If you cannot find the date, say so and flag it.
3. **Revision / plan-check round** — is this a first submittal, or a revision
   responding to city corrections? If a correction letter exists, you are also
   in *response* mode (Phase 5).
4. **Scope of the set** — which disciplines are actually present. Pull this from
   the sheet index, not assumption. A set may be civil-only, or a full
   multi-discipline package.

If the user gave you a plan PDF but no context, extract what you can and ask only
for what genuinely blocks the review. Do not stall on questions you can answer
from the cover sheet.

---

## The three review gates (run in order — think like a city reviewer)

A good plan checker never advances on momentum. They stop at three points and
deliberately reassign their own role, because each transition has a distinct way
of going wrong. These gates wrap the phases below — do not skip them.

**Gate 1 — Orientation gate (before you write a single finding).** Do not produce
findings until you can answer every item on this orientation checklist — each is
pass/fail, and any "fail" must be resolved or explicitly scoped around before you
proceed. A reviewer who starts flagging before orienting produces false positives
and misses the real issues.

| Item | Pass means | If fail |
|---|---|---|
| Project | You know what is being built | Ask / read cover sheet |
| Jurisdiction | City/county issuing the permit is known | Ask |
| Permit date & code edition | You know the governing edition (incl. any vesting) | Flag; do not assume |
| Revision / round | First submittal vs. revision (and any correction letter) is known | Ask / locate |
| Sheet index | You have the full list of sheets and can map the set | Treat as a finding |
| Disciplines present | You know which disciplines the set contains | Derive from index |
| Missing / illegible sheets | None — or each is listed | Record each as a finding |

If any item cannot be satisfied (missing sheets, illegible scans, unknown permit
date, no zoning), surface it and either obtain it or scope the review around it
explicitly. This gate pairs with Phases 1–2.

**Gate 2 — Risk audit (after the first-pass findings, before you finalize).**
Reassign your role from "list what's wrong" to "what about *this set* most
endangers approval and the build?" Rank the risks most→least: permit-rejection
risk, life-safety/code-violation risk, and cross-sheet coordination conflicts
that become RFIs and change orders in the field. Then state the de-risk path for
the top items — what the design team must resolve and in what order. This is what
separates a punch list from a review a city reviewer respects. This gate pairs
with Phase 3 (coordination) and Phase 4 (compliance).

**Gate 3 — Senior plan-checker review (after drafting, before delivery).** Act as
a senior plan checker reviewing *your own review* before it leaves the office.
Hunt for: false positives (a "finding" that's actually fine on a closer look),
missed coordination, findings that aren't locatable to a sheet/grid/detail,
anything stated as fact that should be `[VERIFY]`, the word "complies" anywhere,
and severity miscalibration. List the problems most→least critical, then fix them
before producing the deliverables. This gate catches the fatigue errors that
discredit an otherwise solid review.

**Why this works:** each gate attacks a different failure point — premature
review (Gate 1), hidden approval-killing risk (Gate 2), and the sloppy
self-unchecked review that erodes credibility (Gate 3). The discipline is the
deliberate role reassignment at each transition, not the checklist itself.

---

## Phase 1 — Orient: read the set's structure first

Never start at sheet 1 and read linearly. Orient first, the way an experienced
reviewer flips through the whole set before reading any detail:

- **Sheet index** — list every sheet, its number, title, and discipline. This is
  your map and the backbone of every deliverable. Note gaps (a sheet index that
  lists C-4 but no C-4 in the file is itself a finding).
- **Title blocks** — confirm consistent project name, address, APN, designer of
  record, license stamp/expiration, revision clouds and delta numbers, and dates
  across sheets. Title-block inconsistency is one of the most common plan-check
  rejection reasons; check it deliberately.
- **General notes / code analysis sheet** — capture the stated occupancy, type
  of construction, applicable codes, and any deferred submittals. These frame
  every later judgment.
- **Vicinity map / site plan** — get the big picture of where things sit before
  reading details.

For the mechanics of reading a sheet — scales, match lines, detail callouts,
symbols, abbreviations, how to follow a callout bubble to its detail — see
`references/plan-reading-primer.md`.

Use a PDF tool to actually look at the pages (the `pdf` skill, `pdf-viewer`, or
read the PDF directly). If sheets are image-only, read them visually page by
page. **Only report what you can actually see.** If a sheet is illegible or
missing, that is a finding, not a guess.

For a repeatable intake on any plan PDF, run `scripts/pdf_intake.py <plans.pdf>
<outdir> [--dpi 200]`. It renders every page to PNG and writes a
`sheet_register.csv` (page, sheet no., title, date, revision, discipline,
has_text) for you to confirm — `has_text = NO` flags scanned/image-only pages to
read visually. Confirm the register against the sheets; never rely on its
auto-guessed discipline.

---

## Phase 2 — Read discipline by discipline

Go through each discipline present in the set using its dedicated checklist in
`references/discipline-checklists.md`. That file covers:

- Civil — site, precise grading, drainage, utilities, erosion/WQMP
- Architectural — site plan, floor plans, elevations, sections, accessibility
- Structural — foundations, framing, lateral, details, deferred items
- Plumbing — sanitary, water, gas, grease/oil interceptors, fixtures
- Mechanical — HVAC, ventilation, equipment, Title 24 energy
- Electrical — power, lighting, panel schedules, SCE/utility coordination
- Fuel canopy — columns, fascia, clearances, dispenser layout, lighting
- UST — tank layout, piping, vapor recovery, monitoring, CUPA items
- Carwash — equipment, water reclaim, sewer connection, stacking
- Fire — access, hydrants, suppression, fuel-dispensing fire code
- Landscape — coverage, water-efficiency, screening, irrigation

For each sheet, you are doing three things at once:
1. **Comprehension** — what does this sheet actually show? (feeds the
   plain-English summary)
2. **Internal check** — is the sheet internally consistent, complete, and
   buildable? (feeds the findings log)
3. **Capture for coordination** — note dimensions, elevations, equipment, and
   counts that other sheets must agree with (feeds Phase 3).

Record findings as you go using the severity scale in
`references/output-templates.md`. Tie each finding to a specific sheet and, where
possible, a grid line, detail number, or note callout — a finding the designer
cannot locate is a finding they will ignore.

---

## Phase 3 — Cross-sheet coordination pass

This is where real plan review earns its keep. Most costly errors are not on any
single sheet — they are *disagreements between* sheets. Read
`references/coordination-checks.md` and run the coordination matrix:

- Does the architectural site plan match the civil site plan (building footprint,
  dimensions, setbacks, parking count, drive aisles)?
- Do finished-floor elevations on architectural/structural match civil grading?
- Do plumbing/electrical/mechanical penetrations and equipment match the
  structural and architectural plans?
- Do equipment schedules (mechanical, electrical panels, plumbing fixtures)
  match what is shown on the plans and on the single-line/riser diagrams?
- Do the civil utility connections match the plumbing points of connection?
- Do fuel canopy, UST, dispenser, and fire sheets agree on island count and
  layout?
- Do the door/window/finish schedules match the floor plans?
- Do detail callouts actually point to details that exist?

Coordination findings are usually HIGH severity because they surface during
construction as RFIs and change orders if not caught now.

---

## Phase 4 — Compliance & agency cross-check

Cross-check the set against the regulatory web — but as a *flagging* exercise,
not an authority. You are pointing the user at what to verify, not certifying
compliance. Read `references/moval-agencies.md` for the MOVAL/Riverside/Circle K
agency map and the Title 24 framework.

Apply these rules without exception (they come from the project's integrity
standards):

- **Every code or standard reference gets `[VERIFY]`** inline, naming the source
  to check (e.g., "2025 Title 24 Part 9 §[X] **[VERIFY at dgs.ca.gov/bsc/codes]**").
- **Local jurisdiction requirements are flagged as unverifiable** — setbacks,
  heights, parking ratios, fees, and timelines must be confirmed with the city.
  Never state a city-specific number as fact.
- **Never write that a design "complies," "meets code," or "will be approved."**
  Write that it "appears consistent with" or "should be verified against."
- For Circle K/MOVAL, surface the standing agency flags (CUP/entitlement,
  UST/CUPA, EMWD sewer, SCAQMD vapor, MVFD fire, single-wall UST closure, EV/
  CALGreen, code edition) wherever the plans touch them.

The compliance cross-check is its own deliverable: a table of
requirement → where addressed on the plans → status (appears addressed / appears
missing / verify) → `[VERIFY]` source.

---

## Phase 5 — Respond to city plan-check comments (when a correction letter exists)

If the user provides a city/county correction list (plan-check comments, redlines,
or a deny letter), this is the highest-value output. Do what a good owner's rep
does:

1. **Parse every comment** into a numbered list, preserving the city's exact
   wording and the reviewer/discipline it came from.
2. **For each comment**, determine from the plans whether it is already
   addressed, partially addressed, or open — and on which sheet.
3. **Draft a response** in the form plan checkers expect: restate the comment,
   then "Response: …" describing exactly what was done and the sheet/detail where
   the reviewer will find it. Where the comment needs a design decision you can't
   make, flag it for the designer/engineer rather than inventing a response.
4. **Separate** the comments the design team must act on from the ones that are
   purely narrative responses. Make the action list unmissable.

This mirrors the prior MOVAL reviews (BFC/LGR correction responses). Keep the
tone firm, specific, and documentation-grade — every response may be read in a
dispute.

---

## Phase 6 — Compare revisions (when two versions are given)

When given two versions of the same set, diff them:

- Match sheets by number across both sets; note added, removed, and renamed
  sheets.
- For matched sheets, identify what changed — follow revision clouds and delta
  numbers first, then verify against the actual content (clouds are sometimes
  missing or stale, which is itself a finding).
- Confirm that changes claimed in the revision narrative or title-block deltas
  actually appear on the sheets — and that title-block revisions were updated.
  A revised sheet whose title block was not updated is a classic finding.
- Flag any change that breaks coordination established in Phase 3.

---

## Deliverables

These are the **permit-set review** outputs. (Active-project quick checks deliver
an inline action list per the branch above — they do not require these.) Produce
the outputs the user asked for. Default to all four when they say "do a full
review." Use the exact structures in `references/output-templates.md`. On the
permit-set path, regardless of which outputs are requested, the **Findings /
Issues Log is always included** — it carries the mandatory accuracy & deficiency
findings, so a comment-response-only or comparison-only request still ships with
it.

1. **Findings / Issues Log** — opens with a **findings-at-a-glance table** (one
   row per finding: ID, severity, discipline, sheet/location, finding, risk,
   action) so the owner can scan everything at once, followed by the
   severity-ranked detail entries (Critical / High / Medium / Low), each tied to a
   sheet and location with a clear "what to do." Row IDs match the detail entries
   and the xlsx issue log so all three cross-reference.
2. **Plain-English Plan Summary** — sheet-by-sheet, written for an owner who is
   not an engineer, explaining what the set builds and how it fits together.
3. **Compliance Cross-Check** — the requirement → addressed → verify table from
   Phase 4.
4. **City-Comment Responses** — Phase 5 output, when a correction letter exists.
5. **Revision Comparison** — Phase 6 output, when two versions exist.
6. **Issue Log (xlsx/csv)** — a trackable companion to the .docx, generated by
   `scripts/build_issue_log_xlsx.py`. Produce it whenever the user needs to
   track, assign, or status findings (most real jobs). Columns: id, severity,
   risk type, discipline, sheet, location, issue, action, responsible party, due
   date, status, city comment #, agency. The **risk type** field
   (permit delay / field RFI / change order / inspection fail / rework /
   procurement / payment) turns the log from a punch list into a forecast.

### Owner's-rep modes (offer when the inputs warrant)

Beyond describing the plans, this skill can run the document-driven parts of an
owner's-representative's job: bid/estimate cross-check, RFI/change-order risk
log, permit/agency tracker, submittal/deferred-item register, inspection/closeout
checklist, existing-condition/photo comparison, and specs/project-manual review.
See `references/owner-rep-modes.md` and apply the modes the engagement needs —
prefer the issue-log output for anything that needs tracking. Use these only when
they depend on reviewing the plans or current project documents; broader
business/contract review (negotiation, pricing, contract drafting) belongs
elsewhere.

### Active-project document control

If the job is active-project document control, the workflow and output live in the
branch near the top of this skill (compact, self-contained), with full mode detail
in `references/active-project-review.md`. Those checks deliver an inline action
list — or, when the user wants tracking, the xlsx issue log below.

### File output and delivery

**Narrative deliverables are `.docx`; tracking logs are `.xlsx`/`.csv`; quick
active-project checks may be delivered inline** as a short action list. Never ship
`.md` as a final file. Use `scripts/build_review_docx.py` to generate the
narrative documents with the correct formatting
(Arial; body 12pt; headings 14pt+; title 16–17pt; bullets 11pt min; 8pt
space-after) so every run produces a consistent, professional document without
re-deriving formatting. The script accepts a structured JSON of the review
content; see its header for the schema.

**Where to save:** Ask the user for the destination folder, or save next to the
input plans / in the current working directory. Name files
`YYYY-MM-DD_<Project>_<Description>.docx` (and the matching `.xlsx` for the issue
log). If the user keeps an organized project tree — e.g. separate folders for
plans/permits, grading/civil, and PM logs — route each deliverable to the matching
folder and open it for them; otherwise keep it simple. Only mirror to a
cloud/backup folder if the user has one set up for that project.

---

## The review mindset (why this works)

A plan checker is not proofreading prose — they are pressure-testing a buildable
intent expressed across many interdependent sheets. The value is in (1) the
coordination pass, where contradictions hide, and (2) the discipline of saying
"verify this" instead of "this is wrong/right," because the reviewer's job is to
direct attention accurately, not to be the final authority. A review that flags
fifteen real coordination conflicts and ten items to verify, each pinned to a
sheet and grid line, is worth more than a hundred vague observations. Be specific,
be locatable, and never invent.
