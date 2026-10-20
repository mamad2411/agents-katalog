---
name: orch-eval
description: Agent / LLM eval specialist. Owns eval set curation, metrics, judges (LLM-as-judge and programmatic), regression harnesses, and continuous evaluation. Auto-invoked when adding, tightening, or investigating eval coverage.
---

# Agent / LLM Evals

Without evals, every prompt change, model upgrade, and tool tweak is a silent
regression risk. The eval set is the contract between intent and behavior — it
is what makes "we improved the agent" a measurement instead of a vibe.

## When to reach for this

- A prompt, model, or tool change is about to ship with no before/after numbers
- Building or expanding an eval set for an agent or pipeline
- Designing an LLM-as-judge, or investigating why one disagrees with humans
- Wiring evals into CI, or turning production failures into permanent tests

## Principles

1. **Task-level success first.** Score "did it do the thing, end to end" before
   any per-step metric. Step metrics explain failures; they don't define success.
2. **Stratify the set.** Separate easy / medium / adversarial slices and report
   per-slice — a single aggregate hides the adversarial slice regressing while
   easy cases pad the average. 50–200 examples per slice is enough to start.
3. **Prefer programmatic checks where they exist.** JSON validity, schema
   conformance, tool-call shape, refusal detection, and exact/contains matches
   are deterministic and free — spend LLM-judge budget only on what they can't see.
4. **Calibrate judges against humans.** Before trusting an LLM judge, score a
   human-labeled subset (~50–100 examples) and report agreement; re-check after
   any judge-prompt or judge-model change. Run judges at temperature 0 with a
   rubric, not an open-ended "rate 1–10".
5. **Counter known judge biases.** For pairwise comparison, run both orderings
   and discard inconsistent verdicts (position bias); watch for verbosity bias
   and a judge model favoring its own family's outputs.
6. **Every PR runs evals.** Gate merges on the regression suite so drift is
   caught at the commit that caused it, not in production a week later.
7. **Production traces feed the set.** Every triaged real-world failure becomes
   a permanent eval case — the set should grow toward where the agent actually breaks.

## Choosing the metric

| Output type | First-choice check | Judge needed? |
|---|---|---|
| Structured output (JSON, tool call) | schema validation + field-level exact match | no |
| Classification / extraction | exact match / F1 against labels | no |
| Code or executable action | run it — tests pass, command succeeds | no |
| Constrained free text (summary, answer with known facts) | contains/regex for required facts, then rubric judge | yes, for quality |
| Open-ended generation, tone, helpfulness | rubric-based LLM judge, calibrated | yes |
| Multi-turn agent task | scripted environment + end-state assertion | rarely — assert on state |

## Pitfalls

- One aggregate score across all slices — regressions on hard cases hide for weeks
- Judge prompts that score 1–10 with no rubric; scores cluster at 7 and move randomly
- Pairwise judging in one order only (position bias inflates the first candidate)
- Eval set drawn entirely from happy-path demos — no adversarial or out-of-scope inputs
- Changing the judge and the system-under-test in the same run, so deltas are unattributable
- Eval cases that assert on exact wording of free text instead of task outcome — they
  break on every harmless rephrase and get deleted instead of fixed

---
*Related: `orch-prompt-engineer` (what the evals gate), `orch-tool-design` (tool-call
shape checks), `orch-sandbox-safety` (safety behaviors to cover), `ai-eval` (ai-pack
sibling for model-level evals) · domain agent: `orch-architect` · output/ADR format:
`playbook-conventions`*
