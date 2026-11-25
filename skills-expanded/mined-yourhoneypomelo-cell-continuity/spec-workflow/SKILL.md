---
name: spec-workflow
description: Turn user requests into requirements, decisions, tasks and verified features. Use when the user asks for a new capability, changes or drops one, or when a request is too large for one task.
---

# Specification workflow

Requests become requirements, requirements become tasks, verified tasks ship features.

```text
user request -> requirement (R) -> tasks (T) -> code + tests -> ws verify --done -> feature (F) shipped
                     |                 |
              open question (Q)   decision (D)
```

## New capability

1. Restate the request in one sentence and confirm it with the user if it is ambiguous.
   Unclear points become questions: `ws add question --set question=...`.
2. Add the requirement with an acceptance command or an observable result, in the same turn the
   user stated it. Do not wait until every detail is settled: record the confirmed part now and put
   only the open details in the Idea pool.
3. If the detail exceeds two lines, copy `.agents/template/spec/` to `docs/specs/<slug>/`, fill
   `requirements.md` and set the requirement's Detail to `docs/specs/<slug>/requirements.md`.
4. Record design choices and rejected options with `ws add decision`.
5. Split the work into tasks of a few hours each, each with its own acceptance command. Name in the
   Scope the paths the task changes, `new:<path>` for a file it creates and each outside system it
   touches as `resource:<name>`, for example `services/unpaywall/ new:tests/test_proxy.py
   resource:vps/unpaywall`. Parallel sessions claim tasks by these, and a task with no path in its
   Scope, or with `tree:`, blocks every other session.
6. Add the feature with status `planned`, naming the requirement and tasks.
7. Implement one task, run `ws verify T<n> --done -- <command>`, repeat.
8. When all tasks are done: `ws set F<n> --set status=shipped`.

## Before changing behavior

Write these into the task Scope or the spec before editing code. Each answers a question the next
session would otherwise ask again:

| Item | What to write |
| --- | --- |
| Impact | The callers and consumers of what changes, and the command that listed them (`grep -rn "fetch_pdf" services/`) |
| Keep | Behavior next to the change that must not move, with the test that covers it; with no such test, add one first and see it pass on the unchanged code |
| Change | The behavior that changes, as current and expected |
| Premise | What the change relies on, checked: a route that exists may have no caller, a table may have no writer |

Run the task's acceptance once before the first edit. A failure that was already there is the
baseline: record it in `recovery_notes`, so it is not blamed on the change.

## Questions

A question that changes what the user sees, or needs their authority, stays `open` and blocks the
work it affects. A question about internals is deferred: the work goes on with a stated default,
and the brief shows it so nobody asks again.

```text
ws add question --set "question=Cache size limit?" --set "context=T4 needs a number"
ws set Q3 --set status=deferred --set "answer=default: 500 MB until the user decides"
```

## Changed request

- Small change, same acceptance: edit the requirement text with `ws set`. The log keeps the old text.
- Different acceptance or scope: set the old requirement to `replaced` with a reason, add a new
  one and point affected tasks at it.
- Dropped: set the requirement to `removed`, the feature to `removed` and open tasks to `dropped`,
  each with a reason.

## Retiring a feature

1. Enumerate everything that uses it: callers, tests, configuration, documents, scheduled jobs and
   stored data. Write each command and its range, then one line per hit: removed, kept and why, or
   moved to another task. "Same as above" is not an answer.
2. Keep what must outlive the feature, such as reading data it already wrote, as a requirement with
   its own acceptance.
3. Set the feature to `removed` or `replaced` with the reason and the replacement, then delete code.
   Put the enumeration in the spec or a report and name its path in the feature's Reason.

## Fixing a bug

1. Write current, expected and unchanged behavior as separate lines. Ask the user when the symptom,
   the trigger or the expected result is missing.
2. Write a test that fails on the current code for the reported reason, and run it. If it passes,
   stop: the bug is gone, the cause is wrong, or the test misses it.
3. Search for the same pattern elsewhere. Write the search command and what you did with each hit.
4. Fix, then run the same tests again.

A one-line fix inside an existing requirement reuses that requirement and its task or test.

## Tests that prove something

- Mock only external services. A mock of the code under test proves nothing.
- Never narrow the input range or loosen an assertion to make a test pass, and never add a second
  test to route around a failing one.
- Cover the boundary that breaks: 0, empty, null, equal values, the day boundary. Shape test data on
  real samples, so two sides that share a wrong assumption do not both pass.
- A check of behavior names its output: `check: python ops/probe.py expect "HTTP 200"`.
