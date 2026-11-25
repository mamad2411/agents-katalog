---
name: benchmark-quality-gate
description: Use when a BenchmarkDotNet suite or benchmark-driven performance change needs an expert, evidence-first quality decision with deterministic findings and a go or no-go recommendation.
---

# BenchmarkDotNet Quality Gate

## Specialization

Use this skill to evaluate BenchmarkDotNet suites and benchmark-driven performance changes with deterministic quality checks and one explicit go or no-go recommendation.

This skill is specialized for review and sign-off decisions. It does not design benchmarks or configure CI pipelines.

## Objective

Produce one deterministic benchmark quality verdict with severity-ranked findings, remediation ownership, and a release recommendation.

## Trigger Conditions

- A performance change is promotion-bound and requires evidence-first sign-off.
- A benchmark suite has accumulated quality debt (structural issues, noise, missing baselines).
- A regression was detected and the remediation must be verified before reintroduction.
- A benchmark-driven decision is disputed and requires independent quality assessment.
- A new benchmark suite is complete and needs acceptance review before CI registration.

## Scope Boundaries

In scope:

- Experiment design quality: scope isolation, baseline presence, parameterization adequacy.
- Statistical confidence adequacy: evidence strength classification per `benchmark-statistical-analysis`.
- Environment discipline: Release build, runtime pinning, machine documentation.
- CI integration quality: artifact storage, threshold policy, runner type appropriateness.
- Allocation and GC pressure assessment.
- Decision traceability: hypothesis, decision context, and acceptance criteria documented.

Out of scope:

- Product feature implementation.
- Non-benchmark operational release tasks.
- Statistical result computation (use `benchmark-statistical-analysis` for raw result interpretation).

## Inputs

- Target benchmark artifacts and result tables.
- Benchmark experiment specification (hypothesis, decision context, scope).
- CI configuration and threshold policy.
- Existing defect history or prior regressions.
- Required quality threshold policy.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Findings table with severity, impact, owner, and remediation.
- Evidence adequacy summary per benchmark method.
- CI integration compliance verdict.
- Decision traceability completeness check.
- Final recommendation: pass, pass-with-conditions, or fail.

## Quality Check Dimensions

### D1 — Experiment Design Quality

| Check | Pass Condition |
|---|---|
| One concern per benchmark method | Each method measures exactly one isolated behavior |
| Baseline method present | `[Benchmark(Baseline = true)]` exists and is the current production implementation |
| Parameterization realistic | `[Params]` values reflect production input sizes and shapes |
| Setup in `[GlobalSetup]` | No allocation or state preparation inside measured methods |
| Dead-code elimination mitigated | Methods return computed values or use `Consumer` |
| Sync and async paths separated | No mixed sync/async in the same benchmark method |

### D2 — Statistical Confidence Quality

| Check | Pass Condition |
|---|---|
| Confidence adequacy | `Strong` verdict from `benchmark-statistical-analysis` |
| No overlapping CI declared as winner | CI overlap assessed and documented |
| Error bounds documented | `Error` column recorded and assessed |
| Outlier rationale present | Non-default outlier config has documented justification |
| Minimum two independent runs | Replication requirement satisfied |

### D3 — Environment Discipline Quality

| Check | Pass Condition |
|---|---|
| Release build confirmed | Build configuration is Release |
| SDK and runtime pinned | `global.json` and project TFM are explicit |
| Machine documented | CPU model, OS, RAM, power profile recorded in artifact |
| Thermal state noted | Machine was at steady state before run |

### D4 — CI Integration Quality

| Check | Pass Condition |
|---|---|
| Dedicated runner for blocking gates | Self-hosted stable runner used; GitHub-hosted used only for advisory |
| Artifacts stored with naming contract | Commit SHA and date in artifact name; 90+ day retention |
| Threshold policy documented | Regression threshold and gate classification defined |
| Suite separated from unit test gate | Benchmark job is a distinct, independently reported CI check |

### D5 — Decision Traceability Quality

| Check | Pass Condition |
|---|---|
| Hypothesis documented | What was expected and why |
| Decision context present | What decision this benchmark informs |
| Acceptance criteria explicit | Measurable threshold defined before the run |
| Recommendation recorded | Accept / reject / inconclusive with rationale |

## Severity Model

- `critical`: direct risk of false confidence in a promotion-bound decision.
- `high`: material evidence gap or structural defect that invalidates the result.
- `medium`: meaningful quality debt with bounded risk; must be remediated within one sprint.
- `low`: minor clarity or consistency issue with no immediate decision impact.

## Decision Rules

| Recommendation | Condition |
|---|---|
| **pass** | No unresolved critical or high findings across all five dimensions |
| **pass-with-conditions** | Only medium or low findings remain; each has an owner and remediation target date |
| **fail** | One or more unresolved critical findings, or unresolved high findings in promotion-bound paths |

## Findings Table Template

| ID | Dimension | Severity | Finding | Impact | Owner | Remediation |
|---|---|---|---|---|---|---|
| F1 | D1 | critical | | | | |
| F2 | D2 | high | | | | |

## Final Recommendation Template

```markdown
## Benchmark Quality Gate — [SuiteName]
## Date: [YYYY-MM-DD]
## Evaluator: benchmark-quality-gate skill

### Dimension Verdicts
| Dimension | Outcome | Open Findings |
|---|---|---|
| D1 Experiment Design | Pass / Fail | [count] |
| D2 Statistical Confidence | Pass / Fail | [count] |
| D3 Environment Discipline | Pass / Fail | [count] |
| D4 CI Integration | Pass / Fail | [count] |
| D5 Decision Traceability | Pass / Fail | [count] |

### Recommendation: [PASS / PASS-WITH-CONDITIONS / FAIL]
**Rationale:** [one sentence]

### Residual Risks
[List any medium or low findings that remain after conditional approval, with owner and date.]
```

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Experiment design quality check | Quality Check Dimensions – D1 |
| Statistical confidence adequacy | Quality Check Dimensions – D2 |
| Environment discipline check | Quality Check Dimensions – D3 |
| CI integration compliance | Quality Check Dimensions – D4 |
| Decision traceability check | Quality Check Dimensions – D5 |
| Severity-ranked findings | Severity Model + Findings Table Template |
| One deterministic recommendation | Decision Rules + Final Recommendation Template |

## Sources

- [BenchmarkDotNet Docs](https://benchmarkdotnet.org/articles/overview.html)
- [Andrey Akinshin's Blog](https://aakinshin.net/) — statistical confidence and distribution quality
- [dotnet/performance CI Workflow](https://github.com/dotnet/performance/blob/main/docs/benchmarking-workflow-dotnet-runtime.md) — CI integration quality patterns
- [Adam Sitnik's Blog](https://adamsitnik.com/) — experiment design pitfalls
