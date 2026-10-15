---
name: business-logic-entry-point-primitive-input-types
description: Require business-logic entry point input parameters to use only primitive or basic types. Use when an agent needs to create, modify, review, or interpret the command or query types accepted by business-logic entry points. Input fields must be strings, numbers, or booleans. Do not use domain-entity types, domain aggregate types, branded or opaque primitive types, enums, temporal types, or other complex domain objects as input fields.
---

# Primitive Input Types for Business Logic Entry Points

## Goal

The fields of command and query types accepted by business-logic entry points must use only primitive or basic types.

A business-logic entry point receives raw input data and is responsible for constructing, loading, or looking up domain entities internally. The caller must never be required to build a domain entity before calling the entry point.

Do not use domain-entity types, domain aggregate types, value objects with behavior, or other complex domain objects as fields in command or query types.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a `...Command` or `...Query` type for a business-logic entry point
- defines the fields of an entry-point input type
- passes a domain entity or domain aggregate as a field of a command or query type
- uses a complex domain object where a primitive or basic type would suffice

## Allowed Input Types

The following types are allowed as fields in command and query types:

- **Strings**: `string`, `str`, `String`
- **Numbers**: `number`, `int`, `float`, `Int`, `Long`, `Double`
- **Booleans**: `boolean`, `bool`, `Boolean`
- **Collections of the above**: arrays or lists of any of the allowed types (e.g., `string[]`, `list[str]`)
- **Nested plain data structures**: types composed exclusively of the allowed types above, used to group related input fields (e.g., an `AddressInput` with `street: string`, `city: string`, `zipCode: string`)

## Forbidden Input Types

The following types must not appear as fields in command or query types:

- Domain entities (e.g., `Customer`, `Order`, `Subscription`)
- Domain aggregates
- Value objects that encapsulate behavior or enforce invariants
- Branded or opaque primitive types (e.g., `CustomerId`, `OrderId`, `RequesterId`, `Email`) — use the underlying primitive instead (e.g., `string`)
- Dates and temporal types (e.g., `Date`, `ZonedDateTime`, `Instant`, `LocalDate`, `datetime`) — use `string` in ISO 8601 format instead
- Enums (e.g., `CarClass`, `OrderStatus`) — use `string` instead
- Persistence-layer types (e.g., ORM entities, database records)
- Any type that requires the caller to construct a domain object before calling the entry point

## The Rule

1. Every field in a command or query type must be a primitive or basic type.
   - Use `string`, not `Customer` or `CustomerId`.
   - Use `string`, not `OrderStatus` or `CarClass` — represent enum values as strings.
   - Use `string` in ISO 8601 format, not `ZonedDateTime`, `Instant`, or `Date`.
   - Use `OrderLineDraft[]` (a plain data structure of primitives) not `OrderLine[]` if `OrderLine` is a domain entity.

2. The entry point is responsible for constructing or loading domain entities.
   - The entry point receives primitive input, then creates new domain entities or loads existing ones from a repository.
   - The caller does not need to know how domain entities are structured or instantiated.

3. Nested input structures must also contain only allowed types.
   - If a command field is a nested object, every field in that nested object must also be a primitive or basic type.
   - Do not smuggle domain entities or branded types inside nested input structures.

## Detection Workflow

1. Find command and query types.
   - Identify `...Command` and `...Query` types used by business-logic entry points.

2. Inspect each field.
   - Check whether the field type is a string, number, boolean, or a collection of these.
   - Flag any field whose type is a domain entity, domain aggregate, value object, branded/opaque primitive type, enum, or temporal type.

3. Check nested structures.
   - If a field is a nested object type, verify that all of its fields are also allowed types.

4. Trace the domain entity construction.
   - Verify that domain entities are constructed or loaded inside the entry point, not received as input.

## Writing or Changing Input Types

1. Start from the data the caller provides.
   - Identify what raw data the caller has: IDs as strings, numbers, booleans, dates as ISO 8601 strings, enum values as strings.
   - Express each piece of input data as a string, number, or boolean.

2. Use raw primitives for all values.
   - Use `string` for entity IDs, email addresses, dates (ISO 8601), enum values, and other values that may have domain-specific types in the domain layer.
   - Use `number` for quantities, amounts, and numeric values.
   - Use `boolean` for flags and binary choices.
   - The entry point is the boundary where raw primitives enter and domain types begin.

3. Use plain data structures for grouped input.
   - When multiple related values travel together (e.g., address fields), define a plain input structure with only allowed types.
   - Name these structures to reflect their input purpose (e.g., `AddressInput`, `OrderLineDraft`).

4. Let the entry point build domain objects.
   - Construct new domain entities from the primitive input inside the entry point.
   - Load existing domain entities from repositories using the provided IDs.

## Examples

Use this:

```ts
type CreateOrderCommand = {
  requesterId: string
  customerId: string
  lines: OrderLineDraft[]
}

type OrderLineDraft = {
  productId: string
  quantity: number
}
```

Not this:

```ts
type CreateOrderCommand = {
  requesterId: RequesterId
  customerId: CustomerId
  lines: OrderLine[]
}
```

Use this:

```py
@dataclass(frozen=True)
class CreateOrderCommand:
    requester_id: str
    customer_id: str
    lines: list[OrderLineDraft]

@dataclass(frozen=True)
class OrderLineDraft:
    product_id: str
    quantity: int
```

Not this:

```py
@dataclass(frozen=True)
class CreateOrderCommand:
    requester_id: RequesterId
    customer_id: CustomerId
    lines: list[OrderLine]
```

Use this:

```kt
data class CreateOrderCommand(
    val requesterId: String,
    val customerId: String,
    val lines: List<OrderLineDraft>,
)

data class OrderLineDraft(
    val productId: String,
    val quantity: Int,
)
```

Not this:

```kt
data class CreateOrderCommand(
    val requesterId: RequesterId,
    val customerId: CustomerId,
    val lines: List<OrderLine>,
)
```

## Review Questions

When reading or reviewing code, ask:

- Are all fields in this command or query type strings, numbers, booleans, or collections of these?
- Does any field use a domain-entity type, domain aggregate, value object, branded/opaque primitive type, enum, or temporal type?
- Are nested input structures composed exclusively of allowed types?
- Is the entry point responsible for constructing or loading domain entities from the primitive input?
- Does the caller need to build a domain entity before calling this entry point?

If any input field uses a forbidden type, apply this skill.

## Report the Outcome

When finishing the task:

- state which command or query types were identified or changed
- state which fields were changed from domain or branded types to raw primitive types
- state which nested input structures were introduced or corrected
- state how domain-entity construction was moved inside the entry point
