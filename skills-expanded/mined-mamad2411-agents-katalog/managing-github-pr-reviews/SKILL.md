---
name: managing-github-pr-reviews
description: |
  Use when working with Github Pr Reviews — gitHub pull request review
  management including review assignments, CODEOWNERS enforcement, branch
  protection rules, required reviewers, review dismissal policies, and status
  check integration. Use when configuring or automating GitHub PR review
  workflows across repositories and organizations.
connection_type: github
preload: false
---

# Managing GitHub PR Reviews

## Overview

Manage GitHub pull request review workflows, including reviewer assignment, CODEOWNERS configuration, branch protection rules, and review automation.

## Key Capabilities

- Configure branch protection rules with required reviews
- Manage CODEOWNERS files for automatic reviewer assignment
- Set up required status checks and review counts
- Configure review dismissal and stale review policies
- Automate reviewer assignment with round-robin or load-balance algorithms
- Enforce code review policies across organizations

## Workflow

### 1 — Configure Branch Protection

```
BRANCH PROTECTION SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Required approving reviews: ___ (recommended: 2)
[ ] Dismiss stale reviews on new pushes: YES / NO
[ ] Require review from CODEOWNERS: YES / NO
[ ] Restrict who can dismiss reviews: YES / NO
[ ] Require status checks to pass: YES / NO
[ ] Require branches to be up to date: YES / NO
[ ] Require signed commits: YES / NO
[ ] Require linear history: YES / NO
```

### 2 — CODEOWNERS Configuration

```
CODEOWNERS FILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: .github/CODEOWNERS

Pattern examples:
  *                    @org/engineering-leads
  /src/api/            @org/backend-team
  /src/frontend/       @org/frontend-team
  /infrastructure/     @org/platform-team
  *.sql                @org/dba-team
  /docs/               @org/tech-writers
  Dockerfile           @org/devops
  .github/workflows/   @org/ci-cd-team
```

### 3 — Review Assignment

```
AUTO-ASSIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Algorithm: round-robin / load-balance
[ ] Number of reviewers: ___
[ ] Skip team members who are:
    [ ] On PTO / away
    [ ] Already assigned
    [ ] The PR author
[ ] Notify assigned reviewers: YES / NO
[ ] Review request timeout: ___ hours
```

### 4 — Review Policy Enforcement

```
REVIEW POLICIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Minimum approvals before merge: ___
[ ] Required reviewers for sensitive paths: ___
[ ] Block merge on requested changes: YES / NO
[ ] Require re-review after force push: YES / NO
[ ] Auto-merge when all checks pass: YES / NO
[ ] Merge methods allowed: merge / squash / rebase
```

## Common Operations

### List Pending Reviews
Query open PRs awaiting review, filter by team or reviewer, and track review SLAs.

### Audit Review Coverage
Analyze CODEOWNERS coverage across the repository to identify unowned code paths.

### Review Metrics
Track review turnaround time, approval rates, and reviewer workload distribution.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| CODEOWNERS not triggering | File in wrong location | Must be in `.github/`, `docs/`, or root |
| Reviews not required | Branch protection not set | Enable "Require pull request reviews" |
| Wrong reviewers assigned | Pattern order matters | CODEOWNERS uses last matching pattern |
| Stale reviews not dismissed | Setting disabled | Enable "Dismiss stale pull request approvals" |
| Auto-merge not working | Missing required checks | Ensure all required status checks are configured |

## Output Format

Present results as a structured report:
```
Managing Github Pr Reviews Report
═════════════════════════════════
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

