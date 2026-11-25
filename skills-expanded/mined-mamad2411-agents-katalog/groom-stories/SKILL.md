---
name: groom-stories
description: "Decompose Features into demoable story slices with full bodies, acceptance criteria and estimates, published to the tracker."
disable-model-invocation: true
---

# Groom Stories

Take one Feature at a time and cut it into **slices**: stories that are separately demoable, separately able to fail, and separately estimable.

The failure this skill exists to kill is the **echo**: a Feature holding one story that restates it in different words. `F5.10 Administration and Audit` echoing into *manages users, notifications and reviews the audit trail* is not a story, it is three features in a trench coat. It gets estimated as one number, assigned to one person, and discovered to be three weeks of work in the last sprint before a milestone.

Read `docs/delivery/backlog-map.md`, `docs/agents/backlog-conventions.md` and `docs/agents/delivery-tracker.md` first.

## Work one Epic per session

Grooming is repetitive and context fills fast with published bodies. Take one Epic, or a run of four or five Features, then `/clear` and start the next. Nothing is lost: the tracker and the map carry the state.

## Process

### 1. Read the Feature and everything behind it

For each Feature: its own body, the requirement rows it covers in the register, and the source document sections those cite. The story bodies quote these; a story written from the Feature title alone is a paraphrase of a paraphrase.

### 2. Cut the slices

Slice by **outcome**, never by layer. `Add the API endpoint` and `Add the screen` are two halves of one thing that can neither be demoed nor shipped alone. `Record a top-up and follow it to confirmation` is a slice.

Target three to five per Feature. Then run the four tests, in this order:

- **The echo test.** Say the story title, then the Feature title. If one is the other with different words, the slicing has not happened yet. Cut again.
- **The demo test.** Can somebody stand up and show this working, to a person who does not know the architecture? If not, it is a layer, not a slice.
- **The failure test.** Can this story fail on its own without taking a sibling down? If two stories always pass or fail together, they are one story.
- **The size test.** Above 8 points, it is not a story yet.

### 3. Sweep the unhappy paths

Happy paths write themselves and the register describes them. This sweep is what makes the difference between a backlog that looks complete and one that is, and it is the step to spend the most effort on. For each Feature, ask by name:

- **Stopping.** Sign-out, cancellation, reversal, handover, deactivation, offboarding. A backlog with a story for creating every entity and none for removing any is the normal state of a backlog, and it is wrong every time.
- **Recovery.** Forgotten password, expired session, lost device, resent code.
- **Failure.** Connectivity loss, timeout, retry, **the same request arriving twice**. Idempotency is a story, not an implementation detail, wherever money or state moves: a lost response on a flaky connection is a double debit against a real balance.
- **The other end.** Where a story sends something, the story where somebody sees the result. Whole feedback paths go missing this way, because the request was the interesting part to whoever wrote the document.
- **Being told.** The screen, notification or record that tells a human what just happened, including when it went wrong.
- **Proving it.** Reconciliation, tamper evidence, the adversarial test. Where a requirement says *tamper-evident*, an append-only log is a weaker claim and a different story.

A slice this sweep produces is usually a **gap in the contract**, not just a finer cut. Report each one to the user by name: it may need to reach the client as a change request, and that is their call, not yours.

### 4. Write each story

Five sections in the body, acceptance criteria in their own field, per `backlog-conventions.md`. A full worked example is in [EXAMPLE.md](EXAMPLE.md); read it before writing the first story of a session.

Two rules break most often:

- **Acceptance criteria never go in the body.** Separate field, `Given … when … then …`.
- **Requirements are business-level.** State what must be true, not the schema, the endpoint shape or the mechanism. Those go stale between writing and building, and a story that specifies them is a story that will be wrong before it is picked up.

Cite requirement IDs in Context. That citation is what the audit reads.

### 5. Estimate

Fibonacci, per the conventions. Estimate relatively across the Feature's slices before reaching for absolute numbers: which of these is the smallest, and which is roughly twice it.

An estimate above 8 sends the story back to step 2. Do not record it and move on.

### 6. Quiz the user

Per Feature, present the slices as a numbered list: title, one line on what it delivers, points, and which requirement IDs it carries. One line per story, never the bodies. The five sections and the acceptance criteria are what step 7 publishes, and a user approving granularity is deciding on the cuts, not proofreading forty paragraphs.

Flag separately the slices the unhappy-path sweep produced that are not in the register. Ask whether the granularity is right and whether anything should merge or split.

Iterate until approved.

### 7. Publish idempotently

Publish approved stories with the `create` operation, under their Feature, with body, acceptance criteria, estimate and tags.

**Match on the hierarchy code before creating.** Grooming gets re-run: a Feature is reworked, a title is sharpened, a session is repeated after an interruption. Look the code up first with the `lookup` operation and `update` in place where it exists.

This is not tidiness. A recreated story loses its blocking edges, its comments, its state and its history, and it loses them silently: the board still looks right, and `/map-dependencies` has to run again from nothing. Preserving the item is what makes the chain re-runnable.

Leave stories in the backlog. Scheduling belongs to `/plan-release` and `/plan-sprint`.

### 8. Update the map

Append each published story to `docs/delivery/backlog-map.md`: code, identifier, points, requirement IDs.

Then report: how many stories per Feature, the total points, and the specific stories that need the user (a contract gap from the sweep, an estimate over 8 you could not split, a publish that failed). Not the stories themselves. They are on the board and in the map.

## Done when

- Every Feature in scope holds slices that pass all four tests in step 2.
- The unhappy-path sweep ran against every Feature by name, and what it produced was reported to the user.
- Every story has five body sections, acceptance criteria in the field, an estimate of 8 or less, tags, and at least one requirement ID.
- Re-running the session updated items in place rather than creating duplicates.
- The map carries every story.

## Hand off

Tell the user: **`/map-dependencies`** once every Epic has been groomed, not before. Edges can only be set between items that exist.
