---
name: tanstack-start-project-init
description: >-
  Bootstraps TanStack Start apps with Bun, ESLint, Nitro deployment, and CLI add-ons
  (nitro, table, store, shadcn, form, compiler, drizzle) using bunx @tanstack/cli create
  with --no-examples; after create, runs bunx shadcn init with preset b6Z8GIMhE and
  template start, then removes all route modules under src/routes except index.tsx and
  __root.tsx, clears main in index route, strips Header/Footer from __root.tsx, removes
  Header, Footer, and demo.FormComponent components, and deletes demo.FormComponent file.
  Use when
  scaffolding a new TanStack Start project, this
  preset, or Bun + Nitro + Drizzle + shadcn Start setup.
---

# TanStack Start — Project Init (preset)

Scaffolds a **new** TanStack Start repository using the owner’s default CLI flags. For ongoing patterns (server functions, auth, SSR), use **`tanstack-start-best-practices`**. For shadcn-specific UI work after scaffold, use **`shadcn`** when available.

## Prerequisites

- **Bun** installed (`bun --version`).
- Network access for `bunx` to fetch `@tanstack/cli@latest`.

## Default scaffold command

Replace `<project_name>` with the target directory name (creates that folder).

```bash
bunx @tanstack/cli@latest create --no-examples \
  --add-ons=nitro,table,store,form,compiler,drizzle \
  --package-manager=bun \
  --deployment=nitro \
  --toolchain=eslint \
  <project_name>
```

### What this preset selects

| Flag / add-on                           | Role                                                                       |
| --------------------------------------- | -------------------------------------------------------------------------- |
| `--no-examples`                         | Minimal tree without sample routes/pages from the template.                |
| `nitro` (add-on + `--deployment=nitro`) | Nitro-oriented server/deploy path from the CLI.                            |
| `table`, `store`, `form`                | TanStack Table, Store, and Form add-ons via the scaffold.                  |
| `compiler`                              | React/compiler-related option as offered by the CLI at create time.        |
| `drizzle`                               | Drizzle ORM scaffolding (migrations/schema layout per generated template). |
| `--package-manager=bun`                 | Bun as package manager for the new project.                                |
| `--toolchain=eslint`                    | ESLint (and typical Prettier integration) for lint/format per CLI template. |

## Agent workflow

Copy and track progress:

```
- [ ] Confirm project name (folder) with the user if unclear
- [ ] Run the scaffold command from the repo parent directory
- [ ] cd into <project_name>
- [ ] Post-init: apply in order — `rules/post-init-shadcn-init.md`, `rules/post-init-route-trim.md`, `rules/post-init-shell-cleanup.md`
- [ ] Run the dev script from package.json (typically bun run dev — verify in file)
- [ ] Confirm dev server starts and default page loads without fatal errors
- [ ] Note any .env.example / README env vars for the user
```

## Rules (post-init)

After scaffold, **always** run these in order:

1. **[rules/post-init-shadcn-init.md](rules/post-init-shadcn-init.md)** — `bunx --bun shadcn@latest init --preset b6Z8GIMhE --template start` from project root.
2. **[rules/post-init-route-trim.md](rules/post-init-route-trim.md)** — keep only `__root.tsx` and `src/routes/index.tsx`; regen route tree; run ESLint / project lint script.
3. **[rules/post-init-shell-cleanup.md](rules/post-init-shell-cleanup.md)** — follow it fully: Hello Agent inside `<main>` in `index.tsx`, delete listed template/demo files (components, data, hooks, `src/lib` demo store files; see rule for `utils.ts`), remove Header/Footer **imports and JSX** from `__root.tsx`, remove default TanStack template CSS and keep only shadcn styles/tokens, drop orphaned imports/usages; verify with check + dev.

## After init

1. **Full-stack patterns**: read and follow **`tanstack-start-best-practices`**.
2. **Components / registry**: use **`shadcn`** skill for add-component and styling conventions.
3. **Database**: Drizzle files and commands are template-specific — prefer the generated README and `package.json` scripts over guessing.

## If the command fails

CLI flags and add-on names can change between releases.

1. Run `bunx @tanstack/cli create --help` and align flags with the current output.
2. Retry with corrected names; keep the same intent (Bun + ESLint + Nitro + listed add-ons).

## Anti-patterns

- Do not use this skill for **refactors** or **feature implementation** inside an existing app — only **new project scaffold** (or explicit “recreate from scratch”).
- Do not assume global `tanstack` CLI unless the user prefers it; **default is `bunx @tanstack/cli`**.
