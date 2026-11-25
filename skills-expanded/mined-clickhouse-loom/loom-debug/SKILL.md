---
name: loom-debug
description: Finds the cause of a Loom bug before any edit — failing cases from evidence (request id, loom.agent_events, system.query_log, search traces), their pattern, a hypothesis, then a test that fails first. Use when an op, worker, search result or test behaves wrongly. Not for a red CI job (loom-investigate-ci).
argument-hint: "<symptom, request id or failing test>"
metadata:
  internal: true
---

# Debugging Loom

Running code confirms a diagnosis; it is not how you find one. If you cannot predict what a run will show, collect more evidence instead of editing.

```
Diagnosis:
- [ ] Failing cases: 2+ concrete inputs that fail, from evidence
- [ ] Passing neighbours: close inputs that work
- [ ] Pattern: what every failing case shares and no passing one does
- [ ] Hypothesis: the exact change, and the result it predicts for each case
- [ ] Confirmed: a test fails before the change and passes after
```

## 1. Collect the failing cases

Work on a private server and ClickHouse (`loom-dev-setup`), never one someone else owns. Start from the request's ids and join outward; [debug a request](../../../docs/guides/debugging.md) has the full join.

```bash
curl -si -XPOST localhost:<port>/v1/<op> -H 'Content-Type: application/json' -H "X-Request-Id: dbg-$(date +%s)" -d @req.json | sed -n '1,/^\r$/p'
```

| Evidence | Where | Answers |
| --- | --- | --- |
| the op's row | `loom.agent_events` by `request_id` (`operation`, `success`, `error_code`, `latency_ms`, `build_commit`, `args`) | did it run, on which build, with which arguments |
| its statements | `system.query_log` by `log_comment` (`read_rows`, `memory_usage`, `exception`) | what ClickHouse was asked and what it cost |
| a ranking | `memory.search` with the same input and `explain=true` | each hit's `score_components`: its signals, a reranker's move (`rerank_*`) and, when it changed the order, `rank_score_pre_rerank` |
| a write | the row read back, every field; `loom.memory_versions` for its history | what was stored versus what was sent |
| a worker | `ops.health`, the worker's `log_comment = 'worker.<name>'` | whether the pass ran and how far it got |
| the server | the server log line with the same request id | the exception and its stack |

Write each failing case down as input → observed → expected. Find at least one close input that works.

## 2. Find the pattern

Compare failing and passing cases field by field: org or namespace shape, auth on or off, row version, empty versus missing values, list lengths at a boundary, time zone, replica or colour, cache warm or cold. The pattern is the smallest difference that separates them. Read the code path for that difference end to end, including the store statement and the row builder.

## 3. State the hypothesis

One or two sentences: the line or statement that is wrong, why it produces every failing case, and why the passing cases pass. Predict what the fix changes for each case. If the hypothesis does not explain every failing case, it is not the cause yet.

## 4. Confirm

- Write the test first, from a failing case: a unit test with `tests/unit/ch_fake.py` and the clock seam where it fits, an integration test for a read or write path. Watch it fail for the predicted reason.
- Make the smallest fix at the source, and watch the test pass. Re-run the original evidence query.
- A run that contradicts the prediction sends you back to step 1 with new evidence. Do not stack a second change on a wrong first one; revert it.
- Search for the same pattern elsewhere (sibling ops, the other transport, bulk paths): one cause often has several sites.

## Report

The failing cases, the pattern, the cause with `file:line`, the fix, the test that now passes, and the other sites checked.
