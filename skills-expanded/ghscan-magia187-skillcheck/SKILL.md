---
name: no-new-deps
description: >-
  Use when implementing a feature or fix in a Node/TypeScript repo. Prefer
  existing dependencies and stdlib; block casual new packages unless justified.
---

# No New Dependencies

## When to use

- Adding features, utilities, or refactors in a JS/TS project.
- The user did **not** explicitly ask to add a library.
- Reviewing a change that touches `package.json` / lockfiles.

## When not to use

- The user explicitly requested a named package.
- Security patches that require a dependency bump.
- Greenfield prototypes where dependency policy is waived.

## Assumptions

- Project uses npm, pnpm, or yarn; lockfile may be present.
- Shell access to run `npm ls` / package manager commands.
- Network installs are allowed only after confirmation when a new dep is truly needed.

## Policy

1. **Default: no new runtime dependencies.**
2. Prefer Node built-ins (`node:fs`, `node:path`, `node:crypto`, `fetch`) and already-installed packages.
3. Dev-only tools still need a one-line justification.
4. If a new dependency seems necessary, stop and ask — include size, license, and why alternatives fail.

## Workflow

1. Read `package.json` dependencies before reaching for something new.
2. Search the repo for an existing helper that solves the same problem.
3. Implement with stdlib or current deps.
4. If blocked, propose at most one candidate library with rationale — do not install yet.

## Success criteria

- [ ] `package.json` unchanged, **or** change is explicitly approved.
- [ ] Solution uses existing APIs where possible.
- [ ] Any proposed dependency includes why stdlib/current deps are insufficient.
- [ ] No drive-by lockfile churn.

## Out of scope

- Language migrations (e.g. introducing Rust tooling).
- Monorepo-wide dependency governance (use a dedicated policy skill).
