---
name: review-service
description: Review an entire service for release readiness, evaluating code, contracts, data migrations, dependencies, operational exposure, SLO budgets, and rollout safety. Use when conducting full-service audits, production-readiness reviews, pre-release hardening, or broad release verification.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Review Service

Use this skill for an end-to-end service review, not a narrow code diff.

## When to Use

- full-service release-readiness audit
- pre-release hardening
- broad review across code, contracts, deps, rollout, docs
- production-readiness check

## Core Rules

- decide whether the service is ready to ship, not only whether code looks clean
- map the service boundary before judging release risk
- check code, contracts, data, dependencies, operations, and documentation together
- fix clear local issues when that is in scope
- escalate decisions that require product, architecture, security, or operational ownership
- **SLO-RELEASE-GATE**: Before marking a service release-ready, verify: SLO dashboards show no active burn-rate alerts, error budget remaining for the month is above the team's minimum threshold, and P99 latency is within the service's SLO. A release that depletes remaining error budget requires explicit SRE sign-off.
- **SBOM-IN-RELEASE**: Attach the current SBOM (CycloneDX 1.6 or SPDX format) to the release artifact; verify no new Critical/High CVEs were introduced since the last release using Dependency-Track, Grype, or Trivy.
- **CHAOS-ENGINEERING-PRE-RELEASE**: For critical services, run a limited chaos experiment (LitmusChaos, Toxiproxy) in staging before release; verify graceful degradation under one dependency failure and document the result in the release artifact.

## Suggested Process

### 1. Sync Context

- pull the latest code when allowed
- identify the service root, entry points, worker processes, migrations, configs, and deploy manifests
- locate local standards under `docs/standards/`, `docs/infrastructure/`, or equivalent

### 2. Index The Service

Map the service before judging it:

- transport or API layer
- business logic layer
- data layer
- shared clients and shared libraries
- worker, cron, outbox, or event consumers
- API contracts and migrations

### 3. Run A Full Review

Apply the `review-code` checklist across the service, then expand to service-level risk:

- backward compatibility for APIs and events
- dependency health and version drift
- rollout safety for schema and config changes
- operational readiness such as probes, limits, alerts, and recovery path

### 4. Cross-Service Impact

Check who depends on this service:

- imports of its client or contract packages
- downstream event consumers
- shared tables, topics, or feature flags
- infra objects tied to the service name or ports

### 5. Fix Or Escalate

- fix release-blocking issues before considering release
- fix important issues when the solution is clear and local
- report lower-risk follow-up items unless they are trivial to address
- stop and escalate when a fix requires product or architecture decisions

### 6. Validate

Run the validations that make sense for the repo:

- code generation
- build checks
- unit or integration tests
- linting
- manifest validation or dry-run checks

### 7. Release Readiness

Verify that:

- config added in code exists in manifests or runtime config
- ports, probes, and app IDs line up
- migrations are safe to roll forward
- rollback is possible
- docs and changelog reflect the shipped behavior

## Review Artifact

Create or update a repo-local review artifact when the repository has a convention for it. Good examples:

- `docs/reviews/<service>-review.md`
- `docs/checklists/<service>-release.md`
- a service-local release note or changelog entry

Do not force a specific docs layout if the repo uses a different convention.

## Output Format

```markdown
## Service Review: <service>

Status: Ready | Needs Work | Not Ready

### Blocking
1. [file:line] Blocking issue

### Important
1. [file:line] Issue that should be fixed before release

### Follow-Up
1. [file:line] Follow-up issue

### Completed Fixes
1. Short description

### Validation
- build: pass/fail
- tests: pass/fail/not run
- lint: pass/fail/not run
- deploy checks: pass/fail/not run

### Release Risks
- short list of remaining risk or unknowns
```

## Checklist

- [ ] service boundary and entrypoints identified
- [ ] local standards and docs reviewed when present
- [ ] service layers and key flows mapped
- [ ] code, contracts, data, and dependencies reviewed
- [ ] rollout, config, and operations impact checked
- [ ] clear local fixes applied when in scope
- [ ] repo-local validation completed or explicitly skipped
- [ ] release risks and follow-up items captured

## Adaptation Notes

Adapt these assumptions to the active repo:

- `common/` may be a different shared module
- `gitops/` may instead be `deploy/` or `k8s/`
- standards docs may live outside `docs/standards/`
- some services may not have workers, events, protobuf, or separate manifests

Skip absent concepts. Do not mark them as findings just because this pack mentions them.

## Failure Modes

- **Review without a fixed point**: a review is requested before the diff is complete. **Mitigation:** fail fast on bad ref or empty diff; surface the failure to the reviewer.
- **Two-axis collapse**: the Standards and Spec axes are merged into a single ranking. **Mitigation:** report the two axes side by side; never pick a single winner across axes.
- **Spec missing silently**: a review proceeds without a spec source. **Mitigation:** if the spec is missing, report "no spec available" and skip the Spec axis; do not invent requirements.
- **Smell baseline over repo standard**: a finding flags a smell that the repo explicitly endorses. **Mitigation:** repo-documented standards override the smell baseline; suppress the smell where the repo endorses it.

## Output Contracts

When the service review produces a structured handoff (release
readiness gate, multi-role delivery), emit:

- **`contracts/schemas/incident-report.json`** (or a release-readiness variant) capturing the readiness verdict, the evidence, the blockers, and the residual risk.
- For human-readable reports, the markdown release-readiness summary is the canonical format; emit JSON only when crossing a role boundary.

Skip emission for informal service walkthroughs that do not gate a release.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the service's auth surface and data handling must be reviewed; never expose raw credential patterns in the review findings.
- **ASI04 Supply Chain**: dependency and runtime versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI07 Inter-Agent Communication**: the review deliverable is consumed by SRE, release, and management roles; emit a structured contract so each role can validate.
- **ASI08 Cascading Failures**: a release-blocking issue must be surfaced to the coordinator before the gate opens; do not silently absorb the risk.
- **ASI09 Human-Agent Trust Exploitation**: do not present a service as "release-ready" without the actual evidence; surface the residual risk and the unverified checks.

## Related Skills

- **navigate-service**: Map a service before reviewing it
- **review-code**: Review concrete code paths and diffs
- **security-audit**: Deepen security and trust-boundary review
- **setup-deployment**: Check deployment source-of-truth changes
- **commit-code**: Prepare reviewed fixes for delivery

