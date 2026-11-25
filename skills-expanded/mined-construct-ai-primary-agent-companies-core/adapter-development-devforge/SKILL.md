---
name: adapter-development-devforge
description: >
  Use when building new adapter types, modifying existing adapters, or implementing
  adapter-specific features like model selection, token tracking, and environment
  variables. Handles claude_local, codex_local, opencode_local, gemini_local, hermes_local.
---

# Adapter Development - DevForge AI

## Overview
Handles adapter development for the Paperclip codebase. Creates new adapter types, modifies existing adapters, implements adapter-specific features like model selection, token tracking, environment variable injection, and ensures adapters integrate with the heartbeat/wake lifecycle.

## When to Use
- When adding a new adapter type to `BUILTIN_ADAPTER_TYPES`
- When adapterConfig fields need to be added or modified
- When model selection in adapterConfig doesn't persist between runs
- When adapter environment variables need new fields (PAPERCLIP_WAKE_ACTOR_TYPE)
- When `isLocal` checks in UI miss a new adapter type
- When adapter execute.ts needs model API changes
- **Don't use when:** It's an adapter runtime error (use fixer-devforge-bug-fixing)

## Core Procedures
### New Adapter Workflow
1. **Define Adapter Type** - Add to `BUILTIN_ADAPTER_TYPES` in server adapters module
2. **Create Adapter Package** - Follow existing `*-local` adapter pattern in packages/adapters/
3. **Implement execute.ts** - Handle model API calls, token tracking, error handling
4. **Add Adapter Config Schema** - Define adapterConfig fields (model, thinking, etc.)
5. **Integrate Heartbeat** - Ensure adapter works with heartbeat/wake lifecycle
6. **Write Adapter Tests** - Match existing `*-local-adapter-environment.test.ts` pattern
7. **Update UI** - Add adapter to adapter type selector, update `isLocal` checks

### Common Adapter Patterns
- All `_local` adapters: set `isLocal = true` for instructions bundle access
- Adapter env vars: export `PAPERCLIP_*` vars from execute.ts contextSnapshot
- Config persistence: ensure adapterConfig is saved to DB, not just env vars

## Agent Assignment
**Primary Agent:** codesmith-devforge-backend-engineer
**Company:** DevForge AI
**Role:** Adapter Development Specialist
**Reports To:** codesmith-devforge-backend-engineer
**Backup Agents:** devcore-devforge-core-development, interface-devforge-api-integration

## Success Metrics
- New adapter works with heartbeat/wake lifecycle
- Model selection persists across runs
- UI `isLocal` checks include all local adapter types
- Adapter env vars properly exported

## Error Handling
- **Error:** Adapter config resets between runs
  **Response:** Check config persistence, ensure adapterConfig is saved to DB
- **Error:** UI misses adapter in isLocal check
  **Response:** Add adapter type to isLocal disjunction or derive from suffix

## Cross-Team Integration
**Gigabrain Tags:** devforge, adapter, model-selection, heartbeat, environment-variables
**Related Skills:** codesmith-devforge-backend-engineer, devcore-devforge-core-development, interface-devforge-api-integration
**Last Updated:** 2026-04-07
