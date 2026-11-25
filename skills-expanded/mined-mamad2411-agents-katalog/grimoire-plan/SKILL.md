---
name: grimoire-plan
description: Generate a code-level implementation plan from a ticket or conversation, covering type design, pseudo-code steps, edge cases, and test strategy.
disable-model-invocation: true
---

# Purpose

Generate a code-level implementation plan from a ticket, spec, or conversation. The plan is a temporary design artifact — it documents how to implement, not what or why.

# Scope

This skill writes HTML plans to `.grimoire/plans/`.

This skill does NOT:
- Write specs (use grimoire-spec)
- Decompose into tickets (use grimoire-slice)
- Implement code
- Record domain concepts or ADRs (use grimoire-record)

Completion: A plan file exists at `.grimoire/plans/NNNN-title.html` with all six sections filled.

---

# Workflow

## 1. Pre-flight

Verify `.grimoire/` exists. If not, stop — tell the user to run grimoire-init first.

Verify `.grimoire/plans/` exists. If not, create it.

Determine the input source:

- If the user provided a ticket path (e.g., `.grimoire/ticket/0001-xxx/T0001-xxx.md`), use that ticket.
- If the user provided a spec path (e.g., `.grimoire/spec/0001-xxx.md`), use that spec.
- If neither, treat the conversation as the input. Derive a short kebab-case title from the user's goal. Do not ask.

Assign the next available sequence number from `.grimoire/plans/`. Naming: `NNNN-title.html` (zero-padded).

Completion: `.grimoire/plans/` exists. Input source determined. Plan path known.

---

## 2. Load context

Read every source that constrains the plan:

1. The input source (ticket, spec, or conversation goal).
2. `.grimoire/CONTEXT.md` — domain terms. Include domain split files if the index references them.
3. `.grimoire/adr/*.md` — every ADR. The plan must not violate architecture decisions.
4. Repository structure — explore relevant directories to understand existing types, modules, and conventions. Focus on files the ticket or spec references.

Completion: Input fully understood. Domain terms loaded. Every ADR checked. Relevant repo structure known.

---

## 3. Analyze type design

Identify every type that must change or be created, following the design principles in [references/design-principles.md](./references/design-principles.md).

For each type, record:

- **Action**: Modify or Create.
- **Concept**: What stable concept does this type represent? One sentence.
- **Responsibility**: What rules and behavior does it own?
- **Relationships**: What does it compose, implement, or communicate with?
- **Rationale**: Why this boundary? If modifying an existing type, why extend rather than split? If creating, why split rather than extend?

Apply the litmus test from design principles: "Can this type exist independently, change independently, and be tested independently?"

Prioritize minimal changes. Prefer extending existing types over creating new ones when the change belongs to the same concept. Prefer composition over inheritance.

**Produce a type relationship diagram** using Mermaid classDiagram syntax (see
[references/diagram-guide.md](./references/diagram-guide.md)). The diagram must:

- Show every type from step 3.
- Show relationships: composition (has-a), implementation (can-do), and usage
  dependencies.
- Show key fields and methods relevant to the plan for each type.

Completion: Every affected type has a record with all five fields. The rationale
for every boundary decision is explicit. No type owns more than one concept. A
Mermaid classDiagram exists showing all types and their relationships.

---

## 4. Draft implementation steps

Describe each implementation action as a numbered concrete step. Each step names the specific action:

- "Modify method `X` to ..."
- "Add method `Y` to type `Z`"
- "Add class `W` implementing interface `V`"
- "Remove field `U` from type `T`"

For steps that involve non-trivial logic, follow the action description with pseudo-code. For mechanical changes (add a field, rename a parameter, delegate to an existing method), the action description alone is sufficient.

Each step must also state the observable outcome. Group steps by type or feature area. Order by dependency: foundational types first, integration points last.

Completion: Every step names a concrete action on a specific type or file. Steps with logic changes include pseudo-code. Every step has an observable outcome.

---

## 5. Identify edge cases

List only edge cases that meet the criteria in [references/edge-case-guide.md](./references/edge-case-guide.md):

- The edge case has a non-zero probability in real usage.
- The edge case would produce incorrect behavior or a crash if missed.
- The edge case is not already covered by normal error handling patterns in the codebase.

For each edge case, record: the condition, the expected behavior, and which step (from step 4) must handle it.

Do not list:
- Null/undefined checks unless the value crosses a trust boundary.
- "What if the database is down" unless the plan specifically touches connection handling.
- Generic validation that the language's type system already prevents.

Completion: Every listed edge case has a condition, expected behavior, and owning step. No generic or zero-probability cases are listed.

---

## 6. Design test strategy

Describe how to unit-test the implementation. For each type identified in step 3:

- What observable behavior must be verified?
- What dependencies need mocking/stubbing?
- What input variations produce qualitatively different outcomes?

Prefer testing the type's public contract, not internal implementation.

Completion: Every type from step 3 has a test approach. Mocking boundaries are identified. Test cases cover the edge cases from step 5.

---

## 7. Assemble and write

Use the HTML template in [references/html-template.md](./references/html-template.md).

Fill each placeholder with the content from steps 3–6:

1. **Type Design** — from step 3. Fill `MODIFIED_TYPES_ROWS`, `NEW_TYPES_ROWS`, `DESIGN_DECISIONS`.
2. **Type Relationship Diagram** — from step 3. Paste the raw Mermaid classDiagram body into `MERMAID_DIAGRAM` (no outer ```mermaid fence).
3. **Implementation Steps** — from step 4. Use the `.step` block structure for each step.
4. **Edge Cases** — from step 5. Fill `EDGE_CASES_ROWS`.
5. **Test Strategy** — from step 6. Use the test strategy block structure for each type.
6. **Affected Files** — list every file the plan touches, with action (create/modify) and which step references it. Fill `AFFECTED_FILES_ROWS`.

Write to `.grimoire/plans/NNNN-title.html`.

Verify the file exists, is valid HTML, and all six sections are present.

Completion: HTML plan file exists. All sections present. Sequence number is correct.

---

# Rules

- One plan per ticket or conversation goal. Do not merge unrelated work.
- Never violate an existing ADR. If the input requires it, flag the conflict in the plan and stop.
- Plans are temporary design artifacts. They guide implementation, not archive it. Do not maintain plans after the implementation is complete.
- Use the HTML template structure. Do not improvise sections or styling.
- Design principles are in references. SKILL.md controls workflow only.
