---
name: debug
description: "[OMCP] Root-cause analysis with hypothesis tracking and smallest-fix output."
orchestrates-agents: "debugger, tracer, verifier"
---

# [OMCP] Debug

Use this plugin skill to isolate a bug, regression, or confusing runtime
behavior. The skill returns a diagnosis and the smallest next action; it does
not apply fixes unless the user asks.

## Agent orchestration

This skill coordinates `debugger` for reproduction and diagnosis, `tracer` for
causal paths, and `verifier` for confirming the smallest fix path.

## Run

1. Restate the failure in one sentence: observed vs expected, where.
2. Gather real evidence first:
   - failing test output
   - relevant log lines
   - recent diff (`git log --oneline -20`, `git diff HEAD~5`)
3. List 2-3 hypotheses ordered by prior probability. For each:
   - what evidence would confirm it
   - what evidence would falsify it
   - the cheapest discriminating probe
4. Reproduce narrowly when possible.
5. Distinguish symptom from root cause.
6. Propose the smallest next action. No broad rewrites before isolating the
   cause.

## Output format

```
Observed failure: <one sentence>
Hypotheses:
  1. <name> — confidence <H/M/L>
     evidence for: ...
     evidence against / gaps: ...
  2. ...
Current best explanation: <one sentence + evidence anchor>
Smallest next action: <one concrete step>
```

## Goal

- prefer real evidence over guesses;
- separate symptom from root cause;
- escalate to `trace` when the failure is causal/architectural and needs
  competing hypothesis lanes.
