---
name: write-persistence-representations
description: Create or update persistence-layer data representations in any stack, including ORM entities, schema definitions, table mappings, document models, collection definitions, and similar database-facing code. Use when agents needs to add or change persisted fields, identifiers, relationships, indexes, timestamps, auditing fields, or storage mappings in frameworks, libraries, or ORMs such as Prisma, TypeORM, Sequelize, Drizzle, Mongoose, Hibernate/JPA, Doctrine, Ecto, Active Record, or equivalent persistence technologies.
---

# Write Persistence Representations

## Goal

Write or update the persistence representation that maps application data to the storage technology in use.

Keep business defaults out of the representation layer. Let callers, services, commands, factories, or explicit write flows provide values instead of database or ORM defaults.
Enforce the rule that representation definitions must not declare default values, except for the creation-time audit field such as `createdAt`, `created_at`, `inserted_at`, or an equivalent project-specific name.

## Detect the Representation Style

1. Identify the persistence technology and the project convention before editing.
   - Inspect nearby model, entity, schema, mapping, or migration files.
   - Match the local style for file placement, naming, decorators, schema builders, relation declarations, enums, indexes, and timestamp fields.
   - Use official documentation when framework semantics are unclear or version-sensitive.

2. Map the requested change to the representation type used by the stack.
   - Treat SQL table mappings, ORM entities, schema DSL files, document schemas, collection definitions, record types, and similar storage-facing definitions as the target artifact.
   - Prefer updating the existing representation pattern instead of introducing a new abstraction.

## Write the Representation

1. Add or update only the storage-facing structure that the task requires.
   - Define field names, types, nullability, identifiers, relationships, indexes, constraints, embedded objects, and table or collection names as needed.
   - Keep the representation focused on persistence concerns.
   - Avoid mixing in service behavior or request-layer shaping unless the framework requires it.

2. Keep required data explicit.
   - Use required vs optional markers that reflect the real writing contract.
   - Do not weaken a field to optional only to compensate for a missing default.
   - If a field must exist but the representation cannot supply it automatically, require the application write path to provide it.

## Enforce the No-Defaults Rule

Treat all of these as defaults and avoid them in persistence representations:

- database column defaults
- ORM or schema `default` or `defaultValue` options
- property initializers that silently seed persisted values
- schema hooks or model callbacks that backfill business values
- generated placeholders for status, counters, booleans, enums, arrays, JSON, foreign keys, or similar data

Allow only the creation-time audit timestamp default when the project convention requires it, for example `createdAt`, `created_at`, `inserted_at`, or an equivalent creation field.

Apply the rule strictly:

- Allow `createdAt`-style creation timestamps to use `now`, `CURRENT_TIMESTAMP`, or the framework's equivalent creation-time mechanism.
- Do not add defaults for `updatedAt`, `deletedAt`, `publishedAt`, `status`, `enabled`, `role`, `count`, `version`, `metadata`, or any business field.
- If a framework bundles `createdAt` with other automatic fields behind a single switch, check the existing project convention first. If the bundled behavior violates this rule, model the fields explicitly instead of enabling the switch blindly.
- If the codebase already contains forbidden defaults, do not spread the pattern. Preserve existing behavior unless the task asks to refactor it, but do not introduce new non-audit defaults.

## Validate Before Finishing

1. Verify that field names, relation wiring, indexes, and nullability match nearby code.
2. Verify that omitted defaults do not hide a missing required to be input in the writing flow.
3. Run the normal local validation for the stack when it is safe and in scope, such as type checks, schema validation, or generated client checks.
4. Call out any assumption when application code must now supply a value that used to be implicit.

## Report the Outcome

When finishing the task:

- State which persistence representations were created or updated.
- State which fields, relations, or indexes were added or changed.
- State whether a creation-time audit default was used.
- State whether application code must provide any required values because defaults were intentionally omitted.
