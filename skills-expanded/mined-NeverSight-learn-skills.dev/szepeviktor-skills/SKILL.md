---
name: szepeviktor-skills
description: Use a principal-engineer style Laravel workflow that maps vague requests to the correct Laravel subsystem, prioritizes official documentation, and keeps validation, security, HTTP, and architecture concerns in the right layers.
---

# Szepeviktor Skills

Use this skill when the Laravel request is broad, ambiguous, or spans multiple layers.

## Goal

Translate user intent into the correct Laravel subsystem before editing code.

## Default approach

1. Map the request to Laravel concepts.
2. Identify the affected layer:
   - HTTP interface
   - validation and security
   - database and Eloquent
   - application architecture
   - async work and integrations
   - testing and quality
3. Choose the most Laravel-native implementation.
4. Avoid invented APIs, helpers, facades, or package assumptions.
5. Keep boundaries explicit.

## Preferred defaults

- Prefer route model binding where appropriate.
- Prefer FormRequests for non-trivial validation.
- Prefer Policies or Gates for authorization.
- Keep controllers thin.
- Keep business logic out of Blade templates.
- Prefer Eloquent or Query Builder before raw SQL unless there is a clear reason not to.
- Use Jobs for asynchronous or heavy work.
- Use config files instead of direct `env()` access in app code.

## Validation and security emphasis

- Distinguish validation, authorization, and authentication clearly.
- Use hashing for passwords, not reversible encryption.
- Recommend Sanctum, Fortify, Passport, or other auth packages only when the repository actually uses them or the requirements justify them.
- Keep security guidance conservative and explicit.

## Output expectations

When using this skill:

- State which Laravel subsystem the request belongs to.
- Explain why the suggested solution is the Laravel-native one.
- Call out version-sensitive or package-sensitive assumptions.
- Mention the smallest safe next edit.
