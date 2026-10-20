# CLAUDE.md

Guidance for working on GitOps, an open source internal developer platform built with SvelteKit.

## Product

GitOps combines identity and access management, organizations and projects, Open Report security
analysis, and Pulumi State visibility. The Vault route is currently a UI foundation and does not
yet provide a complete secrets backend. Google SSO and SAML settings are configuration only; no
external authentication strategy is implemented.

Self-service registration (`/auth/registration`) lets a visitor create a plain `cluster-user`
account with no organization membership. It is gated by a cluster-wide toggle managed at
`/cluster-settings/registration` (persisted via `clusterSettingsService` in `$modules/config`,
off by default) and re-checked server-side on submit so it can't be bypassed while disabled. Once
registered and signed in, the user lands on `/org`, where the `cluster:organization:create`
permission (granted to `cluster-user` by default) surfaces a "New Organization" action that
creates the organization, provisions its default roles, and grants the creator the `org-admin`
role so they can manage what they just created.

Password recovery: `/auth/recover-password` accepts an email and, via `passwordResetService` in
`$modules/auth`, emails a time-limited reset link (`password-reset` template, 1 hour TTL, hashed
token stored on the user) without revealing whether the address is registered. The link lands on
`/auth/reset-password?token=...`, which sets a new password and redirects back to `/auth/login`.


The roadmap is in `IDEAS.md`. Do not describe roadmap items as implemented features.

## Stack and commands

- SvelteKit 2, Svelte 5, Vite 8, TypeScript 6 strict mode
- Tailwind CSS 4 and `@lucide/svelte`
- Internationalization via Paraglide JS (Spanish and English)
- Bun package manager; do not use npm or yarn
- GitDB (`@getgitops/gitdb`) as the only persistence layer
- Vitest, ESLint, and Prettier
- Playwright for RBAC end-to-end tests (`e2e/`)

```bash
bun install
bun run dev
bun run build
bun run check
bun run lint
bun run test
bun run test:e2e
bun run test:e2e:ui
bun run format:check
```

Tests use Vitest through `bun run test`. Do not use the native `bun test` runner: it does not load
the Vite/SvelteKit aliases and plugins used by this project.

Import aliases (`tsconfig.json`): Use `$modules` for business logic modules, `$lib` for shared
components and utilities, and relative paths for route-local imports. Examples:
`import { userService } from '$modules/auth'` (not `../../modules/auth`),
`import Button from '$lib/components/Button.svelte'`.

`bun run test:e2e` runs the Playwright RBAC suite under `e2e/` (requires
`bunx playwright install --with-deps chromium` once). `e2e/global-setup.ts` creates its own
throwaway local GitDB repository, seeds every persona the permission matrix needs, and starts the
dev server against it — it never touches the repository configured in `.env`. Session cookies are
minted directly (same HMAC scheme as `SessionService`), so specs don't need to drive the login
form except in `e2e/specs/login.spec.ts`, which covers that mechanism itself.

## Architecture

Business logic lives in `src/modules/<module>/`:

```text
 domain/                    entities, business rules, and data constants
 application/               use cases and services
 infrastructure/            repositories and adapters
 index.ts                   public API and composition root
```

Domain layers include entity classes (e.g., `*.domain.ts`) and centralized data files (e.g.,
`*.data.ts`) for configuration constants: role permissions, default project settings, risk weights,
and tool policy mappings.

Current modules include `auth`, `config`, `organization`, `projects`, `storage`, and
`code-report`. Shared infrastructure lives in `src/lib/`. Routes should import module APIs from
their `index.ts`, not internal layers.

GitDB is the single source of truth. Users, roles, API keys, organizations, projects, storage
metadata, and code reports are GitDB entities in the repository configured by
`GITDB_REPOSITORY_URL`. Writes become auditable Git commits. Use `getGitDb()` and the schemas in
`src/lib/database/schemas.ts`; do not add another database or persistence backend without an
architecture discussion and migration plan.

`GITDB_REPOSITORY_URL` supports both HTTPS and SSH URLs (e.g., `git@github.com:user/repo.git`).
The Docker image includes `openssh-client` and pre-configures the SSH key fingerprints for GitHub,
Bitbucket, and GitLab; in production, ensure SSH authentication credentials are available via
`SSH_AUTH_SOCK` or a mounted SSH directory.

`ORIGIN` environment variable pins the application's public origin (e.g., `http://localhost:3000`).
SvelteKit's CSRF Origin check depends on this value instead of deriving it from the incoming Host
header, preventing bypasses when running behind a proxy that rewrites Host headers.

## Authorization

Permission grants are always scope-prefixed and match the catalog in `src/lib/config/permissions.ts`
exactly: `<scope>:<resource path>:<action>`, where scope is `cluster`, `organization` or `project`
(`project:vault:secrets:read`, `organization:projects:create`, `cluster:users:invite`). A
`<resource>:all` grant covers every action on that resource. Grants stored before this convention
are upgraded on read by `normalizePermissionGrant` in `$lib/permissions`.

Use the helpers exported by `$modules/auth`:

```typescript
import { cancanService } from '$modules/auth';

const allowed = await cancanService.canSessionUser(locals.user, 'project:stateiac:stacks:read', {
  scope: 'project',
  projectId: project.id,
  organizationId: project.organization?.id,
});

if (!allowed) {
  return json({ error: 'Forbidden' }, { status: 403 });
}
```

**UI permission gating:** In route loaders, use `cancanService.canSessionUser()` to check specific
action permissions and pass them to components as props (`canCreate`, `canUpdate`, `canDelete`) to conditionally
render actions in the UI. This prevents users from seeing actions they cannot perform:

```typescript
const canCreate = await cancanService.canSessionUser(locals.user, 'project:roles:create', {
  scope: 'project',
  projectId: project.id,
  organizationId: project.organization?.id,
});
return { roles, canCreate };
```

The root layout (`+layout.server.ts`) calculates granular read permissions for each settings section and
passes them to the AppSidebar component, which filters sidebar items based on specific resource permissions:
- **Project level:** `project:project:read`, `project:users:read`, `project:roles:read`, `project:server-keys:read`, `project:audit:read`, plus module-specific permissions: `project:vault:secrets:read`, `project:vault:environments:read`, `project:codereport:reports:read`, `project:codereport:dependencies:read`, `project:codereport:vulnerabilities:read`, `project:stateiac:stacks:read`, `project:stateiac:states:read`, `project:stateiac:history:read`. High-level read flags combine granular permissions with OR logic (e.g., `canReadProjectVault = canReadProjectVaultSecrets || canReadProjectVaultEnvironments`)
- **Organization level:** `organization:projects:read`, `organization:users:read`, `organization:roles:read`, `organization:settings:read`, `organization:backups:read`, `organization:server-keys:read`, `organization:audit:read`

This ensures the UI only displays navigation items for sections the user has permission to view.

Default roles and permissions are centralized in `src/modules/auth/domain/role-permissions.data.ts`.
Permissions always include their scope as a prefix (e.g., `organization:projects:read`,
`project:vault:secrets:all`) and are stored verbatim—there is no scope-stripping transformation:
- **Cluster Admin** (`vault:all`, `openreport:all`, `stateiac:all`)
- **Cluster User** (no inherent permissions; used as base role for cluster-level access)
- **Organization Admin** (all org-level permissions: projects, users, roles, settings, backups, server-keys, audit)
- **Organization Developer** (read/create/update projects only)
- **Project Admin** (all project-level permissions: project metadata, users, roles, server-keys, audit; plus all module permissions: vault secrets/environments, codereport reports/dependencies/vulnerabilities, stateiac stacks/states/history)
- **Project Developer** (read/create/update project resources; no deletion or admin; granular module access)
- **Project Viewer** (read-only: project metadata, all modules, vault secrets/environments, codereport reports/dependencies/vulnerabilities, stateiac stacks/states/history)

Module resources have granular sub-permissions: `project:vault:secrets:read`, `project:vault:environments:read`, `project:codereport:reports:read`, `project:codereport:dependencies:read`, `project:codereport:vulnerabilities:read`, `project:stateiac:stacks:read`, `project:stateiac:states:read`, `project:stateiac:history:read`. These allow fine-grained access control within each module.

Organization-level permissions cascade into their projects only when no explicit project-level assignment exists
for that user. A user with `organization:projects:read` can satisfy a `project:project:read` check on any project
in that organization—but if they have a project-specific role assignment, that assignment is authoritative and
organization permissions do not apply (most-specific-wins rule). This allows coarse-grained org roles to delegate
authority downward, while still permitting per-project restrictions.

Two helpers distinguish organization visibility from management: `canManageOrganization()` gates the `/settings` area,
while `canViewOrganization()` also includes users whose only access is to a project under that organization
(they see the org overview, but cannot perform org-scope actions).

When creating an organization (via bootstrap or cluster settings), `roleService.createDefaultOrganizationRoles()` is
automatically invoked. When creating a project, `roleService.createDefaultProjectRoles()` is automatically invoked. Both
operations initialize their respective default roles. Keep authorization tests beside changes to permission behavior.
Machine-to-machine requests authenticate with `Authorization: Bearer gvs_...`; `hooks.server.ts`
resolves them into `locals.apiKey` and `cancanService.canApiKey()` confines a project key to its
own project.

`locals.user.role` is a session role object, not the string `admin`. Use `isAdmin()` or the `can*`
helpers. Keep authorization tests beside changes to permission behavior.

## Security rules

- Keep `.env`, API keys, Git credentials, session secrets, and repository credentials out of Git.
- Use a strong production `GITDB_ENCRYPTION_KEY`; the development example is not suitable for
  production.
- Preserve the existing scrypt password hashing, HMAC session signing, and timing-safe checks.
- Never return raw secrets from an API.
- Review organization, project, role, and access changes for privilege escalation.

## Code and tests

Follow the existing naming patterns: `*.domain.ts`, `*.service.ts`, `*.repository.ts`, and
`*.test.ts`. Prefer dependency injection and in-memory fakes in unit tests. Keep API handlers
permission-first and normalize errors consistently.

Before finishing a change, run the relevant checks. Do not silently fix unrelated bugs or rewrite
generated files. Update `README.md`, `CONTRIBUTING.md`, and this file when architecture or public
commands change.
