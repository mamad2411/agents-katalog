---
name: specspine-grow
description: Create or evolve intended architecture in a linked Markdown SpecSpine from explicit user intent and existing specifications. Use for greenfield initialization, accepted architectural changes, impact analysis, and specification splitting, merging, renaming, or linking. Do not use for repository discovery (specspine-map), integrity review (specspine-doctor), context extraction, implementation, or code/spec conformance.
---

# SpecSpine Grow

Maintain a lightweight network of architectural specifications. Record stable
responsibilities, boundaries, relationships, decisions, constraints, and
relevant uncertainty without turning the Spine into a feature or implementation
workflow.

## Resources

- Read [references/spec-semantics.md](references/spec-semantics.md) when adding,
  reclassifying, conflicting, or resolving an architectural claim.
- Read [references/spec-format.md](references/spec-format.md) before creating or
  restructuring specifications. It is the canonical guide to document content,
  organization, semantic IDs, decomposition, and terminal detail.
- Read [references/examples.md](references/examples.md) when the right
  specification boundary is unclear.
- When creating files, start from the templates under `assets/templates/` and
  omit empty sections.

## Authority and scope

Use the current user request and files inside the resolved `<spine-root>` as the
only project architecture sources. Bundled resources define procedure and
format, not project facts.

Do not inspect project-specific code, configuration, tests, documentation, or
external systems unless the user explicitly authorizes them. Authorized
external evidence remains `Observed` or `Inferred` unless the user accepts it
as architectural intent; it never silently overrides a decision or constraint.
For an uninitialized Spine, do not list, search, or read any existing project
file outside `<spine-root>`, including a root README, even to seek context.
Derive only the smallest useful starting structure from the request.

Grow owns organization and intentional evolution of the specification network.
It does not:

- discover repository architecture or verify code/spec conformance;
- implement source changes;
- create feature requirements, acceptance criteria, plans, tasks, or status;
- decide product or architecture choices for the user.

Use `specspine-map` for repository discovery and drift, `specspine-doctor` for
health review, and `specspine-extract` for a downstream context handoff. Grow
must remain usable without those skills.

## Workflow

1. Resolve `<spine-root>` as defined by `references/spec-format.md`; absent an
   explicit user or project configuration, this is exactly `specspine`
   relative to the current working directory, never the repository root.
   Test for its `README.md` without listing the project. If present, read it
   and follow only relevant links. If absent, immediately initialize from the
   request; do not run any other project discovery or read any other project
   path.
2. Classify the operation: initialize, refine, split, merge, rename, or link.
   Identify the canonical owner, specifications whose architectural meaning or
   boundaries change, and context needed only for understanding.
   For refinement, perform the terminal-depth check immediately after reading
   the index and relevant specification. If the request explicitly adds no
   responsibility, boundary, decision, constraint, or open question and asks
   only for function-by-function flows, internal data structures, SDK calls,
   pseudocode, configuration fields, or similar implementation instructions,
   stop without editing. Do not inspect implementation evidence or load
   additional format resources merely to elaborate the refusal; explain that
   the requested material belongs in the downstream implementation workflow.
3. Reuse an existing owner when possible. Create or extract a specification
   only for an independently meaningful or evolving responsibility, boundary,
   behavior, or decision set; never because a file is long or a feature is new.
4. Treat an explicit in-scope operation or architectural decision as approval.
   Approval does not override Grow's scope or terminal-detail boundary. Apply
   navigation, evidence-only, and clearly meaning-preserving edits directly.
   Ask the user only before introducing unapproved normative intent, resolving
   a conflict or blocking question, choosing among plausible owners, or making
   an ambiguous agent-initiated restructure. State the affected files, reason,
   and unresolved choice without prescribing a rigid response format.
5. Apply the smallest coherent change. Preserve unrelated content, useful
   relative links, reachability from the index, and one canonical home per
   concept. Use summaries and links instead of duplicate definitions. Update
   the index only when top-level navigation or system-wide intent changes.
6. Report changed files, structural choices, and unresolved architectural
   questions concisely.

## Operation guidance

### Initialize

Create the index and the smallest useful set of top-level concept
specifications. Do not anticipate the full system or invent repository
structure. Preserve important unknowns as open questions. Omit semantic IDs
unless the request already establishes a concrete cross-document or downstream
reference that needs one.

### Refine

Preserve an existing responsibility unless the user changes it. Record the
smallest accepted architectural meaning and modify only owners whose behavior
or boundaries change. Treat related specifications needed only for context as
read-only. A dependency's participation, session use, or configuration need
does not by itself change its specification. Modify a related owner only when
the request supplies new durable architectural intent belonging there; report
implementation prerequisites and speculative questions instead.

Stop when the specification already captures the architectural detail defined
by `references/spec-format.md` and the request adds no new intent. Do not add
coding-manual material merely to make the document deeper. An explicit request
for implementation-level content does not turn that content into architectural
intent or authorize storing it in the Spine. Make no changes and explain which
requested detail belongs downstream.

### Split, merge, or rename

For a split, move the independently owned content and update links; retain the
broader document only when it remains a useful overview. For a merge, preserve
unique meaning in the agreed canonical owner. For any move or rename, update
incoming links and preserve externally referenced semantic IDs as required by
`references/spec-format.md`.

## Invariants

- Modify only files inside `<spine-root>`.
- Preserve the distinction between decisions, constraints, observations,
  inferences, and open questions defined by `references/spec-semantics.md`.
- Never imply that documented intent is implemented or conformant.
- Never silently resolve uncertainty, conflicts, or ownership ambiguity.
- Keep specifications architectural, linked, concise, and independent of a
  custom parser or implementation workflow.
