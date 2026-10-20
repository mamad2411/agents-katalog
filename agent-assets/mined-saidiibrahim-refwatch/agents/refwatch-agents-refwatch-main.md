# Agent Routing Map

## Read Order
1. `AGENTS.md` (this file)
2. `docs/AGENT_COLLABORATION_PROCESS.md`
3. `ARCHITECTURE.md`
4. `docs/PRODUCT_SENSE.md`
5. `docs/product-specs`
6. `docs/design-docs`
7. `docs/references`
8. `docs/PLANS.md` and `docs/exec-plans`

## Canonical Paths
- Product intent and feature specs: `docs/product-specs`
- Architecture and design decisions: `docs/design-docs`
- Runbooks and process references: `docs/references`
- Execution plans and task tracking: `docs/exec-plans`
- Generated artifacts (schema snapshots): `docs/generated`
- Quality, reliability, and security governance: `docs/QUALITY_SCORE.md`, `docs/RELIABILITY.md`, `docs/SECURITY.md`

## Routing By Work Type
- New feature or behavior change: start with `docs/product-specs`, then update/create an active plan under `docs/exec-plans/active`.
- Refactor or system change: start with `ARCHITECTURE.md` and `docs/design-docs`, then track work in `docs/exec-plans/active`.
- Bugfix, release, or diagnostics: use `docs/references/process` and `docs/references/testing`.
- Data/backend sync changes: consult `docs/generated/db-schema.md` and Supabase migrations.
- UI/UX changes: consult `docs/DESIGN.md`, `docs/FRONTEND.md`, and related product specs.

## Primary Target Devices
- Physical iOS target: iPhone 15 Pro Max.
- Physical watchOS target: Apple Watch Series 9 (45mm).
- When validating UX, performance, and reliability, prioritize these devices before other hardware.
