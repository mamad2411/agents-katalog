---
name: business-logic-ensure-business-constraints
description: Formalize business constraints at business-logic points using an `ensure ...` style translated into the syntax and conventions of the project language. Use when an agent needs to create, modify, review, or interpret business-rule precondition checks such as eligibility checks, availability checks, permission checks, or invariant-preserving entry checks. These constraints must return only a unit-equivalent success value such as `void`, `unit`, `undefined`, or `None`, or an error when the condition is not satisfied.
---

# Ensure Business Constraints for Business Logic

## Goal

Write business-logic business constraints with a consistent `ensure ...` formalism translated into the syntax and naming conventions of the language in use.

Examples of the intended formalism are:

- `ensure requester is enabled`
- `ensure there are available cars`

Do not copy those phrases verbatim unless the language style truly fits them. Translate them into the local code style, naming style, and control-flow conventions while preserving the same meaning.

These business constraints do not produce business data. They succeed with a unit-equivalent result such as `void`, `unit`, `undefined`, or `None`, or they fail with an error.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- checks a precondition before executing business logic
- validates eligibility, authorization, availability, or required state
- protects a business operation from invalid execution
- enforces business-rule entry checks before state changes or workflow progression
- extracts business-constraint logic into helper functions, methods, or validators inside business logic

## Ensure Rule

1. Restate the business constraint as `ensure ...` before writing code.
   - Phrase the intended rule in plain business language first.
   - Use that formulation to decide the final method name, predicate, branch, or helper shape in code.

2. Translate the `ensure ...` rule into the local language convention.
   - Use the project's naming style, such as camelCase, snake_case, PascalCase, or an idiomatic statement form.
   - Prefer explicit names such as `ensureRequesterIsEnabled`, `ensureAvailableCars`, or the closest local equivalent.
   - Keep the code shape idiomatic for the language rather than forcing foreign syntax.

3. Business constraints return no business data on success.
   - Return only the unit-equivalent success value used by the language or project.
   - If the project uses a result wrapper, keep the success side unit-equivalent instead of returning payload data.

4. Business constraints fail with an error when the rule is not satisfied.
   - Use the project's error convention, such as an error value, thrown domain error, result error, or equivalent failure construct.
   - Make the error correspond to the violated business rule.

5. Keep business constraints focused on one rule each when practical.
   - Prefer small explicit constraint checks over helpers that silently combine unrelated business checks.
   - Compose multiple constraints explicitly when several business rules must hold.

## Detection Workflow

1. Find business-rule entry checks first.
   - Identify `if` conditions, early returns, validation branches, authorization checks, availability checks, and precondition helpers near business operations.
   - Focus on checks that decide whether the business logic may continue.

2. Restate each check in `ensure ...` form.
   - Convert the existing condition into a plain-language rule such as `ensure requester is enabled` or `ensure the order is cancellable`.
   - Use that restatement to clarify whether the check is a business constraint.

3. Check the success and failure shape.
   - Verify that success produces no meaningful data.
   - Verify that failure produces an error aligned with the violated rule.

4. Prefer semantic classification to syntax alone.
   - Do not classify a branch as a business constraint only because it appears early.
   - Classify it by whether it protects the execution of business logic through a rule that must hold.

## Writing or Changing Business Constraints

1. Name business constraints from the business rule.
   - Start from the `ensure ...` formulation and translate it into the local naming convention.
   - Keep names tied to the rule, not to incidental implementation details.

2. Return unit-equivalent success only.
   - Do not return booleans, entities, DTOs, counts, or derived values from a business constraint.
   - Let the absence of error mean the rule holds.

3. Return or raise a meaningful error on failure.
   - Use an error type or error value that explains which business rule failed.
   - Avoid vague failure shapes when the local style supports explicit errors.

4. Keep business constraint code direct and readable.
   - Prefer straightforward predicate checks and early failure paths.
   - Avoid burying the business constraint behind unrelated branching or side effects.

5. Keep the business operation separate from the business constraint.
   - Let the business constraint decide whether execution may continue.
   - Let the main business logic run only after the business constraint succeeds.

## Review Questions

When reading or reviewing code, ask:

- What is the `ensure ...` rule expressed by this check?
- Has that rule been translated clearly into the language's syntax and naming convention?
- Does the business constraint return only a unit-equivalent success value?
- Does it produce an error when the rule is violated?
- Would changing this code blur the business constraint or make it return meaningful data?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which business constraints were identified or changed
- state which `ensure ...` rules they represent
- state how the rules were translated into the local language convention
- state which unit-equivalent success type and failure error shape were used
