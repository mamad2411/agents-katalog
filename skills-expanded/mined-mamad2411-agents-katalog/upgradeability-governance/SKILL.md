---
name: upgradeability-governance
description: Enforce safe upgrade patterns (ERC-7201 namespaced storage, initializer discipline, authorizeUpgrade governance, and upgrade tests). Use when touching proxy/upgradeable contracts, storage layout, admin roles, or deploy scripts.
---

# Upgradeability + Governance (ERC-7201)

## When to use
- Any contract is upgradeable (proxy) OR any PR touches:
  - storage layout
  - initializer/reinitializer
  - upgrade authorization / admin roles
  - deploy/upgrade scripts
  - contract ownership/governance configuration

## Goal (Definition of Done)
- ✅ ERC-7201 namespaced storage used for upgradeable state.
- ✅ No constructors in implementation; initializer discipline is correct.
- ✅ `_authorizeUpgrade()` protected by role + governance (timelock/multisig if applicable).
- ✅ Upgrade process is documented (who/when/how) and test-proven.

## Mandatory rules

### Storage safety (ERC-7201)
- Use namespaced storage for state isolation.
- Avoid using `__gap` as the primary collision mitigation strategy.

### Initialization safety
- Implementation contract:
  - uses `initializer/reinitializer`
  - calls `_disableInitializers()` in constructor (implementation only)
- Never allow re-initialization of the same version.

### Authorization & governance
- `_authorizeUpgrade()` must:
  - require explicit role (e.g., `UPGRADER_ROLE`)
  - ideally be behind multisig/timelock (production)
- Document:
  - who holds roles
  - how keys are stored
  - emergency pause (if any) and boundaries

## Deployment & change control
- All deployments/upgrades must:
  - persist addresses per chainId (deployments/<chainId>.json)
  - record commit hash + timestamp
  - be reproducible by scripts

## Anti-patterns (forbidden)
- ❌ Upgrading without tests proving state persistence.
- ❌ Using `tx.origin` for admin gating.
- ❌ Leaving `_authorizeUpgrade()` open or weakly protected.
- ❌ Silent storage layout changes without explicit review.

## Testing checklist (Foundry)
- Upgrade tests (required when upgradeable or storage changes):
  - initializer runs once
  - state persists after upgrade
  - old storage slot values remain correct
  - unauthorized upgrade reverts
- Fuzz/property (recommended):
  - invariants remain true across upgrade boundary (e.g., "claim cannot pay 2x")

## Documentation checklist
- Add/update an ADR if deviating from reference blueprint.
- Update runbook steps for upgrade (dry-run, verify, post-checks).
