---
name: business-logic-entry-point-repository-interface
description: Require business-logic entry points to depend on a repository interface rather than a concrete repository implementation. Use when an agent needs to create, modify, review, or interpret how a business-logic entry point references a repository. When the project's programming language supports interfaces, protocols, traits, or abstract types, the entry point must depend on the repository abstraction, not on the concrete implementation. When the language does not support such constructs, this skill does not apply.
---

# Repository Interface for Business Logic Entry Points

## Goal

Business-logic entry points must depend on a repository interface — not on the concrete repository implementation.

When the programming language supports interfaces, protocols, traits, abstract classes, or equivalent abstraction mechanisms, the entry point must reference the repository through that abstraction. The concrete implementation is provided from outside the entry point — through dependency injection, constructor parameters, module-level wiring, or the equivalent pattern used by the project.

This rule decouples the business logic from the persistence implementation. The entry point defines what repository operations it needs; the infrastructure layer decides how those operations are fulfilled.

When the language does not support interfaces or equivalent abstraction mechanisms, this skill does not apply.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a business-logic entry point that uses a repository
- imports or references a repository from a business-logic entry point
- defines how a repository is provided to a business-logic entry point
- introduces a new repository dependency in a business-logic entry point

Do not apply this skill when:

- the programming language does not support interfaces, protocols, traits, or equivalent abstraction mechanisms
- the task only modifies the repository implementation without changing how the entry point depends on it

## The Rule

1. Define a repository interface for each repository.
   - Use the language's idiomatic abstraction mechanism — interface, protocol, trait, abstract class, or equivalent.
   - The interface declares the repository operations using domain-term names and domain types.
   - The interface lives in the business-logic or domain layer, not in the infrastructure or persistence layer.

2. The entry point depends on the interface, not the implementation.
   - The entry point's parameters, constructor arguments, or module-level references must use the repository interface type.
   - The entry point must not import or reference the concrete repository implementation.
   - The entry point must not import or reference persistence-technology modules.

3. The concrete implementation is provided from outside the entry point.
   - The infrastructure or composition layer creates the concrete repository and provides it to the entry point.
   - The wiring mechanism follows the project's conventions — constructor injection, function parameters, module wiring, or equivalent.

4. The concrete implementation satisfies the interface.
   - The repository implementation implements, conforms to, or satisfies the repository interface.
   - The implementation handles persistence-technology details internally — ORM calls, database clients, query builders — without leaking them through the interface.

## Detection Workflow

1. Identify repository dependencies in business-logic entry points.
   - Find imports, parameters, constructor arguments, or references to repositories in entry-point code.

2. Check whether the dependency is on an interface or a concrete implementation.
   - If the entry point references a repository interface type — correct.
   - If the entry point references a concrete repository class, module, or implementation — this skill applies.

3. Check whether a repository interface exists.
   - If an interface exists but the entry point bypasses it, fix the dependency.
   - If no interface exists, create one based on the operations the entry point needs.

4. Check where the concrete implementation is provided.
   - Verify that wiring happens outside the entry point — in a composition root, dependency injection container, or equivalent.

## Writing or Changing Entry Points

1. Define the repository interface if it does not exist.
   - Declare the operations the entry point needs, using domain-term names and domain types.
   - Place the interface in the business-logic or domain layer — alongside or near the entry point, following the project's conventions.

2. Make the entry point depend on the interface.
   - Use the interface type for the repository parameter or dependency.
   - Remove any import of the concrete repository implementation from the entry-point file.

3. Implement the interface in the infrastructure layer.
   - Create or update the concrete repository to satisfy the interface.
   - Keep all persistence-technology details inside the implementation.

4. Wire the concrete implementation to the entry point from outside.
   - Provide the concrete repository to the entry point at the composition level.
   - Follow the project's existing wiring conventions.

## Examples

Interface and entry point depending on it:

```ts
// Repository interface — in the business-logic layer
interface OrderRepository {
  save(transaction: Transaction, order: Order): ResultAsync<Order, RepositoryError>
  findById(transaction: Transaction, orderId: OrderId): ResultAsync<Order, RepositoryError>
}

// Entry point depends on the interface
const createOrderCommandHandler = (
  orderRepository: OrderRepository, // interface, not implementation
) => (command: CreateOrderCommand) => {
  return withTransaction((transaction) =>
    orderRepository.save(transaction, Order.create(command.customerId, command.items))
  )
}
```

```py
# Repository interface — in the business-logic layer
class OrderRepository(Protocol):
    def save(self, tx: Transaction, order: Order) -> Order: ...
    def find_by_id(self, tx: Transaction, order_id: OrderId) -> Order: ...

# Entry point depends on the interface
def create_order_command_handler(
    order_repository: OrderRepository,  # protocol, not implementation
) -> Callable:
    def handler(command: CreateOrderCommand):
        with transaction() as tx:
            order = Order.create(customer_id=command.customer_id, items=command.items)
            return order_repository.save(tx, order)
    return handler
```

```kt
// Repository interface — in the business-logic layer
interface OrderRepository {
    fun save(tx: Transaction, order: Order): Order
    fun findById(tx: Transaction, orderId: OrderId): Order
}

// Entry point depends on the interface
fun createOrderCommandHandler(
    orderRepository: OrderRepository, // interface, not implementation
) = fun(command: CreateOrderCommand): Order {
    return withTransaction { tx ->
        val order = Order.create(customerId = command.customerId, items = command.items)
        orderRepository.save(tx, order)
    }
}
```

Not this — entry point depending on the concrete implementation:

```ts
// Bad: entry point imports and depends on concrete implementation
import { PrismaOrderRepository } from '../infrastructure/prisma-order-repository'

const createOrderCommandHandler = (
  orderRepository: PrismaOrderRepository, // concrete implementation, not interface
) => (command: CreateOrderCommand) => {
  // ...
}
```

## Review Questions

When reading or reviewing code, ask:

- Does the programming language support interfaces, protocols, traits, or equivalent abstractions?
- Does the entry point depend on a repository interface or on a concrete implementation?
- Does the entry point import any concrete repository class or persistence-technology module?
- Is the repository interface defined in the business-logic or domain layer?
- Is the concrete implementation provided to the entry point from outside?

If the entry point depends on a concrete repository implementation in a language that supports interfaces, apply this skill.

## Report the Outcome

When finishing the task:

- state whether the language supports interfaces or equivalent abstraction mechanisms
- state which repository interfaces were created or already existed
- state which entry points were changed to depend on the interface instead of the concrete implementation
- state where the concrete implementation is wired to the entry point
