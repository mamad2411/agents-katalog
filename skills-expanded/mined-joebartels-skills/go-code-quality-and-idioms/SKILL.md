---
name: go-code-quality-and-idioms
description: Review and grade code quality and Go idioms in a defined Go changeset or code area across libraries, CLIs, and services. Use for readability, naming, error handling, documentation, value semantics, or version-aware language and standard-library choices; not for a general architecture, testing, security, or performance audit.
metadata:
  review-contract: "1"
---

# Go Code Quality and Idioms Review

Review the specified Go code for clarity, appropriate local idioms, and ease of maintenance. Give one code-quality grade based on observed consequences, not a count of style rules. Review only; do not edit code unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact diff or code area and inspect enough callers, types, tests, and nearby conventions to understand it. Distinguish newly introduced issues from existing constraints. Do not grade unrelated debt.
2. Check `go.mod`, relevant `go.work` context, and file build constraints before judging a language feature or old idiom. The installed toolchain does not by itself determine a file's effective language version. If version-sensitive advice matters and that context is unavailable, qualify the finding rather than assume the newest semantics.
3. Determine whether code is generated. Review its generator or source of truth when available; do not request hand edits to generated output. Apply the same quality standard to libraries, CLIs, and services, scaled to their actual users and contracts.
4. Report only distinct findings with a code location and a concrete consequence. Group repeated symptoms with one root cause. For each finding, explain why the existing code is problematic and why the proposed change helps. Identify verified strengths as specifically as defects; do not invent either.

Read [Idiom decisions](references/idiom-decisions.md) when a finding depends on error exposure, nil versus empty values, receivers, comments, testing idioms, concurrency, or newer Go features. It supplies context-sensitive distinctions and links to primary Go guidance.

## Review questions

| Area | What to establish |
| --- | --- |
| Error flow | Are returned errors checked or deliberately handled? Is context useful without redundant wrapping or duplicate logs? Does `%w` expose a cause callers should be allowed to depend on? Does an ignored cleanup or deferred error affect the result? |
| Readability | Can a reader follow the normal path and state changes? Do guard clauses reduce real nesting? Are helpers, abstractions, generics, and comments earning their complexity? Are shadowed variables or implicit side effects hiding behavior? |
| Names and documentation | Are names clear at their use sites, with scope-appropriate length and consistent initialisms? Does exported documentation state the contract where users need it? Is apparent package stutter actually redundant in client code? |
| Values and methods | Do nil, empty, and zero values preserve the intended observable contract? Do receiver choices preserve mutation and method-set behavior? Are copy-sensitive values such as mutexes copied? |
| Version-aware idioms | Would a supported standard-library or language feature make this code materially clearer? Is that feature available under the file's effective Go version? Avoid modernization churn that changes semantics or merely swaps syntax. |
| Mechanical evidence | If files are available, use `gofmt -d` and relevant `go vet` or build output when useful. A tool diagnostic is evidence to investigate, not an automatic grade. Do not run mutating formatters or `go fix` during a review; `go fix -diff` can preview suggestions on supported toolchains. |

Code Quality's primary remit is local clarity, error handling, value semantics, and version-appropriate idioms, including a language-semantics bug encountered in those areas. Correctness & Compatibility also assesses observable breakage; Testing owns assertion strategy and regression coverage; Architecture owns package/API design; Security owns exploitability; Performance owns measured cost. Assess the local consequence in solo use and cross-reference shared causes in combined reports. Optional stylistic preferences do not lower the grade.

## Grade code quality

Classify each **distinct, substantiated** issue by its effect in this codebase. A minor issue causes localized readability friction or avoidable inconsistency; a moderate issue creates a plausible local bug or substantial maintenance cost under normal use; a major issue breaks important behavior or makes likely mistakes difficult to prevent without rework; a critical issue defeats the stated purpose or causes severe systemic failure. Purely optional stylistic preferences are not findings. A merge recommendation, if requested, is separate from the grade. Count root causes, not occurrences.

Apply the first matching row from the top. These anchors match the other Go review skills; explain any severity judgment that depends on context.

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

If the target contains no assessable Go code or idiom decision, return **Not applicable**. If it is relevant but essential code or version context is unavailable after reasonable inspection and would change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. Do not use either state to avoid a supportable judgment from the available code.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Code Quality & Go Idioms — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. Give each bad finding a corresponding change; distinguish required corrections from optional refinements. The grade assesses code quality and idioms in the requested scope, not overall Go quality.
