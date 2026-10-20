---
name: go-performance-and-resource-management
description: Review and grade performance and resource management in a defined Go changeset or code area across libraries, CLIs, and services. Use for algorithmic cost, allocations, memory retention, GC, I/O and connection reuse, concurrency limits, contention, profiling, benchmarks, or PGO; not for a general Go style, security, or deployment audit.
metadata:
  review-contract: "1"
---

# Go Performance and Resource Management Review

Review whether the specified Go code uses time, memory, connections, goroutines, and other finite resources appropriately for its actual workload. Give one grade for this topic, grounded in code behavior and available measurements. Review only; do not edit code unless asked.

## Shared review contract

- Use this skill independently; other topic names identify related expertise, not prerequisites. Grade consequences within this skill's review questions even when another topic also applies. Mention confirmed issues wholly outside this topic separately as ungraded related findings; do not silently discard them or perform an unrelated audit.
- For a changeset, record the base/head revisions or supplied diff and grade introduced or worsened issues. Unchanged code is context unless the change newly exposes its defect. For a code-area review, grade existing issues in that named area. State the interpretation when the target is ambiguous.
- Assess the relevant questions and record coverage and limits. An omitted file in a partial excerpt is not a missing implementation. Distinguish supplied facts, inspected code, executed checks, and assumptions; never invent paths, line numbers, measurements, or command results. Use symbols or quoted snippets when files are unavailable.
- In a combined review, give a shared root cause one finding ID and a primary remediation owner; other topics cross-reference it. Keep each topic's grade faithful to its own assessed consequences, as in solo use. Do not add topic counts into a total: deduplicate shared IDs first. A production defect and a test gap are separate only when they need independent corrections.
- Review checks must preserve source and configuration. Run reproductions or commands that may alter module files, generated files, or build outputs in a disposable copy when needed. Respect the project's build mode and side-effect constraints; report blocked checks as limits.

## Establish the review boundary

1. Identify the exact diff or code area, its library, CLI, or service context, and relevant workload: input size, call frequency, concurrency, latency or memory budget, and resource limits when known. Inspect callers, benchmarks, profiles, configuration, `go.mod`, `go.work`, build tags, and deployment settings only as needed. Distinguish introduced issues from relevant existing constraints; do not grade unrelated debt.
2. Trace the work and its ownership. What is allocated or retained per call? What grows with input or concurrency? Who closes files, rows, bodies, timers, connections, and background work? Which paths block when a pool or queue is full? Establish whether a suspected cost is on a meaningful path before proposing an optimization.
3. Check the effective Go language and toolchain versions before recommending a version-specific API or interpreting runtime behavior. Verify a current claim against Go documentation when it matters; compiler thresholds, runtime defaults, and benchmark results can change by release and platform.
4. Prefer comparative evidence for speed and allocation claims: representative benchmarks, profiles, traces, resource metrics, or a clearly derived complexity bound. A deterministic leak or unbounded growth path can be reported from code without a production profile. Treat a compiler diagnostic, missing benchmark, or optional optimization as a lead, not an automatic defect. State uncertainty and checks not run rather than inventing a regression.
5. Report distinct root causes with code or measurement evidence and concrete consequences. Give verified strengths the same specificity. Connect each negative finding to a targeted change and explain the expected benefit and how to verify it.

Read [Performance decisions](references/performance-decisions.md) when a finding involves GC or `GOMEMLIMIT`, allocation or `sync.Pool`, profiling or PGO, benchmarks, database or HTTP pools, streaming, concurrency primitives, compiler tricks, or `unsafe`. It supplies context-sensitive distinctions and links to primary Go guidance.

## Review questions

| Area | What to establish |
| --- | --- |
| Work and complexity | Does work scale acceptably with realistic input, calls, and concurrency? Are repeated scans, copying, serialization, database round trips, or N+1 I/O on a consequential path? An asymptotic concern needs a plausible input range, not just a notation. |
| Memory and GC | Are large buffers or object graphs retained longer than needed? Would a measured hot path benefit from preallocation, streaming, reuse, or fewer pointers without undue copying or complexity? Is a `sync.Pool` used only for suitable temporary objects, with safe ownership and retention? Does a service memory limit account for non-Go memory and actual headroom? |
| Resource lifetime | Are `Close`, `Stop`, cancellation, and `rows.Err` handled where they affect completion? Can early returns, loops, or blocked goroutines retain files, sockets, timers, heap, or work indefinitely? Is a resource intentionally transferred to another owner? |
| I/O and pools | Are clients and transports reused when appropriate? Do HTTP bodies get closed, and is any attempted drain bounded by response size and cost? Are database pool limits justified by `DB.Stats`, database capacity, and wait behavior rather than fixed ratios? Is streaming preferable to materializing data for the expected volume? |
| Concurrency and contention | Can goroutines, queues, and in-flight work grow beyond the resource budget? Are backpressure and cancellation effective? If locks or atomics are changed for speed, do profiles show contention and does the replacement preserve correctness? |
| Measurement and compiler choices | Does the supplied benchmark or profile support the claimed performance conclusion for representative work and a comparable baseline? Are relevant allocations or tail behavior considered? Are PGO, inlining, bounds-check, layout, or `unsafe` changes supported by a measurable benefit and their correctness constraints? |

Performance assesses supported cost, resource growth/lifetime, and whether evidence justifies an optimization; preserving ownership and correctness is part of validating an optimization. Testing primarily assesses benchmark implementation; Architecture assesses lifecycle contracts; Observability & Resilience assesses failure containment; Security assesses attacker-driven exposure; Deployment & Operations assesses configured budgets. Apply the shared overlap rule to leaks, unsafe optimizations, and unbounded work. Do not demand profiling, PGO, runtime tuning, pooling, or a fixed benchmark count without a demonstrated need.

## Grade performance and resource management

Classify each **distinct, substantiated** issue by its effect in this codebase. A minor issue causes localized avoidable cost with little expected impact; a moderate issue causes a plausible material cost or resource pressure under normal use; a major issue breaks an important performance or resource budget, or makes likely exhaustion difficult to avoid; a critical issue creates severe systemic exhaustion or defeats the code's stated purpose. Include magnitude, frequency, and workload assumptions in the severity rationale. A merge recommendation, if requested, is separate from the grade. Count root causes, not occurrences. An unmeasured micro-optimization is not a finding merely because it could be faster.

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

If the target contains no assessable performance or resource decision, return **Not applicable**. If the topic is relevant but essential workload, code, or runtime context is unavailable after reasonable inspection and could change the judgment, return **Insufficient evidence**. Explain what is missing and what would permit grading. Absence of a profile alone does not make an obvious leak ungradable; absence of measured impact may make a speculative micro-optimization unreportable. Do not use either state to avoid a supportable judgment.

## Report

Use the template below. For a letter grade retain every field and section; write `None verified`, `None found`, or `None needed` when appropriate. For Not applicable or Insufficient evidence, retain Scope, Coverage, Rationale, and Limits; omit counts and unsupported Good/Bad/changes. Reference each Bad finding by ID in Suggested changes. Put optional follow-ups or ungraded related findings after the required sections and label them explicitly.

```markdown
## Performance & Resource Management — [grade | Not applicable | Insufficient evidence]
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

Prefer `path:line` references when files are available. Give each bad finding a corresponding change; distinguish required corrections from optional experiments. The grade assesses only performance and resource management in the requested scope, not overall Go quality.
