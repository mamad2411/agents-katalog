---
name: business-logic-entry-point-use-repositories
description: Require business-logic entry points to access domain-entity persistence exclusively through repositories. Use when an agent needs to create, modify, review, or interpret business-logic entry points that create, read, or modify domain entities. Entry points must not call the project's ORM, database library, framework persistence API, or any other persistence technology directly. All persistence operations on domain entities must go through a repository.
---

# Use Repositories in Business Logic Entry Points

## Goal

Every business-logic entry point that persists, retrieves, or deletes domain entities must do so exclusively through repositories.

A repository is an abstraction that encapsulates the persistence and retrieval of domain entities. It exposes operations expressed in domain terms — such as save, find, delete — and hides the underlying persistence technology.

Business-logic entry points must not call the project's ORM, database library, framework persistence API, query builder, or any other persistence technology directly. All creation, reading, updating, and deletion of domain entities must go through a repository.

This rule applies regardless of the persistence technology in use: relational databases, document stores, key-value stores, object stores, or any other storage mechanism.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a business-logic entry point that creates, reads, updates, or deletes domain entities
- calls ORM methods, query builders, database clients, or framework persistence APIs directly from a business-logic entry point
- imports or references persistence-technology modules directly from a business-logic entry point
- bypasses a repository to perform domain-entity persistence operations inline

## The Rule

1. Access domain-entity persistence only through repositories.
   - Use a repository to create, read, update, and delete domain entities.
   - Do not call ORM methods, query builders, raw SQL, database clients, or framework persistence APIs from business-logic entry points.
   - Do not import or reference persistence-technology modules from business-logic entry points.

2. Repositories expose domain-term operations.
   - Repository method names must express domain intent: `save`, `findById`, `findByEmail`, `delete`, `existsWithName`.
   - Repository method signatures must use domain-entity types and domain value types, not persistence-layer types.

3. One repository per domain entity or aggregate.
   - Each domain entity or aggregate root has its own repository.
   - Do not create generic or catch-all repositories that operate on multiple unrelated entities.

4. The entry point depends on the repository, not on the persistence technology.
   - The entry point receives or references the repository, not the ORM, database client, or connection.
   - Transaction management at the entry-point level is a separate concern and is allowed alongside repository usage when another skill requires it.

## Detection Workflow

1. Find business-logic entry points that persist, retrieve, or delete domain entities.
   - Identify command handlers, query handlers, use cases, or application services that create, read, update, or delete domain entities.

2. Check for direct persistence-technology usage.
   - Look for imports of ORM modules, database client libraries, query builders, or framework persistence APIs in entry-point files.
   - Look for direct calls to ORM methods such as `create`, `findOne`, `query`, `exec`, `save`, `update`, `destroy`, `insert`, `select`, or their equivalents in the project's persistence technology.
   - Look for raw SQL strings, query builder chains, or database client method calls in entry-point code.

3. Check for repository usage.
   - Verify that a repository is used for every domain-entity persistence operation.
   - Verify that the repository exposes domain-term operations, not persistence-technology passthrough methods.

4. Check repository method signatures.
   - Verify that repository methods accept and return domain-entity types and domain value types.
   - Flag methods that expose persistence-layer types such as ORM entities, database records, row objects, or document models in their signatures.

## Writing or Changing Entry Points

1. Identify the domain entities involved.
   - Determine which domain entities the entry point needs to create, read, update, or delete.

2. Use or create a repository for each domain entity.
   - If a repository already exists, use it.
   - If no repository exists, create one that exposes the needed operations in domain terms.
   - Follow the project's existing convention for repository placement, naming, and structure.

3. Replace direct persistence-technology calls with repository calls.
   - Replace ORM calls, query builder chains, raw queries, and database client calls with repository method calls.
   - Remove persistence-technology imports from the entry-point file.

4. Pass transaction context through the repository when needed.
   - If the entry point manages a transaction, pass the transaction context to the repository so it participates in the same transaction.
   - The repository receives the transaction context but does not own or manage the transaction lifecycle.

## Examples

Use this:

```ts
const createOrderCommandHandler = (
  command: CreateOrderCommand,
): ResultAsync<CreateOrderCommandHandlerSuccess, CreateOrderCommandHandlerError> => {
  return withTransaction((transaction) =>
    ensureRequesterIsAuthenticated(command.requesterId)
      .andThen((requesterId) =>
        orderRepository.save(transaction, order)
      )
  )
}
```

Not this:

```ts
const createOrderCommandHandler = (
  command: CreateOrderCommand,
): ResultAsync<CreateOrderCommandHandlerSuccess, CreateOrderCommandHandlerError> => {
  return withTransaction((transaction) =>
    ensureRequesterIsAuthenticated(command.requesterId)
      .andThen((requesterId) =>
        prisma.order.create({ data: { /* ... */ } })
      )
  )
}
```

Use this:

```py
def find_customer_by_id_query_handler(
    query: FindCustomerByIdQuery,
) -> FindCustomerByIdQueryHandlerSuccess:
    with transaction() as tx:
        customer = customer_repository.find_by_id(tx, query.customer_id)
        return FindCustomerByIdQueryHandlerSuccess(customer=customer)
```

Not this:

```py
def find_customer_by_id_query_handler(
    query: FindCustomerByIdQuery,
) -> FindCustomerByIdQueryHandlerSuccess:
    with transaction() as tx:
        customer = session.query(CustomerModel).filter_by(id=query.customer_id).first()
        return FindCustomerByIdQueryHandlerSuccess(customer=customer)
```

Use this:

```kt
fun cancelSubscriptionCommandHandler(
    command: CancelSubscriptionCommand,
): CancelSubscriptionCommandHandlerSuccess {
    return withTransaction { tx ->
        val subscription = subscriptionRepository.findById(tx, command.subscriptionId)
        subscription.cancel()
        subscriptionRepository.save(tx, subscription)
    }
}
```

Not this:

```kt
fun cancelSubscriptionCommandHandler(
    command: CancelSubscriptionCommand,
): CancelSubscriptionCommandHandlerSuccess {
    return withTransaction { tx ->
        val entity = entityManager.find(SubscriptionEntity::class.java, command.subscriptionId)
        entity.status = "cancelled"
        entityManager.merge(entity)
    }
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this entry point create, read, update, or delete domain entities?
- Does it use a repository for every domain-entity persistence operation?
- Does it import or call any ORM, database client, query builder, or framework persistence API directly?
- Do the repository methods use domain-term names and domain-entity types in their signatures?
- Is the persistence technology hidden behind the repository abstraction?

If any entry point accesses domain-entity persistence without going through a repository, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or changed
- state which repositories were used or created
- state which direct persistence-technology calls were replaced with repository calls
- state which persistence-technology imports were removed from entry-point files
