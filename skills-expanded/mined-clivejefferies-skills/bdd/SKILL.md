---
name: bdd
description: Use whenever the user describes a new feature, screen, or behavior they want built and wants the agent to write code or tests for it. Before implementing, this skill has the agent judge whether anything unanswered would actually change the architecture, data model, permissions, or acceptance criteria — and only then asks targeted clarifying questions, separating true blockers from assumptions it can document and proceed with. Confirms acceptance criteria, then translates them into a BDD (Given/When/Then) scenario file before any implementation code is written. Trigger for requests like "add a feature that lets users X", "build a screen for Y", "I want the app to do Z when...". Skip for trivial UI-only requests, pure bug fixes, refactors, or requests that already include full acceptance criteria.
---

# Feature Intent

Turns a loosely-described feature request into confirmed BDD scenarios
before any implementation code gets written — without turning every
request into an interrogation.

## Step 1: Decide if clarification is even needed

Before asking anything, check: **could an unanswered question materially
change the implementation?** Specifically, would the answer change the
architecture, data model, API shape, permissions/security, persistence,
UX flow, or what counts as "done"?

- If no — the feature really is obvious ("add pull-to-refresh") —
  proceed straight to implementation. Don't manufacture questions to
  seem thorough.
- If yes — ("users can archive projects" implies data model, visibility
  rules, permissions, undo, etc.) — continue to Step 2.

## Step 2: Ask only high-impact questions

Ask about things whose answers would change one of the dimensions above.
Do not ask about things the user clearly doesn't care about (button
color, minor copy) unless they raise it.

Good sources of high-impact questions:

- **Edge cases**: empty state, invalid input, no network, very
  large/small values.
- **Permissions & security**: who can do this, what happens if they're
  not authorized.
- **Persistence**: does this survive app restart, sync across devices,
  need migration for existing data.
- **Interaction with existing behavior** — new features rarely exist in
  isolation. Consider: offline mode, permissions, analytics, navigation
  and deep links, accessibility, feature flags, existing APIs. Ask
  specifically how the new feature should behave alongside these where
  it's plausible they'd conflict.
- **Cancellation / partial completion** — if the feature involves any
  multi-step or async operation, what happens if it's interrupted
  halfway.
- **What must explicitly never happen** — a failure mode worse than
  simply not working (e.g. double-processing, silently corrupting
  state, showing stale data as fresh).

One or two sharp questions beat five perfunctory ones.

## Step 3: Separate blockers from assumptions

Split anything unresolved into two buckets:

- **Blocking** — cannot implement correctly without an answer. Wait for
  the user before proceeding.
- **Assumption** — can proceed safely if documented. If the user says
  "whatever you think is best" (or doesn't answer a lower-stakes
  question), pick a sensible default, state it plainly, and move on.
  Don't stall the conversation waiting for input on things that don't
  need it.

## Step 4: Confirm acceptance criteria

Once blockers are resolved, summarize in plain language:

```
Confirmed behavior:
- ...
- ...

Assumptions (documented, not confirmed):
- ...

Feature is considered complete when:
- ...
- ...
```

This is the checkpoint the user reviews. It stays in plain English —
not Gherkin yet — because prose is what people actually read carefully;
once something looks like a test, review tends to become a syntax
check rather than a content check. Get explicit confirmation on this
summary before moving to Step 5.

## Step 5: Translate into BDD scenarios

Once confirmed, generate Given/When/Then scenarios directly from the
Step 4 summary — one scenario per confirmed behavior, plus one per
edge case or "must never happen" item that came out of Step 2/3.

- Each "Feature is considered complete when" bullet should map to at
  least one scenario.
- Each "must never happen" item becomes its own scenario, asserting the
  forbidden outcome does not occur — these matter as much as the happy
  path scenarios, often more.
- Assumptions get folded into the `Given` of the relevant scenario
  (e.g. an assumed default becomes the starting state), not left
  implicit.
- This is standard deterministic BDD — no judge model, no pass-rate
  threshold, no hard/soft assertion split. Every "Then" here should be
  checkable by running the app once. If a "Then" can't be checked
  deterministically, that's a sign the acceptance criteria in Step 4
  were still too vague — go back and tighten them rather than writing
  a fuzzy scenario.

Show the scenarios to the user before implementing. This is a second,
cheaper checkpoint — catching a wrong scenario here is much cheaper
than catching it after the code and tests are both written against it.

Before showing them, run a quick traceability check:

- Every acceptance criterion from Step 4 maps to at least one scenario.
- Every scenario maps back to an agreed acceptance criterion or
  documented assumption — nothing in a scenario should be new
  behavior the user never saw.
- If a scenario introduces something not traceable to Step 4, either
  fold the missing item back into Step 4 and re-confirm it, or drop it
  from the scenario — don't let it slide through unflagged.

## Step 6: Implement — and stay in scope

Implement against the confirmed scenarios from Step 5. If a related
idea comes up that's useful but outside what was discussed, mention it
as a suggestion afterward rather than building it unasked. Do not
expand scope on your own judgment mid-implementation.

## Notes

- This is intentionally lightweight — no separate spec schema, scripts,
  or judge-model machinery required. The Step 4 summary and Step 5
  `.feature` file are the artifacts.
- On a team where scenarios need review by someone other than the
  requester, save the Step 5 file alongside the feature in the repo
  (e.g. `features/<feature>.feature`) so it's reviewable and diffable
  later — worth doing even solo, since it becomes your regression
  reference the next time this feature is touched.
- The whole point of Step 1 is to prevent this skill from becoming
  friction on obvious requests. If it's asking questions — or writing
  scenarios — for something simple, it's being used wrong.
- This skill assumes deterministic behavior (a normal app feature). If
  the feature involves an LLM/agent acting non-deterministically at
  runtime, standard Given/When/Then and single-run pass/fail don't
  apply cleanly — that needs a different approach (multi-run pass-rate
  thresholds and separate judge-model evaluation for any non-
  deterministic "Then"), which this skill does not cover.