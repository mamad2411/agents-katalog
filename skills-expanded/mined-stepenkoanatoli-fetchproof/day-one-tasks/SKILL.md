---
name: day-one-tasks
description: Turns each KNOWN-UNKNOWN in a Fetchproof project into the first tasks of the build - the day-one verification step its row names becomes a task, a smoke test or a guarded check, done before anything that depends on it. Use at the start of phase 2, when planning the first build steps from research/BRIEF.md, or when the user asks what to do first.
---

# Day-one tasks

A known unknown is an honest gap: the fact was unreachable in phase 1 (login-walled,
private, paywalled, binary), and its row in `research/DISCOVERY.md` names how to verify
it on day one. Phase 2 starts by doing exactly that.

## Steps

1. List them: the brief's **Known unknowns** section, or every `KNOWN-UNKNOWN` row in
   `research/DISCOVERY.md`.
2. For each, write one task, first in the plan:
   - **What is verified** - the row's question.
   - **How** - the row's day-one step, as a command, a smoke test, or a check in code.
   - **What depends on it** - the design decisions that wait for the answer.
   - **If the answer differs from the assumption** - what changes.
3. Do these tasks before the work that depends on them. Work that depends on none of
   them may proceed in parallel.
4. Record each outcome. If a day-one check reaches a page that owns the fact, that is a
   `fact-request` for the collector, so the answer enters the corpus as evidence - a
   builder's observation is a measurement of this system, not a capture of the source.

## Rules

- Never quietly assume the favourable answer. A known unknown that is built over without
  its check has become an unlabeled gap.
- A check that cannot run yet (no account, no access) stays a task, at the top, with
  what it blocks.
