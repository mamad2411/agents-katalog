---
name: renovate-43-security-advisory-response
description: Responds to vulnerable dependency updates surfaced through Renovate 43. Use when Renovate creates security update PRs, vulnerability alerts, OSV/GitHub advisory updates, CVE/GHSA references, dependencyDashboard security items, or when a dependency must be upgraded or mitigated due to a vulnerability.
license: MIT
compatibility: Requires access to repository dependency context. Advisory verification may require network access to official advisory sources.
---

# Renovate 43 Security Advisory Response

Use this skill for Renovate security PRs, vulnerability dashboard items, CVE/GHSA/OSV references, and vulnerable dependency remediation.

## Workflow

- `workflows/renovate-43-security-advisory-response-workflow.md`

## Resources

- `resources/renovate-43-security-advisory-checklist.md`
- `resources/renovate-43-vulnerability-prioritization.md`

## Script

Run `python3 scripts/advisory-response-template.py --help` before use.

## Principles

Prioritize security updates, prefer the smallest safe fixed version, create a major-upgrade plan when needed, and preserve human review for critical dependency categories.
