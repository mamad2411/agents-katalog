---
name: business-logic-entry-point-database-transaction
description: Require every business-logic entry point to wrap its entire flow in a database transaction using the project's library, framework, or ORM, when the underlying persistence technology supports transactions. Use when an agent needs to create, modify, review, or interpret business-logic entry points that interact with a database. The transaction must encompass the full entry-point flow, including business constraints, business operations, and persistence, so that the entire flow succeeds or fails atomically.
---

# Database Transaction for Business Logic Entry Points

## Goal

Every business-logic entry point that interacts with a database must wrap its entire flow in a single database transaction, when the underlying persistence technology supports transactions.

Use the project's existing library, framework, or ORM to open and manage the transaction. Do not introduce a custom transaction mechanism when the project stack already provides one.

The transaction must encompass the full entry-point flow: business constraints, business rules, business operations, and persistence. The entire flow succeeds or fails atomically.

If the persistence technology does not support transactions (e.g., some NoSQL databases, object stores, or file-based storage), this skill does not apply.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a business-logic entry point that reads from or writes to a database
- executes multiple database operations within a single entry point without a wrapping transaction
- partially wraps some operations in a transaction while leaving others outside
- manages transaction boundaries inside inner helpers rather than at the entry-point level

## The Rule

1. Wrap the entire entry-point flow in a single database transaction.
   - The transaction begins before any business constraint that accesses the database.
   - The transaction commits only after the entire flow completes successfully.
   - The transaction rolls back if any step fails.

2. Use the project's transaction mechanism.
   - Use the library, framework, or ORM that the project already uses for database access.
   - Follow the project's idiomatic pattern for transaction management, whether that is a decorator, context manager, callback, wrapper function, or explicit begin/commit/rollback.

3. Place the transaction boundary at the entry point, not inside inner helpers.
   - The entry point owns the transaction.
   - Inner helpers, business constraints, and persistence functions participate in the transaction but do not open their own.
   - Do not nest independent transactions within the same entry-point flow.

4. Include all database-accessing steps in the transaction.
   - Business constraints that query the database to verify preconditions must run inside the transaction.
   - Persistence operations that store or update data must run inside the transaction.
   - Read operations that inform business decisions must run inside the transaction.

## Detection Workflow

1. Find business-logic entry points that access a database.
   - Identify command handlers, query handlers, use cases, or application services that read from or write to a database.

2. Check for a wrapping transaction.
   - Verify that a transaction is opened at the entry-point level.
   - Verify that the transaction encompasses the entire flow.

3. Check for partial or misplaced transactions.
   - Look for transactions opened inside inner helpers rather than at the entry point.
   - Look for database operations that execute outside the transaction boundary.

4. Check the transaction mechanism.
   - Verify that the project's existing library, framework, or ORM is used.
   - Verify that the pattern is idiomatic for the project.

## Writing or Changing Entry Points

1. Open the transaction at the entry point.
   - Use the project's idiomatic transaction pattern.
   - Ensure the transaction wraps the first database-accessing step through the last.

2. Pass the transaction context to inner helpers.
   - If the project's transaction mechanism requires an explicit connection, session, or context object, pass it from the entry point to inner functions.
   - If the project uses implicit transaction propagation (e.g., thread-local, async context), verify that inner helpers participate in the same transaction.

3. Commit on success, rollback on failure.
   - Let the transaction mechanism handle commit and rollback based on the entry-point outcome.
   - Do not manually commit partway through the flow.

4. Do not suppress transaction errors.
   - If the commit fails, propagate the error through the entry point's error convention.

## Examples

TypeScript with a transaction wrapper:

```ts
const createReservationCommandHandler = (
  command: CreateReservationCommand,
): ResultAsync<CreateReservationCommandHandlerSuccess, CreateReservationCommandHandlerError> => {
  return withTransaction((transaction) =>
    ensureRequesterIsAuthenticated(command.requesterId)
      .andThen((requesterId) =>
        ensureAvailableCars(transaction, command.carClass)
      )
      .andThen(() =>
        persistReservation(transaction, reservation)
      )
  )
}
```

Python with a context manager:

```py
def create_reservation_command_handler(
    command: CreateReservationCommand,
) -> CreateReservationCommandHandlerSuccess:
    with transaction() as tx:
        requester_id = ensure_requester_is_authenticated(command.requester_id)
        ensure_available_cars(tx, command.car_class)
        return persist_reservation(tx, reservation)
```

Kotlin with a framework transaction:

```kt
fun createReservationCommandHandler(
    command: CreateReservationCommand,
): CreateReservationCommandHandlerSuccess {
    return withTransaction { tx ->
        val requesterId = ensureRequesterIsAuthenticated(command.requesterId)
        ensureAvailableCars(tx, command.carClass)
        persistReservation(tx, reservation)
    }
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this entry point access a database?
- Is the entire flow wrapped in a single transaction?
- Is the transaction opened at the entry-point level, not inside inner helpers?
- Do all database-accessing steps, including business constraints, run inside the transaction?
- Is the project's existing transaction mechanism used?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or changed
- state how the transaction wraps the entire entry-point flow
- state which transaction mechanism from the project stack was used
- state whether any database-accessing steps were moved inside the transaction boundary
