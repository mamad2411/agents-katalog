---
name: eval-judge
description: >-
  Build a grader for an agent's or model's outputs that agrees with the user's own judgment: collect
  about 20 real runs, have the user label them, write a rubric, run the grader, measure agreement,
  fix the disagreements, repeat, and check on a held-out set. Works with any model or CLI. Use for
  "build an eval", "LLM as judge", "grade these outputs", "auto-score the agent", "is the new prompt
  better", or before tuning a prompt or skill by numbers.
---

# Eval judge

A grader that doesn't match the user's judgment makes every later number a lie. This skill builds
one, then proves it agrees with the user before anyone trusts its scores.

## Before you start

- **Cost.** Every grader run calls a model once per output. Estimate runs x outputs x tokens and tell
  the user. Use a model the user is already signed in to (a CLI subscription, a local model).
  **Never use a paid API key without the user's explicit okay for this task**, and agree a spend cap.
- **Code first.** If a property can be checked by code (valid JSON, tests pass, length, a required
  field, a banned word), check it with code. Use a model grader only for judgment calls.

## Procedure

### 1. Collect real outputs

Gather about 20 real outputs of the thing being judged, with their inputs. Real runs beat invented
ones. Include clear passes, clear failures and borderline cases. Save them as one file per case or one
JSONL file: `{id, input, output}`.

### 2. Split off a held-out set

Put about a quarter aside, untouched until step 7. Tuning the rubric on them makes the final check
worthless.

### 3. Get the user's labels

Show the user each working-set case and ask for pass/fail plus one line of why. The why is the raw
material for the rubric. Don't label for them; if the user can't decide, mark it unclear and leave it
out.

### 4. Write the rubric

From the user's reasons, write 3-6 criteria. Each one:

```
<criterion>: pass if <observable condition>; fail if <observable condition>.
Example pass: <short quote>   Example fail: <short quote>
```

The grader returns, per case, JSON: `{"id", "verdict": "pass"|"fail", "failed_criteria": [], "reason"}`.
Ask for the reason before the verdict. Binary verdicts agree far better than 1-10 scores.

### 5. Run the grader

Run it on the working set with any model you can call headlessly, e.g. a CLI in print mode reading
the rubric plus one case per call. Use a fixed prompt and temperature 0 if the tool allows. Save
every raw verdict.

### 6. Measure and fix

Agreement = cases where grader and user match / labelled cases. Also list false passes and false
fails separately: a grader that passes bad output is worse than one that is strict.

For each disagreement, read the grader's reason. Then either sharpen a criterion, add an example of
that case to the rubric, or, if the user's label looks inconsistent, ask the user again. Change one
thing per round and re-run. Stop at about 90% agreement or after 3 rounds.

### 7. Check on the held-out set

Have the user label the held-out cases, run the grader once, and report agreement. If it drops well
below the working-set number, the rubric was overfit: add cases and go back to step 4.

## Report

```
Grader: <model/CLI>   Rubric: <path>   Cases: <n working> + <n held out>
Agreement: working <x%>, held-out <y%>   False passes: <n>   False fails: <n>
Cost per full run: <calls, est. tokens or $>
Known weak spots: <case types it still gets wrong>
```

## Rules

- The user's labels are the ground truth, not yours.
- Never tune on the held-out set.
- Re-check agreement whenever the rubric, the grader model or the kind of output changes.
- No paid API key without the user's okay and a cap.
