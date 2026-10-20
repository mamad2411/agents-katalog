---
name: go-deployment-and-operations
description: Review and grade deployment and operations for a defined Go changeset or code area across libraries, CLIs, and services. Use for build and release artifacts, containers, CI gates, runtime configuration, probes, shutdown, resource limits, rollout, or rollback; not for a general Go security, observability, or performance audit.
metadata:
  review-contract: "1"
---

# Go Deployment and Operations Review

Review whether the changed Go code and delivery configuration can be built, released, started, operated, and stopped reliably in its intended environment. Give one grade for this topic, based on the actual artifact and deployment path. Review only; do not edit code or trigger a release or deployment unless asked. A targeted local build or check may provide review evidence when feasible.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact diff or code area and what it produces: a library module, CLI binary, batch job, service, container image, or several of these. Inspect the relevant `go.mod`/`go.work`, build constraints, Dockerfile, CI workflow, packaging, runtime configuration, deployment manifests, and release instructions only as needed. Distinguish introduced issues from relevant existing constraints; do not grade unrelated infrastructure debt.
2. Trace the artifact from source to runtime: which toolchain and build settings are used, what files and credentials enter the build, which artifact is deployed, what configuration it receives, how traffic or work reaches it, and how it terminates. A library may have release and compatibility questions but no container or health probe. A CLI may have cross-platform packaging and exit behavior but no rollout.
3. Check version- and platform-sensitive advice against the module's minimum Go version, the selected build toolchain, target `GOOS`/`GOARCH`, cgo and native dependencies, and the deployed runtime. A `go` directive alone does not prove which compiler CI used. Consult current primary documentation when a release, image, orchestrator, or tool behavior matters.
4. Report distinct, supported consequences. A missing preferred tool, small image, pinned digest, scanner, or Kubernetes feature is not a finding by itself. Verify that an existing platform or workflow does not already supply the control. Treat absent manifests or operational data as a limit when they could change the judgment; do not assume they are absent from the deployment.

Read [Deployment and operations decisions](references/deployment-operations-decisions.md) when judging image/build flags, credentials, probes, termination, memory limits, diagnostics, release gates, or rollouts. It supplies context-sensitive distinctions and links to primary documentation.

## Review questions

| Area | What to establish |
| --- | --- |
| Build and artifact | Does the release workflow invoke the intended build and produce the artifact it deploys? Are source, toolchain, dependencies, and flags identifiable from that workflow? Do the packaged binary, certificates, time zones, native libraries, and filesystem contents match runtime needs? Do cache and base-image choices preserve correctness and a viable update path? Grade dependency selection and repeatable resolution under Dependencies & Reproducibility. |
| CI and release | Do applicable checks run on the code and artifact that will ship? Can maintainers identify the source, toolchain, dependency set, and artifact being released? Where supply-chain evidence, vulnerability scanning, signing, or SBOMs are required by policy or threat model, is that evidence produced and checked? For modules, do tags and major-version paths fit Go's release rules? |
| Container and privileges | Does the runtime image contain what the program needs without unnecessary build tools, source, credentials, or writable privilege? Is the execution user and filesystem policy suitable for required ports and paths? Multi-stage and minimal images are useful options, not mandatory shapes. |
| Runtime configuration | Are required values parsed before serving, with clear failure on invalid configuration? Do secret delivery, access, rotation, and diagnostics fit the actual platform? Check whether credentials enter build layers, image metadata, logs, or other unintended outputs. |
| Health and traffic | If probes or routing gates exist, does liveness indicate a reason to restart and readiness indicate ability to receive the work actually routed to this instance? Is a startup probe needed for the observed startup behavior? Are checks cheap, bounded, and aligned with the platform's protocol and thresholds? |
| Termination and drain | Does the process receive the platform's stop signal, stop taking new work, and finish or explicitly hand off owned work within the grace period? Do HTTP, background jobs, long-lived connections, and telemetry have appropriate owners and budgets? Check the real routing and termination sequence before proposing a propagation delay. |
| Resources and diagnostics | Do container requests and limits, Go runtime settings, storage, and log egress fit measured workload and platform behavior? Is `GOMEMLIMIT` treated as a soft Go runtime limit rather than an OOM guarantee? Are diagnostic controls reachable by operators without exposing them to unintended callers? |
| Rollout and recovery | Can a new artifact be introduced and observed without violating availability or data compatibility requirements? Where schema or protocol changes span versions, can old and new versions coexist during rollout and rollback? Is a stalled rollout detectable, and is recovery actionable through the actual deployment system and operator procedure? |

Deployment assesses the configured build, packaging, release, and runtime path. Dependencies & Reproducibility primarily assesses graph selection and controlled inputs; Correctness & Compatibility assesses program contracts; Observability & Resilience assesses lifecycle and signal behavior; Security assesses exploitability; Performance assesses code-level costs; Testing assesses test signal. A release's wrong compiler, leaked credential, probe wiring, or grace-budget mismatch remains assessable here in solo use. Cross-reference shared causes in combined reports using the shared overlap rule.

## Grade deployment and operations

Classify each **distinct, substantiated** issue by its effect in this release path. A minor issue is a localized operational friction or low-impact gap; a moderate issue creates a plausible release failure, degraded operation, or material recovery burden; a major issue can break an important build, deployment, availability, or recovery contract under normal conditions; a critical issue creates severe systemic failure or defeats the release path's stated purpose. Explain prerequisites, blast radius, and whether a platform already mitigates the issue. A merge recommendation, if requested, is separate from the grade. Count root causes, not occurrences.

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

If the target implicates no build, packaging, release, configuration, runtime, or operations decision, return **Not applicable**. If the topic is relevant but essential artifact, workflow, platform, or runtime information is unavailable after reasonable inspection and could change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. A visible deployment defect can be graded even if other infrastructure is unavailable; do not use either state to avoid a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Deployment & Operations — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. Give each bad finding a corresponding change and rationale. The grade assesses only Deployment & Operations in the requested scope, not overall Go quality.
