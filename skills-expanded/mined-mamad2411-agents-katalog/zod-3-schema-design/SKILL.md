---
name: zod-3-schema-design
description: Designs and modifies Zod 3 schemas, validation boundaries, preprocessing, transforms, inferred types, and explicit validation source-of-truth modules. Use when the task mentions Zod schemas, runtime validation, z.object, z.string, z.infer, safeParse, parse, environment validation, API validation, or TypeScript schema-first design.
license: MIT
compatibility: Requires Node.js for bundled helper scripts. Intended for TypeScript or JavaScript projects using Zod 3.
---

# Zod 3 Schema Design Skill

## When to Use

Use this skill when creating or changing Zod 3 schemas, parsing code, validation helpers, schema-derived TypeScript types, data normalization, environment/config validation, or boundary validators.

## First Checks

1. Identify the installed or intended Zod version.
2. Confirm the target is Zod 3.
3. Prefer root imports from `zod` for application code.
4. Run helper scripts with `--help` before using them:
   - `scripts/check-zod-version.mjs --help`
   - `scripts/zod-3-command-guard.mjs --help`

## Design Principles

- Treat external input as `unknown` until parsed.
- Validate at trust boundaries: API request bodies, route params, search params, headers, webhooks, queues, files, config, environment variables, and third-party responses.
- Keep shared schemas in a deliberate validation or contracts package when multiple runtimes consume them.
- Prefer explicit composition with `.extend()`, `.pick()`, `.omit()`, `.partial()`, `.required()`, and named schema constants.
- Use `.strict()` for external object payloads unless extra keys are intentionally accepted.
- Use `.passthrough()` only when callers must preserve unknown keys.
- Use `.catchall()` when unknown keys are allowed but must match a schema.
- Use `.superRefine()` for cross-field validation and multi-issue reporting.
- Use `z.preprocess()` for parsing raw strings, environment variables, dates, or numbers only when the conversion is intentional and tested.
- Use `.transform()` for deterministic normalization after validation.
- Export inferred types from schemas when schemas are the source of truth.

## Workflow References

- `workflows/schema-design-workflow.md`: Use when designing or changing a schema.
- `workflows/boundary-validation-workflow.md`: Use when adding validation to an API, config, environment, queue, file, or webhook boundary.

## Resources and Examples

- `resources/schema-patterns.md`: Zod 3-compatible schema patterns.
- `resources/zod-3-compatibility-matrix.md`: Zod 3 compatibility notes and Zod 4-only API warnings.
- `examples/schema-patterns.example.ts`: Practical schema examples.
- `examples/safe-parse-boundary.example.ts`: Boundary parsing helper example.
