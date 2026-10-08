---
globs: .ts,.tsx
alwaysApply: false
---

# Essential TypeScript standards

You are an expert writing typescript. You are an expert, but you want to avoid being clever
You know that the type system only works if you fully use it and don't try and trick it with type casting.
Code that can't be typed properly is not good code and needs to be rewritten.

## Type annotations

- Exported functions need explicit return types
- Type arrays correctly using fixed length arrays and non empty array types when possible

## Solving type errors

- If data has the `any` or `unknown` type, create a zod schema and parse it to get a known type. We are using Zod v3.
- Never try and type cast to solve a type error

## Design

- Prefer tagged unions for types that have different states over creating objects with optional fields
- Follow "Domain Driven Design Made Functional" when creating new features

## Functional Programming

- You MUST not use switches or complex if/else statements
- All functions, hooks, and components MUST be single purpose
- You MUST NOT use null or undefined. You do not have to change existing code unless you are asked.
- You MUST NOT throw errors

# Use Strict types

- Never use the any type
- Never use type casting or force assertions
- Never use `as` to force a type to be something else
- You MUST NOT use `@ts-expect-error` outside of a unit test. All types must be correct. You may use it in a unit test when testing bad data if you have a comment with an explanation
