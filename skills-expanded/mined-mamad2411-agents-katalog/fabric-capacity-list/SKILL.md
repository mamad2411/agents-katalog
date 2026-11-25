---
description: List Available Fabric Capacities
name: fabric-capacity-list
status: preview
since: 2026-05-28
related: fabric-workspace-create, ops-init
---

# /fabric-capacity-list — List Available Fabric Capacities

> **Status**: preview. F2 Fabric workspace lifecycle suite, 2026-05-28.
> Source pattern from `distributions/demo-claude/.../local/_run_migration_dev.py`
> (workspace provisioning preflight).

## What it does

Lists Fabric capacities visible to the current identity, with id + state +
SKU. Pre-flight for `/fabric-workspace-create` — you need a capacity id to
assign the new workspace to a capacity (without one the workspace lands on
the default "trial" capacity, which has different limits).

## When to use

- Before `/fabric-workspace-create` when you don't know the target capacity id
- Auditing what capacities the current identity has access to
- Verifying a capacity is in `Active` state before assigning workloads

## Prerequisites

- `FabricConnector` credentials configured (`config/credentials.yaml`)
- `az login` or service principal credentials in scope
- The identity needs at least *Reader* on the capacity to see it

## Usage

```
/fabric-capacity-list                          # all capacities visible
/fabric-capacity-list --filter Active          # only Active capacities
/fabric-capacity-list --json                   # raw JSON output
```

## Pipeline summary

1. Load project + credentials
2. Build `FabricConnector` from credentials
3. Call `connector.client.list_capacities()` (GET `/v1/capacities`)
4. Render as a table: `id | displayName | sku | state | region`
5. Filter / format per flags
6. ops.log: `CAPACITY-LIST | - | - | n capacities returned | ok`

## Example output

```
id                                    displayName       sku   state    region
6f8b3c44-...                          DemoCapacity      F2    Active   westeurope
a1b2c3d4-...                          TrialCapacity     FT1   Active   eastus
```

## Preview tracking — known unknowns

1. **State terminology**: Fabric returns `Active`, `Paused`, `Suspended`,
   `Deleting`. V1 surfaces them verbatim; future may add hint text
   ("Paused = workspace creation will fail").
2. **Region filtering**: not exposed in V1. Caller filters output manually
   if needed.
3. **Trial capacities**: appear in the list with SKU prefix `FT*`. Not
   labelled specifically — caller infers.

## Status — promotion to `stable`

1. 3+ uses across different identities (different `az login` accounts) with
   identical structured output.
2. At least 1 case where the listing prevented a bad capacity assignment
   (caught a `Paused` or wrong-region capacity before create).
3. No silent failures on permission errors (403 surfaced clearly).

ARGUMENTS: $ARGUMENTS
