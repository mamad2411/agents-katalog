---
name: agent-platform-detections
description: >-
  Write detections whose subject is the agent platform itself — sandbox escape,
  orphaned processes, artefact cache tampering, secret exposure — and compare
  them against a generic volume anomaly on the same events. Use when the thing
  being attacked is the harness rather than the application.
allowed-tools: Read, Grep, Glob
---

# A generic anomaly score gives an escape sequence 0.07

An escape from an agent sandbox is seven quiet events. It does not look like
volume, it does not look like a spike, and a generic anomaly detector ranks it
near zero. Detections whose subject is the platform are specific by necessity,
and each of them names a mechanism rather than a statistic.

## When to use this

Any estate running agent workloads on shared infrastructure, and after any
incident where "we would have seen it" was asserted without a named rule.

## Procedure

**1 — Enumerate the platform's own failure modes.** Escape from the sandbox,
processes that outlive their tool call, artefact cache contents changing between
runs, credentials appearing in output, tools invoked outside the manifest.

**2 — Write one named rule per mechanism.** Each with the specific condition it
matches — a process tree deviating from the baseline, a PID alive after its call
returned, a manifest hash mismatch. Named rules can be argued with; scores
cannot.

**3 — Run them against a real sequence.** All the rules that should fire, should.
Record which fired and on which event, because that mapping is what an analyst
uses to reconstruct.

**4 — Score the same sequence with a generic anomaly detector.** Report both
numbers side by side. The comparison is the argument for writing platform
detections at all.

**5 — Check each rule's data dependency.** A cache-diff rule needs a manifest; an
orphan rule needs process accounting. A rule whose input is not collected is a
plan.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_platform_detections.py`](scripts/agent_platform_detections.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
  t  rule                                process
  3  ptrace attach to a non-child        solve.py
  4  LD_PRELOAD on a spawned process     solve.py
  5  non-harness write to the RPC path   x.so
  5  process outside the baseline tree   x.so
  7  process outside the baseline tree   sidecar

generic anomaly score for this run: 0.07  (seven syscalls is unremarkable)
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
  "mechanisms": ["str"],
  "rules": [{"name": "str", "condition": "str", "requires": "str"}],
  "sequence": [{"event": "str", "rules_fired": ["str"]}],
  "generic_anomaly": {"score": 0.0},
  "coverage": {"fired": 0, "expected": 0, "missing_inputs": ["str"]}
}
```

## Failure modes

- **Relying on a generic anomaly detector.** The sequence is quiet by
  construction.
- **Rules whose inputs nobody collects.** Check the pipeline, not the rule.
- **One rule for "escape".** Escape is several mechanisms with different
  evidence.
