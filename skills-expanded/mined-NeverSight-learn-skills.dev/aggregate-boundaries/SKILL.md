---
name: aggregate-boundaries
description: Determine and enforce aggregate boundaries when domain entities relate to other domain entities. Use when an agent needs to create, modify, review, or interpret a domain entity that references another domain entity. The agent must determine whether the related entities belong to the same aggregate or to different aggregates, apply the correct reference style — direct reference within the same aggregate, identity reference across aggregates — and document the boundary decision in the project's agent instructions file so future tasks reuse the same decision without asking again.
---

# Domain Entity Aggregate Boundaries

## Goal

When a domain entity relates to another domain entity, determine whether they belong to the same aggregate or to different aggregates, apply the correct reference style, and persist the boundary decision so it is available to future tasks.

An aggregate is a cluster of domain entities that share a consistency boundary. One entity is the aggregate root. Entities inside the same aggregate reference each other directly. Entities in different aggregates reference each other exclusively by identity — the identifier of the other aggregate root.

The boundary decision depends on whether the related entity has an independent lifecycle. If it can be created, modified, or deleted independently, it belongs to a separate aggregate. If it cannot exist or make sense without the other, it belongs to the same aggregate.

When the boundary is not documented and cannot be determined objectively from the code or domain context, the agent must ask the human before proceeding.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a domain entity that holds a reference to another domain entity
- defines a domain entity that holds an identifier referencing another domain entity
- introduces a new relationship between two domain entities
- changes how one domain entity references another
- creates a new domain entity that relates to an existing one

## The Rule

1. Check for an existing boundary decision before writing code.
   - Look in the project's agent instructions file — `AGENTS.md`, `CLAUDE.md`, or equivalent — for a documented aggregate boundary that covers the two entities in question.
   - If a decision exists, follow it.

2. If no decision is documented, determine the boundary.
   - Ask: can entity B exist independently of entity A? Can it be created, queried, modified, or deleted without entity A being involved?
   - If the answer is clearly yes, they are separate aggregates.
   - If the answer is clearly no, they belong to the same aggregate.
   - If the answer is ambiguous or depends on business context that is not evident from the code, ask the human before proceeding. Do not guess.

3. Apply the correct reference style.
   - **Same aggregate**: the parent entity holds a direct reference to the child entity or a collection of child entities. The child entity does not need a reference back to the parent — the parent owns and provides access to it.
   - **Different aggregates**: each entity holds only the identity (ID) of the other aggregate root. Do not hold a direct reference to the full entity from another aggregate.

4. Name reference attributes to reflect the reference style.
   - **Same aggregate (direct reference)**: name the attribute after the entity itself — `order`, `items`, `discount`. For collections, use the plural form — `items`, `discounts`, `variants`.
   - **Different aggregates (identity reference)**: name the attribute with the entity name followed by `Id` — `orderId`, `customerId`, `productId`. For collections of identities, use the plural form followed by `Ids` — `orderIds`, `productIds`, `tagIds`.
   - Do not name an identity reference without the `Id` suffix. An attribute named `order` implies a direct reference to the entity; an attribute named `orderId` implies a reference by identity. This distinction must be consistent and unambiguous.

5. Persist the boundary decision.
   - After the boundary is determined — whether by objective analysis or by asking the human — document it in the project's agent instructions file.
   - Use the format described in the section below.
   - This ensures that the next task involving these entities does not need to re-derive or re-ask the same question.

6. Repositories follow aggregate boundaries.
   - Create one repository per aggregate root, not per entity.
   - Child entities within an aggregate are persisted and retrieved through the aggregate root's repository.
   - Entities in separate aggregates have their own repositories.

## Boundary Decision Format

Document aggregate boundaries in the project's agent instructions file under a dedicated section. Use this format:

```markdown
## Aggregate Boundaries

- **Order aggregate**: Order (root), OrderItem, OrderDiscount
- **User aggregate**: User (root)
- **Product aggregate**: Product (root), ProductVariant
```

Each line names one aggregate, identifies its root, and lists the entities it contains. Entities not listed as part of another aggregate are assumed to be their own single-entity aggregate.

When adding a new boundary decision, append to the existing list. Do not remove or change prior decisions unless the human explicitly requests it.

## Detection Workflow

1. Identify the relationship.
   - Find the two domain entities involved.
   - Determine the nature of the relationship: does one own the other, or do they merely reference each other?

2. Check for a documented boundary.
   - Search the project's agent instructions file for an aggregate boundary section.
   - Search for both entity names in that section.

3. If documented, apply the documented decision.
   - Use direct references for entities in the same aggregate.
   - Use identity references for entities in different aggregates.

4. If not documented, assess lifecycle independence.
   - Can entity B be created without entity A existing?
   - Can entity B be deleted without affecting entity A?
   - Can entity B be queried or modified in a context where entity A is irrelevant?
   - If all answers are yes, they are separate aggregates.
   - If any answer is no, they likely belong to the same aggregate.

5. If ambiguous, ask the human.
   - State the two entities and the relationship.
   - State why the boundary is ambiguous.
   - Ask whether they should belong to the same aggregate or separate aggregates.
   - Wait for the answer before writing code.

6. Document and proceed.
   - Record the decision in the agent instructions file.
   - Apply the correct reference style.

## Writing or Changing Domain Entity References

1. Determine the aggregate boundary using the detection workflow above.

2. For entities in the same aggregate:
   - The aggregate root holds direct references to its child entities.
   - Child entities are created, accessed, and modified through the aggregate root.
   - Invariants that span multiple entities in the aggregate are enforced by the aggregate root.
   - The aggregate root's repository persists and retrieves the entire aggregate, including child entities.

3. For entities in different aggregates:
   - Hold only the identity of the other aggregate root, using the project's identity type convention (e.g., `UUID`, `OrderId`, typed ID).
   - Do not import or reference the other aggregate's entity type in the domain entity definition.
   - Load the other aggregate through its own repository when its data is needed by the business logic entry point.
   - Do not embed or nest one aggregate inside another.

4. Update the agent instructions file if the boundary was not previously documented.

## Examples

Same aggregate — Order owns its OrderItems:

```ts
class Order {
  readonly id: OrderId
  readonly customerId: CustomerId // different aggregate — ID only
  readonly items: ReadonlyArray<OrderItem> // same aggregate — direct reference

  addItem(productId: ProductId, quantity: number, unitPrice: Money): Order {
    // invariant enforcement happens here, inside the aggregate root
    return new Order({ ...this, items: [...this.items, new OrderItem(productId, quantity, unitPrice)] })
  }
}

class OrderItem {
  readonly productId: ProductId // different aggregate — ID only
  readonly quantity: number
  readonly unitPrice: Money
}
```

```py
@dataclass(frozen=True)
class Order:
    id: OrderId
    customer_id: CustomerId  # different aggregate — ID only
    items: tuple[OrderItem, ...]  # same aggregate — direct reference

    def add_item(self, product_id: ProductId, quantity: int, unit_price: Money) -> "Order":
        new_item = OrderItem(product_id=product_id, quantity=quantity, unit_price=unit_price)
        return Order(id=self.id, customer_id=self.customer_id, items=(*self.items, new_item))

@dataclass(frozen=True)
class OrderItem:
    product_id: ProductId  # different aggregate — ID only
    quantity: int
    unit_price: Money
```

```kt
data class Order(
    val id: OrderId,
    val customerId: CustomerId, // different aggregate — ID only
    val items: List<OrderItem>, // same aggregate — direct reference
) {
    fun addItem(productId: ProductId, quantity: Int, unitPrice: Money): Order {
        return copy(items = items + OrderItem(productId, quantity, unitPrice))
    }
}

data class OrderItem(
    val productId: ProductId, // different aggregate — ID only
    val quantity: Int,
    val unitPrice: Money,
)
```

Different aggregates — Order references User by ID only:

```ts
// In the entry point, not inside the entity
const createOrderCommandHandler = (command: CreateOrderCommand) => {
  return withTransaction((transaction) =>
    userRepository.findById(transaction, command.userId)
      .andThen((user) =>
        orderRepository.save(transaction, Order.create(user.id, command.items))
      )
  )
}
```

```py
def create_order_command_handler(command: CreateOrderCommand):
    with transaction() as tx:
        user = user_repository.find_by_id(tx, command.user_id)
        order = Order.create(user_id=user.id, items=command.items)
        return order_repository.save(tx, order)
```

```kt
fun createOrderCommandHandler(command: CreateOrderCommand) {
    return withTransaction { tx ->
        val user = userRepository.findById(tx, command.userId)
        val order = Order.create(userId = user.id, items = command.items)
        orderRepository.save(tx, order)
    }
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this domain entity reference another domain entity directly or by identity?
- Is the reference style consistent with the aggregate boundary for these two entities?
- Is the aggregate boundary documented in the project's agent instructions file?
- If not documented, can the boundary be determined objectively from the domain context?
- If ambiguous, was the human consulted before a decision was made?
- Does each aggregate root have its own repository, and are child entities persisted through the root's repository?

If any reference style contradicts the documented or determined aggregate boundary, apply this skill.

## Report the Outcome

When finishing the task:

- state which domain entities were involved and what relationship was identified
- state whether the entities belong to the same aggregate or different aggregates
- state the reference style applied — direct reference or identity reference
- state whether the boundary was already documented, determined objectively, or decided by the human
- state whether the agent instructions file was updated with a new boundary decision
