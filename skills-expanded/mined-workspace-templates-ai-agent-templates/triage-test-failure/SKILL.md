---
name: triage-test-failure
description: Diagnoses one failing test from its output and tells you whether the test or the code is wrong, with the evidence.
disable-model-invocation: true
---

Triage this failing test: $ARGUMENTS (a test name, a file, or pasted output).

1. Run the test alone and capture the full output. Run it three times to see if the result is stable. Then run it with the rest of its file to check for order effects.
2. Read the test and the code it exercises. Identify exactly which assertion fails, expected against actual.
3. Check what changed recently: `git log -n 5 --oneline -- <test file> <source file>` and the working tree diff. Name the commit most likely responsible.
4. Look for flake causes: wall-clock time, timezone, random data without a seed, shared global state, network calls, unawaited promises, hash or dict ordering.
5. Reach a verdict: **code bug**, **stale test**, **flaky test**, or **environment**. Give the three strongest pieces of evidence.
6. Do not edit anything.

Report the verdict, the evidence, the smallest fix and where it goes. Ask whether to apply it.
