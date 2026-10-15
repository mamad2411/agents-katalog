---
name: immutable-domain-entities
description: Require the immutable design pattern for domain entities. Use when an agent needs to create, modify, review, or interpret domain entities and should preserve identity while expressing state changes through new immutable instances. Domain entities must be modeled as immutable classes, not as plain type aliases or interfaces paired with standalone functions.
---

# Immutable Domain Entities

## Goal

Apply the immutable design pattern when writing or changing domain entities.

An immutable domain entity keeps the same domain identity while preventing in-place mutation of its state. Domain operations that would otherwise change the entity must instead return a new entity instance, or the closest immutable equivalent the stack supports, preserving the same identity and enforcing the same invariants.

Treat this skill as construction and change-management guidance for domain entities. The key question is whether the entity can be modeled so its state is fixed after creation and all valid changes are expressed as explicit creation of a new immutable version.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a domain entity's fields, properties, or constructor
- defines domain operations that would change a domain entity's state
- exposes getters, setters, collections, or nested objects on a domain entity
- loads, reconstructs, or rehydrates domain entities from persistence or transport data
- copies, clones, replaces, or updates domain entity instances
- enforces invariants during creation or state transitions of domain entities

## Immutable Rule

1. Model domain entities as immutable when the task writes or changes them.
   - Use immutable classes or the closest immutable class-like construct the language supports.
   - A plain type alias, interface, or record paired with standalone functions is not a class-like construct. Do not model an immutable domain entity that way.
   - Keep the entity's identity stable while returning a new entity instance for every valid state change.

2. Do not mutate entity state in place.
   - Do not add public setters, writable public fields, or in-place mutation methods.
   - Do not let domain methods silently change internal state on the existing entity instance.

3. Keep all entity data effectively immutable.
   - Make fields readonly or the closest equivalent when the stack supports it.
   - Prevent mutation through exposed references, including collections, maps, nested objects, or buffers.
   - Copy or freeze mutable inputs and outputs when needed to preserve immutability.

4. Express change through intention-revealing operations.
   - Domain operations such as `changeAddress`, `approve`, `cancel`, or `assignOwner` should return a new entity with the same identity and the updated valid state.
   - Preserve invariant checks in those operations instead of pushing validation to callers.

5. Keep framework constraints at the boundary.
   - If a persistence or framework layer requires a mutable representation, keep that requirement outside the domain entity when possible.
   - Preserve an immutable domain entity model even if boundary adapters need to map to or from another shape.

## Detection Workflow

1. Find the mutation surface first.
   - Identify setters, writable fields, mutable collections, direct property assignment, and methods that update state in place.
   - Identify whether callers can change the entity without going through an explicit domain operation.

2. Trace identity-preserving changes.
   - Determine which operations are meant to evolve the same domain concept over time.
   - Verify that those changes can be represented by returning a new instance with the same identity.

3. Check nested mutability.
   - Inspect collections, child objects, and other referenced data carried by the entity.
   - Verify that immutability is not broken through aliases to mutable internal data.

4. Prefer semantic classification to framework conventions.
   - Do not assume a mutable ORM or framework model should also dictate the domain entity shape.
   - Classify and design the entity by domain needs first, then adapt boundaries as needed.

## Writing or Changing Immutable Domain Entities

1. Make construction explicit.
   - Use constructors, factories, static creation methods, or equivalent project patterns that fully establish a valid immutable entity.
   - Validate invariants at creation time.

2. Return new instances for state changes.
   - Replace in-place updates with methods that produce a new entity value carrying the same identity.
   - Keep method names aligned with domain intent rather than generic copy or patch semantics when possible.

3. Eliminate mutable write paths.
   - Remove or avoid public setters and writable public fields.
   - Replace mutation-oriented helpers with copy, replace, or transition methods that preserve invariants.

4. Protect internal references.
   - Use immutable collections or defensive copying when the language requires it.
   - Do not expose mutable internal references that let callers bypass entity rules.

5. Preserve rehydration and reconstruction safely.
   - Ensure entities loaded from persistence or transport can still be reconstructed as immutable objects.
   - Keep rehydration paths explicit enough to preserve identity and invariants.

## Review Questions

When reading or reviewing code, ask:

- Can this domain entity be mutated after construction?
- Do state-changing operations return a new instance with the same identity?
- Are invariants preserved in the creation and transition methods?
- Can callers mutate the entity through setters, writable fields, or exposed mutable references?
- Would changing this code weaken immutability for a domain entity?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which domain entities were identified or changed
- state which immutable constructs or patterns were used
- state how identity-preserving updates were implemented
- state which mutable writing paths or exposed mutable references were removed or prevented
