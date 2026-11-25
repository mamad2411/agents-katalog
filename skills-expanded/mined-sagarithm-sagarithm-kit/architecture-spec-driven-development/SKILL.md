<!-- SAGARITHM:START - DO NOT EDIT DIRECTLY -->
---
id: "architecture.spec-driven-development"
name: "Specification-Driven Architecture"
version: "1.2.0"
domain: "architecture"
description: "Transforms validated ideas into formal, testable architectural specifications. Defines bounded contexts, contract interfaces, state machines, and acceptance criteria before implementation."
triggers:
  - "Writing specifications for new features or subsystems"
  - "Translating validated ideas into technical requirements"
  - "Defining system contracts or public API schemas"
---

# 📐 Specification-Driven Architecture

> **"Code is ephemeral; specifications and contract interfaces are durable. Without a clear specification, tests verify assumptions rather than requirements."**

Specification-Driven Architecture ensures that every feature, service, and module is specified with mathematical precision prior to code authoring. It establishes unambiguous boundaries between what a system *must do* (contracts) and *how it does it* (implementation).

---

## 🏛️ Specification Anatomy

Every production specification in Sagarithm Kit must reside in `docs/specs/[name]-spec.md` and include:

1. **Context & Motivation**: Why this abstraction exists and the business/system need it fulfills.
2. **Domain Boundary & Ubiquitous Language**: Clear definitions of domain entities, value objects, and states.
3. **Public Interface Contracts**: Strongly-typed function signatures, DTOs, and event payloads (in TypeScript/Rust/Go).
4. **State Machine & Invariants**: Exhaustive states (e.g., `PENDING` -> `PROCESSING` -> `COMPLETED` | `FAILED`) and prohibited transitions.
5. **Acceptance Criteria (Given / When / Then)**: Concrete, automatable behavioral scenarios.
6. **Non-Functional Requirements**: Latency budgets (p99), memory ceiling, and security boundary isolation.

---

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Architectural Reality | Mandatory Requirement |
|---|---|---|
| *"The requirements are obvious from the prompt."* | Prompts are ambiguous natural language. Implementation details hide silent breaking changes. | Author the contract interfaces and DTOs before touching application code. |
| *"I'll write the spec while writing the code."* | Writing specs concurrently produces code-coupled specs that merely mirror whatever code was typed. | Spec must be drafted, reviewed, and finalized before the first implementation line. |
| *"We don't need formal state machines for this flow."* | Implicit state machines cause distributed edge-case bugs and race conditions. | Map all valid states and illegal transitions explicitly. |
| *"Any generic error handling is fine for now."* | Undefined failure states cause unrecoverable crashes and corrupted data stores. | Specify discrete, typed error cases for every public contract. |

---

## ⚙️ Standard Workflow: Spec to Implementation

```
  1. Draft Spec (docs/specs/) ──► 2. Invariant Review ──► 3. Contract Tests (Red)
                                                                 │
                                                                 ▼
                                                        4. Implementation (Green)
```

1. **Drafting**: Write the specification with complete type signatures.
2. **Invariant Review**: Verify acyclic dependency rules and ensure no circular imports are introduced.
3. **Contract Tests**: Convert the Acceptance Criteria into failing test cases (`npm test`).
4. **Implementation**: Fulfill the contract until all verification vectors achieve `[VERIFIED]` state.
<!-- SAGARITHM:END -->
