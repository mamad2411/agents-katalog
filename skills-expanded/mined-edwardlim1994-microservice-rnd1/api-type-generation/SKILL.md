# API Type Generation

## Purpose
Runs code generation to produce TypeScript types from all schema definitions, making them available to developers.

## Role
Data Engineer

## Phase
Development (CRITICAL — must complete before backend/frontend start)

## Triggered By
`api/` branch merged to `feat/` (schemas ready).

## Inputs
- Merged schema files in `contracts/`

## Rule
HARD SEQUENCING: `api-type-generation` MUST complete before `task/` branches start. Signal completion in kanban card description immediately after success.

## Process

### Commands
```
bun run gen         ← runs all generation (proto + graphql + prisma)
bun run gen:proto   ← proto only (buf generate)
bun run gen:graphql ← GraphQL only (graphql-codegen)
bun run gen:prisma  ← Prisma client only
```

### Generated Output (NEVER edit these files)
- `packages/api/src/generated/{service}-grpc/proto/` ← from proto
- `packages/api/src/generated/{service}-graphql/graphql/` ← from graphql
- `apps/servers/{service}/generated/prisma/` ← from prisma

### After Generation
1. Verify generated files compile: `bun turbo check`.
2. Commit generated files (they must be committed — consumers depend on them).
3. Update kanban card description: "Types generated and committed. packages/api/src/generated/ ready. Backend Developer tasks unblocked: KAN-{N}, KAN-{N}".
4. Signal PM: backend/frontend tasks can now start.

## Outputs
Generated, committed TypeScript types; unblocked task cards.

## Quality Gates
- [ ] All generation commands pass without errors
- [ ] Generated files compile (bun turbo check)
- [ ] Generated files committed to repo
- [ ] Kanban card updated with unblocked task numbers

## References
- `.claude/skills/data-engineer/schema-implementation/SKILL.md`
- `.claude/skills/data-engineer/schema-release-coordination/SKILL.md`
- `.claude/skills/backend-developer/tdd-workflow/SKILL.md`
