---
name: scaledock-repo-standard
description: Create a new repo or bring an existing one up to the ScaleDock standard (latest Node supported by Vercel, latest pnpm and TypeScript, Next.js or Expo, Supabase with better-supabase, PermDock, oRPC, MCP, CLI, Fumadocs, Vercel). Use when scaffolding a new monorepo, product, library or tooling repo, adding an iOS and Android app with Expo, auditing a repo against the ScaleDock standard into a gap table, upgrading this repo to the standard, or aligning several repos.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.14.0"
---

# Repo standard

A workflow for creating, upgrading or aligning repos so every ScaleDock repo has the same toolchain, layout, surfaces, guardrails and delivery pipeline.

**Follow the workflow below step by step.** Load a reference when its step names it, and only for the repo kind and surfaces the inputs select.

## Inputs (fill in, or ask the user before starting)

- Mode: `new`, `upgrade` (this repo) or `align` (several repos).
- Repo kind: `product` (default; apps and surfaces), `library` (publishes npm packages) or `tooling` (toolchain, hooks, CI and repo files only). [`references/audit.md`](references/audit.md) lists which references apply to each kind.
- Product in one sentence: {{PRODUCT_ONE_LINER}}
- Surfaces: `app`, `api`, `mcp`, `docs`, `marketing`, `mobile`, `cli`. The default for a product is `app`, `api`, `mcp` and `docs`. `mobile` adds a native-only Expo app beside a Next.js `app`.
- Framework for `app`: `next` (default) or `expo` (one universal Expo app for iOS, Android and web). `docs` and `marketing` always use Next.js. Use another framework only when the user names it, with an ADR.
- Offline: yes or no, only with Expo (yes means PowerSync on native).
- CLI kind: `none` (default), `product` (end users call the API), `library` (ships with an npm package) or `tooling` (private repo scripts).
- Database: yes or no (yes means Supabase with better-supabase).
- Roles and permissions: yes or no (yes means PermDock).
- Multi-tenant: yes (default) or no.
- Publishes npm packages: yes or no (always yes for a library).
- npm scope `@{{SCOPE}}`, GitHub owner `{{GITHUB_OWNER}}`, Vercel team `{{VERCEL_TEAM}}`, issue prefix `{{ISSUE_PREFIX}}` (optional).

Resolve the placeholders listed in [`references/audit.md`](references/audit.md) from these inputs before you write any file.

## Ground rules

1. **Upgrade and align modes audit first.**
   - Fill the gap table from [`references/audit.md`](references/audit.md), then apply the changes as small conventional commits on one branch (rule 5).
   - Never discard uncommitted work. For unshipped code, prefer one breaking cutover over shims.
   - A deliberate deviation is an ADR in `docs/decisions/` ([`assets/adr-template.md`](assets/adr-template.md)) plus a line in the AGENTS.md "Deviations" list. Never change a deviation silently, and never add one without asking.
2. **Always the latest, including new majors in pre-release.**
   - This skill names no versions. Look up the latest release of every runtime, package, SDK, action, skill and spec when you run (`pnpm view <pkg> dist-tags`, GitHub releases, vendor docs), never from memory or another repo.
   - **New majors first.** When a newer major is in alpha, beta or rc, adopt it now, absorb its migration guide, and note the API changes in the commit. Otherwise use the latest stable; never a pre-release of a minor or patch.
   - **Exceptions.** Stay on the current major only when the pre-release fails `minimumReleaseAge` or breaks a peer with no compatible release. Record the blocker in the gap table.
   - **Tracking.** List every pre-release pin under "Pre-release pins" in AGENTS.md (package, version, why), and move it to stable when the major ships.
   - Pin exactly in the catalog. Never bypass `minimumReleaseAge`; use the newest release that passes, and add a commented exclude only when a fix needs it.
3. **Read installed docs before configuring.** For Next.js, ask the running dev server's `/_next/mcp` first, then read the bundled `node_modules/next/dist/docs`. Read `node_modules/turbo/docs`, the Expo, Ultracite, oxlint, oxfmt, Fumadocs, AI SDK and MCP SDK docs, and the matching skill. Flag and option names in the references drift; check each against the installed version.
4. **Done means `pnpm verify` passes.** Report with [`assets/report.md`](assets/report.md).
5. **One branch and one PR for this whole run.** Follow the agent workflow in [`references/git-workflow.md`](references/git-workflow.md).

## Workflow

Run these steps in order. Each step names the references to load and the check it must pass. Skip a reference when the repo kind or inputs exclude it.

1. **Start the run.** Settle the mode and every input; ask for anything missing. Resolve the placeholders. Check the working tree, then create or reuse the branch.
   -> [`references/audit.md`](references/audit.md) (placeholders), [`references/git-workflow.md`](references/git-workflow.md) (agent workflow).
   ✓ All inputs are known, the tree is clean or yours, and you are on a `<type>/<short-topic>` branch.
2. **Audit or sketch.**
   - **New:** sketch the tree from the selected surfaces and packages.
   - **Upgrade:** walk the `audit.md` checklist row by row, opening a row's reference only to judge that row.
   - **Align:** audit each repo the same way, one column per repo.
     -> [`references/audit.md`](references/audit.md), [`references/architecture.md`](references/architecture.md) for the target tree, and the Baselines section of [`references/performance.md`](references/performance.md) when the repo ships code.
     ✓ Every row has an `audit.md` status, every dependency behind latest is listed, and the starting baselines are recorded.
3. **Foundation.** Install the skills, set up the toolchain, workspace, TypeScript, Knip, lint and format, and lay out the folders and boundaries.
   -> [`references/skills.md`](references/skills.md), [`references/toolchain.md`](references/toolchain.md), [`references/lint-format.md`](references/lint-format.md), [`references/architecture.md`](references/architecture.md).
   ✓ `pnpm install` passes under the strict workspace settings, every workspace has a boundary tag, and `pnpm check` runs.
4. **Platform.** Configure Vercel, Turborepo, Remote Cache, local dev with Portless, and env and secrets.
   -> [`references/vercel.md`](references/vercel.md), [`references/local-dev-env.md`](references/local-dev-env.md).
   ✓ Each need maps to the Vercel-first table or an ADR, `turbo.json` uses strict env mode, and every web app has a `dev:portless` script.
5. **Surfaces.** Build or upgrade only the selected ones.
   - Web (Next.js `app`, `docs`, `marketing`): the `nextjs-app-architecture` skill (required), [`references/nextjs.md`](references/nextjs.md), [`references/web-design.md`](references/web-design.md), [`references/i18n.md`](references/i18n.md), [`references/ui.md`](references/ui.md), and [`references/app-shell.md`](references/app-shell.md) for `app`.
   - Expo (`mobile`, or `app` on Expo): [`references/expo.md`](references/expo.md), [`references/i18n.md`](references/i18n.md), and [`references/offline-sync.md`](references/offline-sync.md) when Offline is yes.
   - Data and identity: [`references/data-permissions.md`](references/data-permissions.md), [`references/data-conventions.md`](references/data-conventions.md), [`references/auth.md`](references/auth.md).
   - Programmatic: [`references/api.md`](references/api.md), [`references/mcp.md`](references/mcp.md), [`references/cli.md`](references/cli.md).
   - Docs and AI: [`references/docs-site.md`](references/docs-site.md), [`references/ai.md`](references/ai.md).
   - Performance, for every kind that ships code: [`references/performance.md`](references/performance.md).
     ✓ Apps stay thin adapters over `services`, every procedure is contract first, every surface acts as the signed-in user, every Next.js page passes the `nextjs-app-architecture` checklist, and names follow the naming rules.
6. **Repo hygiene.** Write the AI files, repo files, VS Code settings, CI, Dependabot and tests.
   -> [`references/agent-files.md`](references/agent-files.md), [`references/repo-files.md`](references/repo-files.md), [`references/ci.md`](references/ci.md), [`references/tests.md`](references/tests.md).
   ✓ AGENTS.md is at most 12 KB and lists the deviations and pre-release pins, and CI runs the same gates as `pnpm verify`.
7. **Verify and finish.** Run `pnpm install`, `pnpm format` and `pnpm verify`; fix code, not tests. Add a changeset, push, mark the one PR ready, and put the report in its body.
   -> [`assets/report.md`](assets/report.md), [`references/git-workflow.md`](references/git-workflow.md) (Changesets, PR), the Baselines section of [`references/performance.md`](references/performance.md), the checklist below.
   ✓ `pnpm verify` passes, the final baselines are recorded, and the report is complete.

## Verify before done

The tag in brackets names the input that switches an item on; untagged items always apply.

- [ ] `pnpm verify` passes locally (rule 4).
- [ ] [Turbo] `verify` is one cached, parallel `turbo run` of tasks with `inputs`, and no check runs twice.
- [ ] Coverage `autoUpdate` is off in CI, and thresholds come from the test set CI runs.
- [ ] The naming rules hold, and the `docs:drift` naming check passes.
- [ ] The baselines from before and after the run are in the report.
- [ ] Every dependency is `catalog:` or `workspace:*` at the latest release that passes `minimumReleaseAge`; every override, exclude, `allowBuilds` entry and patch has a comment.
- [ ] Every pre-release pin is in AGENTS.md (rule 2).
- [ ] `pnpm-workspace.yaml` has no key the installed pnpm rejects, and TypeScript is the stable native compiler with no preview package.
- [ ] Every deviation has an ADR in `docs/decisions/` and a line in the AGENTS.md "Deviations" list.
- [ ] [workspaces] Every workspace has a Turbo boundary tag, apps never import each other, and `pnpm boundaries` passes.
- [ ] No Zod in our code, no `@radix-ui/*` or vaul, and each concern uses its one library.
- [ ] Dates use `Temporal` through the one `temporal.ts` module; no other date library is installed.
- [ ] Lint and format run on Ultracite: a root `oxlint.config.ts` on the Ultracite presets with type-aware linting and `denyWarnings`, `oxfmt.config.ts` spreading `ultracite/oxfmt`, and `pnpm check` running `ultracite check`.
- [ ] Every disabled lint rule carries a reason and a finding count.
- [ ] GitHub-owned actions use major tags, third-party actions use a commit SHA with a `# vX.Y.Z` comment, same-repo actions use `$/...`, and public repos run zizmor.
- [ ] `verify.yml` runs the static gates in one job with a `parallel` group, services run as `background` steps, only the default branch saves caches, the Remote Cache step is not skipped in CI, and every job sets `timeout-minutes`.
- [ ] The managed AGENTS.md blocks (Next.js, Turborepo) are committed as the tools wrote them.
- [ ] Installed skills and `skills-lock.json` are committed, and the lock tracks every skill in `.agents/skills`; in a repo that publishes skills, `pnpm dlx skills add . --list` offers only its own.
- [ ] [apps] Each app has one `env.ts`, the only file that reads `process.env`; every env key is in t3-env, `turbo.json`, `.env.example` and all three Vercel environments.
- [ ] [docs, web] Agent routes send `Cache-Control`, no `proxy.ts` lacks a `matcher`, and no experimental flag or twoslash is installed without a use.
- [ ] [web] Every Next.js surface passes the `nextjs-app-architecture` checklist and has its own `DESIGN.md`.
- [ ] [web] The `[web]` rows of the Shared web surfaces checklist in `audit.md` are `done` or `kept`: layout, shared chrome, URL state, lazy client code, images behind Services.
- [ ] [docs, marketing] The `[docs]` and `[marketing]` rows are `done` or `kept`: "Get code", icon and integration maps, server SVG, highlighting, generated data, `.md` mirrors.
- [ ] [api] Every procedure lives in `packages/contract` with `openapi()` meta, and the committed OpenAPI snapshot matches.
- [ ] [api, mcp, cli] Errors are RFC 9457 Problem Details on every surface.
- [ ] [Database] Every table has RLS and pgTAP tests; every domain table has the audit trigger.
- [ ] [Database] Timestamps are `timestamptz`, money is integer minor units plus a currency, and public IDs are UUIDs (v7 when the Postgres major provides it).
- [ ] [Database] Every foreign key is indexed and has an explicit `on delete`.
- [ ] [Database] The only keys in use are `sb_publishable_` and `sb_secret_`, and `sb_secret_` appears only in `createAdminContext()`.
- [ ] [Expo] `expo-doctor` passes, `ios/` and `android/` are gitignored, and each `APP_VARIANT` has its own name, bundle ID and scheme.
- [ ] [Offline] Every synced table is in the PowerSync publication and a sync stream, and web never opens a PowerSync database.
- [ ] The whole run is on one branch and one PR, with conventional commits (and a changeset when Changesets apply).
- [ ] The report follows [`assets/report.md`](assets/report.md), including its manual steps.

## Reference index

- **Run:** [`audit.md`](references/audit.md) (placeholders, repo kinds, gap checklist), [`report.md`](assets/report.md) (final report, manual steps), [`adr-template.md`](assets/adr-template.md).
- **Foundation:** [`skills.md`](references/skills.md) (agent skills), [`toolchain.md`](references/toolchain.md) (Node, pnpm, TypeScript, workspace, Knip, root scripts), [`architecture.md`](references/architecture.md) (tree, boundaries, contract, errors, one library per concern, env, naming and layout), [`performance.md`](references/performance.md) (baselines, agent-route caching, client bundle, library runtime, generated code), [`lint-format.md`](references/lint-format.md) (Ultracite on Oxlint and Oxfmt, anti-slop).
- **Platform:** [`vercel.md`](references/vercel.md) (Vercel first, Services, `turbo.json`, Remote Cache), [`local-dev-env.md`](references/local-dev-env.md) (Portless, native toolchain, env and secrets).
- **Web:** [`nextjs.md`](references/nextjs.md) (config, additions to `nextjs-app-architecture`, pitfalls), [`web-design.md`](references/web-design.md) (patterns app, docs and marketing share), [`i18n.md`](references/i18n.md) (next-intl, and i18next for Expo), [`ui.md`](references/ui.md) (shadcn, ReUI Pro), [`app-shell.md`](references/app-shell.md) (auth pages, shell, page templates, screens).
- **Expo:** [`expo.md`](references/expo.md) (shapes, app config, EAS, dev client, native UI, Uniwind, push, universal web), [`offline-sync.md`](references/offline-sync.md) (PowerSync).
- **Data and identity:** [`data-permissions.md`](references/data-permissions.md) (tenancy, Supabase, better-supabase, audit log, PermDock), [`data-conventions.md`](references/data-conventions.md) (UTC timestamps and Temporal, money, IDs, naming, pagination, deletion), [`auth.md`](references/auth.md) (OAuth 2.1 server, sign-in per surface).
- **Programmatic:** [`api.md`](references/api.md) (Hono, oRPC, Scalar), [`mcp.md`](references/mcp.md) (MCP SDK, tools from the contract, docs MCP), [`cli.md`](references/cli.md) (CLI kinds, OAuth login).
- **Docs and AI:** [`docs-site.md`](references/docs-site.md) (Fumadocs for people and agents), [`ai.md`](references/ai.md) (AI SDK 7 through AI Gateway, approvals, `WorkflowAgent`, Run SDK).
- **Delivery:** [`git-workflow.md`](references/git-workflow.md) (branches, agent workflow, the direct-to-develop variant, commitlint, lefthook, Changesets), [`ci.md`](references/ci.md) (Actions, pins, `$/` actions, linters, parallel steps, caching, security, EAS builds, Dependabot), [`tests.md`](references/tests.md), [`agent-files.md`](references/agent-files.md) (AGENTS.md, rules, "also update" table), [`repo-files.md`](references/repo-files.md) (README, standard files, VS Code).
