---
name: managing-codeball
description: |
  Use when working with Codeball — codeBall AI-powered pull request risk
  assessment including automatic PR quality scoring, risk classification, and
  auto-approval for low-risk changes. Use when configuring CodeBall for
  automated PR triage, risk-based review routing, and review workload
  optimization.
connection_type: codeball
preload: false
---

# Managing CodeBall

## Overview

Manage CodeBall AI-powered PR risk assessment, including automatic quality scoring, risk classification, auto-approval for safe changes, and integration with review workflows.

## Key Capabilities

- Automatically assess PR risk level using AI analysis
- Auto-approve low-risk PRs to reduce reviewer burden
- Classify PRs by risk: low, medium, high
- Integrate risk scores into existing review workflows
- Track risk assessment accuracy over time
- Configure risk thresholds and auto-approval policies

## Workflow

### 1 — Risk Assessment Configuration

```
RISK ASSESSMENT SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Enable AI risk scoring: YES / NO
[ ] Risk classification thresholds:
    - Low risk (auto-approve eligible): score < ___
    - Medium risk (standard review): score ___ - ___
    - High risk (senior review required): score > ___
[ ] Analysis scope:
    - All PRs: YES / NO
    - Exclude draft PRs: YES / NO
    - Exclude WIP PRs: YES / NO
```

### 2 — Auto-Approval Policy

```
AUTO-APPROVAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Enable auto-approve for low-risk PRs: YES / NO
[ ] Additional conditions for auto-approve:
    [ ] All CI checks pass
    [ ] PR size < ___ lines
    [ ] No changes to critical paths (auth, payments, etc.)
    [ ] Author has > ___ merged PRs
[ ] Label auto-approved PRs: YES / NO
[ ] Post approval comment: YES / NO
```

### 3 — Review Routing

```
RISK-BASED ROUTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Low risk: auto-approve or assign to any reviewer
[ ] Medium risk: assign to team reviewer
[ ] High risk: assign to senior engineer + additional reviewer
[ ] Critical risk: assign to tech lead + security review
[ ] Add risk label to PR: YES / NO
```

## Common Operations

### Risk Score Dashboard
View aggregate risk scores across PRs, trending over time.

### Auto-Approval Audit
Review auto-approved PRs to validate AI assessment accuracy.

### Threshold Tuning
Adjust risk thresholds based on false positive/negative rates.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| All PRs marked high risk | Threshold too low | Increase high-risk threshold based on score distribution |
| False auto-approvals | Threshold too permissive | Lower auto-approve threshold or add conditions |
| Risk score not appearing | GitHub App permissions | Verify CodeBall app has read access to PR content |
| Assessment delayed | Queue backlog | Check CodeBall service status |

## Output Format

Present results as a structured report:
```
Managing Codeball Report
════════════════════════
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

