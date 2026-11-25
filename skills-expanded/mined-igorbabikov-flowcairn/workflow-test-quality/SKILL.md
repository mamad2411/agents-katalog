---
name: workflow-test-quality
description: Improve behavior assertions during implementation or verification and inspect important gaps in existing tests during read-only review. Use the approved contract, test policy, scopes and registered checks.
license: MIT
---

# Behavior checks and credible gaps

Use the current Task Contract to choose the behavior, requirement IDs, observable boundary and allowed verification. This method supports the existing workflow; it does not choose a lifecycle, executable, permission, retry budget or completion verdict. Read relevant source, test fixtures, assertions and project conventions only within the supplied context. Match the project's installed framework and version.

## Behavior-changing work

- Prefer a small vertical red/green step when a meaningful behavior test can be added or changed within the approved scope. Expected results come from the criterion, an independent worked example or a protected oracle, not a copy of the implementation's calculation.
- Respect the current test policy. Under `keep`, preserve tests byte-for-byte and use existing checks; do not demand a new test, expand write scope or create a second approval conversation. Under `add` or another explicit test-write permission, target the behavior at issue and preserve the existing oracle. A routine change does not require test writing merely to follow TDD.
- Prefer caller-visible inputs, outputs, errors and state transitions over assertions about private collaborators. When the criterion concerns storage, events, receipt identity or another explicit invariant, observe that effect directly as well as the caller's result. HTTP success alone does not prove a database write or exactly-once effect.
- Propose the smallest relevant registered check through the Executor. A red result means a relevant assertion failed on the known source/artifact with confirmed execution; missing tools, discovery/build failure, timeout or uncertain termination do not establish a source defect. AI text cannot claim a test ran.
- After a brokered implementation step, use fresh registered evidence for the same criterion. Preserve mandatory checks and scenarios even when unrelated procedures are omitted. Do not weaken criteria, expected values, assertions or required scenarios to obtain green output; classify an inconsistent oracle as a verifier issue.
- Preserve existing test style and dependency boundaries. Use mocks only where they help control the contracted scenario; identify them as mocks. A mock or internal call count cannot replace a required real dependency effect. Do not add a framework, DI layer or test runner for this method.

## Read-only gap review

For a risky change or a requested test-quality review, map the affected mandatory outcomes before judging coverage:

`requirement -> public input or sequence -> expected observation -> reaching test and assertion -> credible gap`

Trace shared helpers and indirect assertions first. An absent dedicated test does not imply an uncovered behavior. Include relevant allow/deny, error, async ordering, retry/idempotency, boundary and state/effect outcomes; do not expand a named risk into an unrelated repository audit. Use nearby boundary values only when they are meaningful under the contract.

For a suspected gap, supply one concrete counterexample: an exact change to an existing condition, expression or effect; a fixed witness input/sequence; and different original versus changed observations through the complete caller flow. Explain which current assertion would fail or why the tests could still pass. Prefer one missing outcome over many syntax variants.

Exclude non-compiling changes, impossible inputs, equivalent boundaries, and private representation changes without an observable effect. A guard removal that falls through to the same contracted error is not a gap. Do not invent an exact expected value when the supplied criterion or context cannot establish it.

Keep evidence levels explicit:

- **Protected (inferred):** an existing assertion would detect the changed observation; this is source reasoning.
- **Candidate gap (unverified):** a distinguishing observation appears unasserted; it has not been executed.
- **No reaching test:** source-to-test mapping demonstrates an unexercised contracted outcome.
- **Detected / survived (executed):** only supplied Executor evidence for that exact source, mutation, registered check and witness supports this label. Infrastructure failure does not mean the mutation was detected.

Review itself is read-only. Existing navigation within the supplied context is allowed; do not run checks/build/restore, execute or import production code, mutate source, add tests or invoke another workflow. If actual counterexample execution is necessary and already authorized, propose a separate isolated fixture check to the Executor with preserved baseline/oracle hashes, bounded execution and confirmed restoration. An uncertain write or process must be reconciled before another effect. Keep unverified candidates visible rather than turning them into PASS.

## Report useful evidence

Return only requirement-linked findings that change a decision: source/test location, observable wrong behavior and witness, detection reasoning or an actual receipt/report reference, and the smallest permitted assertion or check that closes the gap. Distinguish a current input from a proposed new witness. An empty findings list is valid.

Prioritize contract-critical denials, errors and state/effect changes. Missing material, unknown assertion semantics or an unavailable verifier leave the affected outcome unverified. Static review, a loaded Skill, a coverage percentage, a test-count increase or a quota of negative tests is not completion evidence. Final acceptance remains with the Executor's current requirement evidence and gates.

## Source attribution

Adapted from [Matt Pocock TDD](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md) and [.NET test-gap-analysis](https://github.com/dotnet/skills/blob/9864ca798f9448ef954ad1f05baf0dfca6501d51/plugins/dotnet-test/skills/test-gap-analysis/SKILL.md). Flowcairn contract, permission and evidence rules take precedence over the upstream workflow preferences. Pinned sources, reference hashes and the complete MIT notices are in [LICENSES.md](LICENSES.md); no upstream scripts or agent configuration are bundled.
