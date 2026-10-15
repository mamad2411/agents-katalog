---
name: domain-entity-uuidv4-ids
description: Require UUIDv4 identifiers for domain entities. Use when an agent needs to create, modify, review, or interpret domain entity ID fields, ID types, constructors, persistence mappings, serialization, or API contracts tied to domain entity identity. Prefer the programming language's built-in UUID type when it exists. If the language has no built-in UUID type, use `string` while preserving explicit UUIDv4 generation and validation semantics.
---

# Domain Entity UUIDv4 IDs

## Goal

Represent domain entity identifiers with UUIDv4.

When the programming language or standard library provides a built-in UUID type, prefer that type for domain entity IDs. When no such built-in type exists, use `string` for domain entity IDs and keep UUIDv4 generation and validation explicit.

Treat this skill as identity-format guidance for domain entities. It determines the identifier format (UUIDv4) and the underlying type (built-in UUID or `string`). Whether to wrap that underlying type in a distinct type per domain entity — such as `OrderId` or `CustomerId` — is a separate concern handled by the `domain-entity-typed-ids` skill.

The key question is whether the edited code defines, carries, validates, stores, serializes, or exposes the identifier of a domain entity.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines the ID field or property of a domain entity
- defines constructor parameters or factory inputs for domain entity identity
- defines the type used to carry a domain entity ID through the domain model
- parses, validates, serializes, or deserializes domain entity IDs
- maps domain entity IDs to persistence, transport, or integration boundaries
- creates new domain entity IDs
- compares or stores identity values used to distinguish one entity from another

## UUIDv4 Rule

1. Use UUIDv4 for every domain entity identifier touched by the task.
   - Preserve UUIDv4 semantics across in-memory representation, persistence mappings, and exchanged payloads.
   - Do not weaken the identifier representation to an unconstrained string when a built-in UUID type exists.

2. Prefer the language's built-in UUID type when available.
   - Use the native or standard-library UUID type directly when the language makes it available and the project conventions allow it.
   - Do not fall back to `string` when a built-in UUID type exists.

3. When no built-in UUID type exists, use `string`.
   - Use `string` as the underlying identifier type.
   - Keep generation, parsing, and validation explicit enough that UUIDv4 remains the enforced format.
   - This rule determines the underlying type only. Whether to wrap it in a typed ID such as `OrderId` is determined by the `domain-entity-typed-ids` skill.

## Detection Workflow

1. Find the identity boundary first.
   - Locate the fields, properties, constructor arguments, factory inputs, or persistence mappings that represent domain entity identity.
   - Check whether the identifier appears in domain code, serialization code, persistence code, or communication contracts.

2. Detect UUID type support in the stack.
   - Identify whether the language or standard library offers a UUID type.
   - Follow the project's established conventions for importing, constructing, and storing that type.

3. Trace generation and conversion points.
   - Identify where new IDs are created.
   - Identify where IDs are parsed from text, converted for storage, or emitted across boundaries.
   - Verify that UUIDv4 remains the enforced format at each point.

## Writing or Changing Domain Entity IDs

1. Keep UUIDv4 explicit in the model.
   - Name ID fields and parameters clearly.
   - Use the built-in UUID type when available, otherwise use `string`.

2. Prefer native UUID handling over ad hoc strings.
   - Use the built-in UUID type when available instead of representing IDs as generic text.
   - Keep conversions at boundaries small and explicit.

3. Use `string` when the language has no built-in UUID type.
   - Keep the UUIDv4 contract explicit at parsing, validation, serialization, and generation points.
   - This determines the underlying type. Whether to wrap it in a typed ID is a separate concern.

4. Preserve identity consistency end to end.
   - Verify that the same UUIDv4 value can move through constructors, domain methods, persistence mappings, serializers, and external contracts without losing meaning.
   - Verify that new IDs are generated as UUIDv4, not merely accepted in that format.

5. Keep validation close to parsing or construction.
   - Reject malformed or non-UUIDv4 inputs when IDs enter the system as text or external data.
   - Make the valid construction path obvious in the code.

## Review Questions

When reading or reviewing code, ask:

- Is this code defining or carrying the identity of a domain entity?
- Is that identity represented as UUIDv4?
- Does the stack provide a built-in UUID type that should be used here?
- If not, is the identity represented as `string` with explicit UUIDv4 handling?
- Where is UUIDv4 generated, parsed, validated, stored, or serialized?
- Would changing this code risk weakening the UUIDv4 guarantee for domain entity identity?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which domain entity IDs were identified or changed
- state whether a built-in UUID type or `string` was used, and why
- state where UUIDv4 generation, parsing, validation, or conversion was implemented or preserved
