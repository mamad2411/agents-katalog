---
name: issue-triage
description: Classify, deduplicate, label, and prioritize incoming issues with reproduction checklists and routing rules.
category: development
aliases:
- triage-issues
- bug-triage
- issue-classifier
- issue-routing
triggers:
- triage incoming issues
- classify this bug report
- prioritize GitHub issues
- label and route this issue
- check issue for reproduction steps
keywords:
- issue
- triage
- github
- bug
- label
- priority
- reproduce
- classify
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- issue-classification
- reproduction-verification
- priority-routing
inputs:
- issue_body
- labels
- repository_context
outputs:
- triaged_issue
- severity_rating
- recommended_assignee
- reproduction_checklist
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- bug
- development
- github
- issue
- triage
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Issue Triage

## Purpose
Systematically triages, validates, categorizes, and routes incoming GitHub issues and bug reports. Ensures reproducible bugs are fast-tracked, duplicates are consolidated, and missing environment details are immediately requested.

## When to Use
- Managing high-volume open-source or team issue trackers.
- Reviewing new community bug reports, feature requests, or questions.
- Enforcing standardized issue metadata, severity tiers, and SLA priorities.
- Filtering low-quality or non-reproducible tickets before engineering intake.

## When NOT to Use
- Implementing the actual code fix (route to `development.debugging` or `development.coding`).
- Managing customer support billing inquiries outside technical issue tracking.

## Capabilities
- **Classification**: Categorize tickets into bug, feature request, documentation, performance, or question.
- **Reproduction Quality Check**: Verify presence of minimal reproduction steps, OS/browser versions, and error logs.
- **Duplicate Detection**: Identify semantically similar open and closed issues.
- **Severity & Impact Scoring**: Assign P0–P3 priority ratings based on blast radius and workarounds.

## Inputs
- `issue_text` (required) — Title, description, and logs from the reported issue.
- `existing_labels` (optional) — Available repository label taxonomy.
- `milestones` (optional) — Active release targets.

## Workflow
1. Read the issue title, description, and diagnostic logs.
2. Check for required reproduction criteria: minimal code sample, environment details, expected vs. actual behavior.
3. Search for duplicate existing issues or known resolved problems.
4. Assign appropriate labels (`bug`, `priority: high`, `needs-repro`, `component: auth`).
5. Draft an immediate response requesting missing details or confirming triage status.

## Tools
- GitHub CLI (`gh`) or repository API clients for query and label mutations.

## Examples
- "Triage incoming issues from the last 24 hours."
- "Classify this bug report and check if it has a reproducible example."
- "Evaluate the severity rating for this database timeout issue."

## Safety
- Require human approval before closing community issues or applying destructive state changes.
- Never expose sensitive tokens, passwords, or PII found within raw user issue logs.

## Source
Custom skill maintained in this library following open-source project management practices.

## Notes
Integrates cleanly with `development.github-cli` and `development.github`.
