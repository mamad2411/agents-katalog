---
name: business-logic-entry-point-vocabulary
description: Map common industry names to the concept of business-logic entry point. Use when an agent encounters or the user mentions terms such as use case, application service, service layer, command handler, query handler, interactor, or similar names that refer to entry points to business logic. Recognize these terms as synonyms for business-logic entry point and apply all business-logic entry-point skills accordingly.
---

# Business Logic Entry Point Vocabulary

## Goal

Recognize the many names that software developers use in practice for business-logic entry points and treat them as synonyms for the same concept.

Developers, architects, and codebases frequently call business-logic entry points by different names depending on the tradition, framework, or architectural style they follow. These names all refer to the same idea: a function, method or class that a caller invokes to trigger business logic.

## Common Names

The following terms are commonly used to refer to business-logic entry points:

- **use case** — from Clean Architecture and hexagonal architecture traditions
- **application service** — from Domain-Driven Design and layered architecture traditions
- **service layer** — from service-oriented and layered architecture traditions
- **command handler** — from CQS and CQRS traditions, for entry points that change state
- **query handler** — from CQS and CQRS traditions, for entry points that return data
- **interactor** — from Clean Architecture tradition
- **facade** — when used as the public interface to business operations
- **action** — used in some frameworks and codebases for entry points that perform a business operation

This list is not exhaustive. Other names may appear in specific communities, frameworks, or codebases. The key criterion is not the name but whether the code acts as the entry point where a caller triggers business logic.

## Mapping Rule

1. When the user or codebase uses any of these names, treat the referenced code as a business-logic entry point.
   - Apply all business-logic entry-point skills that are in scope.
   - Do not require the code to be literally named "entry point" to recognize it.

2. When the user asks to create, modify, or review a use case, application service, command handler, query handler, interactor, or similar construct, interpret the request as work on a business-logic entry point.
   - Apply the relevant entry-point skills such as CQS, handler signatures, payload types, typical domain-entity entry points, business constraints, and authentication constraints.

3. Do not enforce a single naming convention from this vocabulary.
   - The project may use any of these names or its own equivalent.
   - This skill maps vocabulary to concepts. Other skills govern naming conventions within the code.

## Detection Workflow

1. Listen for vocabulary in user requests.
   - Watch for terms like use case, application service, service layer, command handler, query handler, interactor, facade, or action.
   - Treat these as references to business-logic entry points.

2. Scan the codebase for vocabulary in code structures.
   - Look for classes, functions, modules, or files named with these terms.
   - Treat matching code as business-logic entry points for the purpose of applying entry-point skills.

3. Do not rely on vocabulary alone for classification.
   - Verify that the code actually acts as an entry point to business logic.
   - A class named `Service` that only does HTTP routing is not a business-logic entry point. A class named `UseCase` that orchestrates business rules is.

## Review Questions

When reading or reviewing code, ask:

- Does this code use a name from the common vocabulary for business-logic entry points?
- Does it actually act as the entry point where a caller triggers business logic?
- Have all relevant business-logic entry-point skills been applied to it?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which vocabulary term the user or codebase used
- state that it was recognized as a business-logic entry point
- state which business-logic entry-point skills were applied as a result
