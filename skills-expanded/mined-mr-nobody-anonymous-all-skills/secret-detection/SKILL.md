---
name: secret-detection
description: Detect accidentally committed secrets (API keys, tokens, passwords) in code and history.
category: security
aliases:
- secret-scanning
- leak-detection
- credentials
triggers:
- find secrets in this code
- check for API keys
- secret scan
- did I commit a secret
keywords:
- secret
- leak
- api
- key
- token
- credential
- scan
- detect
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- api
- detection
- key
- leak
- secret
- security
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

# Secret Detection

## Purpose

Detect secrets accidentally committed to code or history. Recommend rotation if found.

## When to Use

- Pre-commit hygiene
- After accidental commit
- Regular audits

## Safety

- If a real secret is found, advise immediate rotation
- Never echo full secrets back to the user

## Source

Custom skill, written for this library.

## Notes

Pairs with `dependency-audit`, `secure-coding`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the secret-detection workflow consistently.
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

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "find secrets in this code"; "check for API keys"; "secret scan".
