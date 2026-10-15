---
name: jan-fe-dev
description: Use when asked to create, scaffold, build, restructure, standardize, or improve a frontend project, including Astro, React, Vue, Next.js, TypeScript, Tailwind CSS, frontend architecture, and project conventions.
---

# Jan Frontend Development

## Overview

Use one decision and structure workflow for new and existing frontend projects. Do not change files until the required context is known.

## Required opening

1. Determine whether this is a new or existing project without changing files.
2. Ask for the project name when the user has not supplied one. This is always the first question.
3. For a new project, ask its purpose and whether it needs SEO.
4. Read [frameworks-and-bootstrap.md](references/frameworks-and-bootstrap.md), explain the applicable choices and trade-offs, and let the user choose. Do not scaffold before explicit selection.
5. For an existing project, inspect its framework, package manager, lockfile, routing, dependencies, source layout, tests, and agent instruction files. Preserve the current framework unless the user requests a migration.
6. Before changing either kind of project, read and apply [project-conventions.md](references/project-conventions.md).

Ask one focused question at a time. Reuse supplied information.

## Execution contract

### New project

After framework approval, follow the bootstrap checklist. Include TypeScript, Git, environment files, Tailwind theme foundations, state and query libraries, Zod, required directories, root-level tests, and the generated initial favicon.

Write the conventions into the instruction file recognized by the active agent environment. Merge with existing instructions instead of overwriting them.

### Existing project

Establish a baseline before edits. Apply conventions incrementally, preserve framework behavior, reuse compatible libraries, and avoid unrelated rewrites. Report naming conflicts before using the framework-compatible form.

## Quick reference

| Situation                 | Required action                                                    |
| ------------------------- | ------------------------------------------------------------------ |
| Missing project name      | Ask for it first                                                   |
| New project               | Ask purpose and SEO, present choices, wait for framework selection |
| Existing project          | Inspect and retain its framework by default                        |
| Before file changes       | Read both referenced documents as applicable                       |
| Existing instruction file | Merge; never replace unrelated rules                               |
| Completion                | Run lint, typecheck, tests, and production build when available    |

## Common mistakes

- Inferring a framework without presenting the choices to the user.
- Treating a small demo as permission to use raw HTML instead of offering React or Vue.
- Omitting setup items because the first page does not use them yet.
- Installing a second component, icon, state, or query solution without checking existing dependencies.
- Moving tests into `src/` or colocating them with business code.
- Forcing `index` onto a router that requires a reserved entry filename.

## Completion check

Confirm the chosen framework, secret-free `.env.example`, applied favicon, merged agent instructions, root `test/`, and verification results. Report unavailable commands or unresolved conflicts.
