---
name: generate-implementation-design
description: Generate complete Chinese implementation design documents from a product PRD. Use when Codex needs to turn PRD content into a High-Level Design plus Low-Level Design document, ask focused clarification questions for missing implementation details, follow a fixed design template, apply C4-based architecture design, and save the final result as a markdown design file.
---

# Generate Implementation Design

## Overview

Turn a product PRD into a complete Chinese implementation design document that follows a fixed High-Level Design plus Low-Level Design structure.
Use `./resources/design-template.md` as the mandatory document scaffold and keep its section order and heading format unchanged.

## Workflow

Follow these phases in order.
Do not skip a phase unless the user explicitly asks for a partial result.

### Phase 1: Clarify Missing Information From The PRD

1. Read the user's request and define a concise requirement name.
2. Read `./resources/design-template.md` before asking questions.
3. Compare the PRD against every template section and identify missing, ambiguous, or weak information.
4. Ask focused clarification questions one by one or in very small batches.
5. Prioritize gaps that block design quality:
   - business background, current process, and pain points
   - system boundary, actors, and external dependencies
   - key use cases, interaction flow, and business rules
   - data entities, storage constraints, and consistency requirements
   - API contracts, error handling, and configuration needs
   - non-functional requirements such as performance, security, observability, and availability
   - deployment topology, release constraints, rollback expectations, and risks
6. Stop asking questions when the remaining gaps can be handled through explicit assumptions without weakening implementation feasibility.
7. If assumptions are necessary, mark them clearly as `待确认` in the design document rather than presenting them as confirmed facts.

### Phase 2: Generate The Implementation Design Document

1. Use the exact structure from `./resources/design-template.md`.
2. Write the full document in Chinese.
3. Replace every placeholder with concrete content derived from the PRD, follow-up answers, or explicit assumptions.
4. Save the document as `<需求名称>-design.md`.
5. Keep the requirement name short, specific, and file-system safe. Replace illegal path characters with `-` when needed.
6. Ensure the output clearly separates HLD and LLD content:
   - HLD covers context, containers, major components, data flow, deployment, and cross-cutting concerns
   - LLD covers API definitions, data models, storage structures, detailed flows, logic rules, error handling, configuration, and observability implementation
7. Use the C4 model as the architecture backbone:
   - `2.1 系统上下文` maps to C4 Level 1
   - `2.2 容器架构` maps to C4 Level 2
   - `2.3 组件设计` maps to C4 Level 3
   - Write all C4 diagrams in Mermaid format rather than PlantUML or plain text blocks
   - Prefer Mermaid `flowchart` for C4-style context, container, and component diagrams, using subgraphs, clear node labels, and labeled edges to express system boundaries and responsibilities
   - Each C4 diagram must reflect the real module split, upstream/downstream dependencies, and key interactions instead of generic placeholders
8. Add Mermaid diagrams for key design areas when they improve implementation clarity:
   - Use `sequenceDiagram` for cross-role interaction timing, request/response order, and exception branches
   - Use `flowchart` for business decision flow, orchestration logic, and branching control paths
   - Use `stateDiagram-v2` for lifecycle-heavy modules such as workflow state, order state, task state, or approval state
   - Use `erDiagram` for core data entities and relationships when the data model is non-trivial
   - Use `journey` only when user-role experience stages are essential to understanding the requirement
   - Use `mindmap` only for compact capability decomposition or module responsibility breakdown when that is clearer than a list
9. Choose diagram types based on the module's nature instead of forcing one diagram style everywhere.
10. Keep the design implementable enough that engineering can build the core capability directly from the document.

### Phase 3: Validate, Improve, And Save

1. Review the document section by section against the template.
2. Remove every placeholder or example marker such as `【功能名称】`, `[目标1]`, `YYYY-MM-DD`, `[例如:]`, `[功能1]`, `[不包含1]`, `[待补充]`, and similar text.
3. Verify that architecture decisions, terminology, and process names are consistent throughout the document.
4. Verify that each major design item traces back to PRD content, user answers, or explicitly labeled assumptions.
5. Verify that the design is actionable enough for engineering implementation and cross-functional review.
6. Tighten vague wording. Replace terms such as `可能`, `大概`, `尽量`, or similarly ambiguous phrases with concrete statements.
7. Save the improved version to the same file path.

## Questioning Rules

- Ask only for information that materially improves the design.
- Tie each question to a missing template section or an implementation decision that cannot be made safely yet.
- Prefer questions that produce concrete constraints, examples, thresholds, volumes, roles, interfaces, or failure scenarios.
- When the PRD describes a feature but not the system boundary, ask which systems own which responsibilities.
- When the PRD gives a business flow but not technical responsibilities, ask about service boundaries, data ownership, and integration points.
- When the PRD lacks non-functional requirements, ask for baseline load, latency target, availability target, security requirements, audit needs, and observability expectations.
- When the user cannot provide precise data, ask for the best available proxy and label it clearly in the document.

## Writing Rules

- Keep the template headings, numbering, and major section order intact.
- Preserve markdown readability and concise phrasing.
- Use structured lists and tables when they make relationships clearer.
- Keep architecture-level content and implementation-level content in their proper sections. Do not mix them.
- Use consistent terms for users, systems, services, modules, data objects, and environments.
- When diagrams are used, render them with valid Mermaid syntax in fenced code blocks such as ```mermaid```.
- Do not insert decorative or redundant diagrams. Each Mermaid diagram must answer a concrete design question and align with the surrounding section content.
- Select Mermaid diagram types according to the design intent:
  - architecture boundaries and dependencies: `flowchart`
  - interaction timing and responsibility handoff: `sequenceDiagram`
  - lifecycle and status transitions: `stateDiagram-v2`
  - entity relationships and storage structure: `erDiagram`
  - step-by-step operational or exception handling flow: `flowchart`
- For complex modules, combine text with one or more complementary Mermaid diagrams when necessary, but avoid repeating the same information in multiple formats.
- In each diagram, use concrete Chinese labels for business meaning and append technical identifiers only when they improve implementation clarity.
- For design decisions and risks, include the reason or trade-off rather than only naming the item.
- For APIs and data models, provide enough detail for direct implementation discussion.
- For data flow and detailed flow, describe normal flow, decision points, and exception flow where relevant.
- For release and rollback, describe concrete steps rather than generic statements.

## Quality Bar

Enforce these principles in every output:

- Layered clearly: separate architecture design from implementation detail.
- Implementable: provide enough detail for developers to implement core functions.
- Consistent: keep structure, terms, and logic aligned across sections.
- Traceable: connect design content back to PRD requirements and clarified assumptions.
- Concise and clear: prefer direct, specific wording over long explanations.
- Collaboration-oriented: use neutral wording that supports review and discussion.
- Diagram-driven where helpful: use Mermaid diagrams to reduce ambiguity in architecture, flow, state, and data design.
- Diagram fit matters: choose the Mermaid diagram type that best matches each module's design problem instead of applying a single chart style mechanically.

## Template Handling

- Always load `./resources/design-template.md` before drafting.
- Treat the template as mandatory output scaffolding.
- Update dates to the current working date when the user does not provide one.
- Replace placeholder owners, status, examples, and sample links with real values or `待确认` when the source information is missing.
- If the PRD path is known, update the related PRD link in the design document.
- Do not leave emoji placeholders, sample arrows, or example identifiers unchanged when the real design can be stated more precisely.

## Output Pattern

When responding after writing the file:

1. State the saved file path.
2. Summarize the requirement name and major architecture choices.
3. Call out key assumptions or unresolved items that still require stakeholder confirmation.
