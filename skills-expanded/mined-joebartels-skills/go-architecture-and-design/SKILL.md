---
name: go-architecture-and-design
description: Review a defined Go changeset or code area for architecture and design quality across libraries, CLIs, and services. Use when asked to grade package boundaries, APIs, dependencies, interfaces, composition, or lifecycle design; not for a general Go style or performance review.
metadata:
  review-contract: "1"
---

# Go Architecture and Design Review

Review the specified code as a design that other code and people must use and change. Give one architecture grade, grounded in observed behavior and repository context. Review only; do not edit code unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact changeset or code area. Read affected callers, implementations, tests, module version, and repository conventions as needed to understand it. If the target is unclear, state the interpretation used. Do not treat unrelated existing debt as introduced by the change.
2. Identify whether the code is a library, CLI, service, or a mix; distinguish public contracts from internal implementation. Judge the cost of a design choice against its actual users and expected evolution, not an assumed application template.
3. Check the applicable design questions below. Follow a value across boundaries when necessary: who owns it, which package depends on which, how errors and cancellation travel, and who shuts down acquired resources or work.
4. Report only findings with a concrete consequence and supporting code evidence. Group symptoms of one cause into one finding. Mark a suspected issue as a question or limitation when behavior cannot be established; do not lower the grade for a guess. In particular, do not invent HTTP status, durability, or transaction requirements absent a stated contract.

For nuanced examples and handbook corrections, read [Design decisions](references/design-decisions.md) when the review encounters layering, interfaces, context, error translation, or background work. Do not load it for an unrelated, straightforward change.

## Design questions

| Area | What to establish |
| --- | --- |
| Package and API boundaries | Do packages have coherent responsibilities and dependencies? Are exported types, names, and behaviors usable without importing unrelated implementation details? Does the API shape fit its intended consumers? |
| Data and protocol boundaries | When persistence or transport models differ from business concepts, is translation owned at a clear boundary? Is there demonstrated coupling or duplicated mapping, rather than merely a struct tag or direct handler call? |
| Interfaces and abstraction | Does an interface represent a real protocol or consumer need? Is its method set no larger than users need? Would a concrete type, function, or existing standard interface be clearer? Producer-owned interfaces are valid when the protocol itself is the product. |
| Dependencies and composition | Are important runtime dependencies visible and replaceable where needed? Is construction as simple as the invariants allow? Can users tell who configures, starts, and closes a dependency? |
| Cross-boundary behavior | Can callers observe meaningful errors and cancellation without depending on accidental implementation details? Check whether raw infrastructure errors cross a public protocol boundary. Is the success contract truthful when work continues asynchronously? |
| Simplicity and fit | Does each package, layer, DTO, option, and background task solve a present problem? Could fewer boundaries express the same design more clearly? |

Architecture's primary remit is package/API boundaries, abstraction, and ownership contracts. Module resolution belongs primarily to Dependencies & Reproducibility; actual behavior and consumer breakage to Correctness & Compatibility; local expression and naming to Code Quality & Go Idioms. Apply the shared overlap rule when a boundary defect also has one of those consequences. Do not require another skill to assess a demonstrated architectural problem.

## Grade the architecture

Classify each **distinct, substantiated** issue by its effect in this codebase. A minor issue causes localized avoidable complexity; a moderate issue creates a plausible failure or substantial maintenance cost under normal use; a major issue breaks an important contract or makes a likely failure hard to prevent without redesign; a critical issue defeats the stated purpose or creates severe systemic failure. A merge recommendation, if requested, is separate from the grade. Count root causes, not repeated occurrences.

Apply the first matching row from the top. These are grade anchors, not points awarded for following a checklist. Context can raise or lower a finding's severity, but explain the evidence for that choice.

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

If no architecture decision is implicated, return **Not applicable**. If the area is relevant but essential code, contract, or runtime context is unavailable after reasonable inspection, return **Insufficient evidence**. Explain the missing evidence and what would permit grading. Do not use either state to avoid making a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Architecture & Design — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. For each bad finding, provide a corresponding change; distinguish required corrections from optional refinements. Positive findings need evidence too. The grade assesses architecture in the requested scope, not overall Go quality.
