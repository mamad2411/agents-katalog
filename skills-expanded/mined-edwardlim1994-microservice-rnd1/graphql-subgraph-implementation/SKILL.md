# GraphQL Subgraph Implementation

## Purpose
Implements a `*-subgraph` as a thin layer over the sibling `*-grpc` service, with no direct database access.

## Role
Backend Developer

## Phase
Development (AFTER `*-grpc` service is complete and PR merged)

## Triggered By
Sibling `*-grpc` PR merged, types available.

## Inputs
- SDL from `contracts/graphql/`
- Generated types from `packages/api/src/generated/{service}/graphql/`
- Sibling `*-grpc` service's GrpcClient

## Rules
- ALWAYS paired with `*-grpc` — never a standalone subgraph.
- NEVER access database directly from subgraph.
- ALL data access through sibling `*-grpc` via GrpcClient.
- SDL defined by Architect in `contracts/graphql/` — NEVER define in service.
- Generated types: `packages/api/src/generated/{service}/graphql/` — NEVER edit.

## Process

### Class Generation Order
1. `bun turbo gen → usecase` (`{Operation}UseCase`)
   - Wraps GrpcClient calls
   - Handles gRPC → GraphQL type mapping
   - Contains no business logic (that lives in `*-grpc`)
2. `bun turbo gen → router` (`{Entity}GraphqlRouter`)
   - Extends GraphqlRouter
   - Maps GraphQL resolvers to UseCase invocations
3. Wire GrpcClient for sibling service.
4. Wire into `ServerApp`:
   ```
   new ServerApp()
     .use(new ApolloDriver({ ... }))
     .use(new {Service}GrpcClient())
     .use(new {Operation}UseCase())
     .use(new {Entity}GraphqlRouter())
     .start()
   ```
5. Run `bun run supergraph` after implementation complete.

## Outputs
Implemented `*-subgraph` service, verified against composed supergraph.

## Quality Gates
- [ ] No database access in subgraph (verified by code review)
- [ ] GrpcClient used for all data access
- [ ] Generator used for all class creation
- [ ] bun run supergraph passes

## References
- `.claude/skills/backend-developer/grpc-service-implementation/SKILL.md`
- `.claude/skills/solution-architect/graphql-schema-design/SKILL.md`
