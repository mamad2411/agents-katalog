---
name: business-logic-entry-point-repository-operations
description: Require repository interfaces to expose a standard set of operations with specific signatures and naming conventions. Use when an agent needs to create, modify, review, or interpret repository interfaces used by business-logic entry points. Repositories must offer findById, create (returns created entity), update (returns updated entity), search (returns collection), and deleteById (returns nothing). Do not use a generic "save" operation — always distinguish between create and update explicitly.
---

# Repository Operations for Business Logic Entry Points

## Goal

Repository interfaces must expose a standard set of operations with clear naming, explicit intent, and predictable return types.

Each operation must make its purpose unambiguous. A caller reading the repository interface must know immediately whether it is creating a new entity, updating an existing one, retrieving one by identity, searching for several by criteria, or deleting one by identity.

Do not use a generic `save` operation. Always distinguish between `create` and `update` explicitly so the caller's intent is never ambiguous.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a repository interface or repository class
- defines repository method signatures for domain-entity persistence operations
- introduces a `save` method that handles both creation and update
- defines find, search, create, update, or delete operations on a repository

## The Operations

### 1. findById

Retrieves a single domain entity by its identity.

- Name: `findById` or the project's idiomatic equivalent (e.g., `find_by_id`).
- Parameter: the entity's identity value.
- Returns: the domain entity.
- When the entity does not exist, use the project's error or absence convention (e.g., error type, exception, null, optional).

### 2. create

Persists a new domain entity and returns the created entity.

- Name: `create` or the project's idiomatic equivalent.
- Parameter: the domain entity to persist.
- Returns: the created domain entity.
- The returned entity must reflect the state after persistence, including any identity or field assigned during creation.

### 3. update

Persists changes to an existing domain entity and returns the updated entity.

- Name: `update` or the project's idiomatic equivalent.
- Parameter: the domain entity with updated state.
- Returns: the updated domain entity.
- The returned entity must reflect the state after persistence.

### 4. search

Retrieves a collection of domain entities matching a combination of filter clauses. Search operations also support pagination and sorting.

- Name: `search` or the project's idiomatic equivalent.
- Parameters: a list of filter clauses, pagination parameters (page number and page size), and a list of sort clauses.
- Returns: a paginated result containing the collection of domain entities and the total count of matching entities.
- When no entities match, return a paginated result with an empty collection and a total count of zero, not an error or absence value.
- One `search` method per repository. Express filter criteria as filter clauses that reference an attribute, a comparison operator, and a value. This avoids creating a separate method for each filter combination.

The search operation combines filtering, pagination, and sorting in a single method:

- **Filtering**: a list of filter clauses, each referencing an attribute of the domain entity, a comparison operator (e.g., `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `contains`), and a value. This allows the caller to filter by any combination of attributes without requiring a dedicated method for each combination.
- **Pagination**: a page number and a page size. The return type must include both the collection of domain entities and the total count of matching entities so the caller can compute the total number of pages.
- **Sorting**: a list of sort clauses, each specifying an attribute name and a direction (ascending or descending). Accept a list of sort clauses to support multi-attribute sorting.

### 5. deleteById

Removes a domain entity by its identity.

- Name: `deleteById` or the project's idiomatic equivalent (e.g., `delete_by_id`).
- Parameter: the entity's identity value.
- Returns: nothing (void, unit, `None`, or the project's empty equivalent).

## The No-Save Rule

Do not define a `save` operation on repositories.

- `save` is ambiguous: it does not communicate whether the caller intends to create a new entity or update an existing one.
- Always use `create` for new entities and `update` for existing entities.
- If the project already has `save` methods, do not spread the pattern. When creating or modifying repository interfaces, use `create` and `update` instead.

## Detection Workflow

1. Find repository interfaces and classes.
   - Identify repositories used by business-logic entry points.

2. Check for a `save` method.
   - Flag any repository that defines a `save`, `persist`, `upsert`, or similarly ambiguous method that conflates creation and update.

3. Check each operation against the standard.
   - Verify `findById` exists and returns a single domain entity.
   - Verify `create` exists, accepts a domain entity, and returns the created entity.
   - Verify `update` exists, accepts a domain entity, and returns the updated entity.
   - Verify the `search` method accepts filter clauses, pagination parameters, and sort clauses.
   - Verify the `search` method returns a paginated result with the collection and the total count.
   - Verify `deleteById` exists, accepts an identity value, and returns nothing.

4. Check return types.
   - Verify `create` and `update` return the domain entity, not void or an ID.
   - Verify `deleteById` returns nothing, not the deleted entity.
   - Verify the `search` method returns a paginated result, not a bare collection, a single entity, or null.

## Writing or Changing Repository Interfaces

1. Define the operations the entry point needs.
   - Start from the business-logic entry point's requirements.
   - Add only the operations that are needed. Not every repository needs every operation.

2. Name each operation explicitly.
   - Use `create`, not `save`, when persisting a new entity.
   - Use `update`, not `save`, when persisting changes to an existing entity.
   - Use `findById` for identity-based retrieval.
   - Use `search` for criteria-based retrieval with filtering, pagination, and sorting.
   - Use `deleteById` for identity-based deletion.

3. Follow the project's naming convention.
   - Adapt to the project's casing style: `findById`, `find_by_id`, `FindById`.
   - Adapt to the project's collection types, error handling, and return conventions.

4. Add operations incrementally.
   - Add a repository operation only when a business-logic entry point needs it.
   - Do not pre-populate repositories with operations that no entry point uses yet.

## Examples

TypeScript:

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

type PaginatedResult<T> = {
  items: T[]
  totalCount: number
}

interface OrderRepository {
  findById(transaction: Transaction, orderId: OrderId): ResultAsync<Order, OrderNotFoundError>
  create(transaction: Transaction, order: Order): ResultAsync<Order, RepositoryError>
  update(transaction: Transaction, order: Order): ResultAsync<Order, RepositoryError>
  search(
    transaction: Transaction,
    filters: FilterClause<Order>[],
    pageNumber: number,
    pageSize: number,
    sortBy: SortClause<Order>[],
  ): ResultAsync<PaginatedResult<Order>, RepositoryError>
  deleteById(transaction: Transaction, orderId: OrderId): ResultAsync<void, RepositoryError>
}
```

Not this:

```ts
interface OrderRepository {
  save(transaction: Transaction, order: Order): ResultAsync<Order, RepositoryError>
}
```

Python:

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
class PaginatedResult(Generic[T]):
    items: list[T]
    total_count: int

class OrderRepository(Protocol):
    def find_by_id(self, tx: Transaction, order_id: OrderId) -> Order: ...
    def create(self, tx: Transaction, order: Order) -> Order: ...
    def update(self, tx: Transaction, order: Order) -> Order: ...
    def search(
        self,
        tx: Transaction,
        filters: list[FilterClause[Order]],
        page_number: int,
        page_size: int,
        sort_by: list[SortClause[Order]],
    ) -> PaginatedResult[Order]: ...
    def delete_by_id(self, tx: Transaction, order_id: OrderId) -> None: ...
```

Not this:

```py
class OrderRepository(Protocol):
    def save(self, tx: Transaction, order: Order) -> Order: ...
```

Kotlin:

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

data class PaginatedResult<T>(
    val items: List<T>,
    val totalCount: Int,
)

interface OrderRepository {
    fun findById(tx: Transaction, orderId: OrderId): Order
    fun create(tx: Transaction, order: Order): Order
    fun update(tx: Transaction, order: Order): Order
    fun search(
        tx: Transaction,
        filters: List<FilterClause<Order>>,
        pageNumber: Int,
        pageSize: Int,
        sortBy: List<SortClause<Order>>,
    ): PaginatedResult<Order>
    fun deleteById(tx: Transaction, orderId: OrderId)
}
```

Not this:

```kt
interface OrderRepository {
    fun save(tx: Transaction, order: Order): Order
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this repository define a `save` method? If so, replace it with explicit `create` and `update`.
- Does `create` return the created domain entity?
- Does `update` return the updated domain entity?
- Does `deleteById` return nothing?
- Does the `search` method accept filter clauses, pagination parameters, and sort clauses?
- Does the `search` method return a paginated result with both the collection and the total count?
- Does `findById` return a single domain entity with proper absence handling?

If any repository operation violates these conventions, apply this skill.

## Report the Outcome

When finishing the task:

- state which repository interfaces were identified or changed
- state which operations were added, renamed, or corrected
- state whether any `save` method was split into `create` and `update`
- state which return types were corrected to match the expected convention
