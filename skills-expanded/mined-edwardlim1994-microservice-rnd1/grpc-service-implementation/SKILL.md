# gRPC Service Implementation

## Purpose
Implements a `*-grpc` service following proto-first development, UseCase pattern, and Repository pattern.

## Role
Backend Developer

## Phase
Development

## Triggered By
`tdd-workflow` initiated for a grpc service task.

## Inputs
- Proto contract from `contracts/proto/services/`
- Generated types from `packages/api/src/generated/{service}/proto/`

## Rule
Proto-first: schema defined by Architect in `contracts/proto/services/`. NEVER define proto schema inside the service — reference `contracts/` only. Generated types: `packages/api/src/generated/{service}/proto/` — NEVER edit.

## Process

### Class Generation Order
1. `bun turbo gen → repository` (`{Entity}Repository`)
   - Extends BaseRepository, uses PgAdapter or VaultPgAdapter
   - Implements: findById, findAll, create, update, delete
2. `bun turbo gen → usecase` (`{Operation}UseCase` per operation)
   - One class per operation (CreateItemUseCase, GetItemUseCase, etc.)
   - Constructor receives repository and plugins as dependencies
   - Contains ONLY business logic — no DB calls directly
3. `bun turbo gen → router` (`{Service}GrpcRouter`)
   - Extends GrpcRouter
   - Maps proto RPC methods to UseCase invocations
   - Contains NO business logic — only maps and delegates
4. Wire into `ServerApp` in `app.ts`:
   ```
   new ServerApp()
     .use(new GrpcDriver({ ... }))
     .use(new DbPlugin(VaultPgAdapter.fromEnv()))
     .use(new AuthentikAuthInterceptor())
     .use(new {Entity}Repository())
     .use(new {Operation}UseCase())
     .use(new {Service}GrpcRouter())
     .start()
   ```

`AuthentikAuthInterceptor`: ALWAYS applied to all gRPC services.

## Outputs
Implemented `*-grpc` service with Repository/UseCase/Router layers wired.

## Quality Gates
- [ ] Generator used for all class creation
- [ ] UseCase has no direct DB calls (goes through Repository)
- [ ] GrpcRouter has no business logic (delegates to UseCase)
- [ ] AuthentikAuthInterceptor wired in ServerApp
- [ ] All generated types referenced from packages/api/src/generated/

## References
- `.claude/skills/backend-developer/tdd-workflow/SKILL.md`
- `.claude/skills/solution-architect/proto-contract-design/SKILL.md`
