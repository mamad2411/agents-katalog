---
name: business-logic-entry-point-colocate-types
description: Require project-declared parameter types and return types of a business-logic entry point to be declared in the same file as the entry point itself, when the project stack allows it. Use when an agent needs to create, modify, review, or organize type definitions for command types, query types, success types, error types, or other project-declared types used in the signature of a business-logic entry point. Do not place these types in separate files, shared type modules, or barrel exports.
---

# Colocate Types with Business Logic Entry Points

## Goal

When a business-logic entry point has parameters or return values whose types are declared by the project, those types must live in the same file as the entry point, as long as the project stack allows it.

This keeps each entry point self-contained: opening one file reveals the full signature, including the shape of its inputs and outputs, without navigating to other files.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- declares a business-logic entry point with project-declared parameter types or return types
- places command types, query types, success types, or error types in separate files from the entry point that uses them
- creates shared type modules or barrel exports for types that belong to a single entry point
- imports project-declared signature types from another file into an entry point module

## What Counts as a Project-Declared Type

A project-declared type is a type that was created within the project specifically for use in the codebase. This includes:

- command types, query types, success types, error types
- DTOs, value objects, or payload types declared for a specific entry point
- any type alias, interface, struct, class, enum, or equivalent declared by the project

This does not include:

- types from the language's standard library
- types from third-party libraries or frameworks
- domain-entity types that are shared across multiple entry points
- primitive types or built-in generic types

## The Rule

1. Project-declared types used in the signature of a business-logic entry point must be declared in the same file as that entry point.
   - The command or query type goes in the same file as the handler.
   - The success type goes in the same file as the handler.
   - The error type goes in the same file as the handler, unless it is shared across multiple entry points.

2. Do not create separate files for types that belong to a single entry point.
   - Do not place `CreateReservationCommand` in a `create-reservation-command.ts` file and the handler in a `create-reservation-command-handler.ts` file.
   - Keep both in the same file.

3. Types shared across multiple entry points are exempt.
   - Domain-entity types, shared error types, shared value objects, and other types used by more than one entry point may live in their own modules.
   - This rule applies only to types that are specific to a single entry point's signature.

4. Apply this rule only when the project stack allows it.
   - Some languages or frameworks impose file-per-type conventions (e.g., Java's one-public-class-per-file rule).
   - In those cases, follow the language or framework convention instead.
   - When the language allows multiple type definitions per file, apply this rule.

## Examples

Prefer this:

```ts
// create-reservation-command-handler.ts

type CreateReservationCommand = {
  requesterId: RequesterId
  carClass: CarClass
  startsAt: ZonedDateTime
  endsAt: ZonedDateTime
}

type CreateReservationCommandHandlerSuccess = {
  reservationId: ReservationId
}

export const createReservationCommandHandler = (
  command: CreateReservationCommand,
): ResultAsync<CreateReservationCommandHandlerSuccess, CreateReservationCommandHandlerError> => {
  // business logic
}
```

```py
# create_reservation_command_handler.py

@dataclass(frozen=True)
class CreateReservationCommand:
    requester_id: RequesterId
    car_class: CarClass
    starts_at: ZonedDateTime
    ends_at: ZonedDateTime

@dataclass(frozen=True)
class CreateReservationCommandHandlerSuccess:
    reservation_id: ReservationId

def create_reservation_command_handler(
    command: CreateReservationCommand,
) -> CreateReservationCommandHandlerSuccess:
    # business logic
```

Avoid this:

```
# Types in a separate file
create-reservation-command.ts          ← command type
create-reservation-command-handler.ts  ← handler imports the type

# Types in a shared barrel
types/commands.ts                      ← all command types together
handlers/create-reservation.ts         ← handler imports from barrel
```

## Detection Workflow

1. Find the business-logic entry point.
   - Identify the handler function, use case, or application service method.

2. Inspect the signature types.
   - List the parameter types and return types in the signature.
   - Determine which of those types are project-declared.

3. Check where each project-declared type is declared.
   - If a project-declared signature type is in a different file from the entry point, it violates this rule.
   - If the type is shared across multiple entry points, it is exempt.

4. Check the project stack.
   - If the language enforces file-per-type conventions, the rule does not apply.

## Writing or Changing Entry Points

1. Declare signature types in the same file as the entry point.
   - Write the command or query type, success type, and entry-point-specific error types in the same file as the handler.

2. Do not pre-create type files.
   - When starting a new entry point, create one file and put everything in it.

3. Extract a type to its own module only when it becomes shared.
   - If a second entry point needs the same type, move the type to its own module at that point.
   - Until then, keep it colocated.

## Review Questions

When reading or reviewing code, ask:

- Are there project-declared types in the entry point's signature that live in a different file?
- Are those types used by only this entry point?
- Does the project stack allow multiple type definitions per file?
- Would moving those types into the entry point's file make the module self-contained?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or changed
- state which types were colocated into the entry point's file
- state which types remained in separate modules because they are shared
- state whether the project stack imposed any constraints on colocation
