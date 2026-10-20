---
name: benchmark-baseline-management
description: Use when BenchmarkDotNet baselines must be tracked, locked, compared, or governed across commits, branches, and releases to prevent longitudinal performance regression.
---

# BenchmarkDotNet Baseline Management

## Specialization

Use this skill to design and operate a longitudinal benchmark baseline governance model — covering when to lock a new baseline, how to compare across runs using ResultsComparer, what constitutes a suite-level regression, and how baseline history is stored and audited.

This skill is specialized for baseline lifecycle governance. It does not cover per-run statistical interpretation (handled by `benchmark-statistical-analysis`) or PR-gate threshold configuration (handled by `benchmark-ci-integration`).

## Objective

Produce a deterministic baseline governance model with explicit lock criteria, comparison workflow, regression classification policy, and history storage contract that can be applied consistently across projects.

## Trigger Conditions

- A performance improvement is confirmed and the baseline must be advanced.
- A regression was accepted (intentional trade-off) and the baseline must be updated with rationale.
- Benchmark results across multiple commits must be compared to detect longitudinal drift.
- A new benchmark suite is ready for initial baseline lock.
- A project needs a baseline governance policy before enabling CI regression gates.

## Scope Boundaries

In scope:

- Baseline lock criteria and lock decision workflow.
- ResultsComparer usage for cross-run and cross-commit comparison.
- Baseline artifact naming, storage, and history retention policy.
- Suite-level regression classification (beyond single-method PR gates).
- Baseline rollback policy for reverted changes.
- Baseline ownership and approval requirements.

Out of scope:

- Per-run statistical confidence interpretation (covered by `benchmark-statistical-analysis`).
- PR-gate threshold enforcement and runner configuration (covered by `benchmark-ci-integration`).
- Benchmark experiment structural design (covered by `benchmark-experiment-design`).

## Inputs

- Benchmark suite name and target project.
- Current baseline artifact path and commit reference.
- Candidate results for comparison.
- Threshold policy for regression and improvement classification.
- Approval requirements for baseline advancement.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Baseline lock decision with criteria assessment and approval record.
- ResultsComparer comparison output with suite-level verdict.
- Regression or improvement classification table.
- Updated baseline artifact with commit reference and lock rationale.
- History ledger entry for the lock event.

## Baseline Lock Criteria

A new baseline may be locked when **all** of the following are satisfied:

| Criterion | Requirement |
|---|---|
| Statistical confidence | `Strong` verdict from `benchmark-statistical-analysis` for all changed methods |
| Replication | Minimum two independent runs on the same machine confirm the result |
| Environment stability | Machine identifier, SDK, and OS recorded and match prior baseline environment |
| Change traceability | Commit SHA or PR reference that introduced the change is recorded |
| Approval | At least one named owner has approved the advancement |

A baseline must **not** be locked when:

- Confidence is Weak or Insufficient for any method showing a material change.
- Results were produced on a GitHub-hosted runner (advisory only; baselines require self-hosted stable runners).
- The change is a known temporary regression accepted under a documented exception.

## Baseline Regression Classification

Suite-level regression is distinct from per-PR-gate regression. Evaluate at the suite level after each baseline comparison:

| Class | Condition | Action |
|---|---|---|
| **Confirmed regression** | Any method Ratio > 1.10, Strong confidence, not previously acknowledged | Block baseline advancement; open regression finding |
| **Accepted regression** | Ratio > 1.10, Strong confidence, intentional trade-off with explicit rationale | Advance baseline with rationale recorded in lock entry |
| **Advisory drift** | Any method Ratio 1.05–1.10 across three or more consecutive baseline comparisons | Escalate to owner for investigation |
| **Improvement** | Any method Ratio < 0.90, Strong confidence | Eligible for baseline advancement |
| **Stable** | All methods Ratio 0.90–1.10, Weak or Strong confidence | No lock action required |

## ResultsComparer Usage

`ResultsComparer` is the .NET team's tool for structured cross-run comparison. It consumes BenchmarkDotNet JSON artifacts.

### Installation

```bash
dotnet tool install -g ResultsComparer
```

### Basic Comparison

```bash
# Compare candidate results against locked baseline
dotnet-results-comparer --base ./baselines/baseline-<commit>.json \
                        --diff ./BenchmarkDotNet.Artifacts/results/*.json \
                        --threshold 5%
```

### Output Interpretation

| ResultsComparer Output | Meaning |
|---|---|
| `Faster` | Candidate is faster than baseline by more than the threshold |
| `Slower` | Candidate is slower than baseline by more than the threshold |
| `Same` | Difference is within the noise threshold |
| `Unknown` | Insufficient data to classify |

- Use `--threshold` matching the project's regression sensitivity (default: 5%).
- `Unknown` results require re-running with a larger iteration count before classification.
- Always run ResultsComparer on JSON exports, not markdown tables (markdown precision is insufficient).

### Generating JSON Artifacts

Add the JSON exporter to the benchmark configuration:

```csharp
var config = DefaultConfig.Instance
    .AddExporter(JsonExporter.Full);
```

Or via command-line argument:

```bash
dotnet run -c Release --project MyProject.Benchmarks -- --exporters json
```

## Baseline Artifact Storage Contract

| Field | Requirement |
|---|---|
| File naming | `baseline-<suite-name>-<commit-sha>.json` |
| Storage location | `./baselines/` in the benchmark project, or dedicated artifact store path |
| Baseline index file | `./baselines/INDEX.md` — lists all locked baselines with commit, date, environment, and rationale |
| Retention | Permanent for locked baselines; do not prune without explicit governance approval |
| Environment record | Machine identifier, CPU, OS, .NET SDK version embedded in the lock entry |

## Baseline Index Entry Format

```markdown
## Baseline: <suite-name>-<commit-sha>
- Locked: <YYYY-MM-DD>
- Commit: <sha>
- Environment: <CPU model>, <OS>, .NET SDK <version>
- Locked by: <name or role>
- Rationale: <why this result is the new baseline>
- Prior baseline: <prior commit-sha or "initial">
- ResultsComparer verdict: <Faster / Improvement / Stable>
```

## Baseline Rollback Policy

A baseline rollback is required when:

- The commit that introduced the baseline has been reverted.
- The baseline was locked with insufficient evidence (Weak or Insufficient confidence discovered post-lock).
- The locked environment was non-compliant (discovered post-lock).

Rollback procedure:

1. Restore the prior baseline artifact as the active baseline.
2. Record a rollback entry in the baseline index with the rollback reason and approver.
3. Notify CI owners to update the artifact reference in the threshold enforcement job.
4. Do not delete the rolled-back baseline artifact — retain it with a `ROLLED-BACK` prefix in the index.

## Baseline Ownership and Approval

- Every baseline lock requires a named approver recorded in the index entry.
- For performance-sensitive modules, require two approvers: one engineering owner and one performance owner.
- Accepted regressions require explicit sign-off from the product or delivery owner in addition to the engineering owner.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Lock criteria and decision workflow | Baseline Lock Criteria |
| Suite-level regression classification | Baseline Regression Classification |
| ResultsComparer usage | ResultsComparer Usage |
| Artifact naming and storage | Baseline Artifact Storage Contract |
| Baseline history and audit trail | Baseline Index Entry Format |
| Rollback policy | Baseline Rollback Policy |
| Approval requirements | Baseline Ownership and Approval |

## Sources

- [dotnet/performance – ResultsComparer](https://github.com/dotnet/performance/tree/main/src/tools/ResultsComparer) — canonical comparison tool and usage patterns
- [dotnet/performance – Benchmarking Workflow](https://github.com/dotnet/performance/blob/main/docs/benchmarking-workflow-dotnet-runtime.md) — baseline governance patterns from the .NET runtime team
- [BenchmarkDotNet Docs – Exporters](https://benchmarkdotnet.org/articles/configs/exporters.html) — JSON export configuration
- [Andrey Akinshin's Blog](https://aakinshin.net/) — longitudinal result interpretation and drift detection
