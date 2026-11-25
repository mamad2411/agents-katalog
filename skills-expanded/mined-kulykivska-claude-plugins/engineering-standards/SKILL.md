---
name: engineering-standards
description: >-
  The one standard both the coding work and the reviewers work from: architecture,
  failure handling, security, scalability, performance, naming, data and migrations,
  behaviour analytics, and tests. Also defines review scope (the diff plus the code
  around it) and the one-pass discipline. Load it before writing code and before
  reviewing any, so what is written and what is judged come from the same list.
---

# Engineering standard

One base for writing and for judging. Before this existed, each skill carried its own
idea of what good looks like, so code was written against one list and marked against
another, and the gap arrived as review findings the author had no way to avoid. Where
a repository's own `CLAUDE.md` or `AGENTS.md` is more specific, the repository wins
and this fills the gaps.

## 1. Architecture

- Logic belongs in the layer that owns it: transport handles transport, services
  orchestrate, domain code holds the rules, and data access stays in the data layer.
  Business logic in a controller or a repository is a finding, not a shortcut.
- Mirror a sibling module before inventing a shape. Two ways of doing the same thing
  in one codebase cost more than either way costs alone.
- Shared contracts stay in step across repositories. A change to a shared schema
  ripples to every consumer, and the clients have to agree on names and payloads.
- New public surface is a decision, not a detail: name it once, and expect to live
  with the name.

## 2. Failure handling (always on)

Every failure mode is handled on purpose. A "nothing happened" path an operator
cannot see in logs and a user cannot see in the UI is a bug even when it compiles.

- No empty catch, no ignored rejection, no silent early return, no swallowed falsy
  response, no dropped `Promise.allSettled` rejection.
- Log at the level the situation deserves: `warn` for expected-but-notable, `error`
  for something needing a human, `debug` for benign detail.
- Surface terminal failures to the caller rather than leaving them hanging. In a UI
  that means a visible failure state, not a blank page.
- Observability writes are the one exception in the other direction: they log and
  swallow, because measuring something must never break it.

## 3. Security

- No secrets, tokens or keys in code, logs or error messages.
- Validate and authorise every input and endpoint. Admin surfaces are actually
  gated, not hidden behind an unguessable path.
- No string-interpolated SQL, no unsafe deserialisation, no shell interpolation of
  user input.
- Never log personal data, message contents or payment identifiers.

## 4. Scalability

- No N+1 queries: batch or join, and check the query count when a loop touches a
  database.
- Every list endpoint paginates. Every result set is bounded — a time window bounds
  the range, not how many rows fall inside it.
- Retried handlers are idempotent, keyed on the business fact rather than the
  delivery attempt.
- Nothing blocking on a hot path; no shared mutable state across requests.

## 5. Performance

- Avoid repeated work: cache or memoise what is stable, and invalidate on write.
- No O(n²) where O(n) fits; no needless allocation per row.
- Async I/O, minimal payloads, an index for each new query pattern.
- Measure before optimising anything non-obvious, and say what you measured.

## 6. Naming, magic values, and smells

- Domain names, not `normalize` / `process` / `handle` / `data2`.
- No magic strings or numbers: extract to named constants, and compare union members
  through the map the union is derived from.
- No dead code, no leftover debug output, no duplication of an existing helper.
- No redundant runtime type checks and no defensive re-sanitisation where the type
  system or the contract already guarantees the shape.
- Comments explain *why*. A comment restating the line above it is noise; the reason
  behind a surprising decision is the thing worth keeping.

## 7. Data and migrations

- Schema changes go through a reviewed migration.
- Forward-only, expand then contract, for anything destructive.
- Concurrent index creation on large production tables.
- Check the migration number against the main branch before pushing.

## 8. Behaviour analytics

Every feature added and every change to shipped logic emits its behaviour events in
the same change: entry, success, failure, drop-out. Reuse the project's existing
taxonomy, name events after mechanics the product actually has, and never let a
tracking failure break the flow it measures. Verify the events arrived rather than
assuming the call fired.

## 9. Tests

- The project's real gate, with the flags CI uses. Green under a different command is
  not green.
- A test per behaviour, not per method. The failure branch matters more than the
  happy path, because nobody drove that one by hand.
- When a dependency is added to a class, fix every test that constructs it rather
  than leaving a silent `undefined` behind.

---

# How review works

## Scope: the diff, and the code it lives in

Review the diff, **and** read the files it touches in full, **and** look at the direct
callers and callees of what changed. A defect two lines above the diff is still a
defect, and scoping strictly to changed lines is how it survives review after review.
This is a deliberate widening: the reviewer is expected to find things that were
already there.

Report in two sections, because they carry different obligations:

- **In this change** — everything the diff introduced. Fix all of it.
- **Pre-existing, found while reading** — defects in the surrounding code. Fix the
  small and safe ones; for anything larger, report it with a suggested fix and let the
  author decide, so the change stays reviewable. Never silently expand the diff.

Do not wander further than callers and callees. "The whole repo" is not a scope, and a
review that never ends is a review nobody runs.

## One pass, not a loop

A review is one analysis, one fix pass, one verification. Not find-fix-rerun until
nothing new turns up.

1. **Collect the scope** once: the diff range, the touched files, the callers.
2. **Analyse every dimension over it in one go** — architecture, failure handling,
   security, scalability, performance, naming and smells, data, analytics, tests. Fan
   the dimensions out as parallel subagents for a large diff, inline for a small one.
   Either way it happens once.
3. **Dedup and verify**: re-read the hunk, check the caller, drop what does not
   survive. A finding that cannot be stated as "input X gives wrong result Y" is a
   suggestion, not a finding.
4. **Fix everything** confirmed, in one pass.
5. **Verify once**: build, tests, linter, formatter.

Re-analysis happens only if step 5 fails, and then only over what it flagged. Findings
that appear while fixing join the list; they do not restart the analysis.

## Severity, so the report is usable

- **Blocker** — wrong behaviour, data loss, a security hole, a silently vanishing
  failure, an unbounded query. Fixed before the push.
- **Should fix** — a real problem with a workaround or a small blast radius.
- **Nit** — style and consistency. Fix it while you are there; never block on it.

Each finding: `file:line`, one sentence on what is wrong, and the concrete failure it
produces. End with a verdict: clean, or the list of blockers.
