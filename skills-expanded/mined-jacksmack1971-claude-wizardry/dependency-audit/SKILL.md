---
name: dependency-audit
description: Audit dependency manifests, lockfiles, supply-chain risk, and upgrade safety. Use when reviewing dependency health, lockfile drift, wallet or chain library duplication, or supply-chain risk in a repository.
disable-model-invocation: false
user-invocable: true
---

# Dependency Audit

Inspect:

- Package manifests and lockfiles
- `viem`, `ethers`, wallet, connector, and chain helper packages
- Deprecated or abandoned dependencies
- Known vulnerable packages
- Duplicate or conflicting dependency trees
- Postinstall scripts and native extensions
- CI install behavior
- Runtime version constraints

Flag mixed web3 stacks when they create duplicate wallet abstractions, conflicting transport logic, or unnecessary bundle weight.

Use `scripts/list_manifests.py` to enumerate likely dependency entrypoints before auditing.

Do not upgrade dependencies during audit-only mode. Create isolated findings with evidence and verification steps.
