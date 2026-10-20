# Server Scaffolding

## Purpose
Two-level scaffolding process for all backend server types using Turborepo generators — never manual.

## Role
Backend Developer

## Phase
Development

## Triggered By
New server needed (from Architect's `service-boundary-definition`).

## Inputs
- Service boundary and type determination from Architect

## Server Types
- `*-grpc`: internal gRPC server (business logic, database)
- `*-subgraph`: Apollo Federation subgraph (public GraphQL, calls `*-grpc`)
- `*-cron`: scheduled job server (Bun native cronjob)

Note: Public endpoints ALWAYS require paired `*-grpc` + `*-subgraph`.

## Process

### Level 1 — Server Scaffold
```
bun turbo gen
→ select: server
→ select type: grpc | subgraph | cron
→ enter service name
```
Generator creates: Dockerfile, docker-compose.yml, Helm chart, `app.ts`, `index.ts`.

### Level 2 — Class Scaffold (ALWAYS use generator — never write manually)
```
bun turbo gen → router     (GrpcRouter, GraphqlRouter, CronRouter, KafkaRouter)
bun turbo gen → usecase    (UseCase per operation)
bun turbo gen → repository (Repository per entity — grpc only)
bun turbo gen → producer   (KafkaProducer — if producing events)
```

### Class Generation Order (strict)
1. Repository first (entity data layer)
2. UseCase (business logic, depends on Repository)
3. Router (handler layer, depends on UseCase)
4. Wire into `ServerApp` in `app.ts`
5. Implement business logic in generated scaffolds

NEVER manually create router, usecase, or repository classes from scratch. ALWAYS read generated code before adding business logic.

## Outputs
Scaffolded server structure ready for business logic implementation.

## Quality Gates
- [ ] Both levels of scaffolding used (not manual creation)
- [ ] Class generation order followed (repo → usecase → router)
- [ ] Generated code read before business logic added
- [ ] app.ts properly wires all generated classes

## References
- `.claude/skills/backend-developer/tdd-workflow/SKILL.md`
- `.claude/skills/backend-developer/grpc-service-implementation/SKILL.md`
- `.claude/skills/solution-architect/service-boundary-definition/SKILL.md`
