---
name: agentic-harness-loop
description: >-
  Build and check the plan-act-verify loop that turns a model into a harness —
  including the exit condition, the parser, and an independent verifier that
  decides what the loop is allowed to accept. Use when writing an agentic
  pipeline, or when a loop reports success on work nobody checked.
allowed-tools: Read, Grep, Glob
---

# The loop is yours; the model is a component in it

A harness is four moves — plan, act, verify, stop — and the security engineer
owns three of them. What the loop **accepts** is decided by the verifier, not by
the model, and a loop with no verifier accepts whatever came back and reports
success.

## When to use this

Whenever you are about to put a model in a for-loop: triage, remediation,
detection authoring, anything that iterates until it is satisfied.

## Procedure

**1 — Write the exit condition before the prompt.** A loop whose exit is easier
than the work will take the exit. Do not offer the model a way to declare
itself done; decide that from the outside, on the artefact.

**2 — Parse defensively, because parsing is the harness's job.** Asked for one
line, a small model returns the whole function and a larger one returns a fenced
block. Both are reasonable readings. Take what you need from what arrives rather
than requiring the model to do you a favour.

**3 — Write the verifier as an independent check.** Independent means it does
not ask the model whether the answer is good. It examines the artefact: does the
line use a placeholder, does the test pass, does the exploit stop working.

**4 — Test the verifier against a correct answer you did not expect.** This is
the step that gets skipped. A verifier that accepts only one spelling of correct
rejects real work and burns the budget doing it — check `%s`, `:name` and `$1`
before shipping a check for `?`.

**5 — Test it against a plausible wrong answer.** Something that reads like a
fix and is not — an escape function wrapped around concatenation. If the
verifier accepts it, the loop ships it, reports success, and the trace looks
clean.

## Example

**Input** — the fixture committed at the top of [`scripts/agentic_harness_loop.py`](scripts/agentic_harness_loop.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the loop, wired: ['plan', 'act', 'verify', 'stop']
backend  : replay
steps    : 1
accepted : return DB.execute("SELECT * FROM bookings WHERE ref=?", (ref,))
verified : None   <- nothing checked it

The loop stopped because the model produced something, which is not the
same as producing something correct. Whatever came back was accepted.
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "loop": {"moves": ["plan", "act", "verify", "stop"], "max_steps": 0, "exit_owned_by": "harness|model"},
  "parse": {"expected": "str", "shapes_seen": ["str"], "strategy": "str"},
  "verifier": {"independent": true, "accepts": ["str"], "rejects": ["str"]},
  "runs": [{"verifier": "none|present", "steps": 0, "accepted": "str", "verified": null}]
}
```

Report the unverified run too. The pair is the lesson: the same model and the
same prompt, with and without something checking the answer.

## Failure modes

- **Offering the model a DONE exit.** It will take it on the first turn.
- **A verifier that accepts one spelling.** It rejects correct work, repeatedly,
  and the budget goes on retries.
- **Asking a model to judge the answer.** That is a second opinion, not a
  verification.
