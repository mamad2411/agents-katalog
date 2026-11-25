---
id: "architecture.system-design"
name: "System Design & Modularity"
version: "1.2.0"
domain: "architecture"
description: "Decompose complex systems into highly cohesive, loosely coupled modules with explicit public interfaces, bounded contexts, and acyclic dependencies."
triggers:
  - "Designing new system modules or packages"
  - "Refactoring cross-cutting abstractions"
  - "Defining inter-service or inter-module communication boundaries"
  - "Integrating third-party systems or external services"
prerequisites: []
risk_profile: "high"
---

# System Design & Modularity

## Overview
This skill guides AI agents and engineers in decomposing system requirements into maintainable, modular components while preventing architectural decay, circular dependencies, and leaky abstractions.

## Core Directives
1. **Define Explicit Boundaries**: Every module must expose a strict public API (e.g. index file or port interface) and hide internal implementation helpers.
2. **Enforce Directional Dependencies**: High-level business policies must never depend on low-level technical mechanisms (database drivers, network protocols). Apply Dependency Inversion.
3. **Prevent Circular References**: Maintain a strict Directed Acyclic Graph (DAG) across modules and packages.
4. **Cohesion Over Fragmentation**: Avoid arbitrary file splitting. Keep concepts that change together within the same domain boundary.
5. **Protect the Domain with ACLs**: Isolate third-party schemas and external API changes through an Anti-Corruption Layer (ACL).
6. **Automate Architecture Verification**: Codify layer boundaries into automated Architectural Fitness Functions.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Architectural Reality | Mandatory Action |
|---|---|---|
| *"I'll just add this function to an existing module to save time."* | Unrelated functions pollute bounded contexts and increase coupling ($Ce$). | Place the function in its own cohesive domain or create a clean port interface. |
| *"A circular import between these two files is harmless."* | Circular dependencies cause runtime undefined imports and brittle initialization bugs. | Refactor shared abstractions into a common contract or use event emission. |
| *"I'll create a `utils/` folder for miscellaneous helpers."* | Prohibited by policy. Generic helper dumps become unmaintainable junk drawers. | Group helpers directly with the domain logic they serve. |

## Detailed Guidance
- [Modularity and Coupling Guidelines](references/modularity-and-coupling.md)
- [Domain Boundaries & Event-Driven Decoupling](references/domain-boundaries-and-events.md)
- [Architectural Fitness Functions](references/architectural-fitness-functions.md)
- [Modular vs. Tightly Coupled Examples](examples/modular-vs-tightly-coupled.md)
- [Architecture Review Checklist](checklists/architecture-review-checklist.md)
