---
name: contract-management
description: Use when working with API contracts in a multi-service project. Ensures contracts stay in sync with implementations and downstream consumers are updated when APIs change.
---

# Contract Management

## Overview

API contracts are the source of truth for how services communicate. Every API change must be reflected in the contracts file before downstream work begins.

**Core principle:** Code follows contracts. Contracts follow code. They must never diverge.

## When to Use

- After modifying any service's API endpoint
- Before implementing a downstream consumer of a changed API
- When onboarding to a multi-service project (read contracts first)
- During code review of cross-service changes

## Contract Files

Cascade looks for contracts in this order:
1. `cascade.yaml` → `contracts:` field
2. `contracts/api-contracts.yaml`
3. `contracts/dependency-map.md`
4. Any `ENGINE_INTERFACES.md` or similar architecture docs

## Versioning

| Change Type | Version Bump | Example |
|------------|-------------|---------|
| New field added | Minor (1.2.0 → 1.3.0) | Added `phone` to User |
| New endpoint | Minor | Added `/api/v1/users/search` |
| Field renamed | **Major** (1.2.0 → 2.0.0) | `role` → `account_type` |
| Field removed | **Major** | Removed `legacy_id` |
| Type changed | **Major** | `price: string` → `price: float` |
| Bug fix | Patch (1.2.0 → 1.2.1) | Fixed typo in contract |

## The Rule

After EVERY service API change:
1. Update the contract to match the actual code
2. Bump the version
3. Commit the contract change
4. THEN move to downstream services
