---
name: scope-decision-form
description: "Close any investigation or scope discussion with a one-page decision form: Goal, What we learned, Decision, One next action, Done when, Do not do. Use when research ends, when a question is answered, or when findings must become a decision instead of a pile of documents."
argument-hint: "[optional topic or question the form closes]"
---

# Scope decision form

Research produces facts. A decision form produces the end of the work: one
decision, one next action, one visible finish line. Long documents are the
evidence trail, not the deliverable.

## When to use

- Ending an investigation ("what does this mean for us?", "which provider?")
- Closing a scope discussion once the answer exists
- Turning a research pile into a decision for an owner
- After a review round that changes a decision (rewrite in place)

## The form

```text
Goal:
What did we learn:
Decision:
One next action:
Done when:
Do not do:
```

### Each field, in plain words

- **Goal** — the question or objective this work closes. One sentence. If no
  decision is needed, say so plainly here.
- **What did we learn** — the facts that changed the answer. Tag each claim
  so the reader can trust it: `[verified-live]` (someone tested it),
  `[documented]` (authoritative source, untested), `[inferred]` (extrapolation
  or single source).
- **Decision** — what we are doing now, in one or two sentences. Not a
  recommendation: the decision. If the owner must still decide, name them and
  the exact input they need (a quoted option list beats an open question).
- **One next action** — the single concrete next step. Startable tomorrow,
  with the place or file named. Not a list: the one thing that changes the
  outcome.
- **Done when** — the observable result that proves the decision landed. A
  test, a recorded value, a live check — not "when it's reviewed."
- **Do not do** — what was deliberately rejected and why, one line each.
  This stops the same debate restarting next week.

## Operating rules

- Fill every field. A blank is a missing part of the decision.
- Write the form after the evidence exists, not before. If research is still
  open, name the missing fact instead of guessing a decision.
- Keep it one screen: one or two sentences per field. Detail lives in the
  linked evidence trail, not the form.
- Name the evidence. Every fact in "What did we learn" cites its source (a
  file path, a probe result, a vendor page) so nobody re-runs the research.
- A "no" decision still completes the form: Goal states the question,
  Decision says no, One next action is whatever follows, Done when says how
  we will know, Do not do lists what the no rules out.
- After a review round that changes the decision, rewrite the form in place
  rather than leaving stale copies around.

## Example — filled

```text
Goal:              Can Apex provide equity quotes?
What did we learn: [verified-live] Apex has no equities market-data endpoint;
                   [documented] Apex expects clients to bring their own provider.
Decision:          Use Alpaca for quotes. Use Apex for account data and execution.
One next action:   Confirm Alpaca feed access in sandbox and production.
Done when:         The feed tier and display rights are recorded.
Do not do:         Do not compare replacement vendors yet.
```