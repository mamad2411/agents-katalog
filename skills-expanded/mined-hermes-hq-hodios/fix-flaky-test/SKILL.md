---
name: fix-flaky-test
description: Finds why a test passes and fails intermittently and fixes the cause instead of adding retries. Use when a test fails only sometimes, locally or in CI.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: testing
  source: https://hermes-ide.com/prompts/fix-flaky-test
  catalog: 2026.1002.0
---

# Fix a flaky test

## Inputs

- [TEST] (required): Test name, file or failing CI job to investigate.
- [FAILURE_LOG] (optional): Output from a failing run, if you have one.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
A flaky test passes and fails on the same code. Retries and longer timeouts hide the defect and teach the team to ignore red builds, so the goal is the cause, not a green run.
</context>

<task>
Investigate [TEST].
Only if [FAILURE_LOG] was provided: Start from this failing output:
[FAILURE_LOG]
1. Read the test and the code it exercises before running anything.
2. List the sources of nondeterminism you can see: time, randomness, ordering, shared state, concurrency, network, environment.
3. Reproduce the failure by running the test repeatedly or in a different order. Report how often it fails.
4. Fix the cause, then run the test enough times to show the failure is gone.
</task>

<constraints>
- Never add retries, sleeps or longer timeouts as the fix.
- Fix the behaviour, not the test. Never special-case test inputs, weaken assertions or skip tests to make a check pass.
- If a test looks wrong, explain why and ask before changing it.
- Before saying the work is done, run the check that proves it (tests, build, type check or the command the user gave) and report the real result.
- If you could not run a check, say so plainly and say which one.
</constraints>

<output_format>
## Cause
One paragraph: the nondeterminism and how it makes the test fail.
## Fix
The diff, then one sentence on why it removes the cause.
## Evidence
Runs before and after, with failure counts.
</output_format>
