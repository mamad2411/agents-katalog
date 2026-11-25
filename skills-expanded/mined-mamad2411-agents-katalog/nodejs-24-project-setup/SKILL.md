---
name: nodejs-24-project-setup
description: Sets up or modernizes Node.js 24 projects with correct runtime metadata, npm scripts, module boundaries, dependency hygiene, native TypeScript constraints, and quality checks. Use when creating, auditing, or normalizing a Node.js 24 project.
license: MIT
compatibility: Requires Node.js 24.x and npm 11.x for command execution examples.
---

# Node.js 24 Project Setup

Use this skill when creating a new Node.js 24 project or aligning an existing project with Node.js 24 runtime expectations.

## Goals

- Confirm the project targets Node.js 24.x.
- Keep runtime guidance framework-neutral.
- Make package metadata explicit.
- Choose ESM or CommonJS deliberately.
- Prefer built-in Node.js 24 capabilities before adding dependencies.
- Add reproducible install, test, type-check, lint, and build scripts when relevant.
- Keep TypeScript runtime behavior honest: Node strips types but does not type-check.

## Workflow

Use [new-project-workflow](workflows/new-project-workflow.md) for repeatable setup or modernization.

## Resources

Use [nodejs-24-project-checklist](resources/nodejs-24-project-checklist.md) for setup checks.

## Example

Use [package-json-example](examples/package-json-example.json) as a minimal metadata reference. Adapt scripts to the repository’s actual tools.

## Instructions

1. Inspect existing files before changing project metadata:
   - `package.json`
   - `package-lock.json`
   - `.npmrc`
   - `tsconfig.json`
   - source and test directories
2. Verify the project actually targets Node.js 24.
3. Recommend `engines.node: ">=24 <25"` for Node.js 24-only projects.
4. Do not add ESLint, TypeScript, bundlers, or test frameworks unless the project already uses them or the user asks for them.
5. Prefer `node --test` for simple runtime-level tests.
6. Prefer explicit `node:` imports in examples.
7. For TypeScript:
   - Explain that Node.js runtime type stripping is not type checking.
   - Keep `tsc --noEmit` when type safety matters.
   - Avoid TypeScript syntax that requires transformation unless the project has a compiler step.
8. For dependencies:
   - Prefer `npm ci` in CI when `package-lock.json` exists.
   - Do not regenerate lockfiles unless dependency changes require it.
9. For scripts:
   - Add only scripts that can actually run in the repository.
   - Avoid scripts that require unavailable dependencies.
10. Before running bundled scripts, run `scripts/nodejs-24-quality-check.sh --help`.
