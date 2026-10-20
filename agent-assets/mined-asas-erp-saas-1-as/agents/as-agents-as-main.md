# ASAS AI Engineering Operating Contract

## Specification authority

The ASAS Enterprise Architecture Blueprint v1.6.1 and its handoff package are the baseline specification. The authority chain is:

1. Live database reality for pre-existing production tables
2. Blueprint Chapter 39 contracts (`schema/asas-contracts.prisma`)
3. Blueprint appendices and machine-readable registers
4. Blueprint chapter prose
5. Existing repository patterns
6. General best practice

Never edit a register merely to make it agree with code already written.

## Non-negotiables

- Inspect reality before schema-touching work.
- Extend; never rewrite production data without an explicit approved migration plan.
- Every mutation is authorization-gated and deny-by-default.
- Lifecycle state changes use the canonical state-machine transitions; no arbitrary status setters.
- Money is integer DZD centimes and posted financial records are immutable.
- Multi-tenant isolation must be enforced at the data layer, not only in UI/API code.
- Auditability is mandatory for material state changes.
- Public website, Studio, CRM, ERP and integrations share canonical domain data rather than duplicated truths.
- Research before non-trivial implementation; evidence before claims; tests before delivery.

## Working loop

Locate task → load required context → inspect current reality → plan → contract-first design → implement the smallest coherent change → run tests/verification → adversarial review → report exact evidence.

Do not claim VERIFIED unless execution evidence exists. Use: VERIFIED / FAILED / BLOCKED / NOT EXECUTED.

## Repository policy

- One coherent task per branch/PR.
- No force-push, reset, destructive migration, or deletion of production data.
- Do not silently change product scope; founder-level product decisions must be recorded.
- Keep architecture modular-monolith-first unless evidence requires a different boundary.
