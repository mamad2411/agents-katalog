---
name: go-behavior-tests
description: Use when a Go task changes meaningful behavior, fixes a defect, or adds or strengthens tests for a supported contract in a library, CLI, service, or worker. Skip comment-only, formatting-only, and mechanical edits with no behavioral change or requested test improvement.
---

# Go behavior tests

Write tests that distinguish the promised behavior from a plausible wrong
implementation. Derive observations from the task, callers and contracts,
then use the smallest understandable test that protects each important risk.

## Choose the observations

Inspect the effective Go version, changed paths, callers and existing tests.
For each consequential promise, identify the input/event, observation boundary,
expected result and regression it should reject. Usually a few focused cases
suffice; this is a thinking aid, not a required document or case count.

| Promise | Observation |
| --- | --- |
| Returned value or error | Complete relevant fields; promised identity/type with errors.Is/As |
| Wire or file representation | Independently known bytes/decoded values, including ordering and presence |
| Stateful or batch failure | Accepted/retained state and forbidden later effects, as well as the error |
| Process outcome | Actual executable status, stdout, stderr and persisted effects |
| Host lifetime or recurrence | Callback completion before host release/return; successful later cycles |

A helper's error cannot establish its process exit status. A worker-only test
cannot establish its host's join-before-release contract. Round trips can
conceal matching encoder/decoder defects: include an independent known
representation when the protocol matters.

## Build cases with independent assertions

- Check consequential success, rejection and boundary cases. Compare concrete
  expected values derived without the implementation under test; avoid using
  its own encoder, parser or rendering helper to calculate the oracle.
- Test the exact accepted set rather than a familiar broader category. Include
  a success-shaped neighbor that must reject when only one status/value is
  allowed. Keep the other fields valid so another check cannot hide wider
  acceptance.
- When changed branches classify interface values, challenge assumptions with
  valid inputs. An error need not be comparable; wrapped/joined causes and an
  independent failure during cancellation can exercise different decisions.
  Assert the promised result and ownership after classification, rather than
  merely observing that some error occurred.
- For failure after successful work, inspect the accepted prefix or last good
  state and absence of later effects. Exercise failures before effects begin
  **and during effects** where the contract requires retention: a write can
  change an existing file before returning an error. Include repeated updates
  to the same target when they can destroy an earlier accepted value.
- When work and cleanup can fail independently, cover work failure with
  successful cleanup, cleanup failure with successful work, and both when
  their joint result is promised. A dual-failure case does not replace either
  independent case. Preserve useful existing regression cases when regrouping
  or rewriting tests.
- Use table-driven subtests for shared setup and understandable variations;
  separate tests suit different boundaries or lifetimes. Follow useful project
  conventions without imposing a framework, test package, filename taxonomy
  or universal subtest form.

Read [behavior observations](references/behavior-observations.md) when choosing
failure-stage checks, independent error combinations or boundary oracles.
Production seams still follow the project's API/composition needs; choose
fixtures, dependency fidelity, timing and cleanup for a trustworthy observation.
Those mechanics belong to test isolation rather than changing this skill's
assertion contract.

## Prove the signal and finish

Name the plausible wrong branch, value or missing effect each important test
would catch. For a bug fix, observe the test fail against the pre-fix behavior
when practical. If a consequential assertion remains doubtful, use one small
temporary mutation or controlled counterexample, then restore the source.
Confirm compilation and a meaningful assertion failure; crashes and unrelated
timeouts do not demonstrate the claimed safeguard.

Use executable examples when runnable usage is requested. Use fuzz/property
tests when broad input risk has a useful deterministic invariant; retain
independent known cases. Coverage locates paths to inspect, not assertion
quality or a target percentage. Run the relevant suite and contract checks,
with race/repeat/shuffle checks where concurrent or shared state makes them
useful. Respect supported Go APIs; do not raise the minimum for test helpers.
Report the behavior verified, checks run and material untested boundaries.
