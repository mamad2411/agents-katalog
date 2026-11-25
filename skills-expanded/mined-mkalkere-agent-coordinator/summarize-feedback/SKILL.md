---
name: summarize-feedback
version: 1.0.0
description: Summarize PR review comments into actionable developer feedback
uses:
  - core/publish-artifact
requires:
  tools: [gh]
  env: []
security:
  risk_level: read
  capabilities:
    - github:pr:read
  requires_approval: false
---

# Summarize Feedback

Analyze all review comments on a PR and create a prioritized, actionable summary for developers. This skill bridges the gap between raw review comments and a clear action plan.

**Platform note**: This skill currently uses GitHub (`gh` CLI). The summarization methodology is platform-agnostic; only the tool commands are GitHub-specific.

## Execution Model

This is a **bash skill** (`handler: type: bash`). When `feedback_fetch` is invoked, the executor runs `gh pr view {number} --json reviews,comments,statusCheckRollup` to fetch all review data. The agent then applies the methodology below to categorize, prioritize, and summarize the feedback.

## When to Use

- After completing a PR review — create a summary for the developer
- When multiple reviewers have commented and feedback needs consolidation
- When a developer needs a clear action plan from review comments

## Methodology

### 1. Gather All Feedback

Fetch from all sources:
- Review comments (inline and general)
- Review verdicts (approve, request changes)
- CI check statuses
- Any additional discussion comments

### 2. Categorize by Severity

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| **Critical** | Security vulnerability, data loss risk, crash | Must fix before merge |
| **High** | Bug, incorrect behavior, performance issue | Should fix before merge |
| **Medium** | Code quality, maintainability, style | Fix recommended |
| **Low** | Nitpicks, suggestions, preferences | Optional |

### 3. Group by File/Component

Organize issues by location so developers can work file-by-file:
- Group all comments for each file
- Order by severity within each file
- Highlight files with the most critical issues

### 4. Create Summary Artifact

Write a structured summary with:
- Overall verdict
- Statistics (count by severity)
- Critical issues first (must fix)
- High priority next (should fix)
- Medium and low grouped separately
- Per-file checklist for the developer

### 5. Publish and Notify

1. Publish summary as an artifact using `publish-artifact`
2. Send `review_summary_ready` message to bus
3. Include the artifact path so the developer can find it

## Output Format

```
## Review Summary: PR #[N]

### Verdict: [Changes Requested / Approved]

### Statistics
- Critical: [count] (must fix)
- High: [count] (should fix)
- Medium: [count] (recommended)
- Low: [count] (optional)
- Total: [count] across [N] files

### Critical Issues
1. **[Issue title]**
   - File: [path:line]
   - Problem: [description]
   - Fix: [suggested fix]

### High Priority
1. ...

### Files Requiring Changes
- [ ] [file] — [N] critical, [N] high
- [ ] [file] — [N] high, [N] medium
```

## Quality Criteria

- All review comments are captured (none missed)
- Severity categorization matches actual impact
- Issues are grouped logically by file
- Summary is actionable (developer knows exactly what to fix)
- Critical issues are prominently listed first
- Summary artifact is published and discoverable
- Bus notification is sent to the developer

## Common Mistakes

- **Missing comments**: Not fetching all comment types (inline, general, review body). Check all sources.
- **Wrong severity**: Categorizing a style issue as critical, or a security issue as low. Severity must reflect actual impact.
- **Not grouping by file**: A flat list of issues is hard for developers to work through. Group by file for systematic fixing.
- **Not being actionable**: Listing problems without suggested fixes. Always include how to resolve each issue when possible.
- **Not publishing the artifact**: Writing the summary but forgetting to publish it and notify via bus. The developer needs to be able to find it.
- **Duplicating issues**: If multiple reviewers flagged the same problem, consolidate rather than listing it multiple times.

## Completion

Feedback summarization is complete when:
- All review comments are gathered and categorized
- Summary is structured by severity and grouped by file
- Summary artifact is published to shared memory
- Developer notification is sent via bus
- Summary is actionable (developer can work through it systematically)
