---
name: github-issue-triage
description: Issue qualification, reproduction verification, deduplication, SLA monitoring, component routing, and automated triage workflows
---
# GitHub Issue Triage & Prioritization

## 1. Initial Issue Qualification
Review newly incoming issues for completeness: verify that all mandatory template fields, reproduction steps, and error logs are present. Request missing details promptly.

## 2. Reproduction Verification
Attempt to reproduce reported defects in a clean local environment or CI container. Mark verified bugs with the 'verified' label and link reproduction tests.

## 3. Deduplication & Search
Search existing open and closed issues before triaging. When an issue duplicates an existing report, link the canonical issue and close the duplicate politely with an explanation.

## 4. Severity & Impact Assessment
Evaluate impact on users and systems: distinguish security vulnerabilities (route to private advisory immediately) from data loss, broken workflows, or cosmetic bugs.

## 5. Component & Team Routing
Apply accurate subsystem labels (area/backend, area/frontend, area/infra) and assign qualified domain owners based on CODEOWNERS.

## 6. SLA & Stale Issue Management
Monitor response times against project SLAs. Identify stale or abandoned issues needing user response and configure automated lifecycle reminders.

## 7. Converting Discussions & Questions
When issues are general questions or support requests rather than actionable engineering tasks, convert them to GitHub Discussions.

## 8. Automated CLI Triage Operations
Triage issues via CLI: gh issue edit 123 --add-label 'bug,verified' --add-assignee 'developer'.

## 9. Security Triage & Disclosure Protocol
If an issue reports a security vulnerability publicly, immediately contact repository maintainers, move discussion to private advisory, and hide sensitive comments.

## 10. Backlog Health & Milestone Planning
Assign qualified and verified issues to upcoming project milestones or active phases (P00, P01) to keep the project roadmap actionable.
