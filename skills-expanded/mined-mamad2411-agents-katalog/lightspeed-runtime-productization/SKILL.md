---
name: lightspeed-runtime-productization
description: Operate the bounded LightSpeed Runtime install/update/config/rollback workflow through managed slots, receipts, exact-head checks, and the single existing Cognigrex/LightSpeed runtime authority.
---

# LightSpeed Runtime Productization

Use for runtime install, update, configuration, rollback, packaged-runtime setup, or operator-productization requests.

This skill manages **named runtime slots** only. It must not create a second canonical runtime, rewrite CGX carriers, mutate the active SQLite database, or expose arbitrary shell execution.

## Routing

Preferred typed route:

- route: `runtime.productization`
- shared MCP tool: `cgx_runtime_productization`
- runtime handler: `lightspeed_runtime.runtime_productization:manage_runtime_productization`
- operator wrapper: `tools/manage_lightspeed_runtime.ps1`

LightSpeed selector aliases:

- `@LightSpeed /install`
- `@LightSpeed /update`
- `@LightSpeed /config`
- `@LightSpeed /rollback`
- `@LightSpeed /runtime`

All selectors may use the global `/runtime` route when current capability state includes it.

## Actions

### status

Read-only. Return current source head, managed/slot roots, marker/config state, installed Python path, selected profile, and recent operator receipts.

### configure

Requires explicit confirmation. Write only the managed slot marker and runtime configuration. Configuration contains no secrets and grants no authority.

### install

Requires explicit confirmation. Resolve the current source head, require a safe slot name, refuse to overwrite an installed slot, use the canonical installer, write receipts, then re-read slot status.

### update

Requires explicit confirmation. Require a valid managed marker and installed slot, reuse the canonical installer with the selected pinned profile, preserve slot identity, write a new receipt, then re-read status.

### rollback

Requires explicit confirmation and a valid managed marker. Delete **only** the selected managed slot directory. Never delete the managed root, repository, live `D:\LightSpeed\Environment`, carriers, active database, archives, or arbitrary paths.

Write rollback evidence outside the deleted slot, then verify the slot no longer exists.

## Profiles

Supported profiles: core, api, data, validation, dev, desktop. Desktop checks dependency imports and Tcl only; it does not prove standalone distribution or UI acceptance.

Profiles remain pinned by the existing Runtime requirements files. FreeCAD is an external host capability and is not pip-managed.

## Evidence and authority

Every write action produces a digital-runtime-management receipt with source head, slot, action, profile, managed root, and authority boundary.

These actions prove software/runtime management only. They do not create CGX semantic authority, distributed governance promotion, public release, physical/engineering validation, manufacturing/certification authority, or legal/financial commitments.

## Failure behavior

Fail closed when action/profile is unknown, slot name is unsafe, confirmation is absent for a write, marker is missing or mismatched, update targets an uninstalled slot, install targets an installed slot, the canonical installer is missing, or the installer exits non-zero/produces no receipt.

Do not silently fall back to arbitrary PowerShell, Python, filesystem deletion, or another runtime.
