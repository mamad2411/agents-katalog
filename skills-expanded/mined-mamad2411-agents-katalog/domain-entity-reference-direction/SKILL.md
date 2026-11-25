---
name: domain-entity-reference-direction
description: Determine whether a domain entity should hold a reference to another domain entity and in which direction. Use when an agent needs to create, modify, review, or interpret a domain entity that relates to another domain entity. A domain entity should only hold a reference to another entity if it needs that reference to enforce its own invariants or execute its own domain behavior. References that exist only to support read queries belong in the repository, not in the entity.
---

# Domain Entity Reference Direction

## Goal

When two domain entities are related, determine whether each entity needs a reference to the other based on its own domain responsibilities — invariants and behavior — not on read or query convenience.

A domain entity should hold a reference to another entity only when that reference is required for the entity to enforce its own invariants or perform its own domain behavior. If the relationship is only needed to answer queries or display data, it does not belong on the entity — it belongs in the repository as a query operation.

Most relationships are unidirectional. Bidirectional references are rare and require both entities to independently need the reference for their own domain logic.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a domain entity that holds or could hold a reference to another domain entity
- introduces a new relationship between two domain entities
- adds a reference to an entity for the purpose of querying or displaying related data
- reviews whether an existing reference on a domain entity is justified by domain behavior

## The Rule

1. A reference must be justified by the entity's own invariants or behavior.
   - The entity needs the reference to enforce a business rule about itself.
   - The entity needs the reference to perform a domain operation that belongs to it.
   - If the entity does not use the reference in any invariant check or domain behavior, the reference does not belong on the entity.

2. Do not add references for read or query convenience.
   - If the only reason to add a reference is to retrieve related data for display, listing, or reporting, do not add it to the entity.
   - Resolve read-direction queries through repository operations instead — for example, `orderRepository.findByCustomerId(customerId)`.

3. Evaluate each direction independently.
   - For entity A and entity B, ask separately: does A need to know about B for its own invariants or behavior? Does B need to know about A for its own invariants or behavior?
   - Only add the reference in the direction where the answer is yes.

4. Bidirectional references require justification from both sides.
   - A bidirectional relationship is only correct when both entities independently need the reference for their own domain logic.
   - Example: `Team` holds `memberIds` to enforce a maximum team size. `Player` holds `teamId` to enforce that a player cannot belong to two teams simultaneously. Both references are justified by independent invariants.

5. When the need is ambiguous, ask the human.
   - If it is unclear whether an entity needs a reference for domain behavior or merely for query convenience, ask before adding the reference.
   - State the two entities, the proposed direction, and why the need is unclear.

## Detection Workflow

1. Identify the relationship and its current direction.
   - Find the two domain entities involved.
   - Determine which entity currently holds a reference to the other, or which entity a new reference is being proposed for.

2. For each direction, check for domain justification.
   - Does the entity use this reference in any invariant check or business rule enforcement?
   - Does the entity use this reference in any domain behavior method?
   - If neither, the reference is not justified on this entity.

3. Check for query-only references.
   - Is the reference used only to retrieve or display related data?
   - If so, the reference should be removed from the entity and replaced with a repository query.

4. If ambiguous, ask the human.
   - State which entity holds or would hold the reference.
   - State what domain behavior or invariant would use it.
   - Ask whether the reference is needed for domain logic or only for read convenience.

## Writing or Changing Domain Entity References

1. Before adding a reference, state the domain justification.
   - Identify which invariant or domain behavior on the entity requires the reference.
   - If no invariant or behavior requires it, do not add the reference.

2. For unidirectional relationships (the common case):
   - Add the reference only on the entity that needs it for its own domain logic.
   - Resolve the inverse direction through a repository query when needed by business-logic entry points.

3. For bidirectional relationships (rare):
   - Verify that both entities independently need the reference for their own invariants or behavior.
   - Document why bidirectionality is required — both justifications must be explicit.

4. When removing an unjustified reference:
   - Verify that no domain behavior or invariant on the entity depends on the reference.
   - Move the query responsibility to the repository if callers need to retrieve the related data.

## Examples

Unidirectional — Order references Customer, not the reverse:

```ts
class Order {
  readonly id: OrderId
  readonly customerId: CustomerId // Order needs to know its owner
  readonly items: ReadonlyArray<OrderItem>
}

class Customer {
  readonly id: CustomerId
  readonly name: string
  readonly email: Email
  // No orderIds here — Customer does not need orders for its own invariants
}

// When you need a customer's orders, use the repository:
// orderRepository.findByCustomerId(customerId)
```

```py
@dataclass(frozen=True)
class Order:
    id: OrderId
    customer_id: CustomerId  # Order needs to know its owner
    items: tuple[OrderItem, ...]

@dataclass(frozen=True)
class Customer:
    id: CustomerId
    name: str
    email: Email
    # No order_ids here — Customer does not need orders for its own invariants

# When you need a customer's orders, use the repository:
# order_repository.find_by_customer_id(customer_id)
```

```kt
data class Order(
    val id: OrderId,
    val customerId: CustomerId, // Order needs to know its owner
    val items: List<OrderItem>,
)

data class Customer(
    val id: CustomerId,
    val name: String,
    val email: Email,
    // No orderIds here — Customer does not need orders for its own invariants
)

// When you need a customer's orders, use the repository:
// orderRepository.findByCustomerId(customerId)
```

Bidirectional — both sides have independent domain justification:

```ts
class Team {
  readonly id: TeamId
  readonly memberIds: ReadonlyArray<PlayerId> // needed to enforce max team size

  addMember(playerId: PlayerId): Team {
    if (this.memberIds.length >= MAX_TEAM_SIZE) {
      throw new TeamFullError()
    }
    return new Team({ ...this, memberIds: [...this.memberIds, playerId] })
  }
}

class Player {
  readonly id: PlayerId
  readonly teamId: TeamId | null // needed to enforce single-team constraint

  joinTeam(teamId: TeamId): Player {
    if (this.teamId !== null) {
      throw new AlreadyInTeamError()
    }
    return new Player({ ...this, teamId })
  }
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this entity use the reference in any invariant check or domain behavior?
- If the reference were removed, would the entity lose the ability to enforce a business rule about itself?
- Is this reference only used to retrieve or display related data?
- If bidirectional, do both entities independently need the reference for their own domain logic?

If a reference exists only for read or query convenience, it should be moved to a repository query.

## Report the Outcome

When finishing the task:

- state which domain entities were involved and what relationship was evaluated
- state the direction of the reference and which entity holds it
- state the domain justification — which invariant or behavior requires the reference
- state whether the relationship is unidirectional or bidirectional, and why
- state whether any query-only references were removed or avoided
