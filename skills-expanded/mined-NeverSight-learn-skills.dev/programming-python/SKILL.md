---
name: programming-python
description: Write, change, review, and test modern Python using repository-native environments, precise static typing, validated boundaries, explicit errors, restrained dependencies, and complete local quality gates. Use for Python applications, libraries, packages, CLI tools, services, scripts, and asynchronous code.
license: MIT
---

# Programming Python

Produce modern Python whose types and tests make behavior explicit. Follow the repository's architecture and configured tools before applying these defaults.

## Establish the Contract

1. Inspect project metadata, every dependency or constraint file, lockfiles, supported Python versions, package layout, entry points, CI, tests, and repository guidance.
2. Determine whether the project is an application, library, service, CLI, package, or script collection. Record its public imports, serialized forms, CLI behavior, exceptions, and other compatibility boundaries before changing them.
3. Use the repository's declared environment, package manager, build backend, and locked commands. Do not infer the interpreter from the machine default, regenerate a lock without an in-scope dependency change, install tools globally, or migrate an established workflow merely because another tool is preferred.
4. For a new project without established tooling, choose a current maintained workflow deliberately from deployment, packaging, and contributor needs. For a library, declare and test an intentional minimum Python version; for an application, follow its declared deployment interpreter.

## Implement Strictly

- Type all changed production interfaces and meaningful local values precisely. Do not introduce unrestricted `typing.Any`, bare containers, unchecked casts, ignored diagnostics, or annotation-only claims unsupported at runtime.
- Receive genuinely untrusted values as `object`, then parse JSON, configuration, environment variables, database rows, CLI input, and network data once at the system boundary. Prefer the repository's existing rigorous validator. Otherwise use a small explicit parser for a small shape or justify one maintained dependency when nested schemas, unions, refinements, or error reporting make handwritten parsing less trustworthy.
- Convert parsed input into explicit domain values such as existing models, dataclasses, enums, tuples, or ordinary typed classes. Keep loose mappings at serialization boundaries rather than passing them through domain logic. Do not add runtime validation machinery to values already guaranteed by trusted construction.
- Raise precise domain exceptions, preserve exception chains, and catch only errors that can be handled meaningfully. Forbid bare `except`, silent failures, and sentinel returns for genuine errors.
- Prefer the standard library and minimize dependencies. Require a concrete benefit for large, overlapping, weakly maintained, or security-sensitive packages; keep direct dependencies declared and environments locked.
- Keep synchronous code by default. Use async only for genuine concurrent I/O, follow the project's existing async stack, and keep blocking work off the event loop.
- Prefer clear functions and composition over speculative classes, frameworks, decorators, metaprogramming, or compatibility layers. Preserve public API compatibility unless a breaking change is requested.

## Prove the Change Locally

Use the project's testing library and conventions. Add focused tests for changed behavior, boundary validation, failure paths, and preserved public behavior; prefer real local integrations over mocks when practical.

Before completion, run every applicable gate through the repository's declared environment against the final worktree:

1. the repository's own formatting, linting, type-checking, and test commands;
2. focused boundary and failure tests, then the complete relevant suite and configured coverage threshold;
3. the repository's strictest configured static type checker without ignored new diagnostics;
4. package builds, metadata checks, and clean installation or import checks for distributable projects;
5. dependency, lock, security, and policy checks when configured;
6. a real invocation of the built application, command, public library interface, or integration boundary.

Do not silently add a formatter, linter, type checker, validator, or packaging migration to satisfy this checklist. When adding a missing gate is separately in scope, require it to be maintained, compatible with the existing workflow, and no weaker than current policy.

Test every supported Python version for libraries when locally practical. Report the exact commands run, interpreter versions exercised, behavior observed, baseline failures, and every gate that could not run with the reason. Mark conflicting or unavailable evidence as unclear rather than assuming it passed.
