---
name: grimoire-slice
description: Decompose a spec or conversation into vertical-slice tickets — each cutting through every architectural layer, independently demonstrable, sized for a single context window.
disable-model-invocation: true
---

# Purpose

Convert a requirement — from a spec file, user conversation, or both — into a folder of vertical-slice tickets in `.grimoire/ticket/`.

A vertical slice is a narrow but complete path through every architectural layer of the project. Every slice is independently demonstrable when complete.

# Scope

This skill writes to `.grimoire/ticket/NNNN-title/`.

This skill does NOT:
- Write specs (use grimoire-spec)
- Record domain concepts or ADRs (use grimoire-record)
- Interrogate the user for requirements (use grimoire-clarify)
- Implement code

Completion: A ticket folder exists with a relationship file and sub-tickets. Every slice cuts through all discovered layers. Every slice is independently demonstrable.

---

# Workflow

## 1. Pre-flight

Verify `.grimoire/` exists. If not, stop — tell the user to run grimoire-init first.

Verify `.grimoire/ticket/` exists. If not, create it.

Determine the input source:

- If the user provided a spec path (e.g., `.grimoire/spec/0001-xxx.md`), use that spec. Derive the folder name `NNNN-title` from the spec filename.
- If a spec was just generated in this conversation (via grimoire-spec), use that spec and its sequence number.
- If neither, extract requirements directly from the conversation. Derive a short kebab-case feature name from the conversation. Do not ask the user. Assign the next available sequence number from `.grimoire/ticket/`.

Completion: `.grimoire/` exists. Input source determined. Target folder name known. `.grimoire/ticket/NNNN-title/` created or confirmed writable.

---

## 2. Load constraints

Read every source that constrains ticket decomposition:

1. **Requirement source**:
   - If a spec file was identified in step 1: read it — understand the requirement, solution, seams, E2E tests, decisions, test plan, out of scope.
   - If extracting from conversation: distill the user's stated goal, constraints, and any decisions already discussed. Treat the conversation as the authoritative requirement description.
2. `.grimoire/CONTEXT.md` — domain terms. Read domain split files if the index references them.
3. `.grimoire/adr/*.md` — every ADR. Tickets must not violate architecture decisions.
4. Repository structure — explore the project tree. Understand existing modules, directory conventions, and integration surfaces.

Completion: Requirement fully understood. Domain context loaded. Every ADR checked. Repository structure known.

---

## 3. Discover layers

A layer is a distinct architectural stratum that every vertical slice must cross. Layers are not assumed — they are discovered from the project.

Discovery process:

1. From the repository structure (step 2), identify the project's **architectural strata** — the distinct concerns that sit between raw data and observable outcome. Examples:
   - Web app: data store → service/business logic → API/transport → UI/rendering → verification
   - CLI tool: data model → core logic → command interface → output formatting → verification
   - Library/SDK: types → implementation → public API surface → documentation → verification
   - Embedded: HAL → driver → application logic → physical output → verification
   - Data pipeline: source schema → transform → storage → query interface → verification

2. Name each layer with a term the project already uses (infer from directory names, package names, or ADR terminology).

3. The discovered layer list becomes the canonical layer checklist for every ticket in this decomposition. Do not ask the user for confirmation.

Completion: Every layer has a name drawn from project terminology. The list has at least 2 layers.

---

## 4. Identify pre-refactoring

Pre-refactoring is work that must complete before any vertical slice can be demonstrated.

Apply the test to each piece of work: "Can any slice be demonstrated without this work?"

- If no: it is pre-refactoring.
- If yes: it belongs in the slice that needs it.

Common pre-refactoring patterns (project-type-agnostic):
- Foundation that every slice reads or writes (shared data structure, base types, core abstraction)
- Cross-cutting infrastructure that no single slice owns (error handling framework, configuration loader, logging setup)
- Dependency setup that the whole feature requires (new library, toolchain addition, environment provisioning)
- Contract or interface definition that multiple slices implement or consume

Pre-refactoring becomes the first ticket (T0001). Every other slice depends on it.

Pre-refactoring differs from vertical slices: it has no user-visible or externally observable outcome. It is verified by tests passing and by the fact that subsequent slices work.

See [references/pre-refactoring-guide.md](./references/pre-refactoring-guide.md).

Completion: Pre-refactoring ticket identified or explicitly declared unnecessary. The pre-refactoring ticket blocks every other ticket.

---

## 5. Decompose into vertical slices

A vertical slice must satisfy all of:

1. **All layers**: touches every layer discovered in step 3 — a complete path from data/input to observable outcome.
2. **Independent demonstration**: when the slice is complete, the outcome can be observed and verified without depending on incomplete slices.
3. **Context-window fit**: a single agent session can implement the entire slice without context overflow.
4. **Narrow path**: the slice does exactly one observable thing. No branching.

Decomposition technique:

1. Start from user-visible or externally observable scenarios. If a spec exists, use its E2E tests. If from conversation, derive scenarios by asking: "What would an external observer see or measure at each step?"
2. If a scenario is too large for one context window, split by: happy path vs. error path; simple input vs. edge case; create vs. update vs. delete; core behavior vs. feedback/polish.
3. If splitting leaves cross-cutting work, promote that work to pre-refactoring.
4. For each slice, list every discovered layer and what changes in it.

See [references/slicing-rules.md](./references/slicing-rules.md).

Completion: Every slice satisfies all four criteria. Layer coverage (against the confirmed layer list) is explicit for every slice. No slice exceeds a context window.

---

## 6. Map dependencies

Determine the relationship between every pair of tickets:

- **Blocks** (A → B): B cannot start until A is complete.
- **Parallel** (A ∥ B): A and B share no files and no runtime contracts. They can be worked on simultaneously.
- **Independent** (A ⊥ B): No constraint either way. Default to parallel unless blocking is proven.

Dependency mapping rules:

- Pre-refactoring blocks every other ticket.
- If slice A creates a module, endpoint, or interface that slice B consumes, A blocks B.
- If two slices touch the same file, they are NOT parallel — one must block the other or they must merge.
- If two slices share a runtime contract (data format, interface signature, config schema), the contract producer blocks the consumer.

Document the graph in the relationship file.

See [references/relationship-file-template.md](./references/relationship-file-template.md).

Completion: Every ticket has its blockers listed. Every blocking relationship has a reason. Parallel groups are identified. Graph is acyclic.

---

## 7. Present decomposition

Present the complete decomposition to the user before writing files. Show:

1. Confirmed layer list (from step 3).
2. Pre-refactoring ticket (if any) — what it covers and why it blocks everything.
3. Slice list with one-line descriptions.
4. Dependency graph — blocking arrows and parallel groups.
5. Recommended implementation order.

Ask the user only one question: is the split appropriate? Do not ask about layers, naming, or any other details. The user may respond with adjustments (merge, split, reorder, dependency changes).

Loop back to the relevant step if changes are requested.

Completion: User confirms the split is appropriate. All adjustments are incorporated.

---

## 8. Generate ticket folder

Create the folder structure:

```
.grimoire/ticket/NNNN-title/
├── README.md                (relationship file)
├── T0001-ticket-name.md
├── T0002-ticket-name.md
└── ...
```

### Relationship file (README.md)

Contains:
- Overview of the feature
- Confirmed layer list (from step 3)
- Dependency graph with blocking arrows and parallel groups
- Ticket index — relative path, title, one-line summary for each sub-ticket
- Recommended implementation order

### Sub-ticket files (TNNNN-title.md)

Every sub-ticket contains:

1. **Goal** — one sentence. What observable outcome does this ticket produce?
2. **Layers** — explicit checklist of what changes in each confirmed layer. If a layer has no work, state why.
3. **Approach** — how to implement. Specific enough to guide execution, not a line-by-line script.
4. **Blocked by** — list of ticket IDs that must complete before this one. Empty if none.
5. **Blocks** — list of ticket IDs that depend on this one. Empty if none.
6. **Acceptance** — observable criteria that verify completion. Every criterion must be testable.
7. **Out of Scope** — what this ticket explicitly does NOT do, even if related.

See [references/vertical-slice-template.md](./references/vertical-slice-template.md) for the full template and example.

Completion: README.md exists. Every sub-ticket file exists. Every sub-ticket has all seven sections filled.

---

## 9. Validate

Run validation checks on the complete ticket folder:

1. **Layer coverage**: every sub-ticket's Layers checklist includes every layer confirmed in step 3. If a layer is absent, the ticket must justify why.
2. **Independence**: every sub-ticket can be demonstrated when its blockers are resolved.
3. **Dependency consistency**: every `Blocked by` has a matching `Blocks` in the referenced ticket, and vice versa.
4. **Context fit**: no sub-ticket describes more work than a single context window can handle.
5. **ADR compliance**: no sub-ticket contradicts an architecture decision recorded in `.grimoire/adr/`.

If any check fails, fix the ticket and re-validate.

Completion: All five checks pass. Every failure is resolved.

---

# Rules

- Never write tickets before user confirms the split is appropriate.
- Layers are discovered from the project, not assumed. Never hardcode layer names. Do not ask the user to confirm layers.
- Pre-refactoring first. Every slice that blocks others must complete before those others start.
- One observable outcome per ticket. If a ticket has two independent outcomes, split it.
- Every ticket must touch all discovered layers. If a layer has no work, state why explicitly.
- Tickets describe what and how. The spec describes why. Do not duplicate spec content in tickets — reference the spec.
- All tickets in a folder belong to the same requirement. Do not mix requirements in one folder.
- Dependency graph must be acyclic. Circular dependencies indicate a decomposition error — merge the tickets.
- No ticket may violate an ADR. If a ticket requires violating an ADR, flag the conflict in the ticket's Out of Scope or the README.
