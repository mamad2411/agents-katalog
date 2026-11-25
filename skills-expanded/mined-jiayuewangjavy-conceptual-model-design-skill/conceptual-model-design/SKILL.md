---
name: conceptual-model-design-skill
description: Turn PRDs, user research, workflows, policies, screenshots, and existing product documentation into an explicit, evidence-linked conceptual model and interactive review workspace before generating information architecture, navigation, or page architecture. Use when a product designer, UX designer, design engineer, researcher, or product team needs to identify or audit actors, objects, actions, attributes, relationships, states, rules, records, assumptions, conflicts, and unresolved structural decisions for a complex B2B or multi-role product. Also use when reviewing whether an existing product's navigation and pages reflect its underlying product model.
---

# Conceptual Model Design

Turn product evidence into a reviewable product model before creating interface
structure.

## Core principle

Turn the AI's hidden, temporary, and non-inspectable inference into an explicit,
discussable, editable, and traceable design artifact.

Do not jump from source documents directly to a polished prototype. First expose
the model, its evidence, its assumptions, and the decisions that could change
the structure. Generate IA, navigation, and page architecture only after the
required review is complete.

## Operating contract

- Treat every extracted concept as a proposal until reviewed.
- Analyze all supplied sources together. Do not privilege the PRD when research,
  policy, workflow, or existing-product evidence contradicts it.
- Preserve source provenance for every material concept and decision.
- Separate objects from actions. A durable thing with identity or lifecycle is
  an object; a verb that changes or queries state is an action.
- Distinguish source facts, reasonable inferences, conflicts, and missing
  information.
- Never invent business rules, permissions, states, cardinality, ownership, or
  lifecycle behavior.
- Keep required decisions small and structural. Do not ask the user to confirm
  facts already supported consistently by the evidence.
- Allow concept create, read, update, and delete operations during review.
- Gate each stage. Do not generate final structure while concepts or required
  decisions remain unresolved.
- Make generated navigation and pages traceable to confirmed model elements.
- Use the interactive workspace as the primary deliverable, not a long chat
  response.
- Match the user's language unless another output language is requested.

## Inputs

Accept one or more of:

- PRDs and feature briefs
- User research, interview notes, journey maps, or service blueprints
- Business rules, policies, permission matrices, or compliance material
- Workflow diagrams and process documentation
- Existing navigation, screenshots, prototypes, or product URLs
- Technical constraints and relevant domain documentation

One source is enough to begin. Explain that additional sources improve conflict
detection and confidence; do not require every possible source.

Record the task name, product boundary, intended users, source list, unavailable
materials, and any explicit scope limits.

## Required references

Read [conceptual-model-method.md](references/conceptual-model-method.md) before
extracting or classifying concepts.

Read [data-schema.md](references/data-schema.md) before creating workspace data.

Read [workspace-delivery.md](references/workspace-delivery.md) before building
or presenting the interactive workspace.

Read [downstream-generation.md](references/downstream-generation.md) only after
the model review and structural decisions are complete.

## Workflow

### 1. Inventory and normalize the evidence

List every supplied or reachable source. Extract relevant terminology,
definitions, user roles, nouns, verbs, states, constraints, and contradictions.
Preserve the source wording where naming disagreements may matter.

Do not silently collapse two terms into one concept. Record the proposed
normalization and evidence for the merge.

### 2. Draft the conceptual model

Identify:

- Actors
- Objects
- Actions
- Attributes
- Object-to-object relationships
- Actor-action-object flows
- States and lifecycle transitions
- Rules, policies, and durable records

For every concept, include a definition, kind, proposed status, attributes,
relationships, evidence, and a review note when needed.

Use only these review statuses:

- `confirmed`: supported and accepted
- `change`: useful concept that needs correction
- `reject`: excluded from the intended product model
- `unknown`: unresolved proposal

### 3. Identify conflicts and structural questions

Create a decision only when different answers would materially change object
boundaries, ownership, relationships, permissions, lifecycle, navigation, or
page architecture.

For each decision, provide:

- The unresolved question
- Why the evidence cannot settle it
- The exact evidence or conflict
- Two or more mutually exclusive options
- The structural consequence of each option

Do not choose for the user when the source evidence is insufficient.

### 4. Build the review workspace

Create `model-data.json` using
[data-schema.md](references/data-schema.md). Then run:

```text
node <skill-directory>/scripts/build_workspace.mjs model-data.json --output conceptual-model-workspace
```

Open `conceptual-model-workspace/index.html` and verify:

- The task appears on the landing-page task list.
- Every supplied source appears in the source inventory.
- Actors, actions, objects, rules, and records are classified correctly.
- Relationship lines connect the intended concepts.
- Hovering a concept clearly de-emphasizes unrelated concepts.
- Clicking a concept opens a focused, scrollable dialog.
- Concept add, edit, review, and delete actions work.
- Required decisions use plain radio groups.
- Future steps remain locked until the current step is complete.
- The left vertical step navigation and fixed Back/Next footer remain visible
  while the main content scrolls.
- Navigation, IA, and page previews render as designed, interactive views.

If file generation or browser preview is unavailable, state the limitation. Do
not claim the interactive workspace was delivered.

### 5. Let the user review inside the workspace

Ask the user to work through the visible stages rather than answering a copied
continuation prompt in chat.

When browser control is available, read the reviewed state from:

```text
window.__conceptualModelWorkspace.getState()
```

When direct browser-state access is unavailable, ask the user to return the
reviewed model data or confirm the changed concepts and decisions. Do not infer
that an untouched draft was approved.

### 6. Generate downstream structure

Proceed only when:

- Every included concept has a non-`unknown` status.
- Every required structural decision has an answer.
- Rejected concepts are excluded.
- Changed concepts contain the user's corrected definition or relationship.

Then follow [downstream-generation.md](references/downstream-generation.md) to
produce:

- Information architecture
- Primary and contextual navigation
- Page and route inventory
- Page architecture for key workflows
- Traceability from each generated surface to the confirmed model

### 7. Verify the artifact

Run:

```text
node <skill-directory>/scripts/build_workspace.mjs model-data.json --output conceptual-model-workspace --force
```

Open the result and test the complete gated flow. Check responsive behavior,
keyboard focus, modal scrolling, fixed footer behavior, and all primary
interactions. Never treat file creation alone as visual verification.

## Existing-product audit mode

When the user supplies an existing product:

1. Infer the apparent conceptual model from the product and supporting sources.
2. Separate observed UI behavior from inferred domain structure.
3. Compare navigation, labels, pages, and workflows with the inferred model.
4. Identify duplicate concepts, hidden objects, action/object confusion,
   inconsistent ownership, missing states, and pages that combine unrelated
   responsibilities.
5. Put the proposed corrected model through the same review gates.
6. Generate revised IA and page architecture only after confirmation.

Do not modify the live product unless the user separately asks for
implementation.

## Final delivery

Return:

- A link to the interactive workspace
- A two-to-five bullet summary of the model boundary, major conflict, and next
  review action
- A short list of sources or capabilities that could not be inspected

Do not paste the full model into chat when the workspace was created
successfully.

## Quality check

Before delivery, verify:

- Every material concept points to evidence or is marked as inference.
- Actions are not mislabeled as objects.
- Attributes belong to the correct object or record.
- Relationships name both endpoints and a meaningful verb.
- States and actions are not conflated.
- Conflicts remain visible instead of being silently resolved.
- Structural decisions explain their downstream impact.
- The user can edit or delete proposed concepts.
- IA, navigation, and page structure are generated only from confirmed inputs.
- The workspace is readable, responsive, and usable without chat instructions.
