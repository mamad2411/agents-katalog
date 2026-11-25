---
name: tdd
description: Cost-aware test-driven development that preserves red-green-refactor quality while grouping related examples into coherent behavior cycles. Use for test-first feature and bug work where repeated test-runner startup or overly granular cycles would add avoidable delay.
---

# Test-Driven Development

Develop through observed RED-GREEN-REFACTOR cycles without trading away behavior coverage, code
quality, or final acceptance proof.

## Core rule

One cycle proves one coherent observable behavior, not necessarily one test case.

Keep behavioral ownership in the main workflow. A read-only subagent may discover test seams or run
an independent validation command, but it must not decide that a RED or GREEN result proves the next
behavior. The main workflow observes and interprets each cycle.

A cycle may contain one test or a small related matrix when every case exercises the same public
behavior or production decision. Do not combine unrelated behaviors, write the whole feature's test
suite before implementation, or remove useful cases to reduce runtime.

Tests should verify behavior through public interfaces. Prefer real internal collaborators and mock
system boundaries when necessary. A mock-call assertion proves wiring, not the capability, and must
not be the sole proof of cross-module behavior.

For critical behavior, a cycle counts only when its proof is sensitive to a plausible defect. Name
the invariant, likely failure mode, and actors or boundaries needed to produce that failure. Do not
use null, no-op, or always-successful doubles that make the failure impossible. For asynchronous
workflows, deterministically exercise meaningful alternative event orderings instead of relying on
one normal scheduling outcome.

## Workflow

### 1. Establish the contract

Use the caller's approved task, acceptance criteria, and resolved decisions as the behavior contract.
Ask the user only when a public interface or expected behavior remains genuinely unresolved.

List observable behaviors and identify the primary test seam for each. For a complete user journey,
decide whether automated end-to-end testing provides unique, reliable evidence beyond deterministic
lower-level tests. If it does, name the smallest meaningful end-to-end scenario. If it would only
duplicate faster proof, is prohibitively slow or flaky, depends on platform behavior that automation
cannot judge reliably, or cannot force the important failure ordering, name the deterministic
integration proof and any targeted manual checkpoint instead. Record the reason rather than claiming
end-to-end coverage.

If the work exposes unrelated capabilities that cannot be understood as one task, report the scope
problem to the caller instead of hiding it behind more test cycles.

### 2. RED for one coherent behavior

Write the smallest test or related test matrix that specifies the next behavior. Run the narrowest
reliable command once.

Proceed only when:

- the new expectation fails;
- it fails because the behavior is absent or incorrect, not because of setup, imports, fixtures, or
  an unrelated failure; and
- the test observes public behavior rather than implementation structure.

If the new test starts GREEN, determine whether the behavior already exists or the test is
insensitive. Strengthen or remove the test; do not count it as a cycle.

### 3. GREEN with a general solution

Implement the smallest general solution consistent with the current public contract and known
domain invariants. Do not hard-code the fixture, special-case the test, anticipate unrelated future
behaviors, or weaken assertions.

Run the same focused command and observe GREEN.

Before counting a critical cycle complete, confirm test sensitivity using the pre-fix behavior or a
temporary mutation that represents the likely defect. The relevant expectation must fail for the
intended reason. If the mutation still passes, strengthen the seam or assertion and repeat RED-GREEN.
Remove every temporary mutation before continuing.

### 4. Repeat at an economical cadence

Choose execution cadence from feedback-loop cost without changing coverage:

- Keep cheap focused tests granular when that gives clearer feedback.
- When runner startup dominates, group related examples for the same behavior or use a reliable
  watch/persistent mode.
- Do not rerun unchanged broad suites after every small cycle.
- When the caller supplies a task log directory, keep bounded verbose command output there and do
  not create a second log location. Otherwise rely on the command runner's bounded output. Return the exit status,
  duration, relevant failure excerpt, and log path when one exists; inspect full output only when the
  concise result is insufficient.
- Run affected feature suites after a connected set of cycles. Reserve one canonical full suite for
  the final post-remediation validation checkpoint; do not run that unchanged suite both before and
  after review.
- Independent read-only checks may run in parallel only after the current diff is stable and only
  when their runners, ports, databases, fixtures, generated outputs, and simulators are isolated.

A cycle commonly has one to three examples, but semantic cohesion matters more than a numeric cap.

### 5. Refactor while GREEN

Refactor production and test code only while GREEN, and only the code this cycle touched: remove
duplication the cycle created, and improve the names and fixtures it introduced. Preserve every
distinct behavior assertion.

Deepening an interface, restructuring a module, or replacing a neighboring test's mock-heavy proof
with a stronger seam is out-of-task work when it reaches code the task does not change. Record it
and confirm with the user rather than doing it here, however well GREEN covers you.

Run the focused tests after each refactor step and the affected feature suite when refactoring is
complete. Batch independent reads, searches, and disjoint test commands in one parent turn to avoid
unnecessary model round trips, but never batch commands whose result determines the next edit.

### 6. Prove the complete journey at the appropriate seam

When automated end-to-end testing provides unique, reliable evidence for the assembled journey, run
the smallest named scenario after assembly and again after remediation that could affect it. Do not
expand E2E coverage merely to duplicate behavior already proved more deterministically at a lower
seam.

An E2E pass proves only the journey and conditions it exercised. It does not replace deterministic
proof of concurrency, event ordering, interruption, retries, persistence, or boundary failures. Use
controlled integration tests for those risks. Use a targeted manual checkpoint when behavior depends
on human judgment, physical devices, or platform surfaces that automation cannot observe reliably.

If the end-to-end feedback loop fails for an unclear reason, diagnose the loop rather than repeatedly
patching production code or retrying until it passes. Do not run E2E checks concurrently when they
share a simulator, server port, fixture, or test account.

## Cycle checklist

- [ ] One coherent observable behavior
- [ ] Primary test seam is appropriate
- [ ] RED observed for the intended reason
- [ ] Critical proof is sensitive to a plausible defect
- [ ] Relevant actors and boundaries were not mocked into making failure impossible
- [ ] Smallest general solution implemented
- [ ] Assertions and coverage were not weakened
- [ ] GREEN observed with the same focused command
- [ ] Refactoring performed only while GREEN
- [ ] Broader validation deferred only to an explicit checkpoint
- [ ] Complete user journey has the smallest reliable E2E proof when it adds unique value, or documented deterministic and manual proof otherwise
