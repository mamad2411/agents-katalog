# System Architecture Diagram

## Purpose
Maintains a living MermaidJS system topology diagram updated incrementally per story — never redrawn from scratch.

## Role
Solution Architect

## Phase
Planning (Stage 3) + Development (when new service added)

## Triggered By
`technical-assessment` identifies new service or topology change.

## Inputs
- Current `system-architecture.md` from `apps/docs/`
- Story's new services/connections (from `technical-assessment`)

## Process
1. Read current `system-architecture.md` from `apps/docs/`.
2. Identify what changes for this story (new service? new connection?).
3. Add new elements to existing diagram (never start from scratch).
4. Commit updated diagram to OpenSpec draft location.
5. Technical Writer publishes to `apps/docs/` when story ships.

### Diagram Content
MermaidJS graph showing:
- All services with their type (`*-grpc`, `*-subgraph`, `*-cron`)
- Communication protocols (gRPC, GraphQL, Kafka, HTTP)
- Infrastructure components (Apollo Router, Kafka, Authentik, Vault, Traefik)
- External boundaries (public internet vs internal network)
- Data stores (PostgreSQL, Redis, ClickHouse, Meilisearch) per service

## Outputs
- Draft: `openspec/changes/{slug}/diagrams/system-architecture.md`
- Published: `apps/docs/src/content/internal/latest/architecture/system-architecture.md`

## Quality Gates
- [ ] Diagram uses MermaidJS format
- [ ] All existing services preserved (never delete existing)
- [ ] New elements clearly added
- [ ] Draft committed to OpenSpec

## References
- `.claude/skills/solution-architect/technical-assessment/SKILL.md`
- `.claude/skills/technical-writer/` (publishing)
