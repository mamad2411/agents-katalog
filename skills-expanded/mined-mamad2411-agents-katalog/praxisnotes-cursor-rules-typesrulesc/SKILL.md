---
description: Guidelines for working with types in the PraxisNotes application
globs: packages/types/**/*
alwaysApply: false
---
# Type Definitions and Usage Guidelines

## 📦 Type Package Structure

The `@praxisnotes/types` package is the centralized location for all type definitions in the PraxisNotes application.

```
packages/types/src/

├── client/           # Client types
├── common/           # Shared utility types
└── index.ts          # Main exports
```

## 🔤 Type Definition Guidelines

1. **All shared types must be defined in the `@praxisnotes/types` package**
   - Local/component-specific types can remain in their component files
   - Any type used across multiple components or packages must be defined in this package

2. **File Organization:**
   - Place types in domain-specific directories (e.g., `activity/`, `client/`)
   - Use separate files for related type groups
   - Follow the naming convention: `feature-name.type.ts`

3. **Type Patterns to Follow:**
   - **Base Types:** Core entity definitions
   - **Relation Types:** Types with relationships (e.g., `EntityWithRelations`)
   - **Create/Update Types:** Use `NewEntity` and `UpdateEntity` patterns
   - **Form Types:** Use `EntityForm` pattern for form handling
   - **API Types:** Use the standardized API response structures

## 🧩 Type Definition Best Practices

1. **Prefer `type` over `interface`** unless declaration merging is required
2. **Use TypeScript utility types** (`Omit`, `Pick`, `Partial`, etc.) where appropriate
3. **Document your types** with JSDoc comments to explain their purpose
4. **Never use `any`** - create proper type definitions
5. **Keep types focused** - each type should have a single purpose
6. **Use readonly** for immutable properties

## 🚀 Using Types in Components/Services

```typescript
// Import from the root for general usage
import { Activity, Client, ApiResponse } from "@praxisnotes/types";

// For more explicit imports from specific domains
import { Activity, ActivityWithRelations } from "@praxisnotes/types/activity";
import { ApiResponse, SearchParams } from "@praxisnotes/types/common";
```

## 🆕 Adding New Types

1. **Create new types** in the appropriate domain-specific directory
2. **Follow the base patterns** for consistency:

```typescript
// Base entity type
export type ExampleEntity = {
  id: string;
  name: string;
  description: string;
  createdAt: Date;
  updatedAt: Date;
};

// Creation type
export type NewExampleEntity = Omit<
  ExampleEntity,
  "id" | "createdAt" | "updatedAt"
>;

// Update type
export type UpdateExampleEntity = Partial<Omit<ExampleEntity, "id">> & {
  id: string;
};

// With relations type
export type ExampleEntityWithRelations = ExampleEntity & {
  relatedEntities: RelatedEntity[];
};

// Form type
export type ExampleEntityForm = {
  name: string;
  description: string;
};
```

3. **Export new types** in the domain directory's index.ts
4. **Add exports** to the main src/index.ts to make types available from the package root

## ⚠️ Common Mistakes to Avoid

1. Duplicating types in multiple locations
2. Creating overly complex generic types
3. Using `any` instead of creating proper types
4. Not documenting complex types
5. Creating circular dependencies between type files 