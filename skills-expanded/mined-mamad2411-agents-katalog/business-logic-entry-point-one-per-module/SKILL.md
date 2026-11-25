---
name: business-logic-entry-point-one-per-module
description: Require each business-logic entry point to live in its own separate module. Use when an agent needs to create, modify, review, or organize business-logic entry points such as command handlers, query handlers, use cases, or application services. Do not group multiple entry points in a single class, object, or file based on the domain entity they operate on. Each entry point must be either a top-level function in its own module, or a class or object with exactly one public function in its own module.
---

# One Entry Point per Module for Business Logic

## Goal

Every business-logic entry point must be a separate module. Do not group multiple entry points together in the same class, object, or file because they operate on the same domain entity type.

A module here means the unit of code organization provided by the language: a file, a single-class file, a single-object file, or equivalent. Each entry point gets its own.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines multiple business-logic entry points in a single class, object, or file
- groups command handlers, query handlers, use cases, or application services by domain entity type into a shared container
- introduces a service class or facade that bundles several business operations as methods on one object
- organizes business-logic entry points by entity rather than by operation

## The Rule

1. Each business-logic entry point must live in its own module.
   - One command handler per module.
   - One query handler per module.
   - One use case per module.
   - One application service method becomes one application service module with a single public function.

2. Do not group entry points by domain entity type.
   - Do not create a `UserService` class with `createUser`, `updateUser`, `findUserById`, and `deleteUserById` as methods.
   - Do not create a `ReservationUseCases` class that bundles all reservation-related operations.
   - Do not create a file that exports multiple entry-point functions for the same entity.

3. Each module exposes exactly one business-logic entry point.
   - If the entry point is a top-level function, the module contains that function as its single public entry point.
   - If the entry point is a class or object, it must have exactly one public function that acts as the entry point. Construction, dependency injection, and private helpers do not count as additional public entry points.

4. Name the module after the entry point.
   - The file or module name should reflect the specific business operation, not the domain entity type.
   - Prefer names like `create-reservation-command-handler`, `find-user-by-id-query-handler`, or the local equivalent over names like `user-service`, `reservation-use-cases`, or `order-handlers`.

## Why Not Group by Entity

Grouping entry points by domain entity creates classes or files that grow with every new operation. This leads to:

- large files with unrelated operations sharing scope and dependencies
- entry points that accumulate shared private state or helpers that blur their boundaries
- difficulty isolating one operation's dependencies from another's
- merging conflicts when different developers work on different operations for the same entity

Keeping each entry point in its own module makes each operation self-contained, with its own explicit dependencies and no accidental coupling to sibling operations.

## Detection Workflow

1. Find classes, objects, or files that contain multiple business-logic entry points.
   - Look for service classes, use-case bundles, handler collections, or files that export several entry-point functions.
   - Check whether the grouping criterion is the domain entity type.

2. Count the public entry points per module.
   - If a class or object has more than one public function that acts as a business-logic entry point, it violates this rule.
   - If a file exports more than one entry-point function, it violates this rule.

3. Check the module name.
   - If the module is named after a domain entity type rather than a specific operation, it likely groups multiple entry points.

## Writing or Changing Entry Points

1. Create a new module for each new entry point.
   - Do not add a new method to an existing entity-grouped class.
   - Create a new file with the entry point as its single public operation.

2. When refactoring, extract grouped entry points into separate modules.
   - Move each method from an entity-grouped class into its own module.
   - Give each module its own explicit dependencies.

3. Keep private helpers local to the entry point that uses them.
   - If a helper is used by only one entry point, keep it in that entry point's module.
   - If a helper is shared across multiple entry points, extract it into its own module rather than keeping it as a shared private method in a grouped class.

## Examples

Avoid this:

```ts
// user-service.ts
class UserService {
  createUser(command: CreateUserCommand): Promise<CreateUserCommandHandlerSuccess> { ... }
  updateUser(command: UpdateUserCommand): Promise<void> { ... }
  findUserById(query: FindUserByIdQuery): Promise<FindUserByIdQueryHandlerSuccess> { ... }
  deleteUserById(command: DeleteUserByIdCommand): Promise<void> { ... }
}
```

Prefer this:

```
create-user-command-handler.ts
update-user-command-handler.ts
find-user-by-id-query-handler.ts
delete-user-by-id-command-handler.ts
```

Each file contains exactly one entry point.

## Review Questions

When reading or reviewing code, ask:

- Does this module contain more than one business-logic entry point?
- Are multiple entry points grouped because they operate on the same domain entity type?
- Does the module name refer to a domain entity type rather than a specific business operation?
- Would adding a new operation for this entity require modifying this module?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or separated into their own modules
- state which entity-grouped classes or files were split
- state how each module was named after its specific business operation
