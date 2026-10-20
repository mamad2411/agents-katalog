---
name: managing-gitlab-merge-requests
description: |
  Use when working with Gitlab Merge Requests — gitLab merge request review
  management including approval rules, merge checks, code ownership via
  CODEOWNERS, merge request policies, and pipeline integration. Use when
  configuring or automating GitLab MR review workflows across projects and
  groups.
connection_type: gitlab
preload: false
---

# Managing GitLab Merge Requests

## Overview

Manage GitLab merge request review workflows, including approval rules, CODEOWNERS enforcement, merge checks, and pipeline-gated merges.

## Key Capabilities

- Configure merge request approval rules at project and group level
- Set up CODEOWNERS for automatic approval requirements
- Define merge checks (pipeline success, resolved discussions, signed commits)
- Manage merge request policies and merge methods
- Configure merge trains for high-throughput repositories
- Enforce approval policies via group-level compliance frameworks

## Workflow

### 1 — Approval Rules Configuration

```
APPROVAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Default approvals required: ___
[ ] Rules:
    Rule Name            | Approvers              | Required
    ─────────────────────┼────────────────────────┼─────────
    Backend Review       | @backend-team          | 1
    Security Review      | @security-team         | 1
    Architecture Review  | @architects            | 1 (optional)
[ ] Prevent author self-approval: YES / NO
[ ] Prevent committers from approving: YES / NO
[ ] Remove all approvals on new push: YES / NO
```

### 2 — Merge Checks

```
MERGE CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Pipeline must succeed: YES / NO
[ ] All discussions must be resolved: YES / NO
[ ] All status checks must pass: YES / NO
[ ] Signed commits required: YES / NO
[ ] Merge method: merge commit / squash / fast-forward
[ ] Merge trains enabled: YES / NO
[ ] Semi-linear history: YES / NO
```

### 3 — CODEOWNERS Setup

```
CODEOWNERS FILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: CODEOWNERS (root or docs/)

Sections:
  [Backend]
  /src/api/         @backend-team
  /src/services/    @backend-team

  [Frontend]
  /src/ui/          @frontend-team
  /src/components/  @frontend-team

  [Infrastructure]
  /terraform/       @platform-team
  .gitlab-ci.yml    @devops-team

Optional vs Required sections:
  ^[Docs]           @tech-writers    (optional)
  [Security]        @security-team   (required)
```

### 4 — Compliance Framework

```
GROUP-LEVEL COMPLIANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Compliance framework applied: ___
[ ] Separation of duties enforced: YES / NO
[ ] Compliance pipeline configured: YES / NO
[ ] Audit events enabled: YES / NO
```

## Common Operations

### Review Pending MRs
List open merge requests awaiting approval, filter by project or group.

### Audit Approval Compliance
Verify that merge requests follow required approval rules and CODEOWNERS requirements.

### Merge Train Management
Monitor and manage merge train queues for high-throughput branches.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Approvals not required | Rules not configured at project level | Set approval rules in Project > Settings > Merge Requests |
| CODEOWNERS not enforced | Premium/Ultimate required | CODEOWNERS approval requires GitLab Premium+ |
| Merge train failures | Pipeline conflicts | Check merge train pipeline logs for conflicts |
| Approvals reset unexpectedly | "Remove approvals on push" enabled | Disable in project settings if not desired |

## Output Format

Present results as a structured report:
```
Managing Gitlab Merge Requests Report
═════════════════════════════════════
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

