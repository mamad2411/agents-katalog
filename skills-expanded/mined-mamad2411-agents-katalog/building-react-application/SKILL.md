---
name: building-react-application
description: Guides building React web applications with TypeScript using consistent patterns for effects, data fetching, component structure, shared JS utilities, and date handling. Use when implementing or reviewing React UI, hooks, side effects, or utility usage in browser-based apps.
version: 1.0.0
---

# React (web)

Opinionated patterns for React web apps: effects, async work, and conventions that keep hooks predictable and lint-friendly.

## When to use

- New or existing React web projects (TypeScript) where side effects and async flows should follow shared conventions
- Code review or implementation questions about `useEffect` and promise-based work
- Choosing or reviewing general-purpose JS utilities (debounce, chunk, object picks, lodash-style helpers) or date/time handling alongside React code
- ESLint and Prettier setup for React web (Vite) or React Native (Expo) TypeScript projects
- Adding or extending reference docs for topics this skill covers (routing, forms, data fetching libraries, etc.)

## Utilities

Prefer established libraries over ad-hoc helpers. Import specific functions so bundlers can tree-shake.

| Focus | Doc / resources | When to use |
| ----- | --------------- | ----------- |
| **General-purpose JS** | [es-toolkit](https://github.com/toss/es-toolkit) | Debounce, chunk, object helpers; TypeScript-first types; optional **`es-toolkit/compat`** for lodash-shaped APIs; strong performance vs older utility stacks |
| **Dates and time** | [date-fns](https://github.com/date-fns/date-fns) · [API docs](https://date-fns.org/) | Format, parse, compare, and manipulate native `Date` values; locale-specific formatting via `date-fns/locale`; first-class time zone support in v4+ |

**Agent skill (es-toolkit, recommended):** install the upstream skill so tooling has es-toolkit-specific guidance:

```bash
npx skills add toss/es-toolkit
```

Use that skill together with this one when adding or refactoring utilities (imports, compat migration, or picking functions over hand-rolled helpers).

## Tooling

| Task / scenario | Doc | When to use |
| --------------- | --- | ----------- |
| **Linting & formatting** | [linting.md](./references/linting.md) | ESLint, Prettier; React web (Vite + Hooks) or React Native (Expo) setup |

## Hook implementation references

| Task / scenario              | Doc                                                                                             | When to use                                      |
| ---------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Handling async in `useEffect`** | [handling-async-in-use-effect.md](./references/handling-async-in-use-effect.md) | Promises in effects; `.then` / `.catch` vs `async` effect callbacks |

## Styling and components

| Task / scenario | Doc | When to use |
| --------------- | --- | ----------- |
| **Overriding `className` on shared components** | [overriding-classname.md](./references/overriding-classname.md) | Tailwind utilities passed via `className` conflict with base classes; use `!` on the consumer utility so the override wins |

### Managing forms (TanStack Form)

TanStack Form guides (linked below use the **Solid** doc tree; for React web, use the same paths under `framework/react/guides/…` and [`@tanstack/react-form`](https://tanstack.com/form/latest/docs/framework/react/overview)).

| Topic                  | Doc                                                                                                                                   | When to use                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Concepts**           | [Basic concepts](https://tanstack.com/form/latest/docs/framework/solid/guides/basic-concepts)                                         | Form options, instances, fields, field state/meta, validation basics, arrays |
| **Validation**         | [Form and field validation](https://tanstack.com/form/latest/docs/framework/solid/guides/validation)                                  | When to validate, field vs form validators, async + debounce, Standard Schema, submit gating |
| **Composition**        | [Form composition](https://tanstack.com/form/latest/docs/framework/solid/guides/form-composition)                                     | `createFormHook`, pre-bound fields/forms, `withForm` / `withFieldGroup`, lazy + tree-shaking |
| **Dynamic validation** | [Dynamic validation](https://tanstack.com/form/latest/docs/framework/solid/guides/dynamic-validation)                                 | `onDynamic`, `revalidateLogic`, mode before/after first submit               |
| **Async initial values** | [Async initial values](https://tanstack.com/form/latest/docs/framework/solid/guides/async-initial-values)                           | Loading remote defaults; pairing with TanStack Query                          |
| **Linked fields**      | [Linked fields](https://tanstack.com/form/latest/docs/framework/solid/guides/linked-fields)                                           | Re-validate when another field changes (`onChangeListenTo` / `onBlurListenTo`) |
| **Arrays**             | [Arrays](https://tanstack.com/form/latest/docs/framework/solid/guides/arrays)                                                         | List fields, `mode="array"`, nested keys, add/remove items                    |
