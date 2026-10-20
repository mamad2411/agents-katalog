---
name: go-observability-and-resilience
description: Review and grade observability and resilience in a defined Go changeset or code area across libraries, CLIs, and services. Use for logs, metrics, traces, deadlines, retries, overload, failure isolation, probes, or graceful shutdown; not for a general Go style, security, performance, or deployment audit.
metadata:
  review-contract: "1"
---

# Go Observability and Resilience Review

Review whether operators and callers can understand failures and whether the changed code behaves predictably when dependencies slow, fail, or overload. Give one grade for this topic, grounded in the actual runtime and contract. Review only; do not edit code unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact diff or code area. Inspect relevant callers, transport configuration, tests, `go.mod`, telemetry setup, and deployment configuration when available. Distinguish introduced defects from existing constraints. A local library, CLI, and network service need different signals and controls.
2. Identify which work can block or fail, who owns its context and lifetime, what the caller may safely retry, and what operational signals exist at the affected boundary. Trace the actual call path before declaring a missing timeout, correlation field, or shutdown step.
3. Report distinct, substantiated consequences. Group repeated symptoms of one root cause. Treat absent service-level objectives, deployment behavior, or telemetry plumbing as limits when they affect the judgment; do not invent them. Avoid demanding instrumentation or resilience machinery for a pure local operation.
4. Check version-sensitive API advice against the module's effective Go version and the project's chosen instrumentation libraries. Existing `zap`, `zerolog`, Prometheus, OpenTelemetry, or platform facilities can be sound; migration to `slog` is not a finding by itself.

Read [Observability and resilience decisions](references/observability-resilience-decisions.md) when the review encounters logging correlation, metric or trace design, retries, circuit breakers, panic recovery, probes, or shutdown. It supplies context-sensitive distinctions and links to primary documentation.

## Review questions

| Area | What to establish |
| --- | --- |
| Logs and correlation | Do important failures produce useful, appropriately leveled events at an owned boundary without duplicate noise? Are request or trace identifiers attached where needed by the configured logger or handler? Could logged values disclose secrets or sensitive data? Structured text can be adequate; JSON and dynamic log levels are choices, not universal requirements. |
| Metrics and alerts | Can operators detect user-visible failure, latency, saturation, or backlog for this workload? Are metric names, labels, and units stable and useful? Could unbounded label values multiply time series? Are histogram boundaries suitable for decisions such as an SLO, rather than merely customized? Can telemetry export failure unexpectedly block primary work? |
| Traces | Where distributed calls exist, does configured propagation carry the active context across relevant boundaries? Are spans meaningful, ended, and annotated without leaking sensitive values? Check whether auto-instrumentation already supplies spans; do not require a child span for every function. Account for sampling when interpreting absent traces. |
| Deadlines and retries | Do external operations respect caller cancellation and an appropriate total budget? Are retries limited to safe, transient failures, with bounded attempts or elapsed time, backoff and jitter when contention warrants it, and no multiplication across layers? Consider existing SDK retries and server-provided retry guidance. |
| Failure containment | Can a slow or failed dependency exhaust workers, queues, connections, or memory? Are concurrency limits, backpressure, fallback, or a circuit breaker justified by observed failure modes? Is retry safety or deduplication defined for side-effecting operations that are actually retried? |
| Service lifecycle | For applicable services, do liveness and readiness reflect their distinct purposes without causing restart loops or needless traffic loss? Is startup probing needed? On shutdown, does the process stop accepting work, allow owned work to finish within its budget, and flush telemetry as needed? Check long-lived or hijacked connections separately. |

This topic assesses diagnostic signals, failure handling, retries, and lifecycle code. Deployment & Operations primarily assesses how manifests and rollout configuration use those controls; Performance assesses resource cost; Security assesses attacker-driven impact or sensitive disclosure; Testing assesses verification. A shared timeout, queue, or shutdown defect stays assessable here when it affects resilience; use the shared overlap rule instead of deferring it away.

## Grade observability and resilience

Classify each **distinct, substantiated** issue by its effect in this codebase. A minor issue reduces local diagnostic clarity or adds low-impact fragility; a moderate issue creates a plausible missed signal, failed request, or substantial operational burden under normal use; a major issue makes an important failure hard to detect or contain, or breaks a stated reliability contract; a critical issue creates severe systemic failure or defeats the stated purpose. A merge recommendation, if requested, is separate from the grade. Count root causes, not occurrences.

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

If the target has no relevant failure, operational signal, or lifecycle decision, return **Not applicable**. If the topic is relevant but essential code, contract, or runtime configuration is unavailable after reasonable inspection and could change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. Do not use either state to avoid a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Observability & Resilience — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. Give each bad finding a corresponding change; distinguish required corrections from optional refinements. The grade assesses only observability and resilience in the requested scope, not overall Go quality.
