---
name: pwrl-plan-design
description: "Create technical design and implementation unit decomposition for planning workflow."
argument-hint: "[scoped context + research findings]"
---

# pwrl-plan-design — Design & Unit Decomposition

**Purpose:** Third step in the planning workflow. Accepts scoped context from `pwrl-plan-scope` (S2) and research findings from `pwrl-plan-research` (S3). Breaks the work into stable, numbered implementation units (U1, U2, … UX), optionally generates Mermaid diagrams for complex workflows, and produces a complexity hint for tier selection.

## Interaction Method

- Use the platform's `ask_user_question` extension for guiding unit decomposition.
- Ask one question at a time. Present each unit for confirmation before proceeding.
- Use multiple-choice questions when possible (e.g., "How many phases does this work involve?").
- If input is missing context or research, ask: "Please provide scoped context (from pwrl-plan-scope) and research findings (from pwrl-plan-research) first."

## Input

This skill expects two inputs:

1. **Scoped context** from `pwrl-plan-scope` (S2) — problem, criteria, domain, learnings
2. **Research findings** from `pwrl-plan-research` (S3) — patterns, tech stack, risk assessment, constraints

If inputs are missing, search for recent `.scope` and `.research` files in `docs/plans/.scope/` and `docs/plans/.research/`, or prompt the user to run the prerequisite skills.

## Output: Implementation Units

After completing the workflow, produce an implementation units block:

````yaml
design-id: YYYY-MM-DD-NNN-design
status: complete

# Implementation Units

## Complexity Hint: fast | standard | deep

## Diagram (Optional)
```mermaid
sequenceDiagram
    ...
````

```

## Units

### U1: [Unit Name]
- **Scope:** [What this unit accomplishes]
- **Dependencies:** [None | U1, U2]
- **Files Affected:**
  - Create: `path/to/new/file`
  - Modify: `path/to/existing/file`
  - Test: `path/to/test/file`
- **Approach:** [Brief technical approach description]
- **Acceptance Criteria:**
  - [Specific condition for completion]
  - [Specific condition for completion]

### U2: [Unit Name]
- **Scope:** [...]
- **Dependencies:** [e.g., U1]
- **Files Affected:** [...]
- **Approach:** [...]
- **Acceptance Criteria:** [...]
```

The units object is passed to `pwrl-plan-generate` (S5) for plan rendering.

## Workflow

### Step 1: Understand Context and Research

1. Read the scoped context: problem frame, success criteria, domain.
2. Read the research findings: patterns, tech stack, risk level, constraints.
3. If the task is non-software (`domain: non-software`), note that design units will be generic (not code-focused).
4. Ask user: "I understand this task involves [problem summary]. The research found [findings summary]. Shall we proceed to break this into implementation units?"

### Step 2: Determine Phases and Unit Count

1. Based on the task scope, estimate the number of implementation units:
   - **Small (1-3 units):** Single-phase, straightforward work
   - **Medium (4-8 units):** Multi-phase, moderate complexity
   - **Large (9-15 units):** Cross-cutting work, likely phased
   - **Very large (16+ units):** Suggest splitting into sub-plans
2. Ask user: "Based on the scope, I estimate this needs approximately [N] implementation units. Does that sound right?"
   - Options: Yes, No (adjust up/down), split into sub-plans
3. If user wants to adjust, iterate until count is agreed.

### Step 3: Implement U-ID Generator

Assign stable, sequential Unit Identifiers (U1, U2, U3, ...) to each unit. For the complete implementation pattern, stability rules (never reassign retired IDs), edge cases (deletion, merging, splitting), and best practices, see **[u-id-generator.md](references/u-id-generator.md)**.

### Step 4: Create Each Unit

For each unit, guide the user through definition. Use `ask_user_question` to collect:

1. **Name:** "What's a short name for unit U{N}?"
2. **Scope:** "What does this unit accomplish?"
3. **Dependencies:** "Does this unit depend on any previous units?" (auto-populate from sequence unless user specifies otherwise)
4. **Files:**
   - Ask for files to create, modify, and test
   - Files must be repository-relative (e.g., `src/main.js`, not `/home/user/project/src/main.js`)
5. **Approach:** "Describe the technical approach for this unit (directional, not code)."
6. **Acceptance Criteria:** Collect 1-3 specific conditions for completion.

Present the completed unit to the user for confirmation before creating the next unit.

### Step 5: Assign Dependencies

After all units are defined:

1. Review dependency chain.
2. If user specified custom dependencies, validate they form a DAG (no circular dependencies).
3. If cycles found, ask user to resolve.
4. Auto-assign sequential dependency if user didn't specify: U1 depends on None, U2 on U1, U3 on U2, etc.

### Step 6: Complexity Hinting

Determine the tier hint based on unit count and complexity:

| Unit Count | Risk Level | Tier Hint |
| ---------- | ---------- | --------- |
| 1-3        | LOW        | Fast      |
| 1-3        | HIGH       | Standard  |
| 4-8        | any        | Standard  |
| 9+         | any        | Deep      |
| any        | HIGH + 9+  | Deep      |

The hint is advisory. The generate skill (S5) uses it for template selection. The user can override in S5.

### Step 7: Optional Mermaid Diagram

Detect if a diagram would add clarity (5+ units, complex interdependencies, high-risk workflow). For decision criteria, diagram type selection (sequence, state, flowchart), user prompts, and embedding instructions, see **[mermaid-diagram-guide.md](references/mermaid-diagram-guide.md)**.

### Step 8: Present and Confirm

1. Present the complete units object to the user via `ask_user_question`.
2. Ask: "Does this design look correct? Should I proceed to plan generation?"
3. If confirmed: Return the units object.
4. If corrections needed: Allow user to add, remove, or modify units.
   - Remember: U-IDs never renumber. Deleted IDs are retired.
5. **Do not proceed to plan generation** — this skill only produces design.

## Edge Cases

Seven edge cases commonly encountered during design: non-software domains, user adjusting unit count, retired U-IDs, circular dependencies, user uncertainty about approach, very large plans, and declined diagrams. For handling strategies, decision trees, and examples, see **[edge-cases.md](references/edge-cases.md)**.

## State Passing (to S5: pwrl-plan-generate)

Implementation units are passed to `pwrl-plan-generate` in markdown format with YAML frontmatter. Downstream skills read it from memory or from `docs/plans/.design/YYYY-MM-DD-NNN-design.md`. For detailed schema documentation, field reference, storage conventions, and versioning rules, see **[state-schema.md](references/state-schema.md)**.

## References

- **Source:** Phase 3 of `pwrl-plan/SKILL.md`
- **Input:** Scoped context from `pwrl-plan-scope` (S2) + Research findings from `pwrl-plan-research` (S3)
- **Downstream:** `pwrl-plan-generate` (S5) — receives units and complexity hint
- **Integration:** `ask_user_question` extension for all unit definition steps
- **Unit template:** See inline examples in this file; no separate reference file needed
