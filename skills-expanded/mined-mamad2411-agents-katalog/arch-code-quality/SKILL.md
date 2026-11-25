---
name: arch-code-quality
description: Write, inspect, and maintain high-quality production code. Covers cross-language
  coding standards, backend and frontend architecture patterns, codebase inspection
  and metrics, repository scanning for assets/quality, and clean git workflow. Use
  for new code, refactoring toward conventions, code-quality audits, dependency/repo
  analysis, and general "write good code" guidance.
---

# Code Quality & Standards (composite skill)

Write, inspect, and maintain high-quality production code. Composed from:
coding-standards, backend-patterns, frontend-patterns, codebase-inspection, repo-scan,
git-commit.

## When to activate

- Writing new production code (any language)
- Refactoring toward project conventions
- Code-quality audit of a module
- Understanding repo structure, language mix, or dependencies
- Git commit / branch hygiene

## A. Coding standards (cross-language)

### Code quality principles
- **Clarity over cleverness**: readable, maintainable, self-documenting.
- **Immutability** where practical; minimize hidden state.
- **Small, focused units** — one responsibility, single reason to change.
- **Naming**: descriptive, intention-revealing, consistent.
- **No dead code**: unused exports, branches, parameters removed.
- **YAGNI**: no speculative abstraction.

### Language conventions
- **TypeScript/JavaScript**: strict typing, no `any`, proper null/undefined handling,
  modern syntax, named exports.
- **React**: components small, hooks rules respected, keys stable, memo only when needed.
- **Python**: PEP 8, type hints, explicit imports.
- **Rust**: idiomatic ownership, `Result` over panics, clippy-clean.
- **Go**: `gofmt`, errors as values, no panics in libs.

### File organization
- Logical grouping by feature/domain, not by type.
- Stable import order, no circular deps.
- Test files co-located or mirrored structure.

### Comments & documentation
- Comments explain WHY not WHAT (code says what).
- Public APIs documented; docstrings accurate.
- No stale/rotten comments.

### Testing standards
- Test behavior, not implementation.
- Cover edge cases, error paths, boundaries.
- Fast unit tests + focused integration tests.
- Tests must fail meaningfully if behavior changes (pin behavior).

### Code smell detection
- Duplication, long methods, god objects, shotgun surgery, feature envy,
  speculative generality, primitive obsession.

## B. Backend patterns

- **API design**: resource naming, status codes, pagination/filtering, versioning,
  validation, rate limiting.
- **Database**: schema design, index strategy, N+1 avoidance, migrations.
- **Caching**: cache-aside, TTL strategy, invalidation on write.
- **Error handling**: typed errors, retries with backoff, circuit breakers,
  fail-closed vs fail-open (deliberate).
- **AuthN/AuthZ**: token strategy, scopes, permissions, least privilege.
- **Background jobs & queues**: idempotency, retries, dead-letter handling.
- **Logging & monitoring**: structured logs with context, request IDs, alert thresholds.

## C. Frontend patterns

- **Components**: single responsibility, controlled/uncontrolled, prop stability.
- **Hooks**: custom hooks for shared logic, deps correct, no stale closures.
- **State management**: local state first, server state cached, avoid over-globalizing.
- **Performance**: memoization when measured needed, code splitting, list keys, bundle size.
- **Forms**: validation UX, error display, controlled inputs, dirty-state handling.
- **Error boundaries**: graceful fallbacks, no blank screens.
- **Accessibility**: semantic HTML, ARIA, keyboard nav, contrast, focus management.

## D. Codebase inspection & metrics

- **Language mix and LOC** per area (e.g. with pygount): `pygount --format=summary`.
- **Exclude** build artifacts, vendored deps, generated code when measuring.
- **Filter by language** to see real production code vs generated.
- **Module/area sizing**: which modules are largest → where complexity lives.

## E. Repository scan (assets & third-party)

- Classify every source file by module and purpose.
- **Detect embedded third-party libraries** (vendored, copied) — they bypass dependency
  management and security scanning.
- Deliver a four-level verdict per module: healthy / needs attention / legacy /
  remove-or-replace.
- Flag: unmanaged dependencies, duplicated code, dead assets, large binaries in git.

## F. Git workflow

- **Descriptive commit messages**: `type(scope): summary` + why.
- Commit related changes together; don't mix concerns.
- Clean up stale local branches marked `[gone]` (deleted on remote) — including
  associated worktrees.
- PR flow: commit → push → PR with clear description.

## Output

For audits: structured findings per module with evidence (file paths, metrics),
prioritized (what to fix now vs later vs leave). For writing: code that passes
conventions, has tests, and is reviewed.

## Related skills
- `arch-code-architecture` — system structure the code implements
- `arch-code-review` — verify the code meets these standards
- `arch-refactoring` — fix code that doesn't meet standards
