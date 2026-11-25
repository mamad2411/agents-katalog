---
name: code-quality
description: Guides code quality through correctness, local reasoning, and safe change. Use when implementing behavior or assessing maintainability during review.
---

# Code Quality

Make required behavior clear, changes local, and failures verifiable. Apply these criteria within the repository's implementation or review workflow. Project standards and established decisions take precedence.

## 1. Establish the change and its risks

Read repository instructions and relevant domain vocabulary and decisions. Trace the affected behavior through callers, state changes, and external effects. Inspect its tests and existing verification commands.

For implementation, identify the intended outcome and a failure case before changing code. For review, establish the comparison and requirements from the request and repository evidence. Ask only for information that remains unresolved; continue independent investigation.

**Complete when:** the affected entry points, behavior owner, and required outcomes are identified. Label inferred requirements as assumptions.

## 2. Apply the quality criteria

| Area | Examine |
| --- | --- |
| Correctness and domain meaning | Rules hold across affected writers; states and errors have explicit meanings; authorization protects the operation. |
| Understandability | Names match domain meanings; control flow and dependencies are apparent; contracts explain required caller knowledge. |
| Modularity and change locality | Each decision has an owner; callers can use the interface without reconstructing its implementation. |
| Proportional design | Each abstraction protects an actual need; shared code represents shared knowledge; the simpler option remains viable. |
| Verification | Assertions distinguish correct from incorrect behavior; checks exercise the contract and failure mechanism being claimed. |
| Operational fitness | Relevant resource limits, partial failures, compatibility, and recovery have defined behavior. |

Before changing or judging interfaces, state models, abstraction, or duplication, read [design.md](design.md). Before changing or judging persistence, external input, asynchronous work, or capacity, read [verification.md](verification.md). Several branches may apply.

Load the installed `architecture` skill for responsibility, dependency, semantic, or consistency decisions. Load `codebase-design` for deep-module vocabulary and interface design. When following TDD, load `tdd`, including its seam-agreement requirements. Resolve these skills from the available skill roots by name. Keep the active workflow's review format and approval boundaries.

**Complete when:** each applicable area has supporting code evidence or an explicit verification gap. Investigate smells through actual behavior and change propagation.

## 3. Improve or report within scope

For implementation, make the smallest complete change that satisfies the behavior and improves the identified problem. Preserve unrelated code. Keep behavior changes distinguishable from structural changes so verification has a clear target.

For review, report actionable findings with location, triggering scenario, consequence, and a proportionate remedy. Distinguish defects, documented-standard violations, and design suggestions. Establish the underlying problem before prescribing a pattern. Respect existing callers and compatibility requirements when proposing deletion.

Evaluate the resulting behavior and structure, including affected callers. Use change locality and necessary caller knowledge to explain a design benefit. Treat size and complexity metrics as investigation signals; style preferences do not establish defects. Report justified tradeoffs without manufacturing findings or a universal quality score.

## 4. Verify the claims

Run the repository checks appropriate to the changed behavior. Choose additional checks from the concrete risks, using existing tooling where possible. Preserve meaningful assertions and enforcement while repairing failures. Propose changes to acceptance criteria explicitly rather than weakening them to obtain a pass.

**Complete when:** affected behavior has appropriate evidence and required gates pass, or an external blocker and its practical consequence are explicit. State what changed, how it was checked, and which claims remain unverified. A review reports findings and gaps without silently starting implementation.

For the rationale and limits of these criteria, see [sources.md](sources.md).
