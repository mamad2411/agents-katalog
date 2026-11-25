---
name: error-analysis-50
description: "Read 50 real failures by hand, cluster them into classes, fix the largest class, and extend the golden set. Use whenever an AI system's score stalls or its failures are 'mysterious'."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [evals, error-analysis, debugging, verify]
    related_skills: [eval-first-development, prompt-suite-versioning, rag-pipeline-checkup]
    program_weeks: [11]
---

# Error Analysis 50

## 1 · Purpose

Replace guessing at fixes with a counted failure distribution, so engineering time
lands on the failure class that actually costs the most.

## 2 · When to use

- When an eval score stalls and the next lever is unclear.
- Before any "improve quality" effort, prompt or model or retrieval.
- After any incident: the 50 reads turn an anecdote into a distribution.

## 3 · Inputs

- A scored system (`eval-first-development`) and its per-case results file.
- 50 failing or borderline cases. Fewer if the system is young, but never zero.
- A spreadsheet or table for the count.

## 4 · Procedure

1. Pull the 50 most recent failures (or lowest-scoring cases). Recent, not
   cherry-picked, you want the distribution as it is, not as you remember it.
2. Read each one fully: input, expected, actual, and the intermediate state
   (retrieved chunks, tool calls) where they exist. Do not skim.
3. Assign each failure exactly one class. Invent classes as you go; keep a class
   only when a second case joins it. Common starters: wrong-source retrieval,
   format drift, hallucinated field, truncation, instruction-ignored, tool mis-call,
   ambiguous-input (the user's fault, not the model's).
4. Count. The table, class × count, is the deliverable. Sort descending.
5. Fix **the largest class only.** Write the hypothesis: "fixing chunk splits at
   tables removes class A (14 of 50)." Resist fixing two classes at once, you will
   not be able to attribute the movement.
6. Add 2 to 4 representative cases of that class to the golden set with a commit
   message naming the class. The class can now never silently return.
7. Re-run the eval. Record the delta and which class moved. If the class did not
   shrink, the hypothesis was wrong, revert and take the next class.
8. Repeat until the gate clears or the top class is `ambiguous-input`, at which
   point the spec, not the system, needs work. Say so, with the table as evidence.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "I already know what the failures are." | You know the failures you remember. The count remembers all of them. |
| "Reading 50 outputs is a waste of a day." | It is the cheapest day in AI engineering. Teams burn weeks fixing the wrong class. |
| "The failures are all unique." | Unclassifiable usually means un-read. Read ten more; classes emerge. |
| "Let's fix the three small classes first, quick wins." | Three classes of 2 cases each are 6 cases. The top class is 14. Do the math. |

## 6 · Red flags

- Fixes are proposed with no failure table behind them.
- Classes named by vibe ("bad answers") instead of mechanism ("retrieval missed
  the policy section").
- The golden set has not grown in a month of active debugging.
- The same failure class reappears after being "fixed" (it was never added to the
  golden set).

## 7 · Verify

- A dated failure table exists: class × count over ≥ 50 read cases.
- The fix under work names the class it targets and its case count.
- The golden set grew with cases from the fixed class, with a commit message.
- The post-fix eval delta is recorded.

## 8 · ZoroLogistics example

Week 11's workshop on the extraction system at 0.90: 50 failures read. Classes:
`scan-noise-misread` 17, `multi-line-consignee` 12, `currency-symbol-strip` 9,
`ambiguous-field-in-source` 7, `format-drift` 5. The fix targets scan noise
(preprocessing + one few-shot), moving the score to 0.94. `ambiguous-field-in-source`
goes to the spec owner, seven cases where even humans disagree, and becomes a
documented "undefined behavior" list, not a model bug.

---
© 2026 Zorost Intelligence LLC · zorost.com
