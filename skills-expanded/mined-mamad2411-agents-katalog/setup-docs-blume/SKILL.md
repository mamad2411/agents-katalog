---
name: setup-docs-blume
description: >
  Scaffold or fully rewrite apps/docs as a Blume product documentation site
  (Ultracite-style template → product marketing home + MDX docs). Wires monorepo
  package.json scripts, pnpm-workspace apps/*, blume.config, homepage examples,
  integrations (Biome/ESLint/Oxlint/Prettier), README updates, install + build.
  AUTO-RUN the global workflow setup-docs-blume when the user asks to set up
  Blume docs, create apps/docs, convert an Ultracite docs template, rewrite the
  docs site for this product, or runs /setup-docs-blume.
---

# setup-docs-blume

## Auto-run

When the user message matches any of:

- set up / create / scaffold **Blume** docs
- create **`apps/docs`**
- convert **Ultracite** docs template to this product
- rewrite the **docs site** / marketing docs app
- `/setup-docs-blume`

…immediately launch the global workflow (do not only describe steps):

```text
name: setup-docs-blume
args: {
  "product_name": "<if known>",
  "package_name": "<if known>",
  "tagline": "<if known>",
  "description": "<if known>",
  "github_owner": "<if known>",
  "github_repo": "<if known>",
  "template_path": "<path to existing Blume/Ultracite apps/docs if user points at one>",
  "force": true
}
agent_budget: 48
```

Omit unknown optional fields rather than inventing wrong GitHub owners.

Then tell the user the run is in `/workflows`. On completion, report:

- `apps/docs` path
- `docs:dev` / `docs:build` commands
- install_ok / build_ok
- scratch report path if any

## What the workflow does

| Phase | Work |
|-------|------|
| Scope | Infer product name, monorepo, package manager, template path |
| Scaffold | Create/copy `apps/docs`, workspace + root scripts |
| Config | `blume.config.ts`, `lib/examples.ts`, integrations, version helper |
| Home | Marketing UI: hero, demo terminal, examples, pipeline, integrations, IDE, footer |
| Docs | Full MDX: install, CLI, features, integrations, safety, FAQ, … |
| Root | README + AGENTS.md links; vercel redirects |
| Verify | `pnpm install` + `docs:build`; repair Blume errors up to 3 times |
| Report | Commands + summary |

## Args

| Arg | Default | Meaning |
|-----|---------|---------|
| `product_name` | infer | Display name |
| `package_name` | infer | npm package |
| `tagline` / `description` | from README | Marketing copy |
| `github_owner` / `github_repo` | git remote | Changelog + edit links |
| `template_path` | detect / empty | Existing Ultracite/Blume docs to copy assets from |
| `force` | true | Overwrite template product copy |
| `dry_run` | false | Plan only |
| `docs_only` | false | Skip homepage rewrite |
| `skip_install` / `skip_build` | false | Skip verify steps |
| `accent` | cyan | Blume theme accent |
| `include_changelog` | true | GitHub releases source |

## Manual invoke

```text
/setup-docs-blume
```

or

```text
/workflow setup-docs-blume product_name=MyProduct
```

## Non-goals

- Does not publish to npm or deploy Vercel
- Does not replace markdown `docs/` in repo unless agents choose to cross-link
- Does not invent false product claims — writers must read README/source
