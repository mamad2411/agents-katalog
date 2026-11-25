---
name: high-fidelity-ecs-engineering
description: Mandatory high-rigor ECS (Entity Component System) game engine engineering and architectural auditing. Use for ALL tasks involving architectural changes, domain materialization, or engine logic to ensure Zero-Trust integrity and Bit-Perfect simulation through formal ADR documentation and verbatim code specs.
---

# High-Fidelity ECS Engineering & Protocol

This skill defines the strict, non-negotiable architectural paradigm and development workflow for the OnceHuman Simulator project. It prioritizes long-term architectural health, bit-perfect simulation fidelity, and absolute type safety through a rigorous ECS architecture and formal documentation.

## I. Core Principles (The ECS Paradigm)
1. **The Anti-Prototype**: We never sacrifice sound engineering for short-term completion. "Getting it to work" is not enough; it must be correct, typed, and architecturally sound.
2. **Zero Tolerance for `as any`**: Any use of `as any`, `any`, or `unknown` casts is a critical failure. If a type is difficult to express, the abstraction must be refined or a better type mechanism (generics, unions) must be used.
3. **Principled ECS Design**: 
    - **Entities**: Strictly opaque IDs (e.g., `EntityId` branded strings).
    - **Components**: Pure data structures (POJOs) with NO methods. They represent state, not behavior.
    - **Systems**: Pure functions that contain ALL logic. Systems query components and write results. No logic in Components, no state in Systems.
4. **Data Fidelity & Zero-Trust**: All game data (formulas, stats, tiers) must be modeled with zero-trust validation at the boundaries.

## II. The Mandatory Workflow (Execution Protocol)
You MUST follow this exact sequence for every architectural change or engine logic task.

### Step 1: ADR & Pipeline Reconnaissance
Before touching any code, you MUST read **ALL** existing ADRs in `simulator/docs/designs/` and the ECS standards in `references/ecs-standards.md`.
- Goal: Maintain absolute continuity with the ECS transition and previous architectural decisions.

### Step 2: Formal ADR Creation
You MUST create or update a formally numbered ADR (e.g., `ADR-014-...`) before implementing any change.
- The ADR must be written in the `simulator/docs/designs/` directory.
- **Verbatim Implementation Specification**: The ADR MUST contain **verbatim code blocks** for:
    1. **Every Component & Type change**: Show the exact interfaces and branded types.
    2. **Every System logic change**: Show the exact pure functions and their ECS queries.
    3. **High-Fidelity Tests**: Include the verbatim code for the integration tests that will verify the change.

### Step 3: Incremental ECS Migration
- Identify "Fat Objects" or logic-heavy data structures and split them into Entities and Components.
- Implement logic as independent, decoupled Systems.
- Use the `Task & Implementation Tracking` pattern in the ADR/Plan to track progress.

### Step 4: Verification & Proof
After implementation, you MUST:
1. Run `npx tsc --noEmit` and `npm test` to ensure zero type errors and passing tests.
2. Prove the presence of the code in the ADR using explicit `grep -F` checks on the verbatim blocks.
3. Verify that the simulation output matches the "In-Game Knowledge Bible" with bit-perfect accuracy.

## III. Guidelines & Specifications
For detailed instructions on ECS patterns, type safety standards, and universal engineering frameworks, see:
- [ECS Standards & Engineering Rigor](references/ecs-standards.md)
- [Universal Engineering Standards: ECS Integration](references/universal-standards.md)

## IV. Usage Scenarios

### Refactoring a "Fat" Class to ECS
**Strategy:** Define pure data `Components`, then implement a `System` (pure function) that queries those components and performs the logic previously in the class methods.

### Implementing a New Mechanic
**Strategy:** Create a new `Component` to hold the mechanic's state and a new `System` to process it during the appropriate pipeline phase. Ensure all inputs are validated at the JSON/API boundary.
