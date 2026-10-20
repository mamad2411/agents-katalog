---
name: typescript-6-implementation
description: Implements and refactors TypeScript 6 code with strict typing, explicit runtime boundaries, maintainable APIs, and practical verification. Use when adding features, changing TypeScript source, improving types, or designing public APIs in a TypeScript 6 project.
license: MIT
compatibility: Requires a repository using TypeScript 6.x or migrating to TypeScript 6.x.
---

# TypeScript 6 Implementation

Use this skill when implementing, refactoring, or reviewing TypeScript 6 source code.

## Operating Principles

1. Confirm the local TypeScript version from project files or `tsc --version` before making version-sensitive changes.
2. Preserve runtime behavior while improving type safety.
3. Prefer explicit types at public boundaries and inferred types inside small, local implementation details.
4. Treat `unknown`, parsing, IO, environment variables, JSON, network responses, and framework inputs as untrusted until validated.
5. Avoid broad suppressions. A narrow suppression must include why it is safe and what would remove it.
6. Keep module format, runtime target, and package exports aligned with the existing project.

## Recommended Approach

- Inspect `tsconfig.json`, package scripts, and the affected source files.
- Identify whether the code is application code, library code, generated code, tests, or declarations.
- Choose types that describe the domain rather than types that merely satisfy the compiler.
- Prefer small pure functions for validation and transformations.
- Keep async errors explicit and avoid losing stack/context.
- Add tests for runtime behavior and, when useful, compile-time expectations through existing type-test tools.

## TypeScript 6 Configuration Awareness

When creating or editing `tsconfig.json`:

- Use explicit `types` for required global type packages.
- Use explicit `rootDir` when sources are under `src` or when project references are involved.
- Choose `moduleResolution` intentionally, typically `bundler` for bundled apps and `nodenext` for Node ESM/CJS package semantics.
- Prefer modern targets only when the runtime supports them.
- Avoid removed/deprecated options listed in `../typescript-6-migration-review/resources/typescript-6-migration-notes.md`.

## Workflows

Use `workflows/feature-implementation-workflow.md` when planning, implementing, and verifying a TypeScript feature or refactor.

## Resources and Examples

- `resources/tsconfig-baseline.md` gives practical TypeScript 6 `tsconfig` baselines.
- `examples/typed-result-pattern.md` shows explicit error modeling without `any`.
