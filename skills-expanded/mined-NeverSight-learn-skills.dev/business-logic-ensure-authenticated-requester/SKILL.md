---
name: business-logic-ensure-authenticated-requester
description: Enforce an authentication business constraint at business-logic entry points using an `ensure requester is authenticated` formalism translated into the syntax and conventions of the project language. Use when an agent needs to create, modify, review, or interpret authentication checks at business-logic entry points. The constraint must verify that the request triggering the execution comes from an authenticated requester before any business logic runs. On success it must return the requester id to facilitate downstream business logic. On failure it must return an error when the requester is not authenticated.
---

# Ensure Authenticated Requester for Business Logic Entry Points

## Goal

Every business-logic entry point that requires authentication must include an `ensure requester is authenticated` business constraint as the first check before any other business logic runs.

This constraint follows the `ensure ...` formalism. Restate the rule as:

- `ensure requester is authenticated`

Translate that formulation into the syntax, naming, and control-flow conventions of the language in use.

On success this constraint returns the requester id so that downstream business logic can use it directly without re-extracting it from the input. On failure it returns an error indicating that the requester is not authenticated.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a business-logic entry point that must only run for authenticated requesters
- checks whether the incoming request originates from an authenticated identity before executing business logic
- protects a business operation from unauthenticated execution
- extracts authentication verification logic into a helper, method, or validator inside business logic

## Relationship to the Ensure Business Constraints Skill

This skill is a specialization of the general `ensure business constraints` skill. All rules from that skill apply here except for the success return value. This skill adds specificity about what the constraint checks, where it must appear, and what it returns:

- The constraint is always `ensure requester is authenticated`.
- The constraint must be the first business constraint checked at the entry point, before any other business constraints run.
- The constraint verifies identity authentication, not authorization, permissions, roles, or eligibility.
- Unlike general business constraints that return a unit-equivalent value on success, this constraint returns the requester id on success to facilitate downstream business logic.

## Ensure Rule

1. Restate the constraint as `ensure requester is authenticated` before writing code.
   - This is the single business rule this constraint enforces.
   - Use that formulation to decide the final method name, predicate, branch, or helper shape in code.

2. Translate the rule into the local language convention.
   - Use the project's naming style, such as camelCase, snake_case, PascalCase, or an idiomatic statement form.
   - Prefer explicit names such as `ensureRequesterIsAuthenticated`, `ensure_requester_is_authenticated`, or the closest local equivalent.
   - Keep the code shape idiomatic for the language rather than forcing foreign syntax.

3. Place this constraint first at every entry point that requires authentication.
   - Before any other business constraint, business rule, or business operation.
   - The entry point must not proceed to any business logic if this constraint fails.

4. The constraint returns the requester id on success.
   - Return the requester id so that subsequent business logic can use it directly.
   - Do not return full user objects, tokens, sessions, or other identity details beyond the requester id.

5. The constraint fails with an error when the requester is not authenticated.
   - Use the project's error convention, such as an error value, thrown domain error, result error, or equivalent failure construct.
   - Make the error correspond to the specific violation: unauthenticated request.

6. Keep the constraint focused on authentication only.
   - Do not mix authorization, permissions, roles, or eligibility checks into this constraint.
   - Use separate `ensure ...` constraints for those concerns.

## Input Convention

The authentication constraint needs to receive the requester's authentication information from the entry point's input.

- The command or query type at the entry point should include the requester identity or authentication token as a field.
- The constraint receives that field and verifies it represents an authenticated requester.
- Do not reach outside the entry point's input to obtain authentication state. The entry point must receive all necessary information through its declared parameter.

## Detection Workflow

1. Find business-logic entry points first.
   - Identify command handlers, query handlers, and other business-logic entry points.
   - Determine which entry points must only run for authenticated requesters.

2. Check for the presence of the authentication constraint.
   - Look for an `ensure requester is authenticated` check or its local equivalent.
   - Verify that it is the first constraint checked at the entry point.

3. Check the constraint shape.
   - Verify that success returns the requester id.
   - Verify that failure produces an error indicating the requester is not authenticated.

4. Check the constraint focus.
   - Verify that the authentication constraint does not also check authorization, permissions, roles, or other concerns.
   - Those checks should be separate `ensure ...` constraints if needed.

5. Prefer semantic classification to syntax alone.
   - Do not classify a check as the authentication constraint only because it appears first.
   - Classify it by whether it verifies that the requester is authenticated.

## Writing or Changing the Authentication Constraint

1. Name the constraint from the business rule.
   - Start from the `ensure requester is authenticated` formulation.
   - Translate it into the local naming convention.

2. Place it as the first constraint at the entry point.
   - Before any other `ensure ...` constraint.
   - Before any business operation or data access.

3. Return the requester id on success.
   - Return the requester id so downstream logic can use it without re-extracting it from the input.
   - Do not return full user objects, tokens, session data, or other identity details beyond the requester id.

4. Return or raise a meaningful error on failure.
   - Use an error type or error value that explains that the requester is not authenticated.
   - Avoid vague failure shapes when the local style supports explicit errors.

5. Keep the constraint direct and readable.
   - Prefer a straightforward check and early failure path.
   - Avoid burying the authentication check behind unrelated branching or side effects.

## Examples

TypeScript with neverthrow:

```ts
const ensureRequesterIsAuthenticated = (
  requesterId: RequesterId,
): ResultAsync<RequesterId, RequesterIsNotAuthenticated> => {
  // verify the requester is authenticated, return the requesterId on success
}

const createReservationCommandHandler = (
  command: CreateReservationCommand,
): ResultAsync<CreateReservationCommandHandlerSuccess, CreateReservationCommandHandlerError> => {
  return ensureRequesterIsAuthenticated(command.requesterId)
    .andThen((requesterId) => {
      // other business constraints and business logic using requesterId
    })
}
```

TypeScript with exceptions:

```ts
const ensureRequesterIsAuthenticated = (
  requesterId: RequesterId,
): Promise<RequesterId> => {
  // verify the requester is authenticated, throw RequesterIsNotAuthenticated if not
  // return the requesterId on success
}

const createReservationCommandHandler = async (
  command: CreateReservationCommand,
): Promise<CreateReservationCommandHandlerSuccess> => {
  const requesterId = await ensureRequesterIsAuthenticated(command.requesterId)
  // other business constraints and business logic using requesterId
}
```

Python:

```py
def ensure_requester_is_authenticated(
    requester_id: RequesterId,
) -> RequesterId:
    # verify the requester is authenticated, raise RequesterIsNotAuthenticated if not
    # return the requester_id on success
    ...

def create_reservation_command_handler(
    command: CreateReservationCommand,
) -> CreateReservationCommandHandlerSuccess:
    requester_id = ensure_requester_is_authenticated(command.requester_id)
    # other business constraints and business logic using requester_id
```

Kotlin:

```kt
fun ensureRequesterIsAuthenticated(
    requesterId: RequesterId,
): RequesterId {
    // verify the requester is authenticated, throw RequesterIsNotAuthenticated if not
    // return the requesterId on success
}

fun createReservationCommandHandler(
    command: CreateReservationCommand,
): CreateReservationCommandHandlerSuccess {
    val requesterId = ensureRequesterIsAuthenticated(command.requesterId)
    // other business constraints and business logic using requesterId
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this entry point require an authenticated requester?
- Is there an `ensure requester is authenticated` constraint or its local equivalent?
- Is it the first constraint checked, before any other business constraint or business logic?
- Does it return the requester id on success?
- Does it produce an error when the requester is not authenticated?
- Does it avoid mixing in authorization, permissions, or role checks?
- Does the entry point receive the requester's authentication information through its declared input parameter?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which entry points were identified or changed
- state where the `ensure requester is authenticated` constraint was added or verified
- state how the constraint was translated into the local language convention
- state that the constraint returns the requester id on success and which failure error shape was used
- state that the constraint is placed before any other business constraint at the entry point