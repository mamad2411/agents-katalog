---
name: refactor
description: Safe refactoring and technical debt remediation skill. Enforces Strangler Fig patterns, characterization testing, and decomposition of bloated files.
---

# Safe Refactoring & Technical Debt Remediation (`/refactor`)

> **Philosophy**: *Never refactor without tests. Change behavior or change structure, never both in the same turn. Decompose god files before they hit 500 lines. Strangler Fig over big-bang rewrites.*

This skill establishes disciplined patterns for paying down technical debt, decomposing bloated modules, and modernizing legacy code without introducing regressions or downtime.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/strangler-fig-pattern.md](references/strangler-fig-pattern.md) | Phased execution steps, abstraction facades, rollback safety nets. |
| **Reference** | [references/characterization-testing.md](references/characterization-testing.md) | Pinning down legacy behavior, boundary assertion protocols, regression prevention. |
| **Utility** | [scripts/detect_refactor_opportunities.py](scripts/detect_refactor_opportunities.py) | Scans codebase for files $>350$ lines, functions $>40$ lines, and nesting $>3$ levels. |

---

## 2. The Two-Hat Refactoring Protocol

```mermaid
flowchart TD
    A["Legacy / Bloated Module"] --> B["Phase 1: Characterization Tests (Pin Current Behavior)"]
    B --> C["Phase 2: Introduce Abstraction Layer (Interface)"]
    C --> D["Phase 3: Implement New Modular Subsystems"]
    D --> E["Phase 4: Verify Full Test Suite Parity"]
    E --> F["Phase 5: Route Traffic to New Subsystem (Branch by Abstraction)"]
    F --> G["Phase 6: Delete Deprecated Code & Verify Line Limits"]
```

### The "Two Hats" Discipline:
1. **The Refactoring Hat**: You restructure existing code to improve maintainability, reduce cyclomatic complexity, and decompose bloated files. You **do not** add new business features or alter external API contracts. Every existing test must remain green.
2. **The Feature Hat**: You introduce new capabilities and write new tests. You **do not** perform sprawling rewrites of unrelated modules in the same commit.

---

## 2. Decomposing God Files (The Multi-Tiered Maintainability Standard)

SkillBuilder enforces the **4-Tier Maintainability Matrix** (Sweet Spot $150-250$, Nominal $251-350$, Warning $351-499$, Hard Ceiling $500$). When any source file (`.ts`, `.tsx`, `.py`, `.go`, `.dart`, `.kt`, `.swift`) reaches the **350-line warning zone**, decompose it proactively before it violates the 500-line physical ceiling:

| File Type | Extraction Target | Destination Path |
| :--- | :--- | :--- |
| **Monolithic Component** | Sub-views & presentational child widgets | `components/<Feature>/<SubView>.tsx` |
| **Inline Validation Schemas** | Zod / Pydantic schemas and types | `schemas/<feature>Schema.ts` |
| **Inline Database Calls** | Repository query methods | `repositories/<feature>Repository.ts` |
| **Complex Pure Functions** | Mathematical or string formatting logic | `utils/<domain>Utils.ts` |
| **State & Effects** | Custom React hooks or store slices | `hooks/use<Feature>State.ts` |

### Cognitive Hygiene & Refactoring Rules:
1. **The 40-Line Function Ceiling**: Any function exceeding 40 lines must be decomposed into focused sub-helpers or extracted into a domain utility.
2. **The 3-Level Nesting Ceiling**: Any block nested $>3$ levels deep must be refactored with early returns and guard clauses (`if (!condition) return;`).
3. **Anti-Shotgun Surgery Principle**: Never chop files arbitrarily just to satisfy line counts. Every split must represent a clean cohesive boundary (presentation, domain logic, persistence, or contracts).

---

## 3. Branch by Abstraction & Strangler Fig Patterns

When replacing a critical production subsystem (e.g. switching from raw SQL queries to an ORM, or replacing an old payment gateway):

```mermaid
flowchart LR
    A["Callers"] --> B["1. Abstraction Interface (PaymentGateway)"]
    B --> C["Legacy Gateway Implementation (Active)"]
    B -.-> D["Modern Gateway Implementation (Testing)"]
    subgraph Migration["Phase 2: Feature Flag Switch"]
        B --> D
    end
    subgraph Cleanup["Phase 3: Deprecation"]
        E["Delete Legacy Gateway File"]
    end
```

1. **Create the Abstraction**: Define a clean interface describing the operations callers need.
2. **Implement Existing Caller Adapter**: Wrap the current legacy code behind the interface without changing behavior.
3. **Build the New Modern Implementation**: Write the replacement subsystem conforming to the interface, backed by unit tests.
4. **Gradually Migrate Callers**: Use a feature flag or configuration toggle to route traffic.
5. **Deprecate & Delete**: Remove the legacy implementation and obsolete tests.

---

## 4. Characterization (Golden Master) Testing

When refactoring legacy code that has zero unit tests:
1. Write characterization tests that capture the **current actual behavior** for a wide matrix of inputs, even if the current behavior includes known quirks.
2. Store the input/output fixtures (Golden Master snapshot).
3. Execute the refactor.
4. Run characterization tests to guarantee zero unexpected behavioral drift.
5. Author dedicated unit tests for the newly extracted components.

---

## 5. Refactor Opportunities Detector CLI

Scan your repository for complex, deeply-nested, or bloated files needing refactoring:
```bash
python3 skills/refactor/scripts/detect_refactor_opportunities.py --path .
```
Audits:
- Source files exceeding 350 lines (approaching the 500-line limit).
- Functions with cyclomatic complexity > 10.
- Deeply nested indentation structures (> 4 levels).
- Files containing duplicate utility implementations.
