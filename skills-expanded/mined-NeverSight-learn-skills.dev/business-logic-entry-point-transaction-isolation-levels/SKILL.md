---
name: business-logic-entry-point-transaction-isolation-levels
description: Set transaction isolation levels for business-logic entry points when Command-Query Separation and database transactions are both in use and the underlying persistence technology supports configurable isolation levels. Use when an agent needs to create, modify, review, or interpret the isolation level of a database transaction at a business-logic entry point that follows CQS. Query handlers must use the least blocking isolation level available in the project's database. Command handlers must use REPEATABLE READ isolation level.
---

# Transaction Isolation Levels for Business Logic Entry Points

## Goal

When a business-logic entry point wraps its flow in a database transaction and follows Command-Query Separation, set the transaction isolation level based on whether the entry point is a command handler or a query handler, when the underlying persistence technology supports configurable isolation levels.

- Query handlers use the least blocking isolation level available in the project's database.
- Command handlers use REPEATABLE READ.

If the persistence technology does not support configurable isolation levels, this skill does not apply.

## When This Skill Applies

This skill activates only when all four conditions are met:

1. The entry point is a business-logic entry point.
2. The entry point wraps its flow in a database transaction.
3. The underlying persistence technology supports configurable isolation levels.
4. The entry point follows Command-Query Separation, so it is classified as either a command handler or a query handler.

If any of these conditions is not met, this skill does not apply.

## The Rule

1. Query handlers must use the least blocking isolation level available.
   - Use READ UNCOMMITTED if the database supports it.
   - If READ UNCOMMITTED is not available, use READ COMMITTED.
   - If neither is available, use the lowest isolation level the database provides.
   - The goal is to minimize locking and contention for read-only operations.

2. Command handlers must use REPEATABLE READ.
   - Set the isolation level to REPEATABLE READ explicitly.
   - This ensures that data read during business constraints and business decisions remains stable throughout the transaction, preventing non-repeatable reads between the constraint checks and the state changes.

3. Set the isolation level when opening the transaction.
   - Use the project's library, framework, or ORM to specify the isolation level at transaction creation time.
   - Do not change the isolation level mid-transaction.

4. Follow the database's naming conventions for isolation levels.
   - Use the exact isolation level name or constant that the project's database and library expect.
   - Map the conceptual levels (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ) to the project's specific syntax.

## Examples

TypeScript with a transaction wrapper:

```ts
// Query handler — least blocking isolation level
const findReservationByIdQueryHandler = (
  query: FindReservationByIdQuery,
): ResultAsync<FindReservationByIdQueryHandlerSuccess, FindReservationByIdQueryHandlerError> => {
  return withTransaction({ isolationLevel: 'READ UNCOMMITTED' }, (transaction) =>
    ensureRequesterIsAuthenticated(query.requesterId)
      .andThen((requesterId) =>
        findReservationById(transaction, query.reservationId)
      )
  )
}

// Command handler — REPEATABLE READ
const createReservationCommandHandler = (
  command: CreateReservationCommand,
): ResultAsync<CreateReservationCommandHandlerSuccess, CreateReservationCommandHandlerError> => {
  return withTransaction({ isolationLevel: 'REPEATABLE READ' }, (transaction) =>
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
# Query handler — least blocking isolation level
def find_reservation_by_id_query_handler(
    query: FindReservationByIdQuery,
) -> FindReservationByIdQueryHandlerSuccess:
    with transaction(isolation_level="READ UNCOMMITTED") as tx:
        requester_id = ensure_requester_is_authenticated(query.requester_id)
        return find_reservation_by_id(tx, query.reservation_id)

# Command handler — REPEATABLE READ
def create_reservation_command_handler(
    command: CreateReservationCommand,
) -> CreateReservationCommandHandlerSuccess:
    with transaction(isolation_level="REPEATABLE READ") as tx:
        requester_id = ensure_requester_is_authenticated(command.requester_id)
        ensure_available_cars(tx, command.car_class)
        return persist_reservation(tx, reservation)
```

Kotlin with a framework transaction:

```kt
// Query handler — least blocking isolation level
fun findReservationByIdQueryHandler(
    query: FindReservationByIdQuery,
): FindReservationByIdQueryHandlerSuccess {
    return withTransaction(isolationLevel = IsolationLevel.READ_UNCOMMITTED) { tx ->
        val requesterId = ensureRequesterIsAuthenticated(query.requesterId)
        findReservationById(tx, query.reservationId)
    }
}

// Command handler — REPEATABLE READ
fun createReservationCommandHandler(
    command: CreateReservationCommand,
): CreateReservationCommandHandlerSuccess {
    return withTransaction(isolationLevel = IsolationLevel.REPEATABLE_READ) { tx ->
        val requesterId = ensureRequesterIsAuthenticated(command.requesterId)
        ensureAvailableCars(tx, command.carClass)
        persistReservation(tx, reservation)
    }
}
```

## Detection Workflow

1. Confirm all three activation conditions.
   - The entry point is a business-logic entry point.
   - It wraps its flow in a database transaction.
   - It follows Command-Query Separation.

2. Classify the entry point as a command handler or a query handler.
   - Use the CQS classification from the project or from the CQS skill.

3. Check the current isolation level.
   - Verify that query handlers use the least blocking level available.
   - Verify that command handlers use REPEATABLE READ.

4. Check that the isolation level is set at transaction creation time.
   - Verify that it is not changed mid-transaction.
   - Verify that the project's library or ORM syntax is used correctly.

## Writing or Changing Entry Points

1. Determine the CQS role first.
   - Classify the entry point as a command handler or a query handler.

2. Set the isolation level accordingly.
   - Query handler: use the least blocking isolation level the database supports.
   - Command handler: use REPEATABLE READ.

3. Specify the isolation level at transaction creation.
   - Use the project's idiomatic way to set isolation levels.
   - Do not rely on database-level defaults unless they match the required level.

## Review Questions

When reading or reviewing code, ask:

- Is this entry point a command handler or a query handler under CQS?
- Does it wrap its flow in a database transaction?
- Is the isolation level set explicitly at transaction creation time?
- Does a query handler use the least blocking isolation level available?
- Does a command handler use REPEATABLE READ?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or changed
- state whether each is a command handler or a query handler
- state which isolation level was set for each
- state which database and transaction mechanism were used
