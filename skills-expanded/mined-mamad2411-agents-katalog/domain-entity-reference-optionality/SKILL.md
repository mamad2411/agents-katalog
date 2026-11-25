---
name: domain-entity-reference-optionality
description: Determine whether a reference from one domain entity to another should be required or optional. Use when an agent needs to create, modify, review, or interpret a domain entity that holds a reference to another domain entity and must decide if that reference can be absent. A reference is required when the entity cannot exist in a valid domain state without it. A reference is optional when the entity can exist in a valid domain state without it. This rule applies only to single-value references — collection references are never nullable because an empty collection represents the absence of related entities.
---

# Domain Entity Reference Optionality

## Goal

When a domain entity holds a reference to another domain entity, determine whether that reference is required or optional based on whether the entity can exist in a valid domain state without it.

A required reference means the entity cannot be created or exist without the referenced entity. An optional reference means the entity can be in a valid state with or without the reference — its absence represents a legitimate domain state, not missing data.

This rule applies only to single-value references. Collection references are never nullable — an empty collection already represents the absence of related entities.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a domain entity with a single-value reference to another domain entity — either a direct reference or an identity reference
- introduces a new single-value reference on a domain entity
- changes the optionality of an existing reference on a domain entity
- reviews whether a reference should be required or optional

This skill does not apply to collection references. A collection of references is always represented as a non-nullable collection type that can be empty.

## The Rule

1. A single-value reference is required when the entity cannot exist in a valid domain state without it.
   - The entity's creation invariants demand the reference.
   - There is no legitimate domain scenario where the entity exists without the referenced entity.
   - Example: an `Order` always belongs to a customer — `customerId` is required.

2. A single-value reference is optional when the entity can exist in a valid domain state without it.
   - There is a legitimate domain scenario where the reference is absent.
   - The absence represents a meaningful domain state, not missing or incomplete data.
   - Example: a `Player` may or may not belong to a team — `teamId` is optional.

3. Collection references are never nullable.
   - Represent collections of references using a non-nullable collection type — list, array, set, or the equivalent in the project's stack.
   - An empty collection represents the absence of related entities.
   - Do not use nullable collection types to represent "no related entities."

4. Express optionality using the stack's idiomatic type.
   - Use the language's standard optional or nullable type — `T | null`, `Optional<T>`, `T?`, `Option<T>`, or the equivalent.
   - Do not use sentinel values, empty strings, zero IDs, or special constants to represent an absent reference.

## Detection Workflow

1. Identify single-value references on the domain entity.
   - Find fields or properties that hold a reference to another domain entity — either a direct entity reference or an identity reference.
   - Exclude collection references — these are always non-nullable.

2. For each single-value reference, assess domain validity without it.
   - Can this entity be created without the reference?
   - Is there a legitimate domain state where the reference is absent?
   - If both answers are no, the reference is required.
   - If either answer is yes, the reference is optional.

3. Check for sentinel values masking optionality.
   - Look for empty strings, zero values, placeholder IDs, or special constants used in place of a proper optional type.
   - If found, replace with an explicit optional type.

4. If ambiguous, ask the human.
   - State the entity and the reference in question.
   - Ask whether the entity can exist in a valid domain state without the reference.
   - Wait for the answer before proceeding.

## Writing or Changing Domain Entity References

1. For required references:
   - Declare the field as a non-nullable type.
   - Enforce presence at creation time — the entity cannot be constructed without the reference.

2. For optional references:
   - Declare the field using the stack's idiomatic optional type.
   - Ensure domain behavior handles the absent case explicitly — do not assume the reference is always present.

3. For collection references:
   - Declare the field as a non-nullable collection type.
   - Initialize to an empty collection when no related entities exist.
   - Do not use a nullable collection type.

## Examples

Required reference — Order always belongs to a customer:

```ts
class Order {
  readonly id: OrderId
  readonly customerId: CustomerId // required — an order cannot exist without a customer
  readonly items: ReadonlyArray<OrderItem>
}
```

```py
@dataclass(frozen=True)
class Order:
    id: OrderId
    customer_id: CustomerId  # required — an order cannot exist without a customer
    items: tuple[OrderItem, ...]
```

```kt
data class Order(
    val id: OrderId,
    val customerId: CustomerId, // required — an order cannot exist without a customer
    val items: List<OrderItem>,
)
```

Optional reference — Player may or may not belong to a team:

```ts
class Player {
  readonly id: PlayerId
  readonly name: string
  readonly teamId: TeamId | null // optional — a free agent has no team
}
```

```py
@dataclass(frozen=True)
class Player:
    id: PlayerId
    name: str
    team_id: TeamId | None  # optional — a free agent has no team
```

```kt
data class Player(
    val id: PlayerId,
    val name: String,
    val teamId: TeamId?, // optional — a free agent has no team
)
```

Collection reference — never nullable, empty when none:

```ts
class Team {
  readonly id: TeamId
  readonly name: string
  readonly memberIds: ReadonlyArray<PlayerId> // never nullable — empty means no members
}
```

```py
@dataclass(frozen=True)
class Team:
    id: TeamId
    name: str
    member_ids: tuple[PlayerId, ...]  # never nullable — empty means no members
```

```kt
data class Team(
    val id: TeamId,
    val name: String,
    val memberIds: List<PlayerId>, // never nullable — empty means no members
)
```

Not this — sentinel values masking optionality:

```ts
// Bad: using empty string instead of null
class Player {
  readonly teamId: TeamId // set to "" when no team — misleading
}

// Good: explicit optionality
class Player {
  readonly teamId: TeamId | null // null means no team
}
```

## Review Questions

When reading or reviewing code, ask:

- Can this entity exist in a valid domain state without this reference?
- Is the reference declared as optional or required, and does that match the domain reality?
- Are there sentinel values being used instead of a proper optional type?
- Are collection references declared as non-nullable types?

If the optionality of a reference does not match the domain validity rules, apply this skill.

## Report the Outcome

When finishing the task:

- state which domain entity references were evaluated
- state whether each reference was determined to be required or optional, and the domain justification
- state whether any sentinel values were replaced with proper optional types
- state whether any nullable collections were changed to non-nullable empty collections
