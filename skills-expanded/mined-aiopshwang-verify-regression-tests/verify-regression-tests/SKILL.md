---
name: verify-regression-tests
description: Verify that a regression test actually detects the defect it claims to guard against. Use after adding or reviewing a bug-fix guard, reproducing the original failure after a fix, or investigating a suspiciously green regression test. Do not use for general TDD, broad test-suite audits, mutation-score optimization, routine test execution, or flaky-test diagnosis.
license: MIT
metadata:
  author: aiopshwang
  version: "0.2.0"
---

# Verify Regression Tests

Test the test, not only the code.

A green test against a candidate fix is weak evidence by itself. Establish a
targeted counterfactual: the same test must turn red when the specific defect is
present, for an observation that distinguishes that defect from unrelated
failures, and return green after the candidate fix is restored.

## Define the regression claim

Inspect the repository instructions, current diff, bug report, implementation,
test, fixtures, and the narrowest relevant command. State the claim before
editing:

- **Trigger:** the input, state, sequence, or boundary that exposed the defect.
- **Bad behavior:** the exact externally meaningful result produced by the
  defect.
- **Expected behavior:** the result required by the contract.
- **Authority:** the requirement, incident evidence, or approved decision that
  establishes the expected behavior independently of the test.
- **Decision point:** the smallest production branch or interaction that
  separates those results.
- **Witness:** the assertion or observable effect that can distinguish bad from
  expected behavior.

Do not substitute a coverage percentage, a passing suite, or an assertion on a
nearby behavior for this claim. If the expected behavior is still a product
decision rather than an established contract, stop and ask for that decision.

## Establish a safe execution boundary

Before running any command, read the repository instructions, status, relevant
diff, target-test configuration, and environment selection. Determine whether
the command can contact a service, mutate shared data, load secret-bearing
configuration, or create artifacts outside the repository. A command named
`test` is not evidence that its effects are isolated.

Confirm that the selected command uses the project's authorized local or
disposable test resources. Capture the status and, when useful, hashes of the
candidate production file and target test before execution. Read
[safe controls](references/safe-controls.md) now; its authority and side-effect
limits apply to the baseline as well as the later control trial. If the boundary
cannot be confirmed without new authority, do not execute it. Explain the risk
and ask for an isolated environment or explicit direction.

## Establish the baseline

Run the narrowest command that selects the target test in the current state.
Confirm from the runner output that the intended test was discovered, executed,
and not skipped, filtered out, retried into green, or satisfied by a stale
artifact.

Record the exact command, test identity, exit status, and decisive output. If the
baseline is already red, classify whether it is the intended regression signal
or an unrelated setup, build, fixture, timeout, or infrastructure failure before
changing anything.

## Introduce one targeted known-bad control

Create the smallest reversible counterfactual that restores the claimed defect
while holding the test and other relevant behavior constant. Prefer the real
pre-fix decision or a semantically equivalent one-line change over arbitrary
mutations. The control must reach the same boundary and produce the same kind of
bad behavior described in the claim; a crash or unrelated validation error does
not count.

Validate the control independently of the target test. Observe the reproduced
bad output, state, or interaction directly, or tie it to trusted incident
evidence and a separate probe. The target test failing cannot be the sole reason
for claiming that the control recreated the defect; that would be circular.

Before changing production code for a control, recheck the loaded
[safe controls](references/safe-controls.md). Never overwrite user changes,
reset a dirty tree, commit the known-bad state, or leave the control behind. Use
an isolated copy or worktree when the target overlaps existing changes or exact
restoration is uncertain. An additional worktree does not automatically contain
uncommitted candidate or test edits: transfer the current candidate and frozen
test deliberately, verify their recorded hashes, then run the comparison.

Keep the test fixed during the control trial. If creating or strengthening the
test, freeze that test version before comparing candidate and known-bad
implementations. Changing both sides destroys the comparison.

## Demand the right red

Run the same narrow target-test command against the known-bad control. A useful
regression guard must satisfy all of these:

1. The intended test and parameter case are discovered and executed alone.
2. The independently validated control reaches the target decision.
3. The test fails without relying on another violated precondition or detector.
4. The decisive failure occurs at the witness in the regression claim, not at
   collection, compilation, setup, teardown, or an unrelated exception.
5. A close non-defect case still passes when it helps isolate the boundary.
6. No instability is observed across proportionate repeated runs.

Do not decide from the runner's `FAIL` or `ERROR` label alone. An unexpected
exception raised from the exercised system can be decisive RED when exception
identity is the stated contract, setup has completed, the exception emerges at
the target witness, and the independent control proves it is the intended bad
behavior. Import errors, fixture failures, and unrelated crashes remain wrong
RED.

One candidate, control, and restored run is the minimum causal loop. Repeat each
variant when the claim involves retries, caches, concurrency, time, randomness,
or another instability risk; use an existing project repeat option when one is
available and report only the stability actually observed.

If the test stays green, or turns red for the wrong reason, read
[false results](references/false-results.md). Treat both outcomes as a failed
proof, even when the overall command exits non-zero.

## Strengthen the guard narrowly

When edits are in scope, correct only the weakness demonstrated by the control:

- make every non-target precondition valid;
- exercise the real decision path instead of a fallback or a mock of the unit
  under test;
- assert a stable public result, state transition, error code, or required side
  effect that distinguishes the defect;
- use a paired witness case when one example could trigger several guards;
- await asynchronous work and assert the effect after its real completion
  boundary;
- avoid copying the production algorithm into the test as its own oracle;
- preserve existing strong assertions instead of weakening them to get green.

Do not broaden the task into production refactoring, dependency replacement, or
whole-suite cleanup unless the user requested it or the target proof cannot be
made without a separately explained change.

## Close the proof loop

Restore the candidate implementation exactly, then rerun:

```text
candidate implementation + frozen target test  -> GREEN
targeted known-bad control + frozen target test -> RED for the claimed defect
restored candidate + frozen target test         -> GREEN
relevant neighboring tests                      -> GREEN
```

Verify that temporary files, mutations, worktrees, environment overrides, and
debug instrumentation are removed, and that unrelated pre-existing changes are
unchanged. Run a broader relevant suite only after the narrow causal signal is
clear.

## Report the evidence boundary

Use one of these verdicts:

- **Verified:** the frozen test was green on the candidate, red for the intended
  reason on an independently validated known-bad control, green again after
  exact restoration, and the relevant surrounding checks passed.
- **Not verified:** a valid, reached known-bad control left the target test green,
  or the target test produced the wrong red.
- **Inconclusive:** the baseline, control validity, artifact identity, target-test
  execution, stability, or restoration evidence was insufficient or
  contaminated. Do not relabel an invalid or equivalent control as false green.

Report:

```markdown
Verdict:
Regression claim:
Baseline command and result:
Known-bad control:
Independent control-validity evidence:
Decisive RED evidence:
Restored GREEN evidence:
Files changed:
Not verified / remaining risk:
```

The verdict applies only to the named defect and exercised boundary. It does not
prove the absence of other bugs, the quality of the entire suite, or production
behavior beyond the environment actually tested.
