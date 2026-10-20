---
description: Build one ad end to end from a brief — validate, generate, render, verify, report
argument-hint: [a campaign brief path, and/or overrides e.g. "ratios 9x16, skip render"]
---

Build **one** ad, end to end.

Arguments — a brief path, overrides, or both (may be empty): **$ARGUMENTS**
Overrides win over the brief. Say which fields they changed.

The brief is a `campaigns/*/briefs/` path if the arguments name one (merged
over that campaign's `campaign.md`), otherwise whatever this conversation has
established. `/brief` and `/generate` own that resolution — don't restate it.

Given a campaign and no specific brief, don't build the whole folder. Say which
briefs are promoted and ask which one — a campaign is a queue of separate runs,
and `/campaign` is where a queue gets planned.

This command is the whole pipeline in one pass. Each stage has its own command
that owns the detail — follow those files rather than working from memory, and
don't restate their guidance here:

| Stage | Follow | Skip it when |
|---|---|---|
| 1. Validate the brief | `/brief` | — |
| 2. Scaffold and author | `/generate` | — |
| 3. Export | `/render` | the overrides said to |
| 4. Check the pixels | `/verify` | never |
| 5. Hand off | `/report` | — |

## Running them together

**Stop at the first blocker.** If `/brief` comes back *Blocked*, ask the
question and stop — don't scaffold an ad around a missing Hook. If `/render`
fails, diagnose it before writing the report.

**Don't re-ask what's settled.** The brief is validated once, at step 1. Later
stages inherit that result instead of re-deriving the same assumptions.

**Verify is not optional.** Correctness here is visual: an exit code of 0 says
the encoder ran, nothing more. If the overrides skip rendering, say explicitly
that the ad is unverified rather than reporting it as done.

**Fix what `/verify` finds.** A defect found at step 4 gets fixed and
re-verified before the report — that's inside the scope of building the ad.
Design opinions are not: if the ad is technically correct but weak, say so in
the report and offer `/critique` rather than redesigning it unasked.

## Report

Follow `/report`, plus what only this run knows: which fields you inferred or
overrode, what `/verify` found and what you fixed, and any placeholder standing
in for proof the brief didn't supply.

**Report should be as condensed and concise as possible.**

Then offer the next move: `/adjust` for a targeted change, `/variant` to test
one element, `/critique` for a design pass.
