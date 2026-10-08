---
name: core-principles
description: >-
  Project-wide defaults: stack role, functional style, naming and exports, safety boundaries (no invented APIs,
  no tooling changes without approval), WCAG and Web Vitals, and hallucination prevention. Use for any task in
  this repository when other skills do not already specify behavior.
---

# Core principles and boundaries

## When to use

Apply as **baseline** guidance for AI-assisted work in this repo: new features, refactors, reviews, and answers about the codebase. When two skills could disagree, use **[Precedence when skills overlap](#precedence-when-skills-overlap)** instead of guessing.

---

## Precedence when skills overlap

Narrower or **file-type-specific** skills **override** broader ones for their scope—use the **first** row below that **matches the file or concern** (row **1** beats **2**, and so on):

1. **`unit-testing-vitest-jest`** — `*.test.*`, `*.spec.*`, and **layout inside** those files (mocks, `describe`, spacing).
2. **`nextjs-route-handlers`** — `app/**/route.ts` / `route.tsx` (return types, colocation with `route.test.ts`).
3. **`react-common-conventions`** — React **components**, **hooks**, **providers**, **client effects**, colocation, rerenders, Next **default exports** for special `app/` files.
4. **`typescript-common-conventions`** — **Language-level** rules in **`.ts`** and in **`.tsx`** outside react-common’s UI focus (e.g. **`let`**, semicolons, **`type`/`interface`**, **`switch`**, generics on helpers).
5. **`core-file-and-filesystem-structure`** — **Paths**, **kebab-case**, **module section order**, **import tiers** (unless overridden above).
6. **`core-error-handling`** — **Errors**, **validation** at boundaries, **async** cleanup, safe logging vs user exposure.
7. **`core-principles`** — **Baseline** when nothing above applies.

---

## Role (expected expertise)

Assume familiarity with **TypeScript**, **Node.js**, **React**, **Next.js** (this project uses the **App Router** under `app/`), **HTML5**, **CSS3** (including **Tailwind** where the project uses it), **WCAG-oriented** UI guidance, and **performance** (especially **Web Vitals**).

Testing and tooling in this repository include **Vitest**, **@testing-library/react**, **Prisma**, **ESLint**, and **Cucumber** E2E—do **not** assume **Jest**, **Vite** as the app bundler, or **React Hook Form** unless they appear in `package.json` or the user asks for them.

---

## Core principles

### Style and structure

- Prefer **functional, declarative** code; **avoid classes** unless integrating with a library that requires them.
- **Modularize** shared logic instead of copying it; extend existing helpers and patterns in the repo.
- Keep explanations **concise and technical**; when showing TypeScript, keep examples **accurate** to this project’s patterns (see sibling rules under `rules/`).

### Naming and APIs

- Use **descriptive names**; for booleans and flags, prefer **auxiliary verbs** (e.g. `isLoading`, `hasError`, `shouldRefetch`).
- Prefer **named exports** at module boundaries unless the file already uses a single default export for a framework convention.

### RORO and parameters

- Prefer **RORO** (receive an object, return an object) for functions with **several** inputs or outputs—see **`rules/react-common-conventions/SKILL.md`** for hooks, component props, and UI helpers; use the same idea for **shared `.ts` utilities** (e.g. `(options: { … })` / `return { … }`) when the API is not a single obvious value.

---

## Safety and scope boundaries

- **Do not invent** APIs, files, routes, env vars, or dependencies: base suggestions on **what exists in the repo** or what the user **explicitly** requested.
- **Do not add packages** or change **tooling** (build, CI, lint config, `package.json` scripts, Husky, etc.) **without explicit approval**, unless the user’s request is specifically to do that.
- **Do not** surface or echo **secrets**, tokens, keys, or credentials; use placeholders and env var **names** only.
- When proposing **UI** changes, respect **WCAG** (semantics, focus, contrast, motion) and **performance** (avoid unnecessary work on the critical path; align with Web Vitals where relevant).
- If requirements are **ambiguous**, **ask** for clarification instead of guessing behavior or scope.

---

## Hallucination prevention

- **Verify** imports, paths, and public APIs (e.g. `app/`, `features/`, `components/`) against the **actual tree** or files before relying on them.
- Use **only** dependencies present in **`package.json`** (or named by the user); do not assume a library is installed because it is common elsewhere.
- Avoid **speculative** behavior: if you must assume something, **state the assumption** and offer to adjust once confirmed.

---

## Installing with the Vercel skills CLI

From this repository root:

```bash
npx skills add . --skill core-principles -a cursor -y
```

List all skills in this repo:

```bash
npx skills add . --list
```
