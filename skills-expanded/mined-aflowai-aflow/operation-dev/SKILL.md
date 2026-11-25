---
name: operation-dev
description: Background knowledge for adding or modifying platform operations — covers operation IDs, registry entries, executor handlers, compact catalog format, and the full development checklist.
user-invocable: false
---

# Operation Development Guide

This skill covers the full lifecycle of adding or modifying an operation on the Aflow platform.

## Checklist — adding a new operation

1. **Define Zod schemas** in `packages/schemas/src/operations/<stepType>.ts`
   - `inputZod`: All input fields with descriptions, defaults, enums
   - `outputZod`: All output fields
   - Derive TypeScript types: `type FooInput = z.infer<typeof FooInputSchema>`

2. **Register in catalog** — add entry to the `OperationRegistrations` array in the same file
   - `stepType`, `group`, `verb` (operationId computed automatically)
   - `name`, `semanticDescription`, `usage` (oneLine, whenToUse, pitfalls)
   - `internalFields` for orchestrator-managed inputs hidden from agents
   - `idempotency`: `'idempotent'` or `'non_idempotent'`

3. **Add executor handler** in `apps/aflow-executor-<stepType>/src/handlers/`
   - Implement `StepHandler` interface: `{ stepType, execute(ctx) }`
   - Register in executor's `index.ts`

4. **Verify catalog** — run `yarn catalog:export` or use MCP `catalog` tool
   - Check compact format shows correct params, enums, pitfalls
   - Verify `usage.oneLine` is clear and unambiguous

5. **Test** — unit test for schema validation, integration test via MCP `run_operation`

6. **Typecheck** — `yarn typecheck` to verify all imports resolve

## Key references

- [registry.md](references/registry.md) — Registry entry anatomy and all fields
- [executor.md](references/executor.md) — Handler pattern and ExecutorRuntime
- [catalog.md](references/catalog.md) — Compact format rules for agent-facing output
- [`docs/dev/integrations-and-capabilities.md`](../../../docs/dev/integrations-and-capabilities.md) — when the op crosses an API or MCP integration, read this first

## Capability placement

Use `buildCoreToolSpec` for both pinned and promoted operation schemas. Assign new agent-reachable operations to one capability bundle (exact-operation ownership takes precedence over group ownership). Changing an operation's default requires updating the authored Helmsman surface; a bundle tier alone is not the runtime default. Skill discovery is `catalog.skill.search`, not an unbounded injected list.
