---
name: defensive-security-review
category: cybersecurity
tags: [security, code-review, threat-modeling, authorized-testing]
---

# Defensive Security Review

## Purpose
Review an application or code change for security weaknesses and produce actionable, proportionate remediation guidance.

## When to use
Use when reviewing code, architecture, configuration, or a system you own or have explicit permission to assess.

## Instructions
1. **Confirm scope.** Identify the authorized application, repository, environment, and excluded systems. If authorization or scope is unclear, ask before testing.
2. **Map assets and trust boundaries.** Identify sensitive data, authentication, authorization, external inputs, privileged operations, and third-party dependencies.
3. **Inspect defensively first.** Review source code, dependency manifests, configuration, access controls, error handling, logging, and secrets handling before considering active tests.
4. **Validate proportionately.** Prefer local tests, static analysis, and harmless proof-of-concept checks. Do not access other users' data, disrupt availability, persist access, or extract secrets.
5. **Prioritize findings.** For each issue, record the affected component, preconditions, impact, evidence, severity rationale, and confidence. Separate confirmed defects from hypotheses.
6. **Recommend fixes.** Give the smallest safe remediation, a regression test, and any relevant defense-in-depth measure.
7. **Recheck.** Explain how to verify the fix and what residual risk remains.

## Inputs
- Authorized scope and exclusions
- Repository, architecture, or configuration under review
- Relevant threat model and deployment context
- Available test constraints

## Outputs
A concise report with an executive summary, prioritized findings, reproducible non-destructive evidence, remediation steps, and verification tests.

## Example
For an endpoint that accepts a user-supplied account ID, trace whether the server checks that the authenticated user owns that account. Recommend a server-side ownership check and tests for both authorized and unauthorized access.

## Limitations
Do not claim a vulnerability is confirmed without evidence. Do not perform testing outside the agreed scope. This skill supports defensive review and does not replace a full professional assessment.
