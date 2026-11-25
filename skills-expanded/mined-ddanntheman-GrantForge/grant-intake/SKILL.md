---
name: grant-intake
description: >
  Parse a grant opportunity into a structured requirements matrix and issue a
  go/no-go recommendation. This skill should be used when the user says "here's
  a grant we want to apply for", "respond to this RFP", "parse this NOFO",
  "we're applying for X grant", "are we eligible for this?", or uploads a
  funding announcement, RFP, NOFO, or foundation guidelines document.
version: 0.1.0
---

# Grant Intake

Turn a funding announcement into a complete, testable specification of what
the application must contain. Everything downstream (research, drafting,
budget, review) works off the requirements matrix produced here.

Requires the `.grantforge/` profile; if missing, run grant-setup first.

## Step 1 — Acquire the full announcement

Accept an uploaded document (PDF/Word), a pasted excerpt, or a URL. If given
a URL or partial text, fetch and read the complete announcement including all
appendices — page limits and scoring rubrics often hide in attachments. For
federal grants, check Grants.gov for the related documents package. Never
proceed on a summary alone; ask for the full document if what was provided
is clearly partial.

## Step 2 — Create the grant workspace

Create `.grantforge/grants/<funder>-<program>-<year>/` containing:

```
requirements.md      # The requirements matrix (this skill)
source/              # The announcement and attachments
research/            # Populated by grant-research
drafts/              # Populated by grant-draft
final/               # Submission-ready outputs
```

Register the opportunity in `tracker.md` with status `intake`.

## Step 3 — Build the requirements matrix

Extract into `requirements.md`, as tables:

**Overview**: funder, program name, CFDA/ALN if federal, total pool, award
range, match/cost-share requirement, indirect rate rules, period of
performance, deadline (date, time, time zone), submission mechanism
(portal, email, Grants.gov) and any registration lead time it implies.

**Eligibility**: every eligibility criterion as a row with columns
`Criterion | Our status | Evidence`. Fill "Our status" from the org profile.
Anything unverifiable becomes a question for the user.

**Narrative requirements**: one row per required section with columns
`Section | Prompt (verbatim) | Limit (pages/words/chars) | Points | Notes`.
Copy the funder's prompts verbatim — drafting will answer exactly these.
Capture the scoring rubric weights if published; grant-review scores
against them.

**Attachments and forms**: every required form (SF-424 family, budget
forms, letters of support, MOUs, IRS letter, audit) with who must produce
it and lead time. Flag long-lead items (letters of support, SAM renewal)
immediately.

**Formatting rules**: font, size, margins, spacing, page limits, file
naming, anything the funder can use to disqualify.

**Compliance traps**: absolute requirements stated with "must/shall",
disqualification conditions, and anything ambiguous worth a question to
the program officer. List suggested questions with the funder's Q&A
deadline if one exists.

## Step 4 — Go/no-go recommendation

Score the opportunity honestly:

- Eligibility: any hard failure is an automatic no-go; say so plainly.
- Fit: alignment between the funder's stated priorities and the org's
  actual programs (not what could be stretched to fit).
- Capacity: can the org deliver the project and the application by the
  deadline? Account for match requirements against the org's budget.
- Competition and effort: award count vs. expected applicant pool, and
  application effort vs. award size.

Deliver a recommendation: **Go**, **Go with conditions** (list them), or
**No-go** (with the specific reason). The user decides; record the decision
in `tracker.md`. On "go", update status to `preparing` and propose the
work plan: research first, then section-by-section drafting, budget in
parallel, review no later than five days before deadline.
