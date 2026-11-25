---
name: business-logic-entry-point-domain-entity-payload-types
description: Require business-logic entry points to use domain-entity types directly in returned payloads whenever they return domain-entity data. Use when an agent needs to create, modify, review, or interpret the success payload of business-logic entry points, including query handlers and any other business-layer API that returns domain-entity data. Do not map domain entities into separate payload types, DTOs, view models, or similar transport shapes at the business-logic entry point when the payload is supposed to contain domain-entity data.
---

# Domain Entity Payload Types for Business Logic Entry Points

## Goal

When a business-logic entry point returns domain-entity data, the payload type must be the domain-entity type itself.

Do not transform or map a domain entity into another return payload type at the business-logic entry point. If the payload is meant to carry a `Customer`, return `Customer`. If it is meant to carry several `Order` entities, return a collection of `Order`. Keep the domain-entity type intact.

This rule applies to the payload type, not merely to the runtime value. The return signature must expose the domain-entity type directly.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines the success payload of a business-logic entry point
- defines a `...QueryHandlerSuccess` or `...CommandHandlerSuccess` type that carries domain-entity data
- maps domain entities into intermediate payload types at business-logic boundaries
- returns one or more domain entities from business logic
- introduces DTO, view-model, projection, response-model, or similar wrapper types where the payload is supposed to contain domain-entity data

## Domain Entity Payload Rule

1. Use the domain-entity type directly whenever the payload contains domain-entity data.
   - Return `Customer`, not `CustomerPayload`.
   - Return `Order`, not `OrderDto`.
   - Return `List<Order>` or `Order[]`, not `OrderListItem[]`, when the payload is meant to contain domain entities.

2. Do not map domain entities into alternate payload types at business-logic entry points.
   - Do not introduce conversion layers whose only purpose is to reshape domain-entity data before returning it from business logic.
   - Keep entity-to-payload mapping out of the business-logic entry point when the intended payload is the entity itself.

3. Keep wrapper success types aligned with the entity rule.
   - If a `...QueryHandlerSuccess` or `...CommandHandlerSuccess` type contains domain-entity data, its relevant fields must use the domain-entity type directly.
   - Use collections, optionals, or other container types around the domain-entity type only when the business result truly requires that shape.

4. Preserve other entry-point rules.
   - If another rule requires a non-create command handler to return the project's empty equivalent, keep that rule.
   - If another rule allows a create command handler to return only created IDs, keep that rule.
   - Apply this skill only in the cases where the entry point is supposed to return domain-entity data.

## Detection Workflow

1. Identify whether the payload is meant to contain domain-entity data.
   - Check the business meaning of the returned value.
   - Determine whether the caller is receiving actual entities from the domain layer rather than identifiers or non-entity summaries.

2. Inspect the declared return types.
   - Look for payload wrappers, DTOs, response models, projections, or other types inserted between the business-logic entry point and the domain entity.
   - Check whether those types merely duplicate the entity shape or rename fields without changing the business meaning.

3. Trace mapping code.
   - Look for `toDto`, `toPayload`, `toResponse`, `fromEntity`, or similar conversions at the business-logic entry point.
   - Treat entity-to-payload mapping at that boundary as a violation when the payload is intended to contain domain-entity data.

## Writing or Changing Business-Logic Payloads

1. Start from the business result.
   - Decide whether the entry point is supposed to return domain entities, entity IDs, or some other business result.
   - Apply this skill only when the result should contain domain-entity data.

2. Use the entity type directly in the return signature.
   - If one entity is returned, use the entity type directly.
   - If several entities are returned, use a collection of that entity type.
   - If the payload is wrapped in a success type, put the entity type directly inside that wrapper.

3. Remove redundant mapping.
   - Delete or avoid payload types that only mirror the entity shape for the business-logic boundary.
   - Delete or avoid conversion code that only repackages the entity without changing the intended business result.

4. Keep the domain meaning intact.
   - Preserve the entity's type, identity, and behavior contract as represented by the domain layer.
   - Do not flatten or rename entity fields merely to satisfy a business-logic return payload shape.

## Examples

Use this:

```ts
type FindCustomerByIdQueryHandlerSuccess = {
  customer: Customer
}
```

Not this:

```ts
type CustomerPayload = {
  id: CustomerId
  name: string
}

type FindCustomerByIdQueryHandlerSuccess = {
  customer: CustomerPayload
}
```

Use this:

```ts
type ListOrdersQueryHandlerSuccess = {
  orders: Order[]
}
```

Not this:

```ts
type OrderListItem = {
  id: OrderId
  total: Money
}

type ListOrdersQueryHandlerSuccess = {
  orders: OrderListItem[]
}
```

## Review Questions

When reading or reviewing code, ask:

- Is this entry point supposed to return domain-entity data?
- If so, does the payload type use the domain-entity type directly?
- Is there any DTO, payload type, response model, or mapping layer inserted without changing the intended business result?
- Would removing the mapping leave the business meaning unchanged?
- Does this code violate another entry-point rule, such as returning only IDs for create commands?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which business-logic entry points were identified or changed
- state which payload fields now use domain-entity types directly
- state which redundant payload types or mappings were removed or avoided
- state any other entry-point rule that still constrained the final return shape
