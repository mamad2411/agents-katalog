---
name: cortivex-drift-detection
version: 1.0.0
description: Detects when a codebase has drifted from its intended state across architecture, config, coverage, dependencies, and documentation
category: analysis
tags: [drift, architecture, config, coverage, dependencies, documentation, baseline]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [drift-scanning, baseline-management, drift-comparison, drift-reporting, scheduled-monitoring]
---

# Cortivex Drift Detection

You have access to a drift detection system that identifies when a codebase has diverged from its intended or documented state. Drift occurs silently -- architecture erodes, configs reference dead modules, test coverage slides, dependencies fall behind, and documentation describes features that no longer exist. This skill detects all of it, scores the severity, and tells you exactly what changed and when.

## Overview

Drift detection works by establishing a baseline snapshot of the codebase's intended state, then comparing the current state against that baseline on every scan. The system tracks five drift categories independently, each with its own detection strategy and severity scoring.

The drift score is a composite 0-100 value where 0 means the codebase perfectly matches its baseline and 100 means catastrophic divergence across all categories. Scores above 60 indicate structural problems that will compound if left unaddressed.

## When to Use

- After a sprint or release cycle to measure how far the codebase has drifted from its documented architecture
- As a nightly scheduled scan integrated into the `nightly-review` pipeline
- Before onboarding new team members to verify that documentation matches reality
- After large refactors to confirm that configs, tests, and docs were updated to match
- When dependency update PRs have been deferred and you need to quantify the technical debt
- Before major releases to catch coverage regressions and stale documentation

## When NOT to Use

- During active development on a feature branch where drift is expected and temporary
- On brand-new projects with no established baseline (run `baseline` first)
- For real-time file watching during coding sessions (use linting and IDE tools instead)
- As a replacement for CI test suites -- drift detection complements CI, it does not replace it

## How It Works

### Drift Categories

**Architecture Drift** measures how far the actual code structure has diverged from architecture documentation. It parses architecture docs (README sections, ADRs, design docs) and cross-references them against the file tree, module boundaries, and import graphs. When docs describe a `services/` layer but all business logic has migrated into `controllers/`, architecture drift catches it.

**Config Drift** detects pipeline configurations, build configs, and CI/CD definitions that reference files, modules, environment variables, or scripts that no longer exist. A webpack config importing a deleted alias, a pipeline YAML referencing a removed node type, or a Makefile target calling a script that was renamed -- all are config drift.

**Coverage Drift** tracks test coverage against established baselines. Unlike a simple threshold check, coverage drift measures the delta from the baseline per-module. If `src/auth/` was at 92% coverage when the baseline was set and has dropped to 71%, that is a 21-point coverage drift even if the overall project coverage is still above the global threshold.

**Dependency Drift** compares installed package versions against lockfile specifications and declared version ranges. It also detects packages declared in the manifest but missing from the lockfile, packages in the lockfile but removed from the manifest, and major version gaps between declared ranges and latest available versions.

**Documentation Drift** identifies README files, API docs, and guides that describe features, endpoints, or configurations that no longer exist in the codebase, as well as new features, modules, or public APIs that have no documentation at all.

### Drift Scoring

Each category produces a score from 0 to 100:

```
category_score = (drift_items / total_items) * severity_weight * 100

where:
  drift_items     = number of items that have drifted from baseline
  total_items     = total items tracked in this category
  severity_weight = multiplier based on item severity (0.5 for low, 1.0 for medium, 2.0 for high)
```

The composite drift score is a weighted average:

```
composite = (arch * 0.25) + (config * 0.20) + (coverage * 0.20) + (deps * 0.15) + (docs * 0.20)
```

Architecture drift is weighted highest because it signals systemic structural decay. Dependency drift is weighted lowest because it is often intentional (pinning versions).

## Pipeline Configuration

### Standalone Drift Scan

```yaml
name: drift-scan
version: "1.0"
description: Full drift analysis against established baseline
nodes:
  - id: drift_scan
    type: DriftDetector
    config:
      action: scan
      repo: .
      baseline_id: latest
      categories:
        - architecture
        - config
        - coverage
        - dependencies
        - documentation
      severity_threshold: low
      output_format: structured

  - id: drift_report
    type: DriftDetector
    depends_on: [drift_scan]
    config:
      action: report
      format: markdown
      include_recommendations: true
      include_history: true
```

### Nightly Review Integration

```yaml
name: nightly-review
version: "1.0"
description: Nightly pipeline with drift detection
nodes:
  - id: drift_check
    type: DriftDetector
    config:
      action: scan
      baseline_id: latest
      categories: [architecture, config, coverage, dependencies, documentation]
      severity_threshold: medium

  - id: security_scan
    type: SecurityScanner
    config:
      scan_depth: standard

  - id: code_review
    type: CodeReviewer
    config:
      review_scope: changed_files

  - id: nightly_report
    type: CustomAgent
    depends_on: [drift_check, security_scan, code_review]
    config:
      system_prompt: |
        Combine drift analysis, security findings, and code review into a
        single nightly health report. Flag any drift score above 40 as
        requiring attention.
      output_format: markdown
```

### Scheduled Drift Watch

```yaml
name: drift-watch
version: "1.0"
description: Continuous drift monitoring with alerting
nodes:
  - id: watch
    type: DriftDetector
    config:
      action: watch
      interval_hours: 24
      baseline_id: latest
      alert_threshold: 40
      categories: [architecture, config, coverage]
      on_alert:
        action: notify
        channel: pipeline-alerts
```

## MCP Tool Reference

### Scan for Drift

```
cortivex_drift({
  action: "scan",
  repo: "/path/to/repo",
  baseline_id: "latest",
  categories: ["architecture", "config", "coverage", "dependencies", "documentation"],
  severity_threshold: "low"
})
```

**Response:**

```json
{
  "scan_id": "drift-8f2a",
  "timestamp": "2025-01-15T09:30:00Z",
  "composite_score": 37,
  "categories": {
    "architecture": {
      "score": 45,
      "items": [
        {
          "severity": "high",
          "description": "Architecture doc describes services/ layer but 6 service classes have been moved into controllers/",
          "baseline_state": "12 files in src/services/",
          "current_state": "6 files in src/services/, 6 moved to src/controllers/",
          "first_detected": "2025-01-10T14:00:00Z"
        }
      ]
    },
    "config": {
      "score": 25,
      "items": [
        {
          "severity": "medium",
          "description": "Pipeline config references LegacyParser node type which was removed in v2.3",
          "file": ".cortivex/pipelines/legacy-scan.yaml",
          "line": 14
        }
      ]
    },
    "coverage": {
      "score": 52,
      "items": [
        { "severity": "high", "description": "src/auth/ coverage dropped from 92% to 71%", "delta": -21 },
        { "severity": "medium", "description": "src/api/orders.ts has 0% coverage (new file)", "current_value": 0 }
      ]
    },
    "dependencies": {
      "score": 18,
      "items": [
        { "severity": "low", "package": "express", "declared": "^4.18.0", "locked": "4.19.0", "installed": "4.18.2" }
      ]
    },
    "documentation": {
      "score": 38,
      "items": [
        { "severity": "medium", "description": "README documents /api/v1/legacy endpoint which was removed", "artifact_status": "deleted" },
        { "severity": "medium", "description": "New public API endpoint /api/v2/analytics has no documentation" }
      ]
    }
  }
}
```

### Establish a Baseline

```
cortivex_drift({
  action: "baseline",
  repo: "/path/to/repo",
  label: "v2.4-release",
  include_categories: ["architecture", "config", "coverage", "dependencies", "documentation"],
  coverage_source: "lcov.info"
})
```

**Response:**

```json
{
  "baseline_id": "bl-3d7e",
  "label": "v2.4-release",
  "timestamp": "2025-01-15T10:00:00Z",
  "snapshot": {
    "architecture": { "modules": 14, "entry_points": 2, "documented_patterns": 5 },
    "config": { "pipeline_configs": 4, "build_configs": 2, "references_validated": 47 },
    "coverage": { "overall": 83, "per_module": { "src/auth/": 92, "src/api/": 78, "src/services/": 85 } },
    "dependencies": { "total_packages": 87, "lockfile_hash": "sha256:a1b2c3..." },
    "documentation": { "documented_endpoints": 12, "documented_modules": 9 }
  }
}
```

### Compare Two Points in Time

```
cortivex_drift({
  action: "compare",
  repo: "/path/to/repo",
  from_baseline: "bl-3d7e",
  to_baseline: "bl-9f1a",
  categories: ["architecture", "coverage"]
})
```

**Response:**

```json
{
  "from": { "id": "bl-3d7e", "label": "v2.4-release", "date": "2025-01-15" },
  "to": { "id": "bl-9f1a", "label": "v2.5-release", "date": "2025-02-01" },
  "score_delta": {
    "composite": { "from": 12, "to": 37, "change": "+25" },
    "architecture": { "from": 5, "to": 45, "change": "+40" },
    "coverage": { "from": 8, "to": 52, "change": "+44" }
  },
  "new_drift_items": 6,
  "resolved_drift_items": 2,
  "worsened_items": 3
}
```

### Generate a Drift Report

```
cortivex_drift({
  action: "report",
  repo: "/path/to/repo",
  scan_id: "drift-8f2a",
  format: "markdown",
  include_recommendations: true,
  include_history: true
})
```

**Response:**

```json
{
  "format": "markdown",
  "content": "# Drift Report - 2025-01-15\n\n## Score: 37/100 (Moderate)\n...",
  "recommendations": [
    { "priority": "high", "category": "coverage", "action": "Add tests for src/auth/ to restore from 71% to 92%", "effort": "2-3 hours" },
    { "priority": "medium", "category": "architecture", "action": "Move service classes back or update architecture docs", "effort": "1-2 hours" }
  ],
  "trend": { "direction": "worsening", "rate": "+4 points/week", "projection": "Exceeds 60 in ~6 weeks at current rate" }
}
```

### Set Up Drift Watch

```
cortivex_drift({
  action: "watch",
  repo: "/path/to/repo",
  baseline_id: "latest",
  interval_hours: 24,
  alert_threshold: 40,
  categories: ["architecture", "config", "coverage"],
  on_alert: {
    action: "notify",
    channel: "pipeline-alerts"
  }
})
```

**Response:**

```json
{
  "watch_id": "watch-4c9e",
  "status": "active",
  "next_scan": "2025-01-16T09:30:00Z",
  "alert_threshold": 40,
  "current_score": 37,
  "headroom": 3
}
```

## Node Reference

```yaml
- id: drift_detector
  type: DriftDetector
  config:
    action: scan                          # scan | baseline | compare | report | watch
    repo: .                               # repository path
    baseline_id: latest                   # baseline to compare against (id or "latest")
    categories:                           # which drift types to check
      - architecture
      - config
      - coverage
      - dependencies
      - documentation
    severity_threshold: low               # low | medium | high (minimum severity to report)
    output_format: structured             # structured | markdown | sarif
    architecture_docs:                    # paths to architecture documentation
      - README.md
      - docs/architecture.md
      - docs/adr/
    coverage_source: auto                 # auto | lcov.info | coverage.json | path
    config_paths:                         # config files to validate
      - .cortivex/pipelines/
      - webpack.config.js
      - .github/workflows/
    ignore_paths:                         # paths to exclude from all scans
      - node_modules/
      - dist/
      - vendor/
    storage_path: .cortivex/drift/       # directory for baselines and scan history
    alert_threshold: 40                   # composite score that triggers alerts
    interval_hours: 24                    # scan interval for watch mode
```

## Quick Reference

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Full scan | `cortivex_drift({ action: "scan", baseline_id: "latest" })` | Compare current state against baseline |
| Set baseline | `cortivex_drift({ action: "baseline", label: "v2.4" })` | Snapshot current state as the target |
| Compare baselines | `cortivex_drift({ action: "compare", from_baseline, to_baseline })` | Diff two baselines to see progression |
| Generate report | `cortivex_drift({ action: "report", scan_id })` | Produce markdown report with recommendations |
| Start watching | `cortivex_drift({ action: "watch", interval_hours: 24 })` | Schedule recurring drift scans with alerts |

## Best Practices

1. **Establish a baseline after every release.** Run `baseline` with a label matching your version tag. This gives you a clean reference point and makes drift reports meaningful.
2. **Integrate drift scans into nightly pipelines.** Daily scans catch drift early when it is cheap to fix. Weekly scans let small drifts compound into expensive problems.
3. **Act on scores above 40 immediately.** Drift is exponential -- a score of 40 today becomes 60 in weeks because drifted areas attract more changes that are also drifted.
4. **Use category-specific scans for targeted work.** After a refactor, scan only `architecture` and `config`. After a test sprint, scan only `coverage`. Full scans are for health checks.
5. **Track drift trends, not just snapshots.** A score of 30 that was 10 last month is more alarming than a stable score of 35. Use the `compare` action and report trend data.
6. **Update baselines intentionally, not to hide drift.** Re-baseline only when the new state is the intended state. Re-baselining to make the score look better without fixing drift defeats the purpose.
7. **Pair drift detection with fix pipelines.** When coverage drift is detected, feed the results into a TestGenerator pipeline. When documentation drift is found, feed it into a DocWriter pipeline.

## Reasoning Protocol

Before running a drift scan or acting on results, reason through:

1. **Is the baseline still valid?** If the project has undergone an intentional architectural change (monolith to microservices, framework migration), the old baseline may be obsolete. Re-baseline if the intended state has changed.
2. **Is this drift intentional or accidental?** Dependency version pins may be deliberate. A developer may have moved service classes into controllers as part of a planned refactor. Check git history and PR descriptions before flagging intentional changes as drift.
3. **Which category should I prioritize?** Architecture drift at 60 with coverage drift at 15 means focus on architecture. Do not spread effort evenly -- fix the highest-scoring category first.
4. **Is the trend getting worse or stabilizing?** A stable drift score means the team is maintaining the current state (even if drifted). A rising score means active decay. Rising scores need immediate attention; stable scores can be scheduled for later.
5. **Can I fix this drift with an automated pipeline?** Coverage drift can be addressed with TestGenerator. Documentation drift can be addressed with DocWriter. Config drift often requires manual review. Match the fix strategy to the drift type.
6. **Am I scanning too frequently or too rarely?** Daily scans suit active development. Weekly scans suit maintenance-mode projects. Scanning every hour wastes resources without adding value because drift accumulates over days, not minutes.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Never establishing a baseline | Drift scans have nothing to compare against; all results are meaningless | Run `baseline` before the first scan and after every release |
| Re-baselining to hide drift | Resets the score to 0 without fixing underlying problems; drift reappears immediately | Only re-baseline when the new state is the genuine intended state |
| Scanning all categories when you only need one | Wastes compute and produces noise that obscures the category you care about | Specify only the categories relevant to your current task |
| Ignoring drift scores below 30 | Small drift compounds silently; by the time it reaches 50+ it requires significant effort to fix | Address drift when it first appears, especially in architecture and coverage |
| Running drift scans without acting on results | Creates alert fatigue and trains the team to ignore drift reports | Every scan should produce assigned action items or an explicit decision to defer |
| Using drift detection as a gate that blocks deploys | Creates pressure to re-baseline or suppress findings rather than fix them | Use drift as an advisory metric, not a hard gate; pair with trend tracking |
| Scanning feature branches against main baseline | Feature branches are expected to diverge; flagging them as drifted is noise | Only scan the default branch or release branches against baselines |

**WRONG:**
```yaml
# Re-baselining every night to keep score at zero
name: nightly-reset
nodes:
  - id: reset_baseline
    type: DriftDetector
    config:
      action: baseline              # This just hides drift every night
      label: "nightly-auto"

  - id: scan
    type: DriftDetector
    depends_on: [reset_baseline]
    config:
      action: scan
      baseline_id: latest           # Always compares against the baseline just created
```

**RIGHT:**
```yaml
# Scan against the release baseline, report trend
name: nightly-drift
nodes:
  - id: scan
    type: DriftDetector
    config:
      action: scan
      baseline_id: "v2.4-release"   # Stable baseline from last release
      categories: [architecture, config, coverage, dependencies, documentation]

  - id: report
    type: DriftDetector
    depends_on: [scan]
    config:
      action: report
      include_recommendations: true
      include_history: true          # Shows trend over time
```

## Grounding Rules

- **No baseline exists for this repo:** Run `baseline` first with a descriptive label. Without a baseline, drift detection cannot function. Do not attempt to scan without one.
- **Drift score is high but the team says it is fine:** Present the specific drift items with evidence. A high score backed by concrete examples (deleted endpoints still in docs, coverage drops with file paths) is harder to dismiss than a number alone. But respect the team's judgment -- if the drift is intentional, re-baseline.
- **Architecture docs do not exist:** Architecture drift detection requires something to compare against. If no architecture documentation exists, skip the architecture category and suggest creating documentation as a prerequisite.
- **Coverage data is unavailable:** Coverage drift requires a coverage report (lcov, istanbul, pytest-cov). If the project has no test coverage tooling, skip the coverage category and flag the absence of coverage tooling as a finding itself.
- **Drift score suddenly jumped after a normal change:** Investigate whether the baseline was corrupted or whether a build artifact changed the file tree. False positives from generated files (dist/, build/) should be resolved by adding those paths to `ignore_paths`, not by suppressing the score.

## Advanced Capabilities

### Automated Remediation Actions

When drift is detected, the system can execute targeted remediation actions to bring the codebase back toward its baseline. Remediation supports three modes: `preview` shows what would change without applying fixes, `apply` executes the remediation, and `rollback` reverts a previous remediation by its operation ID.

```json
{
  "tool": "cortivex_drift_remediate",
  "request": {
    "action": "apply",
    "repo": "/path/to/repo",
    "scan_id": "drift-8f2a",
    "category": "config",
    "item_ids": ["cfg-001", "cfg-003"],
    "mode": "preview",
    "dry_run": true
  }
}
```

```json
{
  "tool": "cortivex_drift_remediate",
  "response": {
    "operation_id": "rem-7b3f",
    "status": "preview_ready",
    "actions": [
      {
        "item_id": "cfg-001",
        "type": "remove_dead_reference",
        "file": ".cortivex/pipelines/legacy-scan.yaml",
        "line": 14,
        "description": "Remove reference to deleted LegacyParser node type",
        "patch": "- type: LegacyParser\n+ type: StandardParser"
      },
      {
        "item_id": "cfg-003",
        "type": "update_path",
        "file": "webpack.config.js",
        "line": 22,
        "description": "Update alias from removed src/old-utils to src/utils",
        "patch": "- '@old-utils': path.resolve('src/old-utils')\n+ '@utils': path.resolve('src/utils')"
      }
    ],
    "risk_level": "low",
    "reversible": true
  }
}
```

### Drift Scoring & Severity Classification

Scoring thresholds and severity classifications are configurable per project. Define weight overrides, category-specific thresholds, and custom severity bands to match your team's risk tolerance.

```yaml
drift_scoring:
  severity_bands:
    - name: healthy
      range: [0, 20]
      color: green
      action: none
    - name: moderate
      range: [21, 40]
      color: yellow
      action: notify
    - name: concerning
      range: [41, 60]
      color: orange
      action: alert
    - name: critical
      range: [61, 100]
      color: red
      action: block_release

  category_weights:
    architecture: 0.30
    config: 0.20
    coverage: 0.20
    dependencies: 0.10
    documentation: 0.20

  severity_multipliers:
    low: 0.5
    medium: 1.0
    high: 2.0
    critical: 3.0

  per_category_thresholds:
    coverage:
      alert_at: 35
      block_at: 55
    architecture:
      alert_at: 30
      block_at: 50
```

### Baseline Management & Snapshots

Baselines can be managed programmatically through the snapshot API. Each snapshot captures the full state of all tracked categories and supports tagging, retention policies, and diff operations between arbitrary points in time.

```json
{
  "$schema": "https://cortivex.io/schemas/drift-baseline-snapshot.json",
  "type": "object",
  "properties": {
    "baseline_id": { "type": "string", "pattern": "^bl-[a-f0-9]{4,8}$" },
    "label": { "type": "string", "maxLength": 64 },
    "created_at": { "type": "string", "format": "date-time" },
    "retention": {
      "type": "object",
      "properties": {
        "policy": { "enum": ["keep_forever", "rolling", "count_based"] },
        "max_age_days": { "type": "integer", "minimum": 1 },
        "max_count": { "type": "integer", "minimum": 1 }
      }
    },
    "tags": { "type": "array", "items": { "type": "string" } },
    "categories": {
      "type": "object",
      "properties": {
        "architecture": { "$ref": "#/definitions/architecture_snapshot" },
        "config": { "$ref": "#/definitions/config_snapshot" },
        "coverage": { "$ref": "#/definitions/coverage_snapshot" },
        "dependencies": { "$ref": "#/definitions/dependency_snapshot" },
        "documentation": { "$ref": "#/definitions/documentation_snapshot" }
      }
    }
  },
  "required": ["baseline_id", "label", "created_at", "categories"]
}
```

### Trend Forecasting & Predictive Alerts

The forecasting system analyzes historical drift scores to project future values and alert before thresholds are breached. It uses linear regression over configurable time windows and can trigger preemptive notifications when a category is projected to cross a severity band boundary.

```json
{
  "tool": "cortivex_drift_forecast",
  "request": {
    "repo": "/path/to/repo",
    "categories": ["architecture", "coverage"],
    "lookback_days": 30,
    "forecast_days": 14,
    "alert_on_projected_breach": true,
    "breach_threshold": 60
  }
}
```

```json
{
  "tool": "cortivex_drift_forecast",
  "response": {
    "forecast_id": "fc-2e8d",
    "generated_at": "2025-02-01T12:00:00Z",
    "projections": {
      "architecture": {
        "current_score": 45,
        "trend_slope": 2.3,
        "projected_score_14d": 77,
        "projected_breach_date": "2025-02-08T00:00:00Z",
        "confidence": 0.87,
        "recommendation": "Architecture drift is accelerating. Address service-layer migration within 7 days to avoid critical threshold."
      },
      "coverage": {
        "current_score": 28,
        "trend_slope": 0.4,
        "projected_score_14d": 34,
        "projected_breach_date": null,
        "confidence": 0.72,
        "recommendation": "Coverage drift is stable and within acceptable bounds."
      }
    },
    "alerts": [
      {
        "category": "architecture",
        "type": "projected_breach",
        "message": "Architecture drift projected to exceed 60 by 2025-02-08",
        "days_until_breach": 7
      }
    ]
  }
}
```

### Custom Drift Rule Definitions

Define custom drift rules to detect project-specific patterns that the built-in categories do not cover. Custom rules specify a detection strategy, matching patterns, a severity level, and an optional remediation hint. Rules are evaluated during every scan alongside the built-in categories.

```json
{
  "$schema": "https://cortivex.io/schemas/drift-custom-rules.json",
  "type": "object",
  "properties": {
    "rule_id": { "type": "string", "pattern": "^rule-[a-z0-9-]+$" },
    "name": { "type": "string", "maxLength": 128 },
    "description": { "type": "string" },
    "category": { "enum": ["architecture", "config", "coverage", "dependencies", "documentation", "custom"] },
    "severity": { "enum": ["low", "medium", "high", "critical"] },
    "detection": {
      "type": "object",
      "properties": {
        "strategy": { "enum": ["file_pattern", "import_graph", "content_match", "metric_threshold"] },
        "pattern": { "type": "string" },
        "target_paths": { "type": "array", "items": { "type": "string" } },
        "baseline_key": { "type": "string" }
      },
      "required": ["strategy"]
    },
    "remediation_hint": { "type": "string" }
  },
  "required": ["rule_id", "name", "severity", "detection"]
}
```

An example rule definition that flags direct database imports outside the data access layer:

```typescript
const noDirectDbImports: DriftRule = {
  rule_id: "rule-no-direct-db-imports",
  name: "No direct database imports outside DAL",
  description: "Detects modules importing database drivers directly instead of using the data access layer",
  category: "architecture",
  severity: "high",
  detection: {
    strategy: "import_graph",
    pattern: "^(pg|mysql2|mongodb|prisma)$",
    target_paths: ["src/**/*.ts", "!src/dal/**/*.ts"],
    baseline_key: "direct_db_import_count",
  },
  remediation_hint: "Move database access through src/dal/ modules. Direct driver imports outside the DAL violate the architecture boundary.",
};
```

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for Cortivex drift detection operations, aligned with the OWASP Agentic Security Top 10 risk framework. Each subsection references the specific AST risk ID it mitigates.

### AST03: Remediation Approval Gates

Automated remediation must never apply changes to the codebase without explicit human or coordinator review. The `apply` mode requires a prior `preview` step and an approval token, preventing drift remediation from silently altering production code (AST03).

```yaml
# AST03 -- No auto-apply without review and approval
drift_detector:
  type: DriftDetector
  config:
    remediation:
      require_preview_before_apply: true       # AST03: must preview before applying
      require_approval_token: true             # AST03: gated by explicit authorization
      approval_sources:
        - coordinator
        - admin
      auto_apply: false                        # AST03: never auto-apply by default
      max_auto_remediate_items: 0              # AST03: zero items can bypass review
      on_unapproved_apply: reject_and_alert
      audit:
        log_all_remediation_requests: true
        log_approvals_and_rejections: true
        alert_on_bypass_attempt: true
```

```json
{
  "$schema": "https://cortivex.io/schemas/remediation-approval.json",
  "type": "object",
  "properties": {
    "operation_id": { "type": "string", "pattern": "^rem-[a-f0-9]{4,8}$" },
    "scan_id": { "type": "string" },
    "action": { "enum": ["preview", "apply", "rollback"] },
    "approval_token": { "type": ["string", "null"] },
    "approved_by": { "type": "string" },
    "items_reviewed": { "type": "integer", "minimum": 0 },
    "items_approved": { "type": "integer", "minimum": 0 },
    "preview_completed": { "type": "boolean" },
    "ast_risk_id": { "const": "AST03" }
  },
  "required": ["operation_id", "scan_id", "action", "preview_completed", "ast_risk_id"]
}
```

MCP tool invocation with approval gate:

```
cortivex_drift_remediate({
  action: "apply",
  repo: "/path/to/repo",
  scan_id: "drift-8f2a",
  category: "config",
  item_ids: ["cfg-001", "cfg-003"],
  approval_token: "apr-admin-4d7f",
  preview_confirmed: true
})
```

### Scan Scope Restrictions

Drift scans must exclude sensitive directories by default to prevent accidental exposure of secrets, credentials, or private keys. The default exclusion list is enforced and can only be reduced by an administrator (AST03).

```yaml
# AST03 -- Restrict scan scope to prevent sensitive data exposure
drift_detector:
  config:
    scan_scope:
      default_exclude:                         # AST03: always excluded unless admin override
        - "**/.env"
        - "**/.env.*"
        - "**/secrets/"
        - "**/credentials/"
        - "**/*.pem"
        - "**/*.key"
        - "**/*.p12"
        - "**/private/"
        - "**/.ssh/"
        - "**/.aws/"
        - "**/.gcp/"
        - "**/node_modules/"
        - "**/dist/"
        - "**/build/"
      enforce_default_exclude: true            # AST03: cannot remove defaults without admin
      admin_override_required_for:
        - removing_default_exclusions
        - scanning_dotenv_files
        - scanning_credential_directories
      max_scan_depth: 15                       # prevent unbounded directory traversal
      max_files_per_scan: 50000                # cap to prevent resource exhaustion
```

```typescript
import { DriftScanner } from "@cortivex/drift";

// AST03: Scanner enforces exclusion policy at construction
const scanner = new DriftScanner({
  repo: "/path/to/repo",
  scopePolicy: {
    enforceDefaultExclusions: true,
    additionalExclusions: ["**/vendor/", "**/tmp/"],
    maxScanDepth: 15,
    maxFilesPerScan: 50000,
    onExclusionViolation: (path: string) => {
      scanner.reportSecurityEvent({
        event: "scope_exclusion_violation",
        path,
        astRiskId: "AST03",
      });
    },
  },
});
```

### Baseline Integrity Verification

Baselines represent the trusted intended state of the codebase. To prevent tampering, each baseline snapshot is hash-signed at creation time. Before any scan comparison, the baseline signature is verified to ensure it has not been modified (AST03).

```json
{
  "$schema": "https://cortivex.io/schemas/baseline-integrity.json",
  "type": "object",
  "properties": {
    "baseline_id": { "type": "string", "pattern": "^bl-[a-f0-9]{4,8}$" },
    "content_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "signature": { "type": "string" },
    "signature_scheme": { "const": "ed25519" },
    "signed_by": { "type": "string" },
    "signed_at": { "type": "string", "format": "date-time" },
    "verification_status": { "enum": ["verified", "failed", "not_checked"] },
    "ast_risk_id": { "const": "AST03" }
  },
  "required": ["baseline_id", "content_hash", "signature", "signature_scheme", "signed_at", "ast_risk_id"]
}
```

```yaml
# AST03 -- Hash-signed baselines to prevent tampering
drift_detector:
  config:
    baseline_integrity:
      sign_on_create: true                     # AST03: sign every new baseline
      signature_scheme: ed25519
      signing_key_path: /etc/cortivex/keys/drift-baseline.key
      verification_key_path: /etc/cortivex/keys/drift-baseline.pub
      verify_before_scan: true                 # AST03: always verify before comparison
      on_verification_failure: halt_and_alert  # never scan against tampered baselines
      hash_algorithm: sha256
      include_in_hash:
        - snapshot_data
        - category_weights
        - severity_multipliers
```

MCP tool to verify baseline integrity on demand:

```
cortivex_drift({
  action: "verify_baseline",
  baseline_id: "bl-3d7e",
  checks: ["signature_valid", "content_hash_match", "no_modification_since_signing"]
})
```

### Alert Channel Authentication

Drift alerts must be delivered only to authenticated channels. Unauthenticated alert delivery creates an injection vector where an attacker could send fake drift alerts to mislead operators or suppress genuine alerts (AST03).

```yaml
# AST03 -- Authenticate all alert delivery channels
drift_detector:
  config:
    alerting:
      channels:
        - name: pipeline-alerts
          type: webhook
          url: https://hooks.internal.corp/cortivex-alerts
          authentication:
            method: hmac-sha256                # AST03: sign alert payloads
            secret_env_var: ALERT_WEBHOOK_SECRET
          tls_required: true                   # AST03: no plaintext alert delivery
          verify_tls_certificate: true
        - name: ops-slack
          type: slack
          channel_id: C04XXXXXX
          authentication:
            method: oauth2
            token_env_var: SLACK_BOT_TOKEN
      delivery_policy:
        require_authenticated_channel: true    # AST03: reject unauthenticated channels
        require_tls: true
        sign_alert_payloads: true
        on_delivery_failure: retry_then_log
        max_retries: 3
        alert_on_channel_auth_failure: true   # meta-alert: channel itself is compromised
```

```json
{
  "$schema": "https://cortivex.io/schemas/drift-alert-envelope.json",
  "type": "object",
  "properties": {
    "alert_id": { "type": "string", "pattern": "^alert-[a-f0-9]{8}$" },
    "scan_id": { "type": "string" },
    "composite_score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "breached_threshold": { "type": "integer" },
    "channel": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload_signature": { "type": "string" },
    "signature_scheme": { "const": "hmac-sha256" },
    "ast_risk_id": { "const": "AST03" }
  },
  "required": ["alert_id", "scan_id", "composite_score", "channel", "timestamp", "payload_signature", "ast_risk_id"]
}
```

### Drift Rule Validation

Custom drift rules can define remediation actions that execute arbitrary changes. Rules with dangerous remediation patterns (file deletion, permission changes, external command execution) must be rejected at load time (AST03).

```yaml
# AST03 -- Validate custom rules to block dangerous remediation actions
drift_detector:
  config:
    rule_validation:
      enabled: true                            # AST03: validate all rules before loading
      blocked_remediation_patterns:
        - "rm -rf"
        - "chmod"
        - "chown"
        - "curl"
        - "wget"
        - "eval("
        - "exec("
        - "sudo"
        - "del /f"
        - "> /dev/"
      blocked_target_paths:
        - "/etc/"
        - "/usr/"
        - "/var/"
        - "C:\\Windows\\"
        - "~/.ssh/"
      max_remediation_scope_files: 20          # AST03: cap blast radius per rule
      require_rule_signature: true             # AST03: only load signed rules
      signature_verification_key: /etc/cortivex/keys/rule-signing.pub
      on_validation_failure: reject_and_alert
```

```typescript
import { DriftRuleValidator } from "@cortivex/drift";

// AST03: Validate rules before registration
const validator = new DriftRuleValidator({
  blockedPatterns: [
    /rm\s+-rf/,
    /chmod/,
    /eval\s*\(/,
    /exec\s*\(/,
    /curl|wget/,
    /sudo/,
  ],
  blockedTargetPaths: ["/etc/", "/usr/", "/var/"],
  maxRemediationScopeFiles: 20,
  requireSignature: true,
  verificationKeyPath: "/etc/cortivex/keys/rule-signing.pub",
});

const result = validator.validate(candidateRule);
if (!result.valid) {
  validator.reportSecurityEvent({
    event: "dangerous_rule_rejected",
    ruleId: candidateRule.rule_id,
    violations: result.violations,   // e.g., ["blocked pattern: rm -rf"]
    astRiskId: "AST03",
  });
}
```

MCP tool to audit loaded rules:

```
cortivex_drift({
  action: "audit_rules",
  checks: [
    "no_blocked_remediation_patterns",
    "all_rules_signed",
    "scope_within_limits",
    "no_blocked_target_paths"
  ]
})
```
