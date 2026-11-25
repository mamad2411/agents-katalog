---
name: go-correctness-and-compatibility
description: Review and grade functional correctness and consumer compatibility in a defined Go changeset or code area across libraries, CLIs, and services. Use for changed behavior, invariants, edge cases, state transitions, concurrency outcomes, or existing public contracts; not for a general style, testing, security, or performance audit.
metadata:
  review-contract: "1"
---

# Go Correctness and Compatibility Review

Review whether the specified Go code does what its supported users and callers are entitled to expect, including after an upgrade. Give one Correctness & Compatibility grade based on demonstrated behavior and credible consequences. Review only; do not edit code unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact diff or code area and its library, CLI, or service context. Inspect the prior behavior, affected callers, tests, documentation, protocol or schema definitions, and release policy as needed. Distinguish introduced defects from existing constraints; do not grade unrelated debt. If intent is unstated, use observable contracts and say which assumptions the grade depends on. A test is evidence of intent, not proof that the implementation or test is correct.
2. Trace changed behavior through at least the paths material to its contract: ordinary input, boundaries, errors, partial completion, and concurrency when applicable. Check the actual caller and downstream effect before calling a suspicious expression a bug. Do not demand that every function handle every hypothetical input.
3. For a compatibility claim, identify the consumer-visible contract and the supported upgrade path. Check source compatibility, documented behavior, error identity, value ownership, wire or file formats, CLI output and exit behavior, or persistence semantics only where the change touches them. A deliberate breaking change can be acceptable under the project's versioning and migration policy; an undocumented change in historically unsupported behavior need not be preserved.
4. Check `go.mod`, relevant `go.work`, file build constraints, supported platforms, and release context before making version-sensitive claims. The installed toolchain alone does not determine a file's language semantics or the project's supported build matrix. For generated code, inspect the source of truth when available rather than proposing a hand edit.
5. Use focused, non-mutating verification when the code and environment permit it: an affected-package build or test, a minimal reproduction, or a comparison with the previous revision. Report exact commands and outcomes. A passing test does not prove an unexercised path correct; a failed command must be tied to this change before it becomes a finding.
6. Report distinct root causes with code or verification evidence and the affected input or caller. Verify positive claims as carefully as negative ones. Treat an unconfirmed concern as a question or limit, not a grade-lowering defect. Connect every bad finding to a specific change and explain why it restores the intended behavior or contract.

Read [Correctness and compatibility decisions](references/correctness-compatibility-decisions.md) when a judgment turns on public Go APIs, module versioning, effective language version, nil or slice ownership, concurrency, or a behavioral contract across CLI, service, or storage boundaries.

## Review questions

| Area | What to establish |
| --- | --- |
| Results and errors | Do valid, invalid, empty, and boundary inputs produce the promised result or error? Are error identities and partial results preserved where callers depend on them? Are conversions, arithmetic, parsing, and zero values correct for supported inputs? |
| State and data integrity | Can an operation report success before its promised effect occurs? Do failed steps leave state in an allowed condition? Are mutation, aliasing, ordering, and copy semantics consistent with the contract? Is atomicity or idempotence actually promised or required by a demonstrated caller? |
| Concurrency and cancellation | Can interleavings cause wrong results, races, deadlocks, lost work, or an incorrect success claim? Does cancellation change observable behavior as specified? Check shared-state access and who waits for work; a race finding needs a reachable concurrent path. |
| Consumer compatibility | Does an existing supported caller still compile and behave as promised? Check exported signatures and method sets, function values, errors inspected with `errors.Is`/`As`, nil versus empty encodings, serialized fields, CLI flags/output/exit codes, and stored data only when affected. Assess breakage against the project's actual compatibility policy and migration plan. |
| Build and platform behavior | Does the change compile and behave under supported Go versions, build tags, operating systems, or architectures? Verify the effective language version and relevant target rather than assuming every possible platform is supported. |

Correctness assesses actual behavior and consumer breakage, including races, hangs, ownership violations, and source-language failures. Dependencies & Reproducibility primarily assesses graph/toolchain resolution; Architecture assesses API design; Code Quality assesses local clarity and idioms; Testing assesses regression detection. Security, Performance, and Observability & Resilience may share a cause with a behavioral defect; assess the contract consequence here and use the shared overlap rule rather than silently deferring it.

## Grade correctness and compatibility

Classify each **distinct, substantiated** issue by its effect on supported behavior or consumers. A minor issue affects a narrow supported case with limited, recoverable impact; a moderate issue produces a plausible wrong result or contract mismatch under normal use but remains contained; a major issue breaks an important supported contract, corrupts meaningful state, or causes a reachable race, hang, or lost operation with material impact; a critical issue causes severe, broad, or irreversible failure across a core workflow or system. Explain the affected inputs, consumers, and impact. A defect can defeat one function's purpose and still be **major** when its demonstrated reach is contained. A race or breaking signature is not automatically critical. Reserve F for evidence of the critical reach, not the mere possibility of a worse outcome. A merge recommendation, if requested, is separate from the grade. Count root causes, not occurrences or hypothetical consequences.

Apply the first matching row from the top. These anchors match the other Go review skills; explain severity judgments that depend on context.

### Apply the anchors consistently

Count independently actionable root causes after grouping repeated symptoms. Two symptoms are one issue when the same causal correction resolves both; unrelated corrections remain separate even in one function. State the counted severities in the report. Verified strengths do not cancel defects, and optional preferences or unconfirmed concerns do not enter the counts.

A contained failure of one important function, target, or contract is normally major. Use systemic major only when one shared cause demonstrably affects multiple distinct important boundaries or workflows; repetition across files alone is insufficient. Critical requires supported severe, broad, or irreversible impact in the topic being reviewed, not merely the words race, unsafe, missing test, or build failure. Explain any systemic or critical classification. These reach rules refine the topic-specific severity definitions above.

For A+, identify two independent safeguards, the distinct meaningful risks they control, and evidence that each works. Ordinary correct setup supports A. Complexity, tool count, or splitting one safeguard into two descriptions does not earn A+; simple designs can qualify when their risk control is demonstrated. If no issue is found but the evidence cannot support even one relevant strength, use Insufficient evidence.

Use Not applicable only when no relevant decision is implicated. Use Insufficient evidence when the topic applies but essential evidence prevents a judgment. A confirmed defect can still receive a letter grade for the inspected scope, with the unassessed parts in Coverage and Limits; do not imply those parts passed. Do not award A or A+ for an incompletely assessed material risk.

| Grade | Anchor |
| --- | --- |
| F | At least one critical issue. |
| C- | Two or more independent major issues, or one major plus two or more moderate issues, or one systemic major issue. |
| C | One contained major issue, with at most one moderate issue. |
| C+ | No major or critical issue; two or more independent moderate issues. |
| B- | No major or critical issue; one moderate issue plus two or more minor issues. |
| B | No major or critical issue; one moderate issue with at most one minor issue. |
| B+ | No moderate or worse issue; two or more minor issues. |
| A- | Exactly one minor issue and no moderate or worse issue. |
| A+ | Meets A, with two independent, verified safeguards controlling distinct meaningful risks beyond routine correct setup. |
| A | No actionable issue; at least one relevant strength is verified and material applicable risks are assessed. |

If the target has no assessable behavior or consumer-contract decision, return **Not applicable**. If it is relevant but essential implementation, contract, consumer, or release context remains unavailable after reasonable inspection and would change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. A confirmed defect can still be graded when some other paths are unknown; do not use either state to avoid a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Correctness & Compatibility — [grade | Not applicable | Insufficient evidence]
Scope: [base/head, supplied diff, or code area; library/CLI/service and relevant version/runtime context]
Coverage: [applicable areas assessed; material areas not assessed and why]
Rationale: [why the evidence and counted severities select this grade; explain systemic/critical reach or both A+ safeguards]
Finding counts: critical=[n], major=[n], moderate=[n], minor=[n]

Good

- [G1] [specific choice and evidence/location] — [why it benefits the relevant contract or risk]

Bad

- [F1][severity][introduced | worsened | existing-in-scope] [issue and evidence/location] — [trigger and supported consequence]

Suggested changes

- [F1] [targeted correction] — [why it resolves the consequence; how to verify it]

Limits: [material missing evidence; exact checks and outcomes, or checks not run]
```

Prefer `path:line` references when files are available. Give each bad finding a corresponding change and rationale. The grade assesses Correctness & Compatibility in the requested scope, not overall Go quality.
