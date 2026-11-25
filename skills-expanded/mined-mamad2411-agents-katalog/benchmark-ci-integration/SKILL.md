---
name: benchmark-ci-integration
description: Use when BenchmarkDotNet results must gate PRs, track regressions across commits, or be stored as durable CI artifacts with threshold-based enforcement.
---

# BenchmarkDotNet CI Integration

## Specialization

Use this skill to design and review CI integration for BenchmarkDotNet suites — covering execution strategy, artifact storage, regression detection, and PR gate configuration.

This skill is specialized for CI lifecycle and threshold enforcement. It does not interpret statistical results or design benchmark experiments.

## Objective

Produce a deterministic, reproducible CI benchmark integration plan with explicit execution strategy, artifact contract, threshold policy, and regression gate rules.

## Trigger Conditions

- BenchmarkDotNet results must gate PR merges.
- Benchmark regressions escaped code review and must be caught in CI.
- Benchmark artifacts are not stored or not traceable across commits.
- A new benchmark suite needs CI lifecycle design from scratch.
- Existing CI benchmark jobs produce noisy or non-deterministic results.

## Scope Boundaries

In scope:

- CI execution strategy: job isolation, machine type, and build configuration.
- Artifact storage: result format, naming convention, and retention policy.
- Threshold enforcement: regression detection rules and PR gate policy.
- Suite separation: benchmark jobs versus unit test gates.
- Preview versus decision-grade run configurations.

Out of scope:

- Statistical interpretation of individual results (use `benchmark-statistical-analysis`).
- Benchmark experiment design (use `benchmark-experiment-design`).
- Release promotion sign-off (use `benchmark-quality-gate`).

## Inputs

- Benchmark project path and target runtime.
- CI platform (GitHub Actions assumed; note differences for other platforms).
- Threshold policy: regression sensitivity and allowed variance.
- Artifact retention requirements.
- PR gate requirements (blocking or advisory).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- CI execution strategy document.
- Artifact storage contract with format, naming, and retention policy.
- Threshold enforcement policy with regression definition and gate classification.
- GitHub Actions job specification (or equivalent).
- Noise-reduction controls checklist.
- Regression alert and owner routing plan.

## CI Execution Strategy Rules

**Job Isolation**
- Never co-locate benchmark jobs with unit test jobs. Run on a dedicated job or self-hosted runner.
- Prefer self-hosted runners with known, stable hardware for decision-grade runs.
- GitHub-hosted runners are acceptable for preview gates only — document the noise limitation.

**Build Configuration**
- Always build in Release configuration.
- Pin SDK and runtime versions via `global.json` and explicit job environment.
- Do not use `ShortRunJob` for regression-detection gates; use full job configuration.
- Use `ShortRunJob` only for PR preview gates where advisory-only results are acceptable.

**Suite Separation**
- Benchmark jobs must not block unit test gates. Run in a separate, parallel job.
- Benchmark gate results should be reported as a separate CI check so failures are attributable.

**Execution Frequency**
- Full benchmark suites: run on merge to main or on schedule (nightly recommended).
- Preview benchmark suites: run on PR with `ShortRunJob` and advisory-only reporting.
- Do not require full benchmark suite completion for every PR unless suite duration is under 5 minutes.

## Artifact Storage Contract

| Field | Requirement |
|---|---|
| Format | BenchmarkDotNet Markdown, JSON, or CSV artifact |
| Naming convention | `{benchmark-class}-{commit-sha}-{date}.{ext}` |
| Storage location | CI artifact store or dedicated performance artifact path |
| Retention | Minimum 90 days; prefer permanent for baseline commits |
| Baseline artifact | Tag baseline commit artifact explicitly for regression comparison |

## Threshold Enforcement Policy

**Regression Definition**
- A regression is confirmed when: Ratio > 1.10 (10% slower), confidence is Strong per `benchmark-statistical-analysis`, and the result is replicated across at least two runs.
- Advisory regressions (Ratio 1.05–1.10) are logged but do not block merge.
- Allocations: a 20% or greater increase in allocated bytes is a regression when accompanied by no time improvement.

**Gate Classification**

| Threshold Breach | Gate Action |
|---|---|
| Confirmed regression (>10%) | Block merge; require explicit owner acknowledgment |
| Advisory regression (5–10%) | Post PR comment; advisory only |
| Allocation regression (>20%, no time gain) | Block merge |
| Inconclusive result (weak/insufficient confidence) | Post PR comment; do not block |

**Noise Budget**
- GitHub-hosted runners: assume up to 15% variance; advisory-only gates only.
- Self-hosted stable runners: assume up to 5% variance; blocking gates supported.

## GitHub Actions Job Skeleton

```yaml
benchmark:
  name: Benchmark Suite
  runs-on: [self-hosted, benchmark]  # Use stable dedicated runner
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        global-json-file: global.json
    - name: Run benchmarks
      run: dotnet run -c Release --project src/MyProject.Benchmarks -- --exporters json markdown
    - name: Upload benchmark artifacts
      uses: actions/upload-artifact@v4
      with:
        name: benchmark-results-${{ github.sha }}
        path: BenchmarkDotNet.Artifacts/
        retention-days: 90
```

## Noise-Reduction Controls Checklist

| Control | Self-Hosted Runner | GitHub-Hosted Runner |
|---|---|---|
| Release build | Required | Required |
| SDK version pinned via global.json | Required | Required |
| Dedicated runner (no co-tenancy) | Required | Not available |
| Power profile: high-performance | Required | Not controllable |
| Background process isolation | Required | Partial |
| Warm machine before run | Required | Not controllable |
| ShortRunJob for PR preview | Acceptable | Required |
| Full job config for merge gate | Required | Advisory only |

## Regression Alert and Routing

- Regression alerts must name an owning team or individual in the PR comment.
- Regression context must include: which method, which run, ratio, error, and linked artifact.
- Acknowledged regressions must be recorded in the change artifact before merge is unblocked.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| CI execution strategy | CI Execution Strategy Rules |
| Artifact storage and traceability | Artifact Storage Contract |
| Threshold policy and regression definition | Threshold Enforcement Policy |
| GitHub Actions job specification | GitHub Actions Job Skeleton |
| Noise-reduction controls | Noise-Reduction Controls Checklist |
| Regression routing and ownership | Regression Alert and Routing |

## Sources

- [dotnet/performance CI Workflow](https://github.com/dotnet/performance/blob/main/docs/benchmarking-workflow-dotnet-runtime.md)
- [dotnet/performance Repo](https://github.com/dotnet/performance) — reference benchmark suite structure at scale
- [BenchmarkDotNet GitHub](https://github.com/dotnet/BenchmarkDotNet) — exporter and runner options
- [GitHub Actions – actions/setup-dotnet](https://github.com/actions/setup-dotnet)
