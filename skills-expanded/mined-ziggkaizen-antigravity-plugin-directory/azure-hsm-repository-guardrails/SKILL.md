---
name: azure-hsm-repository-guardrails
description: Provides repository guardrails for Azure Key Vault Managed HSM work, including hook-backed checks for hardcoded secrets, plaintext key export patterns, Managed HSM access changes, and security-domain material boundary violations. Use when configuring hooks, reviewing generated commands, scanning repository changes, or explaining hook findings.
license: MIT
compatibility: Requires Python 3 for the included hook script.
---

# Azure HSM Repository Guardrails Skill

Use this skill when configuring or interpreting Managed HSM guardrails.

## Guardrails

This skill backs four hooks:

- `azure-hsm-secret-reference-check`
- `azure-hsm-access-change-review`
- `azure-hsm-key-export-blocker`
- `azure-hsm-security-domain-boundary-check`

The hook script reads Antigravity hook JSON from stdin and emits an allow, ask, ask, or deny decision.

## Workflow

Use `workflows/repository-guardrails-review-workflow.md` when tuning or reviewing guardrail findings.

## Resource

Use `resources/repository-guardrails-patterns.md` for the detected pattern categories.

## Script

Use `scripts/azure-hsm-repository-guard.py`. Run it with `--help` before manual testing.

## Operating Rules

- Hooks are conservative and may produce false positives.
- Private key blocks and likely security-domain material in application/admin paths should be blocked.
- Access changes, key release, key backup, restore, delete, purge, and role changes should require review.
- Do not weaken hooks to support convenience workflows that store sensitive material in source control.
