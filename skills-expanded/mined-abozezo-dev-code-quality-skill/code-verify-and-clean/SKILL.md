---
name: code-verify-and-clean-skill
description: |
  Orchestrates focused clean-code, code-verification, runtime/DevTools-audit, and security-review skills.
  Use when a change needs a coordinated end-to-end quality workflow and before/after evidence reports.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Browser
  - WebFetch
---

# Code Verify & Clean Orchestrator

This is a composition skill. Delegate each concern to its focused sub-skill instead of duplicating its guidance:

| Need | Sub-skill | Primary asset |
|---|---|---|
| Dead code, unused imports, duplication, complexity, and architecture | [**clean-code**](../clean-code/SKILL.md) | `../clean-code/SKILL.md` |
| Builds, tests, linting, formatting, and type checks | [**code-verification**](../code-verification/SKILL.md) | `../code-verification/SKILL.md` |
| Browser rendering, console, network, and interaction audits | [**runtime-devtools-audit**](../runtime-devtools-audit/SKILL.md) | `../runtime-devtools-audit/SKILL.md` |
| Input, authorization, secrets, injection, storage, and configuration review | [**security-review**](../security-review/SKILL.md) | `../security-review/SKILL.md` |

## Coordinated Workflow

1. Before application modifications, conduct a read-only review across the applicable sub-skills and create `SCAN.md` from `assets/scan-template.md`.
2. Make focused changes using the appropriate sub-skill guidance.
3. Run **code-verification**. Add **runtime-devtools-audit** for client-facing changes and **security-review** for relevant trust boundaries.
4. Create `REPORT.md` from `assets/report-template.md`, reconciling the scan findings, fixes, checks, and remaining risks.

Read [the reporting workflow](reference/reporting-workflow.md) for the report requirements and evidence standard.
