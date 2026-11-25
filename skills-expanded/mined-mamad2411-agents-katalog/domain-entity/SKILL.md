---
name: domain-entity
description: Identify, interpret, review, or write domain entities in code. Use when an agent needs to decide whether a domain entity is defined by a stable identity that persists over time, or when it must implement, preserve, or refactor entity lifecycle, invariants, and behavior around domain data. When writing or changing a domain entity, use a class or the closest class-like construct the project stack supports. Do not model domain entities as plain type aliases or interfaces paired with standalone functions.
---

# Domain Entity

## Goal

Define a domain entity as a domain object with a unique identity that persists over time, even as its attributes change.

A domain entity encapsulates business behavior, business rules, and invariants related to its own data. It acts as a core building block in the domain or business layer for concepts such as a customer, order, subscription, account, or shipment.

Treat a domain entity as identity-driven code. The key question is whether the object represents a specific domain concept that remains the same thing throughout its lifecycle while its state evolves.

## What Counts as a Domain Entity

Classify code as a domain entity when it does one or more of these things:

- represents a specific domain concept through a stable identity
- carries an identifier that distinguishes one instance from another across time
- preserves continuity as state changes throughout a lifecycle
- exposes behaviors that apply domain rules to its own data
- enforces invariants that must remain true for that specific domain concept
- controls valid state transitions for its own lifecycle
- encapsulates internal state and requires callers to use intention-revealing methods
- protects its data from arbitrary mutation so validity is maintained

Domain entities often appear in code that answers questions such as:

- which specific customer, order, account, or shipment is this
- what makes this object the same domain thing after its attributes change
- which operations may change its state
- which conditions must remain true throughout its lifecycle
- how callers must interact with it to keep it valid

## Detection Workflow

1. Read the code for identity first.
   - Look for identifiers, natural keys, references, or equality rules that distinguish one instance from another.
   - Pay attention to code that tracks the same domain concept over time rather than only its current attributes.

2. Identify lifecycle continuity.
   - Determine whether the object remains the same domain concept as its properties change.
   - Identify the states, transitions, and milestones that define its lifecycle.

3. Trace behaviors and invariants.
   - Identify methods that change the entity's state, enforce rules, or reject invalid transitions.
   - Identify the conditions that must always hold true for the entity to remain valid.

4. Check the encapsulation boundary.
   - Identify whether callers are expected to change state through explicit methods instead of direct arbitrary mutation.
   - Prefer designs where domain operations are expressed as named behaviors with domain meaning.

5. Prefer semantic classification to file or framework conventions.
   - Do not assume code is or is not a domain entity only because of its folder, class name, annotation, ORM mapping, or framework role.
   - Classify by whether the object models a stable domain identity with owned behavior and invariants.

## Writing or Changing Domain Entities

1. Preserve the identity model before refactoring.
   - Restate what makes the entity the same domain concept over time.
   - Keep identifiers and identity semantics explicit.

2. Use a class to co-locate identity, state, invariants, and behavior.
   - Use a class, or the closest class-like construct available in the language, so that identity, state, invariants, and domain behavior live together in a single construct.
   - A plain type alias, interface, or record paired with standalone functions is not a class-like construct. Do not model a domain entity that way.
   - Follow the project's existing conventions for how classes are modeled.
   - Only fall back to a non-class construct when the language has no class support at all, not merely because a functional style is common or preferred by convention.

3. Keep behavior close to the entity.
   - Put state-changing domain operations on the entity when they belong to that entity's own rules.
   - Use method names that express business intent, such as `changeAddress`, `approve`, `cancel`, or `assignOwner`.

4. Protect invariants through explicit operations.
   - Verify that every allowed state change still enforces the required rules.
   - Avoid exposing write paths that let callers bypass validity checks.

5. Preserve lifecycle integrity.
   - Verify that transitions between states remain valid and understandable.
   - Verify that the entity keeps the same identity across creation, loading, updates, and later lifecycle stages.

6. Hide internal structure where validity depends on it.
   - Expose the minimum data and methods needed for callers to interact correctly.
   - Prefer intention-revealing methods over unrestricted setters when rules must be enforced.

## Review Questions

When reading or reviewing code, ask:

- What makes this object the same domain thing over time?
- Which identifier distinguishes it from other instances?
- Which behaviors belong to this object as part of its own domain responsibility?
- Which invariants must remain true for it to stay valid?
- Would changing this code alter the identity, lifecycle, or rule enforcement of a specific domain concept?

If the answer is yes, treat the code as a domain entity.

## Report the Outcome

When finishing the task:

- state which code was identified or treated as a domain entity
- state whether a class or equivalent construct was used, and why
- state which identities, behaviors, lifecycle transitions, or invariants were implemented or preserved
- state which methods or rules protect the entity's validity
