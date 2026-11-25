---
name: dependency-audit
description: Audit project dependencies for known vulnerabilities (CVEs), outdated packages, and supply-chain risks.
category: security
aliases:
- supply-chain
- npm-audit
- pip-audit
- cve
triggers:
- audit my dependencies
- check for vulnerable packages
- are my dependencies safe
- CVE check
- npm audit
- pip audit
keywords:
- dependency
- audit
- cve
- vulnerability
- supply-chain
- npm
- pip
- maven
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- audit
- cve
- dependency
- security
- vulnerability
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

# Dependency Audit

## Purpose

Scan project dependencies for known vulnerabilities and suggest upgrades or removals.

## When to Use

- Pre-release security check
- After a major CVE announcement
- Periodic security hygiene

## Tools

- `npm audit`, `pip-audit`, `osv-scanner`, Dependabot, Renovate

## Source

Custom skill, written for this library.

## Notes

Pairs with `secure-coding`, `secret-detection`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the dependency-audit workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Examples

Requests that should activate this skill include: "audit my dependencies"; "check for vulnerable packages"; "are my dependencies safe".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
