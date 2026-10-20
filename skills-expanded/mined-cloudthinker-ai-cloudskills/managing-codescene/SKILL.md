---
name: managing-codescene
description: |
  Use when working with Codescene — codeScene behavioral code analysis including
  code health scoring, hotspot detection, change coupling analysis, and PR
  integration for code quality gates. Use when configuring CodeScene for
  codebase visualization, technical debt prioritization, and automated code
  review feedback.
connection_type: codescene
preload: false
---

# Managing CodeScene

## Overview

Manage CodeScene behavioral code analysis, including code health monitoring, hotspot detection, change coupling analysis, and pull request integration for automated code quality gates.

## Key Capabilities

- Monitor code health scores across the codebase
- Detect and prioritize hotspots (frequently changed, complex code)
- Analyze change coupling between files and components
- Integrate with PRs for automated code health gate checks
- Track developer knowledge distribution and bus factor risks
- Visualize technical debt and prioritize refactoring efforts

## Workflow

### 1 — Code Health Configuration

```
CODE HEALTH ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Analysis scope:
    - Repositories: ___
    - Branches: main, develop
    - Exclude patterns: test/**, vendor/**
[ ] Code health thresholds:
    - Healthy: 8-10
    - Warning: 4-7
    - Alert: 1-3
[ ] Analysis frequency: daily / weekly
[ ] Track trends over: 30 / 90 / 365 days
```

### 2 — Hotspot Detection

```
HOTSPOT CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Hotspot criteria:
    - Change frequency: high
    - Code complexity: high
    - Combined priority score: frequency x complexity
[ ] Alert on new hotspots: YES / NO
[ ] Refactoring targets (top hotspots):
    File                    | Changes | Complexity | Health
    ────────────────────────┼─────────┼────────────┼───────
    src/core/processor.ts   | 45      | 82         | 2.1
    src/api/handlers.ts     | 38      | 67         | 3.4
    src/db/queries.ts       | 31      | 55         | 4.2
```

### 3 — PR Integration

```
PR CODE HEALTH GATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Enable PR analysis: YES / NO
[ ] Block merge if code health declines: YES / NO
[ ] Minimum code health for new files: ___
[ ] Warn on changes to hotspots: YES / NO
[ ] PR comment with code health delta: YES / NO
[ ] Risk classification: low / medium / high
```

### 4 — Knowledge Distribution

```
KNOWLEDGE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Bus factor analysis enabled: YES / NO
[ ] Knowledge map visualization: YES / NO
[ ] Alert on single-author components: YES / NO
[ ] Off-boarding risk assessment: YES / NO
```

## Common Operations

### Code Health Dashboard
View codebase health scores, trends, and degradation alerts.

### Hotspot Prioritization
Identify highest-impact refactoring targets based on change frequency and complexity.

### PR Risk Assessment
Evaluate pull request risk based on files changed, code health impact, and developer familiarity.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Low code health scores | Complex, frequently changed files | Prioritize hotspot refactoring |
| PR analysis not running | Integration not configured | Connect CodeScene to repository hosting |
| Stale analysis results | Analysis schedule too infrequent | Increase analysis frequency or trigger manually |
| False hotspot alerts | Test files included | Add test directories to exclusion patterns |

## Output Format

Present results as a structured report:
```
Managing Codescene Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

