---
name: master-09-security
description: 09-SECURITY domain of the master skills library (web/API security, authentication, compliance, privacy and audits). Use when the task needs security review, auth design, compliance readiness and no more specific installed skill matches. Not when the request is offensive testing against systems without authorization.
---

# 09-SECURITY

## Purpose
Index for web/API security, authentication, compliance, privacy and audits: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs security review, auth design, compliance readiness.

## When NOT to use
- The request is offensive testing against systems without authorization.
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `authentication/auth-setup/SKILL.md` - Trigger when the user wants to add authentication to their app — sign up, sign in, session management, protected routes, or role-based acces
- `privacy/ai-content-disclosure/SKILL.md` - Check AI-generated marketing content and reviews for required disclosures under the EU AI Act, FTC rules and platform AI-label policies. Use
- `security-audit/security-audit/SKILL.md` - Multi-agent source security audit with a coverage ledger, independently verified findings, and machine-checked records. Use when asked to au

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
