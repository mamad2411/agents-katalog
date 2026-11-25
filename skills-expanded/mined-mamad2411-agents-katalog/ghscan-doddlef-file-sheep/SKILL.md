# Repo Format Skill

## Purpose

Define a consistent repository implementation pattern for all aggregates in File Sheep.

Applies to each domain module:

- `domain/<aggregate>/repo/<XxxRepo>.kt`
- `domain/<aggregate>/repo/<XxxQueries>.kt`
- `infra/<aggregate>/Jooq<Xxx>Repo.kt`

---

## 1. File Layout

For aggregate `Xxx`:

- `XxxRepo.kt`: domain repository interface
- `XxxQueries.kt`: repository input objects (insert/update/list/delete queries)
- `JooqXxxRepo.kt`: jOOQ implementation

This keeps contract and implementation separated.

---

## 2. Repository Interface Contract

### Rules

- Define only persistence contract.
- Use domain objects as return types where appropriate.
- Use query objects for write methods.
- Prefer explicit names:
  - `selectById`
  - `selectBy...`
  - `insert`
  - `updateById`
  - `deleteById` (if needed)

### Template

```kotlin
interface XxxRepo {
    fun selectById(id: UUID): Xxx?

    fun insert(query: XxxInsertQuery): Int

    fun updateById(id: UUID, query: XxxUpdateQuery): Int
}
```

---

## 3. Query Object Conventions

### Rules

- Use `data class` for repo input objects.
- Use explicit names:
  - `XxxInsertQuery`
  - `XxxUpdateQuery`
  - `XxxListQuery`
  - `XxxDeleteQuery`
- Insert query contains required creation fields and defaults.
- Update query is partial update:
  - mutable fields nullable
  - include `updatedAt` default `OffsetDateTime.now()`
- Avoid long primitive parameter lists in repo methods.

### Template

```kotlin
data class XxxInsertQuery(
    val id: UUID = UUIDGenerator.next(),
    val createdAt: OffsetDateTime = OffsetDateTime.now(),
    val updatedAt: OffsetDateTime = OffsetDateTime.now(),
)

data class XxxUpdateQuery(
    val updatedAt: OffsetDateTime = OffsetDateTime.now(),
)
```

---

## 4. jOOQ Implementation Pattern

### Rules

- Class naming: `JooqXxxRepo`.
- Annotate with `@Repository`.
- Constructor inject `DSLContext`.
- Use generated jOOQ table constants.
- Read path:
  - query jOOQ table
  - map POJO/record to domain via internal mapper
- Write path:
  - build `dsl.newRecord(TABLE)`
  - assign insert fields explicitly
- Partial update:
  - set only non-null fields from update query
  - always set `updatedAt`
  - execute only when `record.modified()` is true

### Template

```kotlin
@Repository
class JooqXxxRepo(
    private val dsl: DSLContext,
) : XxxRepo {

    override fun selectById(id: UUID): Xxx? =
        dsl.selectFrom(XXX_TABLE)
            .where(XXX_TABLE.ID.eq(id))
            .fetchOneInto(P_Xxx::class.java)
            ?.toDomain()

    override fun insert(query: XxxInsertQuery): Int =
        dsl.newRecord(XXX_TABLE)
            .apply {
                this.id = query.id
                this.createdAt = query.createdAt
                this.updatedAt = query.updatedAt
            }
            .let { dsl.insertInto(XXX_TABLE).set(it).execute() }

    override fun updateById(id: UUID, query: XxxUpdateQuery): Int =
        dsl.newRecord(XXX_TABLE)
            .apply {
                set(XXX_TABLE.UPDATED_AT, query.updatedAt)
            }
            .let {
                if (it.modified()) {
                    dsl.update(XXX_TABLE).set(it).where(XXX_TABLE.ID.eq(id)).execute()
                } else {
                    0
                }
            }
}
```

---

## 5. Mapping and Enum Conversion

### Rules

- Keep mapper/converter functions `internal`.
- Keep them near `JooqXxxRepo`.
- Use explicit enum conversion functions:
  - domain -> jOOQ enum
  - jOOQ enum -> domain
- Validate non-nullable domain fields with `requireNotNull`.

### Template

```kotlin
internal fun DomainStatus.toJooq(): E_Status = E_Status.valueOf(name)

internal fun E_Status.toDomain(): DomainStatus = DomainStatus.fromString(name)

internal fun P_Xxx.toDomain(): Xxx =
    Xxx(
        id = requireNotNull(id) { "Xxx id cannot be null" },
        createdAt = requireNotNull(createdAt) { "Xxx createdAt cannot be null" },
        updatedAt = requireNotNull(updatedAt) { "Xxx updatedAt cannot be null" },
    )
```

---

## 6. Layer Boundary Rules

- Repo interface belongs to domain contract package.
- jOOQ implementation belongs to infra package.
- Repo layer does persistence only; no business rules.
- Controller DTOs must not appear in repo APIs.
- Service layer orchestrates business behavior; repo executes storage operations.

---

## 7. Style Checklist

- Explicit imports only (no wildcard imports).
- KDoc on public interfaces/functions and complex mappings.
- `data class` + `val` for immutable query objects.
- 4-space indentation, lines near 120 chars.
- Use interface types in APIs (`List`, `Map`, `Set`).
- Keep naming consistent with `XxxRepo` + `JooqXxxRepo` + `XxxQueries`.

---

## 8. Build and Validation

After creating a new repo module:

1. Run `./gradlew build`
2. If schema changed, run `./gradlew jooqCodegen`
3. Add/extend tests for repo integration and service usage

Use this checklist before merge:

- interface and implementation separated
- no layer leakage
- query object naming consistent
- mapping and enum conversion explicit
- partial update logic safe
