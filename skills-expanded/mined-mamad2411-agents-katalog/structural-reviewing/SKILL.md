---
name: structural-reviewing
description: Use when reviewing code, pull requests, merge requests, design diffs, migrations, endpoint changes, jobs, queues, tests, or operational changes.
---

# Structural Reviewing

Review for structure, not taste. The wrong thing should become impossible or hard to express.

Core rule:

> Block what an attacker or unlucky caller can turn into a catastrophe; for the rest, name the cost and let proportionate trade-offs ship.

## Review order

```md
## Must fix
- Wide blast radius / external control:
- Silent corruption or swallowed failure:
- Irreversible unsafe step:

## Consider
- Cognitive load reduction:
- Simpler representation or deletion:
- Optional hardening:

## Evidence requested
- Test / repro:
- Signal / metric:
- Owner / rollout proof:
```

## Review lenses

- Locality: how far from the diff did you need to look? Hidden distance is a finding.
- Boundaries: parse once, bound size before allocation, re-derive authority, preserve old consumers.
- Silent swallow: empty catch, ignored error, promise with no rejection path, fallback with no signal.
- Caller-controlled unbounded growth: payload, list, recursion, retry, fan-out, queue, cache, N+1.
- Race/replay: check-then-act, unsafe retries, non-idempotent side effects, wall-clock ordering.
- Acquire/release: file, lock, listener, timer, subprocess, subscription, connection, shutdown obligation.
- Blast radius and reversibility: least privilege, containment, flags, expand/contract, rollback compatibility.
- Contract tests: behavior at boundary and decision, not private helper shape.

## Red flags

- “Existing style does it this way” used to add new unchecked input or swallowed failure.
- Reviewing only happy path or naming/style while ignoring boundary and replay risks.
- Demanding ceremony where no real interleaving, external input, or wide radius exists.
- Test added but coupled to internals instead of observable behavior.
