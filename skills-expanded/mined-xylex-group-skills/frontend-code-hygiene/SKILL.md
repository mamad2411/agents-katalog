---
name: frontend-code-hygiene
description: Enforce strict React and TypeScript frontend implementation conventions for this workspace. Use when Codex is creating, refactoring, or reviewing TS, TSX, JSX, or component-adjacent frontend code and needs to apply rules around module structure, naming, JSX control flow, hook stability, client component prop shape, icon usage, Tailwind color usage, and mock-first component design.
---

# Frontend Code Hygiene

## Apply the Skill

- Read `references/rules.md` before making frontend edits.
- Treat those rules as the default implementation standard unless the surrounding codebase already enforces a different local pattern or the user explicitly overrides one.
- Fix the named seam first. Do not redesign unrelated code just to satisfy a style preference.

## Work in This Order

1. Define the UI contract first.
   - For a new component, start with a realistic mock data shape that matches the intended final interface before wiring helpers, queries, or backend functions.
2. Keep the module graph lean.
   - Avoid barrel files.
   - Prefer alias imports over long relative traversals when the repo supports them.
3. Make render logic explicit.
   - Replace nested ternaries with named variables, condition blocks, or early returns.
   - Use stable keys from the data model instead of array indices.
4. Keep React APIs stable and serializable.
   - In `"use client"` entry files, keep props serializable unless a prop is an explicit server action that follows the repository naming rule.
   - Avoid placeholder no-op functions, undefined-heavy context defaults, and `void` fire-and-forget patterns.
5. Match the visual system.
   - Prefer shared icon libraries over raw inline SVG.
   - Use CSS color tokens instead of hardcoded Tailwind colors or `dark:` variants.
6. Finish with lint-shaped cleanup.
   - Resolve hook dependency instability, missing iterable callback returns, inconsistent array type syntax, and similar findings listed in `references/rules.md`.

## Decision Rules

- Prefer the repo's existing abstractions over introducing a new wrapper or helper just to satisfy a single rule.
- Keep naming in `owner_trait` form such as `user_settings` and stay consistent about singular versus plural.
- When a rule conflicts with established nearby code, match the local pattern unless the user asked for a cleanup or migration.

## Reference Map

- Read `references/rules.md` for the concrete checklist, examples, and lint-message mappings.
