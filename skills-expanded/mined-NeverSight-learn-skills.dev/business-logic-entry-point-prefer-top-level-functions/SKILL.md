---
name: business-logic-entry-point-prefer-top-level-functions
description: Prefer top-level functions over classes or objects for implementing business-logic entry points when the project stack allows it without introducing friction. Use when an agent needs to decide the code shape for a business-logic entry point such as a command handler, query handler, use case, or application service. Choose a top-level function unless the language, framework, or project conventions make classes or objects the natural, frictionless choice.
---

# Prefer Top-Level Functions for Business Logic Entry Points

## Goal

When implementing a business-logic entry point, prefer a top-level function over a class or object, as long as the project stack allows it without introducing friction.

A top-level function is a function defined at module scope, not inside a class or object. It is the simplest code shape for an entry point: one function, one module, no wrapper.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a new business-logic entry point and must choose between a top-level function, a class, or an object
- wraps a single entry-point function in a class or object without a clear reason
- uses a class or object only as a container for one public method plus dependency injection that could be achieved with function parameters or closures

## The Rule

1. Default to a top-level function for each business-logic entry point.
   - Export the function as the module's single public entry point.
   - Pass dependencies as function parameters, closures, or through the module's imports, depending on the language's idiomatic patterns.

2. Use a class or object only when the project stack makes it the natural choice.
   - The language requires classes for dependency injection and there is no idiomatic function-based alternative.
   - The framework expects classes or objects for registration, routing, or lifecycle management.
   - The project already uses classes consistently for entry points and switching to functions would introduce inconsistency or friction.

3. Do not wrap a function in a class just for the sake of having a class.
   - A class with one public method, a constructor that only assigns dependencies, and no meaningful state is a function in disguise.
   - If the language supports top-level functions and the framework does not require a class, use a function.

## When Classes Are Appropriate

Classes or objects are appropriate when:

- The language does not support top-level functions as first-class module exports (e.g., Java without workarounds).
- The dependency injection framework requires class-based registration and there is no idiomatic function adapter.
- The project has an established convention of using classes for entry points and the team has decided to keep that convention.
- The entry point genuinely manages internal state across its lifecycle, beyond simple dependency references.

In these cases, use a class or object with a single public method, following the one-entry-point-per-module rule.

## Examples

Prefer this when the stack allows it:

```ts
// create-reservation-command-handler.ts
export const createReservationCommandHandler = (
  command: CreateReservationCommand,
): ResultAsync<CreateReservationCommandHandlerSuccess, CreateReservationCommandHandlerError> => {
  // business logic
}
```

```py
# create_reservation_command_handler.py
def create_reservation_command_handler(
    command: CreateReservationCommand,
) -> CreateReservationCommandHandlerSuccess:
    # business logic
```

```kt
// CreateReservationCommandHandler.kt
fun createReservationCommandHandler(
    command: CreateReservationCommand,
): CreateReservationCommandHandlerSuccess {
    // business logic
}
```

Avoid this when a top-level function would work:

```ts
// create-reservation-command-handler.ts
class CreateReservationCommandHandler {
  constructor(private readonly reservationRepository: ReservationRepository) {}

  execute(command: CreateReservationCommand): ResultAsync<...> {
    // business logic
  }
}
```

Use a class when the stack requires it:

```java
// CreateReservationCommandHandler.java
public class CreateReservationCommandHandler {
    private final ReservationRepository reservationRepository;

    public CreateReservationCommandHandler(ReservationRepository reservationRepository) {
        this.reservationRepository = reservationRepository;
    }

    public CreateReservationCommandHandlerSuccess execute(CreateReservationCommand command) {
        // business logic
    }
}
```

## Detection Workflow

1. Check the project stack.
   - Determine whether the language supports top-level functions as first-class exports.
   - Determine whether the framework or dependency injection system requires classes.

2. Inspect existing entry points.
   - Check whether the project uses classes or top-level functions for business-logic entry points.
   - If the project consistently uses classes and there is no initiative to change, respect that convention.

3. Identify unnecessary class wrappers.
   - Look for classes with one public method, a constructor that only assigns dependencies, and no meaningful internal state.
   - These are candidates for conversion to top-level functions if the stack allows it.

## Writing or Changing Entry Points

1. Check the stack first.
   - If top-level functions are idiomatic and frictionless, use a top-level function.
   - If the stack requires or strongly favors classes, use a class with one public method.

2. Pass dependencies explicitly.
   - For top-level functions, pass dependencies as parameters, use closures, or import them at module level, depending on the language's conventions.
   - For classes, inject dependencies through the constructor.

3. Do not introduce a class solely for future extensibility.
   - A function can be refactored into a class later if the need arises.
   - Start with the simpler shape.

## Review Questions

When reading or reviewing code, ask:

- Is this entry point implemented as a class when a top-level function would work?
- Does the class have only one public method and a constructor that assigns dependencies?
- Does the project stack require or strongly favor classes for this purpose?
- Would switching to a top-level function introduce friction or inconsistency?

If a class is used without a clear reason and the stack supports top-level functions, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were implemented or changed
- state whether top-level functions or classes were used and why
- state whether the project stack influenced the choice
