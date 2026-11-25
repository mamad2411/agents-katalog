---
name: building-react-web-application
description: Guides building Vite + React SPA apps with TypeScript using a consistent architecture and library stack (Tailwind CSS v4, class-variance-authority, TanStack Router file-based routes, TanStack Query, Zustand, Axios, shadcn-style tokens, primitives in src/ui). Use when creating a new React web project or updating architecture/UI/state/API/routing/styling to follow these conventions.
version: 1.0.0
---

# React web application

Opinionated ecosystem for building Vite-based React SPAs with a consistent architecture, library stack, and UI system (`src/ui`).

## Tech stack

| Layer               | Choice                                                              |
| ------------------- | ------------------------------------------------------------------- |
| Bundler             | Vite                                                                |
| Language            | TypeScript                                                          |
| Styling             | Tailwind CSS v4, class-variance-authority (`cva` + `cx` from the same package) |
| Routing             | TanStack Router (file-based, `src/routes`)                          |
| Server state        | TanStack Query                                                      |
| Client global state | Zustand                                                             |
| HTTP                | Axios                                                               |
| Presentational UI   | shadcn/ui-style primitives in `src/ui/`                             |

## When to use

- New or existing Vite + React SPAs that use TanStack Router, Tailwind v4, and shared UI in `src/ui/`
- Architecture, library, or folder-structure decisions aligned with [structuring-project.md](./references/structuring-project.md)
- UI, state, API, routing (layouts, path params, search params), or styling work that should follow this skill’s conventions

## Companion skill

For **async `useEffect`**, **TanStack Form**, **ESLint / Prettier**, **es-toolkit / date-fns**, and **overriding `className`** with Tailwind, use together with [building-react-application](../building-react-application/SKILL.md).

Install it:

```bash
npx skills add cedmandocdoc/awesome-skills/skills/building-react-application
```

## References

| Task / scenario             | Doc                                                                                                                                                                                                                                                                       | When to use                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Project structure**       | [structuring-project.md](./references/structuring-project.md)                                                                                                                                                                                                             | Folders, `global.css` + `src/theme.css`, providers, `src/ui`, imports |
| **Environment variables**   | [managing-environment.md](./references/managing-environment.md)                                                                                                                                                                                                           | Per-module `env.ts`, Zod, Vite `VITE_*` / `import.meta.env`             |
| **Styling**                 | [styling.md](./references/styling.md), [styling-preference.md](./references/styling-preference.md), [Tailwind CSS — Using Vite](https://tailwindcss.com/docs/installation/using-vite)                                                                                     | Tailwind v4 + Vite, utilities, `cx` / CVA                               |
| **Theming & tokens**        | [setting-up-theming.md](./references/setting-up-theming.md), [setting-up-tailwind-theme.md](./references/setting-up-tailwind-theme.md)                                                                                                                                    | `global.css` + `src/theme.css`; shadcn **Configure styles** content only; semantic tokens |
| **Routing**                 | [configuring-routing.md](./references/configuring-routing.md), [TanStack Router — Installation with Vite](https://tanstack.com/router/latest/docs/installation/with-vite.md), [File-based routing](https://tanstack.com/router/latest/docs/routing/file-based-routing.md) | File-based routes, layouts, params, generated route tree                |
| **Fonts (web)**             | [MDN — @font-face](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face) · [Google Fonts](https://fonts.google.com/)                                                                                                                                               | Self-hosted or linked webfonts in CSS                                   |
| **Component placement**     | [placing-component.md](./references/placing-component.md)                                                                                                                                                                                                                 | `src/ui/` vs `src/features/`                                            |
| **Component creation**      | [creating-component.md](./references/creating-component.md)                                                                                                                                                                                                               | Props, compound parts, DOM primitives                                   |
| **Wrapper components**      | [managing-wrapper-components.md](./references/managing-wrapper-components.md)                                                                                                                                                                                             | Shallow trees; merge `className` with `cx`                              |
| **Component abstraction**   | [abstracting-component.md](./references/abstracting-component.md)                                                                                                                                                                                                         | Registry-first, shadcn / add script, presentation-only `src/ui/`        |
| **Component naming**        | [naming-component.md](./references/naming-component.md)                                                                                                                                                                                                                   | Names across `src/ui/` and features                                     |
| **Feature modules**         | [creating-feature.md](./references/creating-feature.md)                                                                                                                                                                                                                   | Feature layout, barrels, isolated vs grouped                            |
| **Feature promotion**       | [promoting-feature.md](./references/promoting-feature.md)                                                                                                                                                                                                                 | Promote to `src/ui/` or extract a feature                               |
| **State management**        | [managing-state.md](./references/managing-state.md)                                                                                                                                                                                                                       | Query vs Zustand vs local vs route state                                |
| **API clients**             | [creating-api.md](./references/creating-api.md), [setting-up-axios.md](./references/setting-up-axios.md)                                                                                                                                                                  | Axios, feature hooks, `src/api/`                                        |
| **Adding UI from registry** | [adding-registry-components.md](./references/adding-registry-components.md), [add-registry-component.js](./scripts/add-registry-component.js)                                                                                                                                 | Validate with `shadcn view` + registry-item schema; then vendor into `src/ui/` with `cx` + path fixes, or create UI manually |
| **Linting & formatting**    | [linting.md](./references/linting.md)                                                                                                                                                                                                                                     | Ignore `routeTree.gen.ts`; baseline ESLint/Prettier via companion doc     |
