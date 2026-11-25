---
name: architecture-blueprint-generator
description: Analyze a codebase and generate Project_Architecture_Blueprint.md — detected stacks and architecture patterns, diagrams, layers, cross-cutting concerns, extension guidance. Use to document, map, or blueprint a project's architecture or keep it consistent.
---

# Project Architecture Blueprint Generator

Analyze the architectural patterns actually implemented in the codebase and write a
comprehensive `Project_Architecture_Blueprint.md` that serves as the definitive reference for
maintaining architectural consistency and guiding new development. Document what the code
*does*, not theoretical patterns — every claim should trace to project structure, dependencies,
or configuration.

## Options

Defaults below; adjust any of them when the user specifies:

| Option | Default | Alternatives |
| --- | --- | --- |
| Technology stack | Auto-detect | .NET, Java, React, Angular, Python, Node.js, Flutter, … |
| Architecture pattern | Auto-detect | Clean, Microservices, Layered, MVVM, MVC, Hexagonal, Event-Driven, Serverless, Monolithic, … |
| Diagrams | C4 | UML, Flow, Component, none (textual description instead) |
| Detail level | Detailed | High-level, Comprehensive, Implementation-Ready |
| Optional sections | All included | Drop implementation patterns, extensibility, code examples, or ADRs on request |

## Workflow

1. **Detect** — identify the stack(s) and architectural pattern(s) from project/config files,
   dependencies, folder organization, and dependency flow (detection signals in
   [`references/blueprint-structure.md`](references/blueprint-structure.md) §1).
2. **Write the core sections** — overview, visualization, components, layers, data
   architecture, cross-cutting concerns, service communication, testing, deployment,
   governance, and the blueprint-for-new-development guide, following
   [`references/blueprint-structure.md`](references/blueprint-structure.md) section by section.
3. **Add the per-stack section** for each detected technology, using the checklists in
   [`references/technology-patterns.md`](references/technology-patterns.md).
4. **Add the optional sections** that apply — implementation patterns, extension/evolution
   guidance, code examples, ADRs — per
   [`references/optional-sections.md`](references/optional-sections.md).
5. **Close** with the generation date and recommendations for keeping the blueprint updated as
   the architecture evolves.

## References

Read a reference only when writing that part of the blueprint:

- [`references/blueprint-structure.md`](references/blueprint-structure.md) — the 12 core
  sections in full: detection signals, per-section content checklists, the new-development
  guide · read in **step 2**.
- [`references/technology-patterns.md`](references/technology-patterns.md) — stack-specific
  pattern checklists (.NET, Java, React, Angular, Python + how to derive others) · read in
  **step 3**.
- [`references/optional-sections.md`](references/optional-sections.md) — implementation
  patterns, extension/evolution patterns, code examples, ADRs · read in **step 4**.
