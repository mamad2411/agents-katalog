---
alwaysApply: false
---

# Service Class Guidelines

These guidelines outline the best practices for creating and maintaining service classes in TypeScript, drawing inspiration from NestJS principles and a commitment to clean, SOLID code.

## Core Principles

### Single Responsibility Principle (SRP)
A service must have one, and only one, reason to change. It should be responsible for a single part of the functionality.

- **Scope:** One service per main domain entity (e.g., `RecipeService`, `UserService`).
- **Function:** Encapsulate business logic and data persistence operations related to that entity.

### Encapsulation
Services abstract the business logic from the presentation layer (controllers) and other parts of the application.

- **Public API:** Interaction with a service should only happen through its well-defined public methods.
- **No Internal State Exposure:** Avoid exposing internal properties or implementation details.

### Dependency Injection (DI)
Dependencies (such as database repositories, other services, or external API clients) should be injected into the service's constructor.

- **Inversion of Control:** This adheres to the IoC principle.
- **Testability:** Makes services easier to mock and test in isolation.

## Structure and Naming

### File and Class Naming
- **File Name:** Use kebab-case (e.g., `recipe.service.ts`).
- **Class Name:** Use PascalCase and suffix with `Service` (e.g., `RecipeService`).
- **Location:** Services should be located in `src/lib/services`.

### Size and Complexity
- **Class Size:** Keep classes small and focused, ideally under 200 lines of code.
- **Method Count:** Limit the number of public methods to around 10.
- **Property Count:** Limit the number of properties to around 10.

## Methods

### Naming Conventions
- **Action-Oriented:** Start method names with a verb (e.g., `getRecipe`, `createRecipe`, `deleteRecipe`).
- **Boolean Returns:** For methods returning a boolean, use prefixes like `is`, `has`, or `can` (e.g., `isOwner`, `canUpdateRecipe`).

### Simplicity and Clarity
- **Single Purpose:** Each method should be short (under 20 instructions) and do only one thing.
- **Avoid Nesting:** Use early returns and guard clauses to handle validation and error conditions at the beginning of the method. This keeps the main logic path clear and avoids nested `if` statements.

### Parameters and Return Values (RO-RO Pattern)
- **Request Object (RO):** When a method requires multiple parameters, group them into a single input object with a descriptive type.
- **Response Object (RO):** When a method returns multiple distinct values, group them into a single output object with a descriptive type.
- **Strong Typing:** Always define explicit TypeScript types for these input and output objects.

## Data Handling

### Immutability
- Prefer immutable data structures to prevent side effects.
- Use the `readonly` modifier for class properties and array types that should not be changed after initialization.

## Error Handling

- **Use Exceptions:** Throw exceptions for unexpected or exceptional errors that the service cannot recover from.
- **Contextualize Errors:** If you catch an exception, it should only be to add more context before re-throwing it or to handle a specific, expected error case.
- **Global Handler:** Rely on a global exception handler (e.g., a NestJS filter) to catch unhandled exceptions and format the final error response.