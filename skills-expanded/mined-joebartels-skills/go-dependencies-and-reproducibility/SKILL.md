---
name: go-dependencies-and-reproducibility
description: Review and grade dependency selection, Go module integrity, toolchain and generation inputs, and repeatable builds for a defined Go changeset or code area. Use across libraries, CLIs, and services when modules, imports, workspaces, build tools, or build inputs change; not for a general vulnerability, runtime deployment, or test-quality audit.
metadata:
  review-contract: "1"
---

# Go Dependencies and Reproducibility Review

Review whether the specified Go source resolves the intended dependencies and can be built again from the stated source and build inputs on its supported targets. Give one Dependencies & Reproducibility grade based on the actual module and build context. Review only; do not edit files unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact changeset or code area and whether the deliverable is a reusable module, CLI, service, or several artifacts. Compare the changed `go.mod`, `go.sum`, `go.work`, imports, generation commands, build scripts, and relevant CI or release settings with the prior revision. Distinguish introduced issues from existing constraints. Do not infer that a file omitted from a partial excerpt is missing from the repository.
2. Establish the **resolution context**: main module or workspace; intended standalone consumer or release checkout; selected Go toolchain; supported Go versions and `GOOS`/`GOARCH`; build tags, `CGO_ENABLED`, native libraries, and relevant module environment. A passing workspace or warm-cache build does not establish that a clean standalone build works. Verify both modes when both matter.
3. Trace the **selected** graph and inputs, not just changed lines. For a changed module, inspect the effective version under minimal version selection, transitive requirements, `replace`/`exclude`/`retract`, and whether the import is used by production code, tests, or tooling. Establish whether new checksums, vendored content, local modules, generated files, or private-module access are needed by the documented build. Do not call every indirect change, old version, or absent `go.sum` an issue.
4. Use focused checks in a disposable copy when they may write sums, download inputs, or produce artifacts. Diagnostic choices include `go list -m all`, `go mod graph`, `go mod why -m`, `go mod verify`, and a build or test under the actual vendor/workspace/toolchain mode. For standalone non-vendored builds, `-mod=readonly` prevents required `go.mod` edits; it is not a blanket filesystem write guard. Do not override a shipped vendor build with readonly mode and then claim the vendor path passed. Use `go mod tidy -diff` only when the selected toolchain supports it. Prefer a clean checkout or isolated cache to test fresh resolution when the environment permits. Report exact commands, results, and which context they covered; do not claim a clean build, offline build, checksum verification, or byte-identical binary without actually checking it. Avoid `go get`, `go mod tidy` without `-diff`, or commands that rewrite module files during a review.
5. Report distinct root causes with file or command evidence and the affected target or consumer. Treat an unverified concern as a limit or question, not a grade-lowering defect. For each defect, propose the smallest correction that restores the stated dependency or rebuild contract; separate a required fix from optional hardening.

Read [Dependency and reproducibility decisions](references/dependency-reproducibility-decisions.md) when a judgment turns on `go.sum`, module selection, workspace or replace behavior, toolchain selection, private modules, vendoring, generators, or artifact identity. Check current primary Go documentation and the project's supported versions for version-sensitive claims.

## Review questions

| Area | What to establish |
| --- | --- |
| Selected modules | Does the committed module configuration select the intended versions on supported targets? Do direct, indirect, test, and tool dependencies resolve without an unexplained upgrade, accidental downgrade, or path mismatch? Check actual selection and use; the `// indirect` marker does not mean a module is absent from every build. |
| Integrity and availability | Are needed public module hashes available through `go.sum` or the configured checksum database for the build mode? Are private modules reachable through the stated authenticated path? Does a vendored tree, if used, match `go.mod`? Are local `replace` targets present in the distributable checkout? Judge the configured network and offline requirements, not a universal vendor or checksum policy. |
| Go and target versions | Does each supported build use a toolchain that accepts the module's `go` requirement and its dependencies? Does a `toolchain` suggestion or automatic download actually apply in that environment? Do build constraints, cgo, and native inputs resolve for the targets the project promises? |
| Generation and build inputs | If generated code or assets matter, can the stated source, generator version, and command reproduce them when needed? Are build-time downloads or floating versions controlled where they affect the shipped output? For a bit-for-bit reproducibility claim, are relevant flags, VCS state, paths, timestamps, cgo toolchain, and packaging inputs specified or controlled? |
| Change discipline | Can a fresh checkout perform the documented build without uncommitted module edits or hidden local state? Are graph changes reviewed for their actual effect, including support-policy changes, rather than accepted solely because `go mod tidy` or a warm local build passes? |

Dependencies & Reproducibility assesses selected graphs, toolchains, generation, and build-input resolution. Correctness & Compatibility primarily assesses behavior after those inputs are selected; Security assesses vulnerability; Architecture assesses runtime dependency boundaries; Deployment & Operations assesses artifact delivery and runtime wiring; Testing assesses regression signal. A supported build failure remains assessable here in solo use. Do not require newest versions, vendoring, a particular proxy, or byte-identical binaries without a demonstrated contract and consequence.

## Grade dependencies and reproducibility

Classify each **distinct, substantiated** issue by the reach of its dependency or rebuild failure. A minor issue is localized friction with a low-impact, repeatable workaround; a moderate issue makes a plausible development or regeneration path drift or fail while current shipped builds remain repeatable; a major issue breaks an important supported build, module consumer, or declared artifact path, or leaves a material build input uncontrolled; a critical issue causes severe, broad loss of ability to reproduce the core deliverable or makes essential production dependency contents untraceable across the release path. An important build failure can still be **major** when its demonstrated reach is one target or consumer. Reserve F for evidence of critical reach, not a missing preferred file or a single failing command. Explain the target, prerequisites, and impact. A merge recommendation, if requested, is separate from the grade. Count root causes, not every affected package or checksum line.

Apply the first matching row from the top. These anchors match the other Go review skills; explain context-dependent severity.

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

If the target changes no dependency or build input and presents no dependency or rebuild decision to assess, return **Not applicable**. If the topic is relevant but essential module, build, target, or release context is unavailable after reasonable inspection and could change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. A confirmed failure can still be graded when other paths are unknown; do not use either state to avoid a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Dependencies & Reproducibility — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. Give each bad finding a corresponding change and rationale. The grade assesses Dependencies & Reproducibility in the requested scope, not overall Go quality.
