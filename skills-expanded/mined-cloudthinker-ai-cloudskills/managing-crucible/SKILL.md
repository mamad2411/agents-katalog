---
name: managing-crucible
description: |
  Use when working with Crucible — atlassian Crucible code review management
  including review creation, commenting workflows, approval processes, and Jira
  integration. Use when managing Crucible review workflows, configuring review
  templates, and enforcing review completion policies.
connection_type: crucible
preload: false
---

# Managing Crucible

## Overview

Manage Atlassian Crucible code review workflows, including review creation, commenting, approval workflows, and integration with Jira and Bitbucket/Stash.

## Key Capabilities

- Create and manage code reviews with multiple changesets
- Configure review templates and default reviewers
- Manage commenting and defect tracking within reviews
- Set up approval workflows and completion conditions
- Integrate with Jira for review-to-issue traceability
- Configure notifications and review reminders

## Workflow

### 1 — Review Configuration

```
REVIEW SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Review type: changeset / patch / snippet
[ ] Project: ___
[ ] Default moderator: ___
[ ] Default reviewers: ___
[ ] Allow self-review: YES / NO
[ ] Review template: ___
[ ] Jira issue linkage: required / optional / disabled
```

### 2 — Approval Workflow

```
APPROVAL WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review states:
  Draft -> Under Review -> Summarized -> Closed

[ ] Require all reviewers to complete: YES / NO
[ ] Minimum approvals for completion: ___
[ ] Allow close with open defects: YES / NO
[ ] Require moderator summarization: YES / NO
[ ] Auto-close after ___ days of inactivity
```

### 3 — Comment and Defect Tracking

```
COMMENTING POLICY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comment classifications:
  [ ] Defect — Must fix before approval
  [ ] Comment — Informational, no action required
  [ ] Question — Requires author response

[ ] Inline comments on specific lines: YES / NO
[ ] General review comments: YES / NO
[ ] Defect severity levels: critical / major / minor
[ ] Create Jira issues from defects: YES / NO
```

## Common Operations

### List Active Reviews
Query open reviews, filter by project, reviewer, or author.

### Review Metrics
Track review completion rates, defect density, and reviewer participation.

### Jira Integration
Link reviews to Jira issues and track review status from issue context.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Review not starting | Missing reviewers | Add at least one reviewer before starting |
| Cannot close review | Open defects remain | Resolve or downgrade all defect comments |
| Jira link missing | Integration not configured | Configure Crucible-Jira application link |
| Notifications not sent | Email settings | Verify SMTP and user notification preferences |

## Output Format

Present results as a structured report:
```
Managing Crucible Report
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

