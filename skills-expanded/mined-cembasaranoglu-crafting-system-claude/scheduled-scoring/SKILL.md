---
name: scheduled-scoring
description: Interprets CI report artifacts (JUnit, Sonar, Codecov, OpenSSF Scorecard, SAST/SCA, secret-scan, GitLab code-quality JSON), normalizes them into a 21-score catalog, computes a weighted repository health score, compares against a prior report for trend, and produces immediate / this-week / later recommended actions. Use when reviewing scheduled scan output or planning a daily, weekly, or monthly repository scoring cadence.
---

# Scheduled Scoring

Apply the boundary first: **CI measures, Claude interprets.** Do not run scanners or clone target repos inside a scheduled task; that work belongs in GitHub Actions or GitLab Pipelines.

The full operating contract — score catalog, schedule routing matrix, cadence, weighted profiles, and output schema — is in `references/`:

- `163_scheduled_scoring_system.md` — primary prompt
- `scheduled_scoring_policy.yaml` — weighted profiles, bucket membership, routing matrix, hard rules
- `scheduled_run_report.schema.yaml` — output schema (every run must conform)
- `adr-0005-scheduled-scoring-boundary.md` — boundary rationale

Workflow:

1. Identify the surface (trigger / interpret / summarize). Ask once if unclear.
2. Confirm required inputs (repo identity, CI artifacts, optional previous report, optional profile).
3. If inputs are missing, return a `minimum_input_request` instead of guessing.
4. Parse the provided artifacts and map findings into the score catalog.
5. For any score without an artifact, set `not_run` with a reason — no silent zeros.
6. Compute the weighted total per the active profile (default: `standard`).
7. If a previous report is provided, compute trend (`degraded_areas`, `improved_areas`, `delta`).
8. Produce `recommended_actions` in `immediate`, `this_week`, `later`, each linked to evidence.
9. Validate the output against the run-report schema.

Hard stops:

- Apparent secret in evidence -> stop, follow secret-aware credential handling.
- Recommended action implies destructive change -> escalate for human approval.
- Request asks Claude to run scanners directly -> refuse and redirect to CI.
