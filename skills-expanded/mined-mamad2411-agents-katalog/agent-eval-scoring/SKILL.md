---
name: agent-eval-scoring
description: >-
  Score an agent's runs on tool-call accuracy and output accuracy, then use a
  model as judge only for what those cannot reach — and validate the judge
  against a labelled subset before believing it. Use when asked how good an
  agent is, or when an eval reports a single number with no denominator.
allowed-tools: Read, Grep, Glob
---

# Three metrics, and only one of them needs a judge

"The agent is 90% accurate" is not a measurement until you say accurate at
what. An agentic run has at least three scoreable surfaces and they fail
independently: it can call the right tools and answer wrongly, answer correctly
having taken a path nobody would approve, or do both well and be scored by a
judge that agrees with itself rather than with the truth.

## When to use this

Before quoting any agent accuracy figure, when choosing between two models or
two prompts, and whenever an evaluation uses a model to grade a model.

## Procedure

**1 — Score tool calls against the expected trajectory.** Exact match on the
tool name *and* its arguments, in order. Report `n` beside the rate.

**2 — Report the two weaker matchers next to it.** Name-only, ignoring
arguments; and order-ignored, treating the trajectory as a set. Both score
higher than exact match on the same runs. Quoting either one alone is how a
tool-call number becomes meaningless — a refund for the wrong amount calls
`refund` correctly.

**3 — Score outputs where ground truth exists.** Exact or normalised match
against the recorded correct answer. Count what you could not score separately
and never fold it into the denominator as a pass.

**4 — Use a judge only for what remains.** Free-text answers with no ground
truth. Give the judge the question, the answer and an explicit rubric, and make
`undetermined` a verdict it is allowed to return — a judge with two options
will invent confidence.

**5 — Validate the judge against the labelled subset.** Run it over the runs
you *do* have ground truth for and report agreement, false passes and false
fails. A judge you have not validated is a second unmeasured model.

**6 — State what none of the three measured.** Cost, latency, and whether the
task should have been attempted at all.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_eval_scoring.py`](scripts/agent_eval_scoring.py). Edit it and re-run: the rates, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
tool-call accuracy          n=6
   exact (name + args)      0.500
   name only                0.667   <- +0.167 for free
   order ignored            0.667   <- +0.167 for free

output accuracy             correct 2  incorrect 3  unscoreable 1  = 0.400

Neither number above needed a model. Only the unscoreable run does.
```

The two weaker matchers score the same and are not forgiving the same run:
name-only passes the refund of 1400 instead of 140, and order-ignored passes
the rebooking that held two seats. Either one quoted alone hides a different
real failure.

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "tool_call_accuracy": {"exact": 0.0, "name_only": 0.0, "order_ignored": 0.0, "n": 0},
  "output_accuracy": {"correct": 0, "incorrect": 0, "unscoreable": 0, "accuracy": 0.0},
  "judge": [{"run": "str", "verdict": "pass|fail|undetermined", "why": "str"}],
  "judge_validation": {"labelled_n": 0, "agreement": 0.0, "false_pass": 0, "false_fail": 0},
  "headline": "str",
  "not_measured": ["str"]
}
```

## Failure modes

- **One number, no denominator.** "90% accurate" over six runs and over six
  hundred are different claims; `n` is part of the metric.
- **Name-only tool matching quoted as tool-call accuracy.** It is the most
  flattering matcher and the least informative one.
- **Unscoreable runs counted as passes.** They belong in their own column.
- **An unvalidated judge.** Agreement with ground truth is the only thing that
  makes its other verdicts worth reading.
- **A judge with no `undetermined`.** Forced into a binary it will answer
  confidently on cases it cannot decide.
- **Self-preference.** A judge grading its own family's output scores it
  higher; report which model judged, always.
