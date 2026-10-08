---
name: spec-first-ai-feature
description: "Write the one-page spec for an AI feature, user, golden set, metric, gate, refused tradeoffs, before any code or prompt work. Use when starting any AI feature, agent, or pipeline."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [spec, planning, shaping-the-build, define]
    related_skills: [eval-first-development, prompt-suite-versioning]
    program_weeks: [13]
---

# Spec-First AI Feature

## 1 · Purpose

Force the four decisions that make an AI feature buildable, who it serves, what
"correct" means, how it is measured, and what tradeoffs are refused, onto one page
before any implementation begins.

## 2 · When to use

- Starting any AI feature: extraction, RAG bot, agent, fine-tune, integration.
- When a build has drifted for more than a session without a written target.

Do **not** use for exploratory notebooks whose entire purpose is learning a library.
Label those "spike" and timebox them instead.

## 3 · Inputs

- The feature request, verbatim.
- Access to the requester (or their proxy) for the two questions in step 3.
- One sample of real input data, if any exists.

## 4 · Procedure

1. Create `SPEC.md` in the project root. Use the five headings below, no others.
2. **User & job.** Write who uses the output and what decision or action it feeds,
   in two sentences. If you cannot name the user, STOP and ask.
3. Ask the requester two questions and record the answers verbatim:
   - "Show me three real inputs and the outputs you would accept."
   - "What output would make you reject this on sight?"
4. **Golden set.** Name the file that will hold the accepted input→output pairs.
   Target 20 cases minimum. If three real cases cannot be obtained, STOP: the
   feature is not spec-able yet.
5. **Metric & gate.** Write one measurable definition of correctness (e.g.,
   per-field exact-match accuracy) and the pass value (e.g., ≥ 0.90). One metric,
   one number. Secondary observations (latency, cost) go in a note, not the gate.
6. **Refused tradeoffs.** List what this feature will not sacrifice: e.g. "never
   invent a missing field", "no PII leaves the VPC", "p95 latency under 4 s".
   Write at least one. A spec with no refused tradeoff is a wish, not a spec.
7. **Blast radius.** Write what the feature may write to or send, and what requires
   human approval (deletes, external sends, spend above $X).
8. Show the spec to the requester. Record their "yes" or their edits. A spec nobody
   approved is a draft.
9. Only then begin build work. Point every later dispute at this file; update the
   file when the answer changes.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The request is obvious; spec is overhead." | Obvious requests produce three incompatible demos. The page costs 20 minutes; the wrong build costs days. |
| "We'll know a good output when we see it." | That is the definition of unmeasurable. The gate number is the feature. |
| "The requester is too busy to answer." | Then the feature is not ready to build. Build something with an owner instead. |
| "I can hold the spec in my head." | Your context window forgets. The file does not. |

## 6 · Red flags

- The metric section contains words like "good", "accurate enough", "high quality"
  with no number.
- The golden set is "to be collected later".
- The refused-tradeoffs list is empty.
- The spec was written *after* the first implementation pass and describes it.

## 7 · Verify

- `SPEC.md` exists with all five headings filled.
- The golden-set file exists with ≥ 20 cases or a documented STOP.
- The gate is one metric and one number, approved by the requester.
- Every refused tradeoff names something the team would actually be tempted to do.

## 8 · ZoroLogistics example

Feature: extract bill-of-lading fields. Spec: user = ops clerk clearing exceptions;
golden set = 20 scanned BoLs with field-level answers; metric = per-field
exact-match accuracy, gate ≥ 0.90; refused = "never emit a field value that does not
appear in the document" and "null over guess"; blast radius = writes to staging
table only, no production writes without human review. Week 6's prompt suite then
executes against exactly this contract.

---
© 2026 Zorost Intelligence LLC · zorost.com
