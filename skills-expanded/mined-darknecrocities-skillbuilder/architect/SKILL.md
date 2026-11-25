---
name: architect
description: Interface-first design and shape sketching skill (/architect). Locks types, schemas, state machines, UI layout trees, and file boundaries before implementation.
---

# Interface-First Architecture (`/architect`)

> **Role**: Principal Systems Architect  
> **Philosophy**: *Name the data shape before writing logic. Make illegal states unrepresentable. Lock module boundaries before filling function bodies.*

This skill enforces `Foundational Thinking`, `Model the Domain`, and `Type System Discipline` prior to implementation across backend, frontend, AI, and visual asset tasks.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/interface-first-blueprinting.md](references/interface-first-blueprinting.md) | Discriminated unions, branded IDs, UI layout skeleton contracts, and file-split thresholds. |

---

## 2. The 5-Step Architect Gate

Execute before writing implementation bodies on any non-trivial feature or refactor:

1. **Core Types & Illegal-State Elimination**:
   - Replace boolean flag soups (`isLoading && !isError && hasItems`) with discriminated unions (`{ status: 'idle' | 'loading' | 'ready' | 'error'; ... }`).
   - Brand security-critical IDs (`TenantId`, `UserId`) where mixing IDs causes BOLA/IDOR bugs.
2. **Boundary Contracts (Schema First)**:
   - Define Zod / Pydantic v2 / OpenAPI / JSON Schema validation at ingress and egress boundaries.
   - Define DDL migrations (`CREATE TABLE`, foreign keys, constraints) before writing repository queries.
3. **Domain State & Transitions**:
   - Model workflows as explicit transition tables or state machines (including Rive `.riv` mascot inputs or UI async states).
4. **UI Shape & Responsive Skeleton (When Client-Facing)**:
   - Lock art movement (`/ui`), 60-30-10 color tokens, layout grid (`@container` / safe areas), and interactive states (empty, loading, error, reduced-motion) *before* styling details.
5. **Module & File Ownership Plan (`<= 500` Lines)**:
   - Partition files cleanly (`<= 250` lines for UI components, `<= 300` for domain services, `<= 350` for repositories, `<= 500` absolute ceiling) so sibling subagents never touch the same file.

---

## 3. Architect Output Contract

Emit a compact **Shape Spec** containing:
- Type/Schema definitions (`20–50` lines).
- State transition table or data-flow sequence.
- Exact file tree with per-file responsibility and line-budget tier.
- Verification command proving the shape compiles and passes contracts.
