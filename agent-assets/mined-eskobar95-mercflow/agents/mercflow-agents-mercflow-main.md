# MercFlow Agent Guide

> **Source of truth** for tasks, sprints, roadmap, and feature discovery: Notion (MercFlow workspace).  
> **Orchestration** (webhooks, scripted agents): `mercflow-os` — parallel repository next to this monorepo; see that repo’s README.

## Communication

- Respond to the User in Danish unless the User explicitly requests another language.
- Use English for all code, comments, identifiers, commit messages, and technical documentation.
- Keep status updates concise and actionable.
- When project management context matters, validate the work against the linked Notion task, sprint, and PRD (and this file) before proceeding.

## Project boundaries

- MercFlow is an opinionated Medusa v2 distribution built from MercFlow-owned packages and app-level integration points.
- Do not modify Medusa core packages, `node_modules`, or third-party source files directly.
- Do not touch Guapo production configuration, credentials, environment variables, or other Guapo-specific production assets.
- Current product scope may include admin-controlled SEO infrastructure, Google Shopping XML feed output, inventory and purchase order workflows, order-operation extensions, and backend-served public output such as `sitemap.xml`, `robots.txt`, and feed XML — as reflected in the active Notion roadmap and PRDs.
- Guapo is the first internal validation case, but MercFlow must remain generic. Do not hardcode Guapo-specific assumptions, copy, production assets, credentials, store URLs, or operational configuration into MercFlow packages.
- Do not add Nordic payment modules, shipping label integrations, page builder/blog work, dark mode, automated low-stock ordering, EDI/supplier integrations, Amazon/Pricerunner feeds, or public release work unless the User explicitly changes scope.
- Keep backend custom logic in MercFlow modules and backend registration points. The backend app registers modules; it should not become a dumping ground for custom business logic.

## TypeScript and code style

- TypeScript is strict. Do not use `any`; use `unknown` with narrowing or define proper types.
- Prefer `type` for data shapes. Use `interface` only when extension through `extends` is intended.
- Give functions explicit return types unless the type is trivially inferred from a one-line primitive return.
- Avoid top-level barrel re-exports unless they are required for a package public API.
- Order imports as Node built-ins, third-party packages, internal workspace packages, then relative imports, with a blank line between groups.
- Prefer configured path aliases over deep relative imports.
- Use PascalCase for component files and React components, camelCase for hooks/utilities, SCREAMING_SNAKE_CASE for constants, and snake_case for database columns and API route parameters.
- Do not leave `console.log` or debugging artifacts in completed work.

## UI and design tokens

- The admin UI should be light, clean, spacious, and easy to scan.
- All visual values must come from `packages/design-tokens`. Do not hardcode hex colors, arbitrary Tailwind values, spacing, font sizes, radii, or shadows.
- If a needed visual value is missing, add or request a token instead of working around the token system.
- Build admin UI in this hierarchy: Radix primitives, MercFlow base components in `components/ui`, feature components, then pages.
- Page-level components compose feature components and delegate business logic to hooks.
- Always handle loading and error states explicitly. Do not silently render nothing on errors.
- Interactive UI must be keyboard accessible, use semantic HTML, associate labels with form inputs, and avoid using color as the only way to convey information.

## Navigation and list views

- Use dedicated pages with URL routing for primary entity navigation, forms with more than four fields, deep-linkable flows, and primary workflow actions.
- Use modals only for destructive confirmations, short focused forms, and contextual actions that do not need their own URL.
- Page-level navigation should use the shared page transition pattern. Do not invent custom transitions per page.
- List views should include a header, filters, typed table columns, sortable columns where applicable, row actions in a dropdown, pagination, useful empty states, and skeleton loading for full-page loads.

## Rich text

- Use TipTap v2 for content rich text editing.
- Store rich text as TipTap JSON. Do not store HTML directly.
- Use the standard extension set unless the User explicitly approves an addition: `StarterKit`, `Link` with `openOnClick: false`, `Image` through media upload, and `CharacterCount`.

## Localization and Medusa

- **Core vs MercFlow:** Use **Medusa’s** product and category UIs, translation flows, and Admin APIs for **titles, handles, slugs, and Medusa’s own description/translation fields**. Use the **MercFlow content module and admin content routes** for **rich text (`description_rich`), SEO fields, media gallery, and category banner** per the content module README and field definitions. Do not duplicate the same meaningful field in two places.
- **Locale list:** The set of available editing languages is driven by the **store and Medusa admin** (e.g. `GET /admin/locales` or JS SDK equivalent). **Do not** hardcode a production language list in MercFlow.
- **Locale codes:** The `?locale=` query on MercFlow content APIs must use the **same codes** Medusa uses (typically BCP-47 as returned by the Admin API). Align the content UI with that source.
- **Switching language in admin (UX):** **Autosave (or a clear save) before** changing the active editing language for content; if save **fails**, show an error and **do not** complete a silent switch. Loading and error states must be explicit.
- **Upgrades:** Keep MercFlow schema in the **content module**; do not patch `node_modules` or alter Medusa core entity definitions. Follow Medusa’s upgrade notes for breaking API changes; manage MercFlow migrations separately.
- **Documentation is required** when you touch this area: point operators and the next developer to where core translations are edited vs the Content tab, and how locale is resolved.

## Content module and Medusa data layer

- Content-related data models, services, migrations, and API extensions belong in the MercFlow content module.
- SEO infrastructure belongs in a MercFlow SEO module, feed generation belongs in a MercFlow feed module, and inventory/purchase-order/order-extension data belongs in a MercFlow inventory module. Keep module ownership clear and avoid duplicating the same meaningful field across modules.
- Use Medusa DML through `model.define` for data models. Do not write raw MikroORM entity classes.
- Do not define `created_at`, `updated_at`, or `deleted_at` manually; Medusa DML manages them.
- Extend `MedusaService` for module services. Do not build service classes from scratch.
- Put business validation and transformations in the service layer. Route handlers should validate input and delegate business behavior.
- Use Medusa's `MedusaError` for service-layer errors. Do not throw raw `Error` objects from services.
- Use Zod for admin API request validation before accessing request body fields.
- Locale-aware content should read and write only the active locale, defaulting to `en` when no locale is provided.
- Backend public-output routes such as sitemap, robots, redirect, metadata, and feed endpoints must return correct status codes, content types, and cache behavior for their consumers. Test XML/text output as output, not just as strings.
- Purchase order receipt records MercFlow ordered/incoming/received history and must not silently mutate Medusa stock unless a Task explicitly introduces that behavior. UI and service responses must make this boundary clear.

## Database and migrations

- PostgreSQL is the local database target for development, preferably running through Docker.
- In local development, migrations may be generated, run, reverted, and iterated as needed for the current task.
- Never generate or run migrations against production or staging without explicit written instruction from the User in the current task.
- Generate schema migrations from DML with Medusa tooling. Do not hand-write migration SQL from scratch.
- Add a migration decision log comment to every migration file, including reason, changes, reversibility, and generation method.
- Once committed, migration files are immutable. Create a new migration for later schema changes.
- Use DML defaults for database types: `model.id()` for primary keys, `model.text()` for strings and foreign key IDs, `model.json()` for structured data, and `model.array()` for arrays of IDs.
- Do not use `varchar(n)` for application data unless a third-party integration requires a database-level length. Enforce length constraints in services and API validation.
- Use soft delete behavior through the service layer. Do not hard-delete application records except in migration rollback cleanup or explicitly confirmed purge operations.

## Documentation

- A README belongs in the directory it describes.
- When creating a new package or app directory, create its `README.md` before writing code in that package or app.
- Package and app READMEs must explain responsibility, how to run/test in isolation, key conventions, and what does not belong there.
- The content module README must also include field definitions, API route reference, and migration workflow.
- Update the relevant package README in the same change when adding significant package functionality.
- Do not create extra package-level markdown files unless explicitly needed, such as a changelog.

## Verification

- Run the most relevant available validation for changed code: typecheck, tests, lint, build, migration commands, or local browser smoke checks depending on the touched area.
- After substantive edits, check diagnostics for recently edited files and fix introduced issues when the fix is clear.
- Validate database and backend work against local PostgreSQL, not production or staging.
- For admin UI work, verify accessibility basics, loading states, error states, and token-backed styling.
- For content module work, verify model definitions, migration behavior, service validation, API validation, and README accuracy.
- For SEO and feed work, verify public route output, content types, slug behavior, redirect behavior, XML validity, validation reports, and caching/regeneration behavior where implemented.
- For inventory, purchase order, and order-extension work, verify status transitions, receipt calculations, incoming quantities, internal-note behavior, and the boundary between MercFlow records and Medusa stock/order data.

## Stop and ask

- Stop and ask the User before changing public API contracts, route paths, response shapes, field names, or content model fields.
- Stop and ask if a task requires a production or staging migration.
- Stop and ask if it is unclear whether a new UI element belongs in `admin-ui` or `design-tokens`.
- Stop and ask if two existing codebase patterns conflict and no canonical pattern is clear.
- Stop and ask if the task is underspecified and reasonable interpretations would lead to meaningfully different implementations.
- Stop and ask before adding automatic Medusa stock mutation, external platform connections, wildcard/regex redirects, new feed formats, or new content-module fields not explicitly required by the current task.

## Version control and commits

### Branch strategy

```
main          ← production. Only receives merges from staging via Tech Lead gate (/promote-to-main).
staging       ← general rehearsal. Only receives merges from development via Tech Lead gate (/promote-to-staging).
development   ← active integration. All feature branches merge here after code review.
feature/...   ← per-task worktree branch, always branched from development.
```

- **Never** commit directly to `main`, `staging`, or `development`.
- **Never** branch feature work from `staging` or `main`.
- Feature PRs always target `development`.
- Tech Lead owns the `development → staging → main` promotion gates.

### Commit conventions

- Follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): short description` (English).
- Use types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, and `migration` for database migration commits only.
- One commit per logical, working change (one per layer within a vertical slice).
- Feature branch names: `feature/{package}/{task-slug}` (kebab-case).
- **Worktrees:** `../mercflow-worktrees/{task-id}/` (sibling directory; not committed). See `.cursor/skills/agent-workflow/SKILL.md`.
- **Merge policy:** squash merge feature → development when review and CI pass. Never let approved work diverge unmerged when dependents need it.

## Agent workflow (Cursor)

Every implementation task follows the six-stage pipeline in [`.cursor/skills/agent-workflow/SKILL.md`](.cursor/skills/agent-workflow/SKILL.md). Task breakdown uses vertical slices per [`.cursor/rules/vertical-slicing.mdc`](.cursor/rules/vertical-slicing.mdc).

**Commands:** `/start-task`, `/review-code`, `/open-pr`, `/promote-to-staging`, `/promote-to-main`, `/devops-check`, `/po-grill`, `/tech-lead-plan`, `/prd-review`

## Autonomous pipeline — full status flow

```
Not Started → In Progress → In Review → Ready to Merge → Done
                  ↓                            ↑
               Blocked ─── auto-retry ─────────┘ (1st block only)
```

| Status | Triggered by | Next action |
|---|---|---|
| Not Started | Tech Lead (task creation) | Assign agent + set → In Progress |
| In Progress | Notion webhook → implementation agent | Implementation + push branch |
| In Review | Code Reviewer Agent | Bugbot + CI run automatically |
| Ready to Merge | GitHub Actions (all checks pass) | Merge agent reviews summary + squash merges |
| Done | GitHub Actions (pr-merged.yml) | Unblocks dependencies, closes GitHub Issue |
| Blocked | Code Reviewer Agent | Auto-retry (1st time), human escalation (2nd time) |

## Known automation limitations

| Limitation | Workaround |
|---|---|
| **Agent field does not trigger automation.** Assigning an agent to a Notion task does not fire a webhook. Only Status changes trigger automations. | After assigning an Agent, also set `Status → In Progress` to start the pipeline. |
| **"Ready to Merge" must be added manually.** Add it as a Status option in Notion Tasks UI (in_progress group, purple color). | Open Tasks database → Status property → Edit options → Add "Ready to Merge". |
| **Sprint end auto-trigger requires date update.** The `/sprints/ended` webhook fires when `Dates` is edited, not when all tasks are Done. | When promoting a sprint early, Tech Lead must update `Dates.end` to today in Notion. |
| **Blocked auto-restarts once.** Blocked (previousStatus=In Progress) → new agent runs. Blocked (previousStatus=Blocked) → human escalation only. | Split the task or clarify acceptance criteria, then set → In Progress manually. |
| **Notion automations send static headers.** Webhook signatures from Notion are static Bearer tokens, not HMAC. | The Cloudflare Worker accepts both Bearer (Notion) and HMAC (scripts) auth modes. |

## Cursor subagents (when to delegate)

Use Task subagents only when the work fits the categories below. Routine coordination runs without a subagent.

| Situation | Subagent | When to use |
| --- | --- | --- |
| Large or ambiguous investigation across many files | `explore` (read-only) | Before changing planning documents or implementation when tracing patterns across the tree. |
| Merge conflicts or deep cross-file defects | `generalPurpose` or `shell` | When inline investigation is not enough. |
| Heavy integration verification | `tester` or `explore` | When full validation cannot run in-session. |
| MercFlow module migrations | `migrator` | When a task involves generating or running MercFlow migrations per project rules. |

**Do not** spawn subagents for: drafting routine prompts, trivial log review, or merges that complete without conflicts.
