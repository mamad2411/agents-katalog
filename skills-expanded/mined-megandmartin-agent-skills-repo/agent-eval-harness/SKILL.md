---
name: agent-eval-harness
description: Builds and runs a mini eval for any skill or agent task — 3–5 test prompts, an expected-behavior rubric, a pass threshold set before running, then a scored verdict table. Use when the user says "eval this skill", "does this actually work", "test the agent on this", "build an eval", or before trusting any new skill, prompt change, or model swap. Don't use for choosing which model tier to run once the eval exists — that's model-cost-optimizer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Evals, Testing, QA, Measurement]
    related_skills: [model-cost-optimizer, prompt-debugger, skill-author-coach]
---

# Agent Eval Harness

"It seemed to work when I tried it once" is not evidence. This skill builds the smallest eval that still means something: 3–5 realistic test prompts, a rubric written before any run, a pass threshold you commit to in advance, and a verdict table you can re-run after every change. This is the course's core discipline — nothing about an agent is "good" until it passes YOUR eval.

## When to Use

- A new skill just shipped (including from `skill-author-coach`) and needs proof it works.
- Before and after any prompt, skill, or model change — the eval is the before/after instrument.
- The user asks "is the agent good at X?" and the honest answer is "let's measure."
- A recurring job is being handed to a cheaper model or a Paperclip agent and needs an acceptance bar.
- **Not for:** picking the cheapest passing model (`model-cost-optimizer` — it consumes this harness), or diagnosing WHY a failing output fails (`prompt-debugger`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Create eval file | Write `evals/<task-name>.md` (cases + rubric + threshold) |
| Run one case | Give the agent the test prompt verbatim in a FRESH session |
| Score a case | Judge output against rubric criteria: 2 = meets, 1 = partial, 0 = miss |
| Compute result | `score = points earned / points possible` per case; case passes at ≥80% |
| Verdict | PASS if passing cases ≥ threshold set in step 3, else FAIL |
| Re-run | Same eval file, verbatim, after every skill/prompt/model change |

## Procedure

1. **Define the job in one sentence** — "Given [input], the agent should produce [output] that [quality bar]." If you can't write this sentence, you're not ready to eval — go clarify the job first.
2. **Write 3–5 test prompts** — realistic, varied, and fixed before any run: at least one easy/typical case, one hard case (messy input, ambiguity), and one boundary case (input the skill should REFUSE or route elsewhere — the Don't-use-for clause, tested). Write them exactly as a user would phrase them, not as ideal specs.
3. **Write the rubric and threshold BEFORE running** — per case, list 3–5 checkable criteria (present/absent facts, format matches template, correct refusal, no fabrication). Score each criterion 0/1/2. Commit the pass threshold now — default: 4 of 5 cases pass (or 3 of 3–4), each case needing ≥80% of rubric points. Writing the rubric after seeing outputs is grading your own homework.
4. **Run each case in a fresh session** — one prompt per clean context so cases can't contaminate each other. Capture the full output verbatim into the eval file. Same model, same skill version, same settings across all cases.
5. **Score against the rubric only** — go criterion by criterion, cite the line of output that earns each point. Charm, length, and confidence earn nothing that isn't in the rubric. Note every failure's symptom in one line — this feeds `prompt-debugger`.
6. **Render the verdict table** — fill the template below. Verdict is mechanical: passing cases vs. committed threshold. No "close enough" upgrades after the fact.
7. **File it for re-use** — save prompts + rubric + results in `evals/<task-name>.md`. This exact eval re-runs after every future change; that's the whole point. If the verdict is FAIL, hand the failing cases to `prompt-debugger` — do not ship.

## Output Template

```
## Eval: <task/skill name> — <date>
Model: <model> | Skill version: <x.y.z> | Threshold: <n>/<total> cases

| # | Case (short) | Rubric points | Score | P/F | Failure symptom |
|---|---|---|---|---|---|
| 1 | typical: <...> | 8 | 7 (88%) | PASS | — |
| 2 | hard: <...> | 10 | 5 (50%) | FAIL | <one line> |
| 3 | boundary/refusal: <...> | 4 | 4 (100%) | PASS | — |

VERDICT: PASS | FAIL (<passing>/<total> vs threshold <n>)
Next action: <ship | prompt-debugger on cases X,Y | re-run after fix>
Eval file: evals/<task-name>.md
```

## Pitfalls

- **Rubric written after the outputs** — you unconsciously grade toward what the agent produced. Recovery: throw the scores out, rewrite the rubric blind against the job definition from step 1, re-score the captured outputs fresh.
- **All-easy test set** — 5/5 pass because every case is the happy path. Recovery: require the hard case and the refusal/boundary case in every eval; if the skill has never failed a case, the eval is too soft to be load-bearing.
- **Contaminated sessions** — running all cases in one conversation lets case 1's context prop up case 3's answer. Recovery: invalidate the run, re-run one case per fresh session.
- **Moving the threshold post-hoc** — "3/5 is probably fine" after committing to 4/5. Recovery: the threshold from step 3 stands; if it was genuinely wrong, change it in the eval file with a dated note, then re-run the FULL eval under the new threshold.
- **Eval drift** — the skill changes for weeks but the eval never re-runs. Recovery: re-run the saved eval after every skill/prompt/model change; a stale green result is a red result.
- **Unscoreable criteria** — rubric lines like "output is high quality" that two graders would score differently. Recovery: rewrite each criterion as a check a stranger could apply ("names all 3 stakeholders", "under 200 words", "declines and points to X"); if you can't make it checkable, it doesn't belong in the rubric.

## Verification

- [ ] Rubric and threshold exist in the eval file with a timestamp BEFORE any recorded run
- [ ] 3–5 cases including at least one hard case and one boundary/refusal case
- [ ] Every score cites the output line that earned or lost the points
- [ ] Each case ran in its own fresh session under identical model/skill/settings
- [ ] Verdict follows mechanically from committed threshold — no post-hoc adjustment
- [ ] Every rubric criterion is checkable by a stranger — no "high quality" lines
- [ ] Eval file saved to `evals/<task-name>.md` and re-runnable by a fresh agent verbatim
