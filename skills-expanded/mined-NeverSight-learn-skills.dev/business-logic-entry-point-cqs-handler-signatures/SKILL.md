---
name: business-logic-entry-point-cqs-handler-signatures
description: Enforce a signature pattern for business-logic entry points when Command-Query Separation is being followed. Use when an agent needs to create, modify, review, or interpret command handlers or query handlers at business-logic entry points. Name handlers with an infinitive plus a command-handler or query-handler suffix adapted to the language style, accept exactly one parameter named `command` or `query`, always wrap input values in a dedicated `...Command` or `...Query` type, return the project's empty equivalent for successful non-create command handlers, return a `...CommandHandlerSuccess` type for successful create command handlers, and return a `...QueryHandlerSuccess` type for successful query handlers.
---

# CQS Handler Signatures for Business Logic Entry Points

## Goal

Apply a consistent signature pattern to business-logic entry points when Command-Query Separation is already the governing design rule.

This skill refines the shape of command handlers and query handlers. It does not replace the underlying CQS rule. Keep using the CQS distinction between commands and queries, then apply this signature convention on top of it.

## Core Naming Rule

Name the entry point with:

- an infinitive verb
- the suffix `command handler` for commands
- the suffix `query handler` for queries

Translate that pattern into the syntax and style of the language in use.

Examples:

- `createReservationCommandHandler`
- `approveOrderCommandHandler`
- `findReservationByIdQueryHandler`
- `searchAvailableCarsQueryHandler`
- `create_reservation_command_handler`
- `approve_order_command_handler`

## Parameter Rule

Every handler must accept exactly one parameter.

- For commands, the parameter must be named `command`.
- For queries, the parameter must be named `query`.

Always define a `...Command` or `...Query` type and use it as that single parameter, even when the handler currently needs only one input value.

Examples:

```ts
type CreateReservationCommand = {
  requesterId: RequesterId
  carClass: CarClass
  startsAt: ZonedDateTime
  endsAt: ZonedDateTime
}

const createReservationCommandHandler = (
  command: CreateReservationCommand,
): Promise<CreateReservationCommandHandlerSuccess> => {
  // ...
}
```

```py
@dataclass(frozen=True)
class FindReservationByIdQuery:
    reservation_id: ReservationId

def find_reservation_by_id_query_handler(
    query: FindReservationByIdQuery,
) -> FindReservationByIdQueryHandlerSuccess:
    ...
```

## Success Return Type Rule

On successful completion, use these return shapes:

- non-create command handlers return the project's empty equivalent directly
- create command handlers return a `...CommandHandlerSuccess` type
- query handlers return a `...QueryHandlerSuccess` type

Use a named success type whenever the handler is allowed to return business data. The purpose is to keep the signature stable and consistent if the success result later needs to carry a more complex object with multiple fields.

### Command Success Types

For command handlers:

- keep the success return shape aligned with CQS
- do not return business data from non-create commands
- for non-create commands, return the project's empty equivalent directly
- for create commands, include only the ID or IDs of the created domain entities

Examples:

```ts
type ApproveOrderCommand = {
  orderId: OrderId
  approverId: UserId
}

const approveOrderCommandHandler = (
  command: ApproveOrderCommand,
): Promise<void> => {
  // ...
}
```

```kt
data class ApproveOrderCommand(
    val orderId: OrderId,
    val approverId: UserId,
)

fun approveOrderCommandHandler(
    command: ApproveOrderCommand,
): Unit {
    // ...
}
```

```ts
type CreateOrderCommand = {
  customerId: CustomerId
  lines: OrderLineDraft[]
}

type CreateOrderCommandHandlerSuccess = {
  orderId: OrderId
}

const createOrderCommandHandler = (
  command: CreateOrderCommand,
): Promise<CreateOrderCommandHandlerSuccess> => {
  // ...
}
```

If one create command creates more than one domain entity, the success type may contain only those created IDs.

### Query Success Types

For query handlers:

- return the requested business data inside a `...QueryHandlerSuccess` type
- keep the query parameter grouped inside a single `...Query` type

Example:

```ts
type FindOrderByIdQuery = {
  orderId: OrderId
}

type FindOrderByIdQueryHandlerSuccess = {
  order: Order
}

const findOrderByIdQueryHandler = (
  query: FindOrderByIdQuery,
): Promise<FindOrderByIdQueryHandlerSuccess> => {
  // ...
}
```

### Query Handlers with Filtering, Pagination, and Sorting

A query handler may support filtering, pagination, and sorting when the business-logic entry point requires searching for a collection of domain entities. In that case:

- The `...Query` type includes a list of filter clauses, pagination parameters, and a list of sort clauses as explicit fields.
- The `...QueryHandlerSuccess` type includes the collection of domain entities and the total count of matching entities so the caller can compute the total number of pages.

Express filter criteria as a list of filter clauses, each referencing an attribute of the domain entity, a comparison operator, and a value. This allows a single search query handler per domain entity that accepts any combination of filters, instead of requiring a separate handler for each filter combination. Pagination is expressed as page number and page size. Sorting is a list of sort clauses, each with an attribute name and a direction (ascending or descending), supporting multi-attribute sorting.

Example:

```ts
type SortDirection = 'asc' | 'desc'

type SortClause<T> = {
  attribute: keyof T
  direction: SortDirection
}

type FilterOperator = 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'contains'

type FilterClause<T> = {
  attribute: keyof T
  operator: FilterOperator
  value: unknown
}

type SearchOrdersQuery = {
  filters: FilterClause<Order>[]
  pageNumber: number
  pageSize: number
  sortBy: SortClause<Order>[]
}

type SearchOrdersQueryHandlerSuccess = {
  orders: Order[]
  totalCount: number
}

const searchOrdersQueryHandler = (
  query: SearchOrdersQuery,
): Promise<SearchOrdersQueryHandlerSuccess> => {
  // ...
}
```

```py
@dataclass(frozen=True)
class SortClause(Generic[T]):
    attribute: str
    direction: Literal["asc", "desc"]

@dataclass(frozen=True)
class FilterClause(Generic[T]):
    attribute: str
    operator: Literal["eq", "neq", "gt", "gte", "lt", "lte", "contains"]
    value: object

@dataclass(frozen=True)
class SearchOrdersQuery:
    filters: list[FilterClause[Order]]
    page_number: int
    page_size: int
    sort_by: list[SortClause[Order]]

@dataclass(frozen=True)
class SearchOrdersQueryHandlerSuccess:
    orders: list[Order]
    total_count: int

def search_orders_query_handler(
    query: SearchOrdersQuery,
) -> SearchOrdersQueryHandlerSuccess:
    ...
```

```kt
enum class SortDirection { ASC, DESC }

data class SortClause<T>(
    val attribute: String,
    val direction: SortDirection,
)

enum class FilterOperator { EQ, NEQ, GT, GTE, LT, LTE, CONTAINS }

data class FilterClause<T>(
    val attribute: String,
    val operator: FilterOperator,
    val value: Any,
)

data class SearchOrdersQuery(
    val filters: List<FilterClause<Order>>,
    val pageNumber: Int,
    val pageSize: Int,
    val sortBy: List<SortClause<Order>>,
)

data class SearchOrdersQueryHandlerSuccess(
    val orders: List<Order>,
    val totalCount: Int,
)

fun searchOrdersQueryHandler(
    query: SearchOrdersQuery,
): SearchOrdersQueryHandlerSuccess {
    // ...
}
```

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a business-logic command handler or query handler
- changes the signature of a business-logic entry point already governed by CQS
- passes one or more raw input values directly instead of using a `...Command` or `...Query` type
- returns raw domain data directly instead of the required success shape
- names a CQS entry point without the required handler suffix pattern

## Signature Rule

1. Use an infinitive plus handler suffix adapted to the local language style.
   - Translate `... command handler` and `... query handler` into the project's casing and syntax conventions.
   - Keep the verb in infinitive form.

2. Accept exactly one parameter.
   - Name it `command` for commands.
   - Name it `query` for queries.
   - Always use a dedicated `...Command` or `...Query` type, even when there is only one input field.

3. Return a dedicated success type.
   - Use the project's empty equivalent for non-create commands.
   - Use `...CommandHandlerSuccess` for create commands.
   - Use `...QueryHandlerSuccess` for queries.
   - Do not return raw tuples, domain entities, DTOs, or anonymous objects directly from a success path that is required to use a named success type.

4. Keep success types aligned with CQS semantics.
   - Non-create commands must use the project's empty equivalent directly.
   - Non-create commands must not expose business data through a named success type or any other success payload.
   - Create commands may expose only the created entity ID or IDs.
   - Queries may expose the requested read data through their success type.

## Detection Workflow

1. Confirm that the entry point is under CQS.
   - Determine whether the entry point is already classified as a command or a query.
   - Apply this skill only after that role is clear.

2. Inspect the current signature shape.
   - Check the handler name.
   - Check the number and names of parameters.
   - Check whether the handler uses a dedicated `...Command` or `...Query` type even when only one input value exists.
   - Check whether success returns the correct shape for its role: empty equivalent, `...CommandHandlerSuccess`, or `...QueryHandlerSuccess`.

3. Check the success payload against CQS.
   - Verify that non-create command handlers return the project's empty equivalent and do not leak forbidden business data.
   - Verify that create command handlers use `...CommandHandlerSuccess` and contain only created IDs.
   - Verify that query success types wrap the requested data coherently.

## Writing or Changing Handler Signatures

1. Name the handler first.
   - Choose the infinitive verb.
   - Add the command-handler or query-handler suffix in the local style.

2. Define the single input type.
   - Create a `...Command` or `...Query` type in all cases.
   - Pass that type as the only handler parameter, even when it currently wraps just one field.

3. Define the success type explicitly.
   - Create a `...CommandHandlerSuccess` type for create commands.
   - Create a `...QueryHandlerSuccess` type for queries.
   - Keep named success types reusable instead of returning ad hoc inline objects when a named success type is required.

4. Preserve CQS semantics.
   - Keep non-create command handlers on the project's empty equivalent when no business data may be returned.
   - Keep create command success types limited to created IDs.
   - Keep query success types focused on requested read data.

## Review Questions

When reading or reviewing code, ask:

- Is this handler already classified as a command or a query under CQS?
- Is the name an infinitive plus the correct handler suffix in the local style?
- Does it accept exactly one parameter named `command` or `query`?
- Does it always use a `...Command` or `...Query` type, even when there is only one input field?
- Does success use the correct shape for its role under CQS?
- If this is a non-create command handler, does it return the project's empty equivalent directly?
- If this is a create command handler, does it return `...CommandHandlerSuccess` with only created IDs?
- If this is a search query handler, does the `...Query` type include filter clauses, pagination parameters, and sort clauses as explicit fields?
- If this is a search query handler, does the `...QueryHandlerSuccess` type include both the collection and the total count?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which handlers were identified or changed
- state which `...Command`, `...Query`, `...CommandHandlerSuccess`, or `...QueryHandlerSuccess` types were introduced or updated
- state how the signature was adapted to the local language style
- state how the success payload remains aligned with CQS
