---
name: multi-service-orchestration
description: Use when a change request affects multiple services or needs cross-service coordination. Activates the Cascade orchestration workflow with dependency-aware propagation.
---

# Multi-Service Orchestration

## Overview

When a change touches multiple services, coordinate it through the Cascade workflow instead of making ad-hoc edits.

**Core principle:** Changes cascade downstream. Upstream services first, contracts updated after each, verification at the end.

## When to Use

**Always use Cascade for:**
- Adding/renaming/removing fields that flow through multiple services
- Adding middleware or cross-cutting concerns to all services
- Restructuring response shapes consumed by downstream services
- Updating API contracts after any service API change
- Any change where "I'll update the other services later" is tempting

**Don't use Cascade for:**
- Changes to a single service with no downstream consumers
- Internal refactors that don't change API surface
- Test-only changes
- Documentation updates

## The Cascade Workflow

```
1. PLAN    → Analyze impact, map files, define verification criteria
2. IMPLEMENT → One service at a time, in dependency order
3. SYNC    → Update contracts after each service change
4. VERIFY  → Check cross-service consistency
5. FIX     → Address any verification failures
```

## Key Rules

- **Dependency order is non-negotiable** — upstream before downstream
- **Contracts sync after each service** — not at the end
- **Verification before completion** — evidence before claims
- **One change at a time** — don't batch unrelated changes
