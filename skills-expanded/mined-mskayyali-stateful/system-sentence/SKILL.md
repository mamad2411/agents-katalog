---
name: system-sentence
description: Produce and confirm a structural system sentence describing what a software feature or surface is as an object that exists over time, with enough temporal and lifecycle structure to generate 3–5 materially distinct conditions. Use at the start of Stateful work, when a description is feature-framed or flow-framed, or when an existing-feature audit lacks a clear structural anchor. Do not use for static marketing pages or as generic prompt optimisation.
---

# System Sentence

Produce a structural sentence at feature or surface scale. Do not list the full condition map until the user confirms it.

## Procedure

1. Read `STATEFUL.md` if present. If it already contains a sentence, ask before replacing it.
2. Classify the input as feature-framed, flow-framed, or structural.
3. Check altitude. If it describes a whole product, narrow to one feature or surface. Use a separate cross-cutting inventory for recurring product-wide conditions.
4. Gather only missing raw material in one round:
   - time: schedules, windows, deadlines, expiries;
   - lifecycle: creation, resolution, cancellation, expiry, supersession, abandonment;
   - channels: email, push, other people, devices, or systems;
   - completion differences: changed data, actor, session, permission, dependency, or elapsed time;
   - surfaces: every place the system presents itself.
5. Cite the source of each answer when known. Mark unsupported answers as assumptions.
6. Draft a 15–35 word sentence describing what the system *is*, not what it helps a user do or the order of steps.
7. Extract structural verbs and time-bearing nouns. Derive 3–5 materially distinct lifecycle conditions directly from them.
8. If derivation is thin or relies on facts absent from the sentence, revise the sentence.
9. Present the sentence, structural terms, derived conditions, evidence/assumptions, and why it works. Stop for confirmation.
10. After confirmation, update `STATEFUL.md` with the sentence, raw material, evidence, and known unknowns. Do not start the condition inventory unless the user asks.

## Output

```text
Classification: <feature-framed | flow-framed | structural>

Proposed system sentence:
<sentence>

Structural terms:
- <term>

Initial lifecycle conditions:
- <condition>

Evidence and assumptions:
- <source or explicit assumption>

Why it works:
<one or two lines>

Confirm or adjust?
```

## Done gate

- The sentence is at feature or surface scale.
- Three to five materially distinct conditions derive directly from it.
- Sources and assumptions are visible.
- A human confirms it before write-back or listing.

## Failure modes

- Feature language such as “helps,” “lets,” or “allows.”
- A sequence disguised as a sentence.
- Whole-product altitude.
- A sentence that lists states instead of generating them.
- Treating assumptions as discovered facts.
- Continuing before confirmation.
