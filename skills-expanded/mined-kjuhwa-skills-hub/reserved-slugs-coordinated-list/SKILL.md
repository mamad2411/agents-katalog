---
name: reserved-slugs-coordinated-list
description: Maintain a single reserved-slug list in both frontend and backend with per-entry category rationale so url-based multi-tenancy never collides with top-level routes.
category: architecture
version: 1.0.0
tags: [multi-tenancy, routing, reserved-slugs, url-design, validation]
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

- Multi-tenant URL shape `/:workspace-slug/...` (Linear, Notion, GitHub Orgs).
- You want users to pick their own slug but need to prevent collisions with auth, platform, and dashboard routes.

## Steps

1. Categorize reserved slugs by reason, not alphabetically. A future editor adding `/teams` should be able to see "this is a dashboard segment, add under that heading":
   ```ts
   export const RESERVED_SLUGS = new Set([
     // Auth flow
     "login", "logout", "signin", "signout", "signup",
     "auth", "oauth", "callback", "invite", "verify", "reset", "password",

     // Platform / marketing (current + future)
     "api", "admin", "help", "about", "pricing", "changelog", "docs",
     "support", "status", "legal", "privacy", "terms", "security",
     "contact", "blog", "careers", "press", "download",

     // Dashboard / workspace-scoped segments
     "issues", "projects", "agents", "inbox", "my-issues",
     "runtimes", "skills", "settings",
     "workspaces",   // for `/workspaces/new`
     "teams",        // future team routes

     // RFC 2142 privileged email mailboxes (spoofing risk)
     "postmaster", "abuse", "noreply", "webmaster", "hostmaster",

     // Hostname / subdomain confusables (phishing risk)
     "mail", "ftp", "static", "cdn", "assets", "public", "files", "uploads",

     // Framework-mandated
     "_next", "favicon.ico", "robots.txt", "sitemap.xml", "manifest.json", ".well-known",
   ]);
   export const isReservedSlug = (s: string) => RESERVED_SLUGS.has(s);
   ```
2. Mirror the list in the backend language and keep them in sync via a comment reference:
   ```go
   // Keep in sync with packages/core/paths/reserved-slugs.ts.
   var reservedSlugs = map[string]struct{}{ "login": {}, /* ... */ }
   ```
3. Enforce server-side on workspace create/rename. Client-side is UX only — don't trust it.
4. Follow the "single word OR /noun/verb" rule for any new global route. Never use `/new-workspace`-style hyphenated groups — they collide with common user workspace names and force you to reserve the full string. Reserving the noun (`workspaces`) auto-protects the whole `/workspaces/*` subtree.
5. Add an audit migration after adding new reserved words, renaming any existing workspace that collides (use a suffix like `-1`):
   ```sql
   -- 047_audit_extended_reserved_slugs.up.sql
   UPDATE workspaces SET slug = slug || '-1' WHERE slug IN ('teams', 'runtimes');
   ```

## Example

File layout:
```
packages/core/paths/reserved-slugs.ts       — frontend source of truth
server/internal/handler/workspace_reserved_slugs.go — backend mirror
server/migrations/043_audit_reserved_slugs.up.sql   — audit-and-rename existing collisions
```

## Caveats

- Reserved-slug audits need to be followed by a matching migration. Deploying the frontend alone and letting the server reject creation is brittle; rename existing collisions first.
- Keep the category comments in the code — future editors skim for category, not for alphabet.
- Expect to revisit this list every 6-12 months as new routes ship; treat the categorized structure as documentation, not as one-time work.
