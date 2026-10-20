---
name: monorepo-package-boundaries
description: Use when deciding or consolidating monorepo packages.
---

# Monorepo package boundaries

Use workspace packages for real architectural boundaries, not merely to organize folders. This skill guides deciding whether code belongs in a shared library package, deserves an independent package, or belongs inside a runnable application.

## When to use

- A monorepo has many small internal packages and package maintenance exceeds their architectural value.
- Creating a new shared module, utility, policy, provider adapter, model catalog, or configuration surface.
- Consolidating packages without changing runtime behavior.
- Deciding when a section of a shared library has matured enough to extract.
- Reviewing package manifests, workspace dependencies, subpath exports, or cross-package import graphs.

Do not use package extraction as a substitute for ordinary folders and modules inside one cohesive package.

## Core principle

A package is a compatibility and dependency boundary. A folder is an organization boundary.

Small repository-internal concerns that are versioned, tested, released, and deployed together should normally begin in one shared package such as `@repo/lib`. Preserve conceptual separation with explicit subpath exports:

```ts
import { modelSpecifier } from "@repo/lib/models";
import { clampInteger } from "@repo/lib/utils";
```

Avoid a broad `@repo/lib` root barrel. Explicit subpaths keep dependencies visible, support tree-shaking, and make later extraction mechanical.

## Boundary test

A concern deserves an independent package when at least one concrete boundary exists:

1. **Dependency compatibility:** it needs an independent or conflicting dependency version.
2. **Operational ownership:** it owns deployment, persistence, runtime, scheduling, or infrastructure.
3. **Security:** it owns credentials, trust, permissions, or a distinct attack surface.
4. **External contract:** it has external consumers or an independent release contract.
5. **Organizational ownership:** a distinct team owns a cohesive public API.
6. **Independent replacement:** it must be replaced or versioned without coordinating all shared-library consumers.
7. **Material dependency cost:** unrelated consumers pay a measurable install or bundle cost that explicit subpaths and tree-shaking cannot avoid.

File count, a clean conceptual noun, and speculative future reuse are not sufficient.

## Decision workflow

1. **Inventory the live graph.** Read every workspace manifest, source/test file count, internal import, export map, runtime target, and version pin. Do not decide from directory names alone.
2. **Classify existing boundaries.** Mark deployment, security, persistence, infrastructure, compatibility, external-consumer, and package-resolution boundaries.
3. **Choose the default home.** Put code without a concrete boundary in a shared library section. Keep meaningful boundaries independent even when their source is small.
4. **Design explicit exports.** Give each section a stable subpath. Do not expose a root barrel unless a genuine unified API exists.
5. **Keep internal imports relative.** Sections inside one package should import each other through relative paths, not through the package's workspace name; this avoids self-dependencies and works before workspace linking.
6. **Resolve dependency unions.** Merge runtime dependencies into the shared package, then check for incompatible versions, Node-only modules, Cloudflare/browser constraints, and optional integrations. A version conflict is evidence that a package may deserve independence.
7. **Select compatibility policy.** In a private monorepo with no external consumers, prefer a clean break and remove old package names. Use forwarding packages only when a verified consumer requires a migration window.
8. **Preserve path-sensitive assets.** Inspect encrypted configs, generated files, Markdown skills, Python scripts, and `import.meta.url`/relative-file lookups before moving directories.
9. **Update every consumer.** Change source imports, test imports, manifests, generators, docs, build scripts, config tags, and lockfiles in the same migration.
10. **Verify the real artifacts.** Typechecking alone is insufficient when bundlers, scanners, deployment manifests, or runtime externalization are involved.

## Proportional process

Match ceremony to uncertainty, not to the mere fact that files will move.

- When the user has named the consolidation scope and explicitly says to implement it, do not force a separate spec or implementation-plan approval cycle. Restate the package cut in one sentence, write the red architecture test, and execute.
- Use a design document only when ownership is unresolved, external compatibility must be negotiated, several materially different boundaries remain plausible, or the migration is independently irreversible.
- Do not turn an ordinary internal clean break into a sequence of repeated architecture questions. The live import graph and verification gates should resolve mechanical details.
- If a protected guidance file such as `AGENTS.md` requires a separate write approval, do not bypass or repeatedly retry the gate. Complete safe code changes, report the one blocked documentation edit precisely, and obtain explicit approval separately.

## Test-first migration

Before moving production files, add or update an architecture test and watch it fail for the intended reason. It should assert:

- the new shared package and explicit exports exist;
- forbidden root barrels are absent;
- packages that must remain independent still exist;
- consolidated package directories and old package names are absent;
- live source/manifests contain no old imports;
- application/deployment boundaries remain unchanged.

After the move, run targeted tests first, then the repository-wide static, test, and build gates.

## Verification matrix

Use the repository's canonical commands, plus checks appropriate to its runtimes:

1. frozen dependency install or lockfile consistency check;
2. workspace typecheck/lint/format gate;
3. all offline tests, verifying moved suites are still discovered;
4. every runnable application build;
5. generated artifact inspection for stable registrations, bindings, flags, and migrations;
6. built-runtime health smoke when feasible;
7. searches for old package names, paths, aliases, and forwarding manifests;
8. whitespace/diff validation;
9. no live external deployment unless separately authorized.

See `references/consolidation-checklist.md` for a compact migration worksheet and common failure modes.

## Graduation from the shared library

When a section gains a real boundary, extract it deliberately:

1. prove the boundary with concrete consumers, dependency conflicts, or operational ownership;
2. give it a focused public API and package manifest;
3. move its tests and assets with it;
4. replace the shared-library subpath in one migration;
5. use a compatibility export only if verified external consumers need it;
6. record why it graduated so later cleanup does not merge it back blindly.

## Pitfalls

- **Package per noun:** conceptual neatness creates workspace and release overhead without isolation.
- **Root barrel by default:** consumers accidentally couple to unrelated concerns.
- **Self-imports inside the shared package:** builds depend on workspace resolution and can form false dependency cycles.
- **Merging meaningful boundaries:** security, runtime, infrastructure, or version conflicts are lost in a generic library.
- **Treating source imports and manifests alike:** source uses `@repo/lib/models`, but manifest dependency keys must use the package root `@repo/lib`. Update them separately.
- **Duplicate dependency sections after collapse:** when several old packages become one, deduplicate `@repo/lib` across runtime/dev sections; a runtime dependency already satisfies package tests.
- **Assuming subpath imports prevent all bloat:** inspect real build output. Some bundlers externalize exact direct package names but bundle `@repo/lib/models`, changing artifact size even though `@repo/lib` is declared.
- **Testing the literal root export with dotted-path matchers:** matchers such as `toHaveProperty(".")` may parse the dot as a path. Use `Object.hasOwn(exports, ".")`.
- **Losing tests during directory moves:** stale Vitest globs can report success while running fewer suites.
- **Merged TypeScript projects exposing stricter test errors:** old package tsconfigs may have omitted tests or used different strictness. Keep moved tests in the consolidated `tsconfig`, repair unsafe mock indexing and optional-result assumptions, and do not weaken compiler settings merely to preserve the old accidental gap.
- **Editing encrypted configuration as plain text:** use the authenticated encryption tool so metadata/MAC stays valid.
- **Leaving shims forever:** forwarding packages preserve the package sprawl the consolidation was meant to remove.
