---
name: verifying-deployment-safety
description: Review deployment, upgrade, signer, and release-safety paths in an Ethereum TypeScript repo before high-risk changes are trusted. Use when reviewing deployment scripts, upgrade scripts, signer configuration, admin-role changes, environment-gated addresses, or release-readiness for contract-affecting work.
argument-hint: "[deploy-or-upgrade-scope]"
disable-model-invocation: true
user-invocable: true
---

# Verifying Deployment Safety

This skill is manual-first because deployment and upgrade review is high-risk.

Inspect:

- deployment entrypoints and environment gating
- signer source and privilege boundaries
- admin-role and upgrade authority assumptions
- address publication and post-deploy synchronization
- release workflow coupling between code, artifacts, and deployment actions

Use `references/deployment-safety-checklist.md` before finalizing conclusions.

Output contract:

- Deployment scope audited
- Evidence files
- Confirmed release or signer risks
- Missing verification
- Required human confirmation points
