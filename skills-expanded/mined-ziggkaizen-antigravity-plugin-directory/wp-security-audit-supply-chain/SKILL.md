---
name: wp-security-audit-supply-chain
description: Audits WordPress Core, plugin, theme, Composer, npm, build, and deployment supply-chain trust. Use for provenance, update posture, abandoned components, dependency, and artifact reviews.
---

# WordPress Supply-Chain Security Audit

## Review areas

- WordPress Core source and update channel.
- Plugin and theme source, ownership, support status, and update channel.
- Unused, inactive, bundled, mu-plugin, drop-in, and custom components.
- Composer and npm manifests, lockfiles, registries, scripts, and build inputs.
- Generated assets and whether source maps or secrets are shipped.
- Release provenance, signatures/checksums where available, and artifact retention.
- Repository access, branch protection, CI credentials, release permissions, and dependency update ownership.
- Vulnerability advisories from approved sources.
- Abandoned or takeover-prone packages and plugins.
- Licensing and redistribution constraints that affect update ability.

## Principles

- Inventory first; do not update during the audit.
- Distinguish installed, active, network-active, must-use, drop-in, and bundled code.
- Do not mark an outdated component vulnerable without an applicable advisory or supported-risk rationale.
- Treat unsigned or unverifiable provenance as a trust limitation, not automatic compromise.
- Record exact package name, source, version, and evidence timestamp.

Read [supply-chain-checklist.md](resources/supply-chain-checklist.md) and follow [audit-wordpress-supply-chain-workflow.md](workflows/audit-wordpress-supply-chain-workflow.md).
