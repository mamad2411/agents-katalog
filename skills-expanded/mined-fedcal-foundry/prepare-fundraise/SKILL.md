---
name: prepare-fundraise
description: Decide whether to raise at all, and only then get ready to ask — a readiness verdict built from an evidence inventory of the repository's real numbers, the right funding type for this shape of project, funder targeting verified live from each programme's own page, a narrative and a deck argument in which every figure carries its source and measurement date, a data-room checklist and a rehearsed diligence interrogation. Use before approaching any funder, when a grant call or programme is being considered, when a deck exists but has never been stress-tested, or when someone asks "are we ready to raise". Produces docs/growth/fundraising/.
allowed-tools: Read Grep Glob Bash Write Edit WebFetch WebSearch mcp__plugin_foundry-core_foundry__blackboard_write mcp__plugin_foundry-core_foundry__contract_validate mcp__plugin_foundry-core_foundry__memory_search
argument-hint: "[--type grant|angel|vc|sponsorship|bootstrap]"
user-invocable: true
agent: foundry-growth:fundraising-strategist
model: opus
effort: high
metadata:
  foundry.vertical: growth
  foundry.io: "requirement.v1 -> review.v1 + docs/growth/fundraising/"
license: Apache-2.0
---

# Prepare to fundraise

The deliverable is a defensible answer to two questions in this order: **should this project take
this kind of money at all**, and **if so, what evidence do we actually have**. A deck is the last
artifact produced here, never the first, because a deck written before the evidence inventory
becomes a list of claims looking for backing — and the claims that find none get softened instead
of cut.

The order is fixed: **raise/don't-raise verdict → evidence inventory → funding-type match → funder
targeting → narrative → deck argument → data room → diligence rehearsal**. Every step downstream of
a skipped step produces something that reads like preparation and is not.

**The rule that governs this entire skill:** a figure without a recorded source and an ISO 8601
(`YYYY-MM-DD`) measurement date is **removed, not estimated**. That applies to user counts,
revenue, growth rates, retention, cost savings, pipeline, and to every claim about a funder's
criteria or deadline. There is no "roughly", no "approximately 10k", no "industry average".

**Dates are read, never recalled.** Every date written by this skill — measurement dates, `checked
on` dates, cut dates, the re-run date — comes from `date -I` executed in this session. A date
produced from memory is the same defect as a figure produced from memory, and it is the one that
makes a stale funder deadline look freshly verified.

**Prefer the smallest honest version.** Where the effective move and the honest move diverge, take
the honest one and say that you are doing so, including where the reader expects the opposite
advice. A small counted number with its definition attached reads as weaker than "strong early
traction" and is worth more, because any reader who has seen a hundred decks reads the second as a
countable fact that nobody counted — and then reprices every other line beside it.

`model: opus` / `effort: high` is the AUTHORING.md §2 routing for final synthesis, deliberately
heavier than the rest of `foundry-growth`: this run informs a capital-structure decision that is not
undone cheaply, and most of its work is adversarial checking of the caller's own claims against the
repository.

## When not to use this

- **The money question is really a numbers question.** Break-even, runway, unit economics, NPV/IRR,
  pricing or TCO → `foundry-economics:business-case-analyst` and `foundry-economics:cost-engineer`.
  This skill writes the *argument*; economics writes the *numbers* the argument cites.
- **The grant has already been won and the work is administration** — eligibility forms, budget
  tables, timesheets, milestone reports, audit evidence → `foundry-economics:funding-analyst`.
  Targeting and narrative are ours; the paperwork machinery is not.
- **Nobody can say what the money is for**, in one sentence, with a decision that depends on it.
  Stop and run `position-project` first: a project that cannot state who it is for and what it
  claims cannot state why it needs capital.
- **You want more users, not more money** → `plan-launch` or `build-audience`.
- **You want contributors inside an open source repo** → `foundry-oss`. Growth brings people to the
  project; oss runs what happens once they arrive.
- **The ask is a job, a client or a co-founder, not capital** → `audit-personal-brand` or
  `find-collaborators`.

## Step 1 — should you raise at all

Run this before anything else, and be willing to end the skill here. The four possible verdicts,
one of which must appear as the first line of `docs/growth/fundraising/readiness.md`:

```
VERDICT: RAISE | RAISE-LATER | WRONG-TYPE | DO-NOT-RAISE
```

Answer each of these in writing, with evidence or an explicit "unknown":

1. **What decision does the money unblock?** Name the thing that cannot happen without it. "Grow
   faster" is not a decision. "Hire a second engineer so the migration ships in Q3 instead of Q1
   next year" is.
2. **What is the cheapest honest alternative?** Revenue, a paid pilot, a smaller scope, doing it
   slower, one sponsor, or nothing. Fundraising is itself a months-long project with an opportunity
   cost — state that cost in weeks of the team's time.
3. **What does this money demand in return, structurally?** Equity dilution and a growth obligation;
   reporting and eligibility constraints; a sponsor's expectations of visibility; a lender's
   repayment schedule. Read `references/funding-type-comparison.md` and name the demand.
4. **Are the disqualifiers present?** Each funding type in the reference has a disqualifier list.
   One hit is not fatal; it must be written down and answered.
5. **Would you still want this money if it were the last you ever raised?**

Output **DO-NOT-RAISE** or **RAISE-LATER** when the honest answer supports it, and follow it with a
concrete alternative plan: what to do instead, what evidence would change the verdict, and the date
to re-run this skill. A skill run that ends at step 1 with a written alternative is a successful
run, not a failed one.

**Gate:** if question 1 has no answer that names a specific blocked decision, the verdict is
`RAISE-LATER` and steps 2–9 do not run. Step 10 still runs: `readiness.md` is written with the
verdict, the alternative plan and the re-run date, the six other files are **not** created, and the
`review.v1` artifact carries `verdict: block`. Exit criteria 3–10 are then recorded in
`readiness.md` as `NOT REACHED — stopped at step 1`, which is a complete run.

## Step 2 — evidence inventory, taken from real data

Readiness is an inventory, not a story. Before any narrative exists, collect what is actually
measurable *from this repository and the project's real systems*. Look, do not recall:

```bash
date -I                                                                        # today, for every date below
git log --since="12 months ago" --pretty=%ad --date=format:%Y-%m | sort | uniq -c | cat
git shortlog -sne --since="12 months ago" | cat                                # contributors
git log -1 --date=iso --pretty=%ad | cat                                       # last commit
ls -1 docs/ 2>/dev/null | head -40; wc -l README.md 2>/dev/null                # artifacts, if present
```

Read the output of each. A command that printed nothing is a gap row, not a reason to move on.
Then extend to the systems that hold the rest: analytics export, billing export, package registry
download counts, issue tracker, CRM, the deployment platform. For each candidate figure record a
row in `docs/growth/fundraising/evidence-index.md`:

| id | claim | value | how it was measured | source (path, URL or command) | measured on |
|---|---|---|---|---|---|
| `E-01` | `<claim>` | `<value>` | `<method, and what it excludes>` | `<path, URL or command>` | `<date -I>` |

The row above is a column shape, not sample data. Do not fill it with plausible-looking values to
show the format; a placeholder that survives into the file is indistinguishable from a measurement.

Rules, enforced at exit:

- A row whose **source** or **measured on** cell is empty is deleted from the index. It does not
  move to a "to be confirmed" list and it does not appear in the deck.
- A figure produced by a model, a memory or an analogy is not evidence. Neither is a projection —
  projections belong to `foundry-economics:business-case-analyst` and are cited as such, with the
  model file named.
- Absence is evidence too. Record `E-xx | retention beyond 30 days | NOT MEASURED | — | — | —` as a
  **gap row**, and count the gaps. The gap count is a readiness signal; hiding it is the failure.
- Where a figure exists in `.foundry/memory/`, retrieve it with `memory_search` and cite the fact
  id — but re-measure anything older than its `expires` date rather than quoting it.

**Gate:** the inventory is complete when every claim you would want to make has either a sourced
row or a gap row. Count both. `sourced / (sourced + gaps)` is the readiness ratio quoted in
`readiness.md`.

## Step 3 — match the funding type to the shape of the project

With the inventory in hand, and `--type` treated as a hypothesis rather than an instruction, work
through `references/funding-type-comparison.md`: what each type demands, the shape of project that
fits it, and the disqualifiers. The `--type` values are a shortcut for the five most-asked-about
types; the reference covers eight, and revenue, corporate and community funding are considered even
when they were not named on the command line. Write the conclusion as:

- the type being pursued, and **why this project's evidence fits its demands**;
- the types ruled out, each with the specific demand or disqualifier that ruled it out;
- if `--type` was passed and the analysis disagrees with it, say so plainly and record
  `VERDICT: WRONG-TYPE` in `readiness.md`. Telling someone their project is not venture-shaped is
  the most valuable output this skill produces, and the one it is most tempted to withhold.

## Step 4 — funder targeting, verified at runtime

**Never name a fund, programme, investor, cheque size, equity range, deadline or eligibility rule
from memory.** Anything of that kind is stale, and a stale deadline is worse than no deadline. Every
target in `docs/growth/fundraising/funder-targets.md` is built by fetching its own official page
now and quoting it:

| field | requirement |
|---|---|
| name | as written on the official page |
| url | the official page fetched, not an aggregator |
| checked on | ISO 8601 date of the fetch |
| stated focus | quoted from the page, ≤ 2 lines, in quotation marks |
| stated eligibility | quoted, including the criterion this project might fail |
| stated deadline / process | quoted, or `NOT STATED ON PAGE` |
| fit hypothesis | one sentence, ours, marked as ours |
| evidence they will ask for | mapped to `E-xx` ids from step 2 |

A target row missing `url` or `checked on` is deleted before the file is written. A target whose
eligibility could not be found on its own page is kept only with `ELIGIBILITY UNVERIFIED` in the
row, and may not be contacted until it is resolved.

**Consent and lawfulness.** Targeting means researching organisations and their published contact
routes, and writing to a person individually because there is a real reason to write to *them*. It
does not mean scraped personal data, purchased lists, unsolicited bulk mail, or the same message
automated to many recipients — those are out of scope and are refused by name, not negotiated
down. The instruments to **name and hand over, never to interpret here**: GDPR Art. 6 (lawful basis
for holding a contact list), Art. 14 (what a person must be told when their data was not obtained
from them), and Art. 21(2) (objection to direct marketing). Route those, sponsorship disclosure,
securities and solicitation rules, and the substantiation of any public claim to `foundry-legal`
(`privacy-engineer`, `compliance-engine`) as a `handoff.v1`, with the question and the date raised.
An unanswered legal question is item `D-29` in the data room, not a footnote.

## Step 5 — the narrative

Four paragraphs, no more, written from the inventory:

1. **The problem**, stated as something that happens to someone specific, sourced where a figure
   appears at all.
2. **What we built and what is true about it today** — present tense, only `E-xx`-backed facts.
3. **Why us** — the specific, checkable reason this team is the one doing it. Not "passionate".
4. **The ask and what it buys** — the amount, the runway or milestone it funds, and the decision
   from step 1 it unblocks. The amount comes from an economics model, cited by file path.

Forbidden in all four: a market-size figure without a fetched, dated source; a competitor claim not
backed by their own public page fetched today; "leading", "best-in-class", "10x", "industry
standard" and every other superiority claim the evidence index cannot substantiate. Where a
load-bearing claim has no evidence row, **cut the claim** and log it in the cut list (step 8).
Softening it into a vaguer version of the same unsupported assertion is the failure mode this rule
exists to stop.

## Step 6 — the deck as an argument

The deck outline is a **chain of reasoning**, not a slide template: each section exists to make one
claim, that claim is backed by a named `E-xx` row or by a stated assumption labelled as an
assumption, and the next section is only reachable if the previous one landed. Build it from
`references/deck-argument-structure.md`, which gives each link's job, the evidence it needs and the
failure mode that kills it.

Write `docs/growth/fundraising/deck-outline.md` with one block per section:

```
## 5. Evidence of use
Claim:      <one sentence, no stronger than the index supports>
Evidence:   E-01 (<what>, <date -I>), E-04 (<what>, <date -I>)
Assumption: none | <stated assumption, labelled>
Cut here:   "<the phrase removed>" — no source, removed <date -I>
```

A section whose `Evidence` line is empty and whose `Assumption` line is empty is **deleted from the
deck**, not filled with a stock slide. Run the source pass at the end of
`references/deck-argument-structure.md` over the finished file; its exit condition is zero
`UNSOURCED` lines, and that is what exit criterion 4 counts.

## Step 7 — social proof, or none

Testimonials, logos, user counts, case studies and named adopters are the part of a raise most
often fabricated, so they carry the tightest rule: **each one names the real person or organisation,
the date they said or agreed it, and where that permission is recorded**. No permission record, no
logo. No named human, no testimonial. A case study describes something that happened, to someone
who exists, with numbers from the evidence index.

Invented testimonials, logos of non-users, uncounted user counts, unmeasured metrics, case studies
that did not happen, a mention of a competing term sheet that does not exist, and manufactured
scarcity or deadlines are refused outright. **Refuse in the open, and leave a record:** say which
artifact you will not write and why, produce the honest version of the same section instead, and
record the request as a `finding.v1` of severity `critical` in the `review.v1` artifact of step 10.
A quiet refusal gets re-requested with different wording; a recorded one does not.

If that leaves the deck with no social proof, the deck has no social-proof section — an empty
section is honest and a fabricated one ends the raise and the reputation together.

## Step 8 — data room and the cut list

Build `docs/growth/fundraising/data-room.md` from the checklist in
`references/diligence-readiness.md`, marking every item `HAVE` (with the repository path or system
where it lives), `MISSING`, or `NOT APPLICABLE` with a reason. Nothing is marked `HAVE` without a
path or link that resolves.

In the same file, keep the **cut list**: every claim removed during steps 5–7 for want of evidence,
with the date and what would restore it. The cut list is the artifact that proves the process ran.

## Step 9 — rehearse the diligence interrogation

Take the hard questions from `references/diligence-readiness.md`, add every gap row from step 2 and
every disqualifier from step 3 that was not fully answered, and write the answers in
`docs/growth/fundraising/diligence-rehearsal.md`. Rules:

- Answer in the funder's terms, not yours, and in ≤ 5 sentences.
- At least three answers must be an honest **"we don't know yet"** or **"we don't have that"**,
  followed by what you would do to find out and by when. A rehearsal in which every answer is
  strong has been written as marketing, not as preparation.
- Any answer that requires a figure cites its `E-xx` id. An answer that needs a figure the index
  does not hold becomes a gap row, and the raise is not ready until it is closed or acknowledged.
- Mark each answer `SOLID` / `THIN` / `NO ANSWER`. Count them. The counts go in `readiness.md`.

## Step 10 — write it down

`docs/growth/fundraising/` contains exactly: `readiness.md` (verdict on line one, readiness ratio,
answer counts, re-run date ≤ 90 days), `evidence-index.md`, `funder-targets.md`, `narrative.md`,
`deck-outline.md`, `data-room.md` (including the cut list) and `diligence-rehearsal.md`.

Emit `review.v1` to `.foundry/blackboard/<wave>/prepare-fundraise.json` via `blackboard_write`, with
`dimension: "fundraising-readiness"`, a `verdict` of `block` for `DO-NOT-RAISE` / `RAISE-LATER` /
`WRONG-TYPE` and `pass-with-comments` otherwise, and one `finding.v1` per gap row, per unverified
funder row, per `NO ANSWER` in the rehearsal and per fabrication request refused in step 7. Each
finding needs `id`, `severity`, `title`, `summary`, `failureScenario` and `confidence` — the schema
requires `failureScenario`, and the `validate-contract` hook rejects the whole write without it, so
name what actually goes wrong ("the funder asks Q-06 and the retention figure does not exist"), not
the gap's name again. Validate with `contract_validate` before writing. Return to the caller **only**
the artifact path plus a summary of ≤ 300 tokens — never the contents of `docs/growth/fundraising/`.

## Exit criteria

Criteria 1, 2 and 11 apply to every run. Criteria 3–10 apply only when step 1 opened the gate; on
an early exit each is written into `readiness.md` as `NOT REACHED — stopped at step 1`, and the run
is complete.

1. `docs/growth/fundraising/readiness.md` exists and its first line matches
   `VERDICT: (RAISE|RAISE-LATER|WRONG-TYPE|DO-NOT-RAISE)`.
2. A `DO-NOT-RAISE` or `RAISE-LATER` verdict is followed by a named alternative, the evidence that
   would change it, and a re-run date — otherwise the run is incomplete.
3. `evidence-index.md` exists; **zero** rows have an empty source cell or an empty measurement date;
   every date matches `YYYY-MM-DD` (ISO 8601). Gap rows are counted and the readiness ratio
   `sourced / (sourced + gaps)` is stated in `readiness.md`.
4. Every numeric figure appearing in `narrative.md` and `deck-outline.md` appears verbatim in
   `evidence-index.md`. Verified by the source pass at the end of
   `references/deck-argument-structure.md`, run over both files; the count of `UNSOURCED` lines it
   prints is **0**, and the output is pasted into `readiness.md`.
5. Every row in `funder-targets.md` carries a fetched `url`, a `checked on` ISO date and a quoted
   eligibility line, or is explicitly marked `ELIGIBILITY UNVERIFIED` and flagged as not-contactable.
   The count of rows naming a fund, amount or deadline without a fetched URL is **0**.
6. The count of testimonials, logos, named adopters, case studies and user counts lacking a named
   real source and a recorded permission date is **0**.
7. `deck-outline.md` has one claim per section, each with an `Evidence` or a labelled `Assumption`
   line; the count of sections with neither is **0**.
8. `data-room.md` lists every checklist item from `references/diligence-readiness.md` as `HAVE`
   (with a resolving path or link), `MISSING` or `NOT APPLICABLE` with a reason; the cut list has at
   least one entry or states explicitly that no claim needed cutting.
9. `diligence-rehearsal.md` answers ≥ 15 questions, of which ≥ 3 are an honest "we don't know" with
   a follow-up and a date; each answer is labelled `SOLID` / `THIN` / `NO ANSWER` and the counts are
   reproduced in `readiness.md`.
10. The count of superiority, adoption and performance claims surviving without an `E-xx` id is
    **0**, and every date in every file matches `YYYY-MM-DD` and came from `date -I` in this
    session. Both are checked mechanically:

    ```bash
    grep -rniE 'leading|best.in.class|fastest|most (popular|used)|10x|industry standard|trusted by' \
      docs/growth/fundraising/ | grep -v 'E-[0-9]'      # expect no output
    grep -rhoE '[0-9]{4}-[0-9]{2}-[0-9]{2}' docs/growth/fundraising/ | sort -u   # inspect each
    ```
11. `review.v1` written and validated by `contract_validate`, carrying one finding per gap,
    unverified target, `NO ANSWER` and refused fabrication request, each with a `failureScenario`;
    the returned summary is ≤ 300 tokens and no file contents are returned with it.

## Degradation

- **`WebFetch` / `WebSearch` unavailable** → say so in the first line of `funder-targets.md`, do not
  name a single programme, and instead emit the *search plan*: the queries to run, the official
  domains to check, and the empty table with its required fields. Mark the file
  `UNVERIFIED — NO NETWORK ACCESS` and record that no funder may be contacted from it.
- **`gh` absent** → repository signals come from `git log` and the working tree only; issue, PR and
  release counts are recorded as gap rows rather than guessed.
- **No analytics, no billing, no registry data** → the readiness ratio is dominated by gaps, and that
  *is* the finding: the verdict is `RAISE-LATER` with "instrument the three figures a funder will
  ask for first" as the alternative plan.
- **A grant deadline is imminent** → do not skip step 2 to make it. Record the deadline as fetched
  and dated, state which evidence rows are missing, and let the human decide whether to apply with a
  known gap. Applying with acknowledged gaps is legitimate; applying with invented figures is not.
- **`foundry-economics` not installed** → the ask amount and any projection stay marked
  `UNMODELLED` in `narrative.md` and `deck-outline.md`. Do not improvise a financial model here.
- **`superpowers` installed** → use `superpowers:brainstorming` to pressure-test the step 1 verdict
  and the narrative's framing, and `superpowers:verification-before-completion` before any file in
  `docs/growth/fundraising/` is shown to a funder. If it is absent, apply the same discipline by
  hand: state the claim, name the artifact that proves it, and reread the exit criteria list above
  before declaring the pack ready.

## Deliberately not covered

Financial projections, unit economics, break-even and TCO (`foundry-economics:business-case-analyst`,
`foundry-economics:cost-engineer`); grant administration, budget tables, timesheets and audit
evidence (`foundry-economics:funding-analyst`); the one-sentence claim, naming and differentiation
(`position-project`); launch sequencing (`plan-launch`); sustained editorial attention
(`build-audience`); the founder's own public credibility (`audit-personal-brand`); contributor
onboarding and governance inside the repository (`foundry-oss`); README and documentation
(`foundry-research`); roadmap and delivery reporting (`foundry-pmo`); and every question of personal
data, marketing consent, advertising-claims substantiation, sponsorship disclosure or securities
regulation (`foundry-legal`) — flagged here, decided there.

## Bundled references

- `references/funding-type-comparison.md` — bootstrap, revenue, grant, angel, VC, sponsorship,
  corporate and community funding: what each demands, the project shape that fits, and the
  disqualifiers. Contains no amounts and no named funds by design.
- `references/deck-argument-structure.md` — the deck as a chain of reasoning: each link's job, the
  evidence it needs, and the failure mode that breaks it.
- `references/diligence-readiness.md` — the data-room checklist and the hard questions, each with
  guidance on answering it honestly and on what an evasive answer costs.
