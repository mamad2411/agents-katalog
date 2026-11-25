---
name: entities
description: "[Pragmatic DDD Architecture] Guide for creating DDD Entities and Aggregates. Use when defining new domain entities with business rules, private state, and getters. Covers entity instantiation via objects, integration with Value Objects, and the rule against using setters."
---

# DDD Entities & Aggregates

## 1. Core Principles (RFC 2119)

Entities represent domain concepts with a distinct identity (usually a `UUID`). Their primary role is to encapsulate state and business logic, ensuring that the object is always valid.
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

- **Identity**: Every entity MUST have an explicit identifier (e.g., `folderId`, `userId`) typed as a Value Object (e.g., `UUID`).
- **Encapsulation**: State MUST be `private` for mutable properties, and `private readonly` for identifiers and immutable creation dates. Public fields are STRICTLY FORBIDDEN.
- **No Setters**: You MUST NOT use `set` accessors or generic `update(data)` methods. You MUST create domain-specific behavior methods indicating intent (e.g., `rename(newName: FolderName)` instead of `setName(newName: string)`).
- **Constructors**: Constructors MUST always take a single `params` object pattern (`constructor(params: { ... })`). They MUST ONLY accept valid domain types (Value Objects or native Dates), never primitives.
- **Factories / Hydration**: The constructor is primarily used by the `infrastructure/` layer to reconstruct (hydrate) entities from the database, or by use cases when creating completely new entities.
- **Getters**: Expose internal state *only* when necessary using explicit getters (e.g., `getId()`, `getName()`). These getters MUST return Value Objects or Dates, never primitives.
- **Snapshots**: Every entity MUST define a `<EntityName>Snapshot` type and expose a `toSnapshot()` method. This method MUST return a plain object containing only Branded Primitives (via `.toBranded()`) and native Dates. The snapshot MUST NEVER include truly private or internal data (such as password hashes or internal security states).

## 2. Structure of an Entity

Here is the template for a domain entity.

```typescript
import { UUID, type BrandedUUID } from "@/shared/domain/value-objects/uuid";
import { FolderName, type BrandedFolderName } from "../value-objects/folderName";

// 1. Snapshot definition (No private fields like password hashes)
export type FolderSnapshot = {
  folderId: BrandedUUID;
  folderName: BrandedFolderName;
  createdAt: Date;
  updatedAt: Date;
};

export class Folder {
  // 2. Private properties, strictly typed with VOs
  private readonly folderId: UUID;
  private folderName: FolderName;
  private readonly createdAt: Date;
  private updatedAt: Date;

  // 3. Object parameter constructor
  constructor(params: {
    folderId: UUID;
    folderName: FolderName;
    createdAt: Date;
    updatedAt: Date;
  }) {
    this.folderId = params.folderId;
    this.folderName = params.folderName;
    this.createdAt = params.createdAt;
    this.updatedAt = params.updatedAt;
  }

  // 4. Domain behavior (mutates state with intent)
  rename(newName: FolderName): void {
    // Optionally apply business rules here before mutation
    this.folderName = newName;
    this.updatedAt = new Date();
  }

  // 5. Explicit Getters
  getId(): UUID {
    return this.folderId;
  }

  getName(): FolderName {
    return this.folderName;
  }

  getCreatedAt(): Date {
    return this.createdAt;
  }

  getUpdatedAt(): Date {
    return this.updatedAt;
  }

  // 6. Snapshot builder
  toSnapshot(): FolderSnapshot {
    return {
      folderId: this.folderId.toBranded(),
      folderName: this.folderName.toBranded(),
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}
```

## 3. Creating vs Reconstituting

Entities don't return `Result` from constructors because the primitives passed to them are already validated Value Objects (which handled the `neverthrow` validation). 

- **Infrastructure Layer**: Reads primitives from the DB, calls `UUID.from()`, `FolderName.from()`, etc. If valid, it MUST pass them into the `new <Entity>({ ... })` constructor.
- **Use Cases**: Creates entirely new identifiers `UUID.random()`, takes validated input from the Server Action, and instantiates the Entity to persist it.

## 4. Data Boundaries (Snapshots & Serialization)

Entities MUST NOT be returned directly from Server Actions to the Client, as class instances lose their methods across the RSC (React Server Component) / Client boundary. 

When an Entity needs to be serialized for the client, Server Actions MUST extract data using the entity's `.toSnapshot()` method. The `Snapshot` type is a structured plain object explicitly mapping Value Objects down to Branded Primitives.

Crucially, a Snapshot MUST NEVER include restricted private fields (like cryptographic hashes or internal server configurations). The Snapshot serves simultaneously as the serialization format and the public boundary type.

## 5. Aggregate Roots

If an entity controls child entities (e.g., a `Workspace` controlling `TeamMembers`), the workspace is the Aggregate Root. 
- All modifications to child entities MUST route through the Aggregate Root's methods.
- Repositories MUST ONLY be built for Aggregate Roots, not for child entities directly.