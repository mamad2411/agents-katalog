---
name: conceptual-model-design
description: Build or review a product conceptual model when entities, roles, relationships, states, permissions, or lifecycle choices determine how the product should work. Use for product briefs, IA, prototypes, and data-model alignment. Do not invent a single correct model from missing policy.
---

# Conceptual Model Design

Turn product evidence into an inspectable model that product, design, and engineering can discuss together.

## Model the product

1. Extract candidate actors, concepts, actions, state words, lifecycle clues, and governing rules from the supplied evidence.
2. Decide whether each concept is an object or an attribute:
   - Use an object when it has independent identity, lifecycle, or relationships.
   - Use an attribute when it only describes another object.
   - When the answer depends on an unstated product choice, show alternatives and request or record the decision.
3. Identify roles and permitted actions. Separate current evidence from proposed policy.
4. Add relationships and cardinality only when supported; mark unknowns explicitly.
5. Describe meaningful state transitions, including failure, expiry, cancellation, reversal, and recovery when relevant.
6. Translate the model into product implications: what information, actions, permissions, states, and boundaries the experience must reveal.
7. Identify which unresolved model decision creates the greatest downstream design or engineering risk.

## Output

1. Roles
2. Objects and attributes, including non-obvious rationale
3. Relationships
4. Lifecycle and state transitions
5. Rules and permissions
6. Assumptions requiring human review
7. Product implications
8. Highest-risk model decision and next evidence

## Boundaries

- Do not turn every noun into an object.
- Do not silently invent policy, permissions, cardinality, or business rules.
- A polished diagram is not proof that the model is correct.
- Preserve vocabulary users already understand unless evidence supports changing it.
- When updating a model, state what changed and which evidence or decision caused the change.
