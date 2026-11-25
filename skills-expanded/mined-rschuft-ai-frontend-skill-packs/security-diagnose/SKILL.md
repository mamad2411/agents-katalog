---
name: security-diagnose
description: "Classify suspected web application security weaknesses by actual trust boundary, identify affected ASVS 5.0.0 requirements, and route to a focused security specialist. Use for ambiguous security reports and code review findings."
---

# Diagnose an application security concern

## Scope

Use this skill when an observed behavior, code pattern, architecture, scan finding or user complaint suggests a security weakness. Do not turn a hypothesis or scanner alert into a confirmed vulnerability without corroboration. Limit activity to code and systems the user has authorized.

## Procedure

1. Record the affected asset, data flow, entry point, actor, security boundary, environment and authorized inspection scope. Separate observed evidence from assumptions.
2. Read `references/standard-selection.md`; resolve the explicit application baseline, project policy or ASVS 5.0.0 Level 2 planning fallback. Confirm whether server-side or infrastructure evidence is available.
3. Use `references/issue_taxonomy.json` to select one primary category and, if needed, two secondary categories. Read only matching chapters from `references/asvs/5.0.0/index.json` and `references/asvs/5.0.0/source-access.md` to obtain full authoritative requirement text when assessing an ID. If unavailable, report it as untested.
4. Check `references/remediation_recipes.json`, OWASP Top 10:2025 awareness mappings and `references/nist-ssdf-mapping.json` when development-process questions matter. Do not treat an awareness category as an ASVS requirement.
5. Route to a relevant `security-*` specialist and propose a bounded repair or discriminating test. For code changes use `security-build`; full assessment `security-review`; verification `security-validate`.

## Evidence discipline

Report confirmed weakness, suspected weakness, informational observation and not tested separately. Do not label an unobserved server-side control as pass. Include ASVS version-prefixed IDs, evidence limits, and the safest authorized verification path. Never disclose production secrets or unapproved exploitation steps.
