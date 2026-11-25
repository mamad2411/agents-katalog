---
name: ci-failure-triage
description: "Investigates failed CI/CD jobs by correlating the failing step, logs, workflow configuration, dependency state, and recent changes. Use when a GitHub Actions or other pipeline run fails, hangs, or becomes flaky."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# CI Failure Triage

## Goal
Classify the pipeline failure and isolate the smallest evidence-backed cause without masking real defects.

## Workflow
1. Identify the exact workflow, job, step, commit, runner/OS, trigger, and failure time. Separate the first meaningful failure from cascading errors.
2. Read the workflow definition and repository instructions. Inspect the relevant logs around the earliest causal error, not only the final summary.
3. Classify the failure: product/test regression, dependency or lockfile drift, environment/toolchain mismatch, credentials/permissions, network/external service, cache corruption, resource exhaustion, timeout, or likely flake.
4. Compare against a known-good run or previous commit when available. Check changes to workflow files, runtime versions, action versions, package manifests, lockfiles, environment variables, and service containers.
5. Form a hypothesis and choose the smallest safe check to distinguish it. Reproduce locally or rerun only when rerunning is safe and the signal is useful.
6. Apply a targeted fix only when the evidence supports it. Keep separate failures separate; do not change many unrelated variables at once.
7. If a flake is suspected, identify the non-determinism (timing, shared state, retries, ordering, resource contention, external dependency) and propose or add instrumentation/test isolation.
8. Verify the failure is resolved with the same or equivalent checks. Confirm workflow syntax and permissions when configuration changed.

## Recommendations by class
- **Code/test regression:** reproduce the failing test and fix the product or test setup.
- **Toolchain/dependency drift:** align pinned runtime, package manager, and lockfile; avoid floating versions where reproducibility matters.
- **Permission/authentication:** apply least-privilege permissions and use supported secret injection; never print tokens.
- **Network/external service:** distinguish transient provider outage from application defect; use bounded retries only for retryable failures.
- **Cache:** prove the cache is causal before changing keys or disabling it permanently.
- **Flake:** do not use repeated retries as the sole fix. Preserve the test and investigate nondeterminism.
- **Resource/timeout:** inspect resource use and job boundaries before increasing timeouts.

## Final report
State the failure class, first causal evidence, likely/verified cause, exact fix, verification status, and any provider or environment limitation. Mark the root cause as unconfirmed when evidence is inconclusive.

## Safety
Do not expose secrets from CI logs. Do not weaken branch protection, disable required checks, grant broad permissions, or skip failing tests merely to make the pipeline green. Avoid triggering deploy workflows unless authorized.
