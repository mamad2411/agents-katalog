---
name: repo-audit
description: System-wide audit that creates one actionable finding per confirmed issue. Use when auditing a repository for architecture, risk, DX, governance, or release readiness without immediately implementing fixes.
disable-model-invocation: false
user-invocable: true
---

# Repository Audit

For Ethereum TypeScript repositories, pay extra attention to:

- Chain configuration and network switching
- RPC client construction
- ABI and contract-address drift
- Wallet connection flow and signer boundaries
- Indexing, caching, and stale on-chain data assumptions
- Deployment, upgrade, and admin-control scripts

Prefer composing specialized skills before final synthesis:

- `stack-detection` for client-layer classification
- `auditing-wallet-flows` for browser and signing paths
- `auditing-contract-surfaces` for ABI and contract-write surfaces
- `verifying-deployment-safety` for deployment and upgrade paths
- `dependency-audit` for manifest and lockfile risk

Audit:

- Runtime source code
- Tests and test infrastructure
- CI/CD workflows
- Dependency manifests and lockfiles
- Build, release, and package configuration
- Security-sensitive code and configuration
- Environment, secrets, and config handling
- Error handling and observability
- Data, storage, migrations, and schemas
- Public APIs, CLIs, SDKs, and integrations
- Architecture, coupling, and duplication
- Performance and scalability risks
- Developer experience and local setup
- User-facing documentation
- Repository governance

Confirm findings before creating issues.

Output contract:

- Audit scope
- Evidence-backed findings
- Verification gaps
- Suggested next skill if deeper drilling is needed
