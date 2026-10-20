---
name: workspace-slug-url-refactor
description: Migrate a multi-tenant SPA from header-based workspace identity to URL-based (/{slug}/...) to fix shareable links, mobile switching, multi-tab leakage, and mutation side-effect races.
category: architecture
version: 1.0.0
tags: [multi-tenancy, url, refactor, routing, workspace]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Your app's workspace identity is carried by `X-Workspace-ID` header + Zustand store + localStorage.
- You see: shareable URLs opening wrong workspace, mobile has no switcher, multi-tab tabs clobber each other, mutation `onSuccess` races.
- Product is pre-launch or you're willing to break existing bookmarks.

## Steps

1. Audit what the data layer already supports:
   - DB has `workspace.slug TEXT UNIQUE NOT NULL`? Good.
   - Backend has `GetWorkspaceBySlug`? Good.
   - TS `Workspace` type has `slug`? Good.
   - If any of these are missing, land them first (separate PRs).
2. Reorganize routes to carry the slug:
   - Next.js web: `apps/web/app/(dashboard)/*` → `apps/web/app/(dashboard)/[workspaceSlug]/*` (or `/(dashboard)/ws/[slug]/` if you want a prefix).
   - Desktop react-router: add `/:workspaceSlug` prefix to every session route.
3. Write a `NavigationAdapter` in each app's `platform/` layer that auto-prepends the current slug to `push(path)`, so shared views call `useNavigation().push('/issues')` and the adapter resolves to `/my-team/issues`.
4. Replace all hardcoded path strings with a `paths.*` builder:
   ```ts
   export const paths = {
     issues:  () => `/issues`,
     issue:   (id: string) => `/issues/${id}`,
     settings: () => `/settings`,
     // ...
   };
   ```
5. Delete the imperative `switchWorkspace` / `hydrateWorkspace` actions. Switching becomes pure navigation:
   ```tsx
   // Before
   <button onClick={() => { push('/issues'); switchWorkspace(ws); }}>

   // After
   <Link href={paths.issues({ slug: ws.slug })}>
   ```
   This single change eliminates a family of mutation-`onSuccess` race bugs (create-workspace flash, delete-workspace-no-nav, accept-invite-no-switch).
6. Delete the global `multica_workspace_id` localStorage key. Per-workspace-scoped persist stores switch to a workspace-aware storage adapter (`${key}:${slug}`).
7. Add a server-side slug-first resolver with UUID fallback so CLI/daemon don't break:
   ```
   1. X-Workspace-Slug header   → GetWorkspaceBySlug → UUID
   2. ?workspace_slug query     → same
   3. X-Workspace-ID header     (legacy / CLI compat)
   4. ?workspace_id query       (legacy / CLI compat)
   ```
8. Ship all of these in one PR — intermediate states don't run because the URL shape is an atomic change.
9. Update E2E tests to assert on URLs with slugs. Internal markdown links (`[foo](/issues/abc)`) must auto-prepend the current slug when dispatched.

## Example

Before: `/issues/abc123` (wrong workspace when shared).
After: `/my-team/issues/abc123` (unambiguous, shareable, bookmarkable, multi-tab safe).

## Caveats

- Existing bookmarks break. Acceptable if pre-launch; otherwise add `/issues/:id` → lookup-by-id-and-redirect path for a grace period.
- Reserved-slug list must be complete and enforced server-side before launch; see the `reserved-slugs-coordinated-list` skill.
- Email invite links (`/invite/:id`) and auth callback URLs remain workspace-agnostic — they're pre-workspace flows.
