---
name: carbon-monitor-adapt-harness
description: Adapt the Carbon Monitor harness to a new use case. Interviews the user in at most ten questions and writes a SPEC for spec-driven implementation. Use when asked to adapt, reuse or repurpose this harness, run a different job on it, point it at another repository, or swap the worker agent. Produces one Markdown file; makes no code changes.
---

# carbon-monitor-adapt-harness

You are in a clone of Carbon Monitor. This skill produces one file,
`specs/<slug>/SPEC.md`, that a later session implements from. It reads
documentation and writes that file; it makes no code changes and runs no
project scripts.

Load documents in stages, each at the step that needs it, and read a section
rather than a file wherever a section is enough: find the heading, read to the
next heading of the same level, stop. `reading-map.md` lists what each step
and each SPEC section needs.

## Step 1. Orient (one short read)

Read `docs/HARNESS.md` **section 1 only**: the loop and its three invariants.
That is enough context to run the interview. Nothing else is read yet.

## Step 2. Branch

Ask this, word for word, then wait:

> Which of these are you doing?
> **A.** PR reviews for another repository, keeping the review job.
> **B.** A different job on this harness: scheduled, in IBM Cloud, with cost
> tracking, telemetry and a Slack report, against some other system.

Load `interview/pr-review.md` for A or `interview/new-job.md` for B. B is a
larger adaptation than A; say so once.

## Step 3. Interview

- One question at a time, in the file's order, at most ten.
- State the default with each question; accept "default".
- Skip a question the user has already answered in any form.
- If an answer names a worker agent other than Bob, note it. `bob` and `claude`
  are supported as built, so either is configuration only. Any other CLI needs an
  adapter (`docs/HARNESS.md` section 4, "Add an agent"); its agent file is read
  later, at the step that needs it.
- Stop early when every SPEC section can be filled.

## Step 4. Write the SPEC, pulling context section by section

Read `reading-map.md`, then `templates/SPEC.md`. Copy the template to
`specs/<slug>/SPEC.md` (short kebab-case name for the adapted system), fill
the header (the short SHA from `git rev-parse --short HEAD`, today's date) and
fill the sections in order. For each SPEC section, read only the sources the
map lists for it, at the granularity it lists, and do not read ahead for later
sections. Rules:

- Every row of the tables in `docs/HARNESS.md` sections 2 and 3 gets a
  decision in SPEC section 3.
- Every file and function the SPEC cites as existing today is in the
  repository; cite the path. Confirm a name by searching for it, not by
  reading the file through. A name the SPEC introduces is marked as new: it
  sits in a replace or add row, in the New column of section 6, or in a task.
- Branch B always fills section 6 with every name in `docs/HARNESS.md`
  section 5, old and new.
- The invariants from step 1 stay unless section 9 states why one must change.
- Acceptance criteria are testable given/when/then statements.
- Tasks are ordered, small, and name their files and criteria.
- Anything unsettled goes in section 13 with who decides. No guesses.

## Step 5. Check, then finish

- [ ] Every template section present, none left as a placeholder
- [ ] A decision for every row of `docs/HARNESS.md` sections 2 and 3
- [ ] Section 6 complete for B, or "none" for A with no renames (an agent
      other than Bob or Claude adds new names; see the reading map)
- [ ] Every file or function cited as existing today found in the repository;
      every new name marked as new
- [ ] Every open question has an owner

Print the SPEC path, the three highest-risk open questions, and this next
step, then stop:

> Start a fresh session and say: "Implement `specs/<slug>/SPEC.md`, one task at
> a time, verifying each against its acceptance criteria."
