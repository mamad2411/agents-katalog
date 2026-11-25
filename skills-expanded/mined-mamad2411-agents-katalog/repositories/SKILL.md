---
name: repositories
description: "[Pragmatic DDD Architecture] Guide for creating DDD Repositories (Interfaces and Infrastructure). Use when creating repository contracts or implementing them using Drizzle ORM, Zod, and Postgres. Enforces completely typed transactions with Drizzle Transaction types (no 'unknown'), Result returns for Railway-oriented programming via neverthrow, and mapping pg node errors to domain errors. Fits our docker-compose / drizzle-kit standard testing workflow."
---

# Repositories

This skill documents how to structure **Repository Interfaces** in the Domain and **Concrete Implementations** in Infrastructure using our tightly coupled stack: `drizzle-orm`, `node-postgres`, `drizzle-kit`, and Railway-Oriented Programming (`neverthrow`).

**DEPENDENCY NOTICE**: This skill works in tandem with the `use-cases` skill. Review both when managing vertical slices of domain logic.

## 1. RFC 2119 Language

This skill uses RFC 2119 keywords for precise requirement specification:
- **MUST** / **MUST NOT**: Mandatory requirements. Violations break correctness or security.
- **SHOULD** / **SHOULD NOT**: Strong recommendations. Only deviate with documented justification.

## 2. File Location & Naming

**Interfaces** 
- Location: `src/<context>/domain/interfaces/`
- Naming: File named `entityRepository.ts` containing the inner `EntityRepository` class.

**Implementations**
- Location: `src/<context>/infrastructure/`
- Naming: `postgresEntityRepository.ts`

## 3. Defining the Domain Interface

**Reference**: `references/examples/repository-interface-example.md`

- **MUST**: Be defined as an `abstract class`, NOT an `interface`. This is required so the class symbol can be used as an injection token by our service containers.
- **MUST**: Accept only **Value Objects (VOs)** or **Domain Entities** as method parameters. Raw primitives MUST NOT be used in signatures.
- **MUST**: Return objects or boolean wrapped over `Result<T, Errors>`.
- **MUST**: Use explicit Error Unions for the return type.
- **MUST**: Support optional injected transactions for mutations (`tx?: Transaction`).

```typescript
// MUST: Accept VOs, explicit Error typing
export abstract class WorkspaceRepository {
  // MUST: Require scope context (userId)
  abstract list(params: {
    userId: UUID;
    itemsPerPage: PositiveInteger;
    page: PositiveInteger;
  }): Promise<Result<Workspace[], RepositoryError>>;

  // MUST: Require scope context (userId)
  // Method Overloading: Repositories MAY expose overloaded signatures for different 
  // authorization levels or unique constraint checks.
  abstract exists(params: { workspaceId: UUID }): Promise<Result<boolean, RepositoryError>>;
  abstract exists(params: { userId: UUID; workspaceId: UUID }): Promise<Result<boolean, RepositoryError>>;

  // MUST: Require scope context (userId)
  abstract create(params: {
    tx?: Transaction; // Strongly typed
    userId: UUID;
    workspace: Workspace;
  }): Promise<Result<void, RepositoryError | UserNotFoundError>;
}
```

### 3.1 Security via Scope Isolation

Security and multi-tenant data segmentation happen at the Repository level:
- **MUST**: Read/List/Exists/Update/Delete operations MUST require parent scope identifiers (e.g., `userId`, `workspaceId`, `folderId`) alongside the target entity ID.
- By demanding parent scope IDs, the Repository physically isolates data via row-level `WHERE` queries (e.g., `AND folderId = ?`). If a user tries to alter an entity in another workspace, the DB responds cleanly as if the entity does not exist.

### 3.2 Error Typology: Structural / Constraint Mappings

Not every method fails in the exact same ways. Errors should be precisely typed:
- **MUST (Constraint Errors):** Repository methods that **ADD** or **MODIFY** information in the DB hitting structural constraints (like `UNIQUE` or `FOREIGN KEY` constraints) MUST return domain-specific database errors (e.g. `<Dependency>NotFoundError` or `<Field>AlreadyInUseError`) parsed from the constraints mapped via Postgres error codes.
- **MUST NOT (Read Errors):** Standard Read or Exists operations WITHOUT constraint impacts MUST ONLY return `RepositoryError`. A purely failed read or a `count()` logic usually returns standard generic db connection failures. Do not bleed unnecessary Domain Errors on simple queries.

### 3.3 Method Overloading for Scope Flexibility

Repository methods MAY and SHOULD use TypeScript method overloading when different Use Cases require different levels of scope isolation or querying logic (e.g., an Admin role vs a User role, or querying by different unique constrained columns).

- **MUST**: Define clear overloads in the Interface. 
- **MUST**: Implement them with union types or discriminate unions in the implementation class, ensuring the scope hierarchy is NEVER accidentally bypassed.

```typescript
export abstract class WorkspaceRepository {
  // Admin scope: no user restriction
  abstract exists(params: { workspaceId: UUID }): Promise<Result<boolean, RepositoryError>>;

  // User scope: isolated by userId
  abstract exists(params: { 
    workspaceId: UUID; 
    userId: UUID; 
  }): Promise<Result<boolean, RepositoryError>>;
}
```

## 4. Implementing the Postgres Repository

**Reference**: `references/examples/repository-implementation-example.md`

The Implementation class transforms Drizzle database queries into `neverthrow` values, taking raw Postgres `error.code` strings and interpreting them cleanly as specific Domain Entities.

- **MUST**: Unwrap `ValueObjects` (`vo.getValue()`) just before the `.insert()`, `.update()` or `where` clauses using `drizzle-orm`.

### Handling Typed execution (`executor`)

- Takes the primary pure database instance type from the ORM definition, strictly typed via `NodePgDatabase`, rather than loose `typeof db`.
- **MUST**: For any mutation method, explicitly declare the fallback executor: `const executor = p.tx ?? this.db`, then use `executor.insert()`. Since `Transaction` from `@/shared/domain/types/withTransaction` maps exactly to the PgTransaction DB pool, both TS types can be aligned easily without conflicts.

### Handling Postgres Errors

- **MUST NOT**: Use `any` for caught errors. The `catch (error)` block defaults to `unknown` in modern TypeScript.
- **MUST**: Validate instances. Drizzle and Postgres errors surface through `DrizzleQueryError` mapping to a `DatabaseError` object containing the `code` and `constraint` strings.
- **MUST**: Compare `error.cause.code` against the typed constants in `PG_ERROR_CODES` from `@/shared/infrastructure/drizzle-postgres/pgErrorCodes`.

Instead of raw string parsing, node-postgres codes are matched:
- `PG_ERROR_CODES.UNIQUE_VIOLATION` (Map to `...AlreadyInUseError`).
- `PG_ERROR_CODES.FOREIGN_KEY_VIOLATION` (Map to `...NotFoundError`).

Always verify `error.cause.constraint` naming patterns (defined natively in schema/drizzle indexing via exports) to figure out *which* foreign key or unique node failed. 
**MUST NOT**: Use magic strings for `error.cause.constraint`. Instead, explicitly export and import the constraint names from the schema file (e.g., `FK_WORKSPACES_USER`).

```typescript
import { DrizzleQueryError } from "drizzle-orm";
import { DatabaseError } from "pg";
import { PG_ERROR_CODES } from "@/shared/infrastructure/drizzle-postgres/pgErrorCodes";
import { FK_WORKSPACES_USER } from "@/shared/infrastructure/drizzle-postgres/schema";

// ...
  async create({ tx, userId, workspace }: CreateParams): Promise<Result<void, CreateErrors>> {
    const executor = tx ?? this.db;

    try {
      await executor.insert(workspaces).values({
         id: workspace.getId().getValue(),
         name: workspace.getName().getValue(),
      });
      return ok(undefined);
    } catch (error) {
      if (error instanceof DrizzleQueryError && error.cause instanceof DatabaseError) {
        if (
          error.cause.code === PG_ERROR_CODES.FOREIGN_KEY_VIOLATION && 
          error.cause.constraint === FK_WORKSPACES_USER
        ) {
          return err(new UserNotFoundError({ id: userId, cause: error }));
        }
      }
      return err(new RepositoryError(error as Error));
    }
  }
```

### Zod validations and Testing Strategy Notes (Docker/PG)

- Drizzle schema definition arrays in this stack rely on configurations managed via `drizzle-kit` and mapped via UI `zod` later.
- Postgres specific integration tests tied to this class run connected via `testcontainers` running standard `docker` Postgres tests with isolated rollback strategies (see `testing` skill).