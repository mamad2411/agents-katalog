---
name: testing-pi-agent-orchestrator
trigger: /test
description: Test the pi-agent-orchestrator VS Code extension. Use when verifying code changes, running the test suite, or writing adversarial tests.
---

# Testing pi-agent-orchestrator

## Overview
This is a VS Code extension (no browser UI). All testing is shell-based via vitest.
No recording needed — capture command outputs as text evidence.

## Key Commands

```bash
# TypeScript compilation check
npx tsc --noEmit

# Lint (Biome)
npm run lint

# Run all tests
npx vitest run

# Run specific test files
npx vitest run test/handoff.test.ts test/agent-manager.test.ts

# Run tests matching a pattern
npx vitest run -t "session limits"
```

## Test Structure
- `test/handoff.test.ts` — Handoff parsing, prompt generation, rendering
- `test/error-chaos-handoff.test.ts` — Resilience: corrupted JSON, oversized payloads, DOS prevention
- `test/agent-manager.test.ts` — Session limits, usage accounting, spawn/turn enforcement
- `test/settings.test.ts` — Settings sanitization and persistence
- `test/e2e-chain.test.ts` — End-to-end agent chain execution
- `test/schedule.test.ts` / `test/schedule-e2e.test.ts` — Scheduled job execution
- `test/audit-logger.test.ts` — Audit logging: ring buffer, filtering, silent mode, outcome types, copy semantics
- `test/cross-extension-rpc.test.ts` — RPC handlers, auth, rate limiting, audit trail integration

## Code Conventions
- No `any` types (AGENTS.md rule)
- Conventional commits format
- Biome for formatting/linting (not ESLint/Prettier)
- `Number.isInteger()` does NOT narrow TypeScript types — always pair with `!== undefined` checks when the source type is `T | undefined`

## Devin Secrets Needed
None — this is a pure library/extension with no external service dependencies for testing.

## What You Must Do When Invoked

### Step 0 — Load adversarial testing reference

Read [references/adversarial-patterns.md](references/adversarial-patterns.md) for known flaky tests, adversarial test patterns, and immutability testing guides.

Use the adversarial patterns when writing or reviewing tests for core modules.
