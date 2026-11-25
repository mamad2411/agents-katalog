---
name: product-context
description: Create or update a shared, evidence-aware product context for product design and independent product-building work. Use when starting an initiative, consolidating scattered product inputs, or preparing reliable context for discovery, conceptual modeling, prototyping, evaluation, implementation, or marketing. Do not use as a substitute for missing user research or to silently turn assumptions into decisions.
---

# Product Context

Create the smallest durable context that helps downstream skills make consistent product decisions without repeatedly asking for the same information.

## Locate before creating

Inspect the user's supplied artifacts and the project's existing product brief, research, strategy, design-system, analytics, decision-log, and marketing-context files. Reuse the project's established location and terminology when one exists. Otherwise propose or create `.agents/product-context.md` when the task authorizes file changes.

Do not create a parallel source of truth when a current canonical document can be updated. Do not overwrite unrelated content or restructure an existing document beyond what the request needs.

## Build the context

1. Inventory every source actually inspected. Record its path or URL, date when known, and what it contributes.
2. Extract only decision-relevant information into these classes:
   - `Evidence`: directly supported by research, behavior, analytics, policy, or an authoritative product source.
   - `Inference`: a reasoned interpretation of evidence.
   - `Assumption`: important but not yet verified.
   - `Decision`: explicitly chosen, with owner or source when known.
   - `Preference`: a user, brand, or team preference that is not a universal product principle.
3. Describe the users and buyer separately when they differ. Include the critical job, current alternative, pain, desired outcome, and adoption constraints.
4. Record the product promise, scope, non-goals, business model or value exchange, and meaningful technical, legal, accessibility, brand, and operational constraints.
5. Capture unresolved questions and rank them by how much a different answer would change the product.
6. Identify stale, contradictory, or weakly sourced context. Never silently resolve conflicts.
7. End with the next decision and the minimum evidence needed to make it.

Use [references/TEMPLATE.md](references/TEMPLATE.md) when creating a new context file. Preserve an existing useful structure when updating one.

## Interaction rules

- Use concrete information already provided; do not ask the user to repeat it.
- Ask only when a missing choice materially changes the product. Otherwise record it as an assumption or unresolved question and continue.
- When the user confirms or rejects something, update the decision record and retain the rejected option plus the reason when it can prevent repeated debate.
- Keep product context distinct from task instructions. This file records product truth and uncertainty; it does not prescribe how every downstream skill must work.
- External research may add evidence, but popularity, competitor behavior, or a framework is not proof of the user's customer need.

## Completion check

The context is ready when:

- every consequential statement is labeled by epistemic status;
- evidence has provenance;
- user, buyer, problem, outcome, constraints, scope, and unknowns are findable;
- contradictions are visible;
- downstream work can name the next decision without inventing missing facts.

Return the saved path, the highest-risk unresolved assumption, and the recommended next skill or validation step.
