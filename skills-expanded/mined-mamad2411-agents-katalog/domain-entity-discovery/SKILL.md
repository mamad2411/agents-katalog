---
name: domain-entity-discovery
description: Identify which domain entities are needed to represent a business domain before implementing them. Use when an agent receives a task that requires modeling a new domain area or extending an existing one — such as implementing a new feature, module, or end-to-end flow — and the domain entities involved are not yet defined in the codebase. The agent must extract domain concepts from the requirements, propose a set of domain entities with their relationships, validate the proposal with the human, and document the agreed model before proceeding to implementation.
---

# Domain Entity Discovery

## Goal

Before implementing domain entities, identify which ones are needed to correctly represent the business domain described in the task.

Domain entity discovery is the process of extracting domain concepts from requirements and determining which of those concepts should be modeled as domain entities. This step must happen before applying any implementation skill — aggregate boundaries, reference direction, optionality, typed IDs, immutability, repositories, and entry points all depend on knowing which entities exist and how they relate.

The agent must propose a domain model and validate it with the human before writing code. The agent should not guess or assume which entities the domain needs — it should reason from the requirements, propose explicitly, and wait for confirmation.

## What Counts as In Scope

Apply this skill when the task does one or more of these things:

- requires modeling a new domain area that does not yet exist in the codebase
- introduces a new feature or flow that involves domain concepts not yet represented as entities
- extends an existing domain area with concepts that may require new entities
- asks the agent to implement something end-to-end where the domain model is not predefined

Do not apply this skill when:

- the domain entities are already defined in the codebase and the task only modifies behavior
- the task explicitly lists which domain entities to create
- the task is limited to refactoring, fixing, or reviewing existing entities

## The Rule

1. Extract domain concepts from the requirements.
   - Read the task description carefully and identify every noun or noun phrase that represents a business concept.
   - Distinguish between concepts that are likely domain entities — things with identity and lifecycle — and concepts that are likely attributes, value objects, or enums.

2. Check the existing codebase for already-modeled concepts.
   - Search for domain entities that already exist in the project.
   - Determine which concepts from the requirements are already represented and which are new.

3. Propose a domain model to the human.
   - List every proposed domain entity with a one-line description of what it represents.
   - List the proposed relationships between entities — which entity references which, and in which direction.
   - Identify which concepts you considered but excluded from the entity list, and state why — for example, "modeled as an attribute of X" or "modeled as an enum."
   - Be explicit about what you are unsure about. State open questions clearly.

4. Wait for the human to validate before implementing.
   - Do not write entity code until the human confirms the proposed model.
   - If the human corrects, adds, or removes entities, update the proposal accordingly.
   - If the human asks for changes to relationships, adjust and re-confirm if the change is significant.

5. Document the agreed model.
   - After the human confirms, document the agreed domain entities and their relationships in the project's agent instructions file under the aggregate boundaries section, following the format defined by the `aggregate-boundaries` skill.
   - This documentation feeds into all downstream skills — aggregate boundaries, reference direction, optionality, repositories, and entry points.

## Discovery Workflow

1. Read the task and list candidate concepts.
   - Identify every business concept mentioned or implied.
   - For each concept, note whether it likely has identity and lifecycle (entity candidate) or is a descriptor, measurement, label, or classification (value object or attribute candidate).

2. Search the codebase for existing entities.
   - Check if any candidate concepts are already modeled.
   - Note which existing entities the new concepts will relate to.

3. For each entity candidate, apply the identity test.
   - Does this concept have a unique identity that persists over time?
   - Does it have a lifecycle — can it be created, changed, and potentially deleted?
   - Do different instances of this concept need to be distinguished from each other?
   - If all answers are yes, it is a domain entity candidate.
   - If the answers are unclear, include it in the proposal as an open question.

4. For each pair of related entities, propose the relationship.
   - State which entity references which.
   - State whether the relationship is one-to-one or one-to-many.
   - Do not determine aggregate boundaries, reference style, direction, or optionality at this stage — those are handled by their respective skills after the model is confirmed.

5. Present the proposal to the human.
   - Use the format described below.
   - Wait for confirmation before proceeding.

## Proposal Format

Present the domain model proposal to the human using this structure:

```
Proposed domain entities:

- **EntityA**: one-line description of what it represents
- **EntityB**: one-line description of what it represents
- **EntityC**: one-line description of what it represents

Proposed relationships:

- EntityA → EntityB (one-to-many): brief reason
- EntityA → EntityC (one-to-one): brief reason

Modeled as attributes or value objects (not entities):

- conceptX: modeled as an attribute of EntityA because ...
- conceptY: modeled as an enum because ...

Open questions:

- Is ConceptZ a separate entity or an attribute of EntityB?
- Should ConceptW be tracked with its own identity?
```

## Examples

Task: "implement a system to manage laboratory tests"

The agent should propose something like:

```
Proposed domain entities:

- **LabTest**: a specific laboratory test ordered for a patient, with its own lifecycle from ordered to completed
- **Sample**: a biological sample collected from a patient, identified and tracked independently
- **TestResult**: the outcome of a lab test performed on a sample

Proposed relationships:

- LabTest → Sample (one-to-many): a lab test may involve multiple samples
- Sample → TestResult (one-to-one): each sample produces one result

Modeled as attributes or value objects (not entities):

- testType: modeled as an attribute or enum on LabTest — it classifies the test but does not have its own identity or lifecycle
- referenceRange: modeled as a value object on TestResult — it describes the expected range but has no identity

Open questions:

- Is Patient a domain entity in this module, or does it already exist in the codebase and we reference it by ID?
- Should TestType be a separate entity if the system needs to manage a catalog of test types with their own configurations?
- Does a Sample have an independent lifecycle (can it exist before being assigned to a LabTest)?
```

Then the agent waits for the human to confirm, correct, or extend the proposal.

## Review Questions

When reviewing whether domain entity discovery was applied correctly, ask:

- Were all business concepts in the requirements identified and considered?
- Was a clear proposal presented to the human before implementation started?
- Were entities distinguished from value objects and attributes with stated reasoning?
- Were relationships between entities identified?
- Were open questions surfaced rather than silently assumed?
- Did the human confirm the model before code was written?
- Was the agreed model documented in the project's agent instructions file?

## Report the Outcome

When finishing the task:

- state which domain concepts were extracted from the requirements
- state which concepts were proposed as domain entities and which were excluded, with reasons
- state which relationships were proposed
- state which open questions were raised and how they were resolved
- state whether the human confirmed the model before implementation began
- state whether the agreed model was documented in the project's agent instructions file
