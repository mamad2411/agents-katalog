---
name: keystatic
description: Keystatic CMS standards — typed config, collections vs singletons, storage modes, reading content, admin route safety. Load when working with Keystatic.
user-invocable: false
stack: cms/keystatic
paths:
  - "**/keystatic.config.*"
  - "**/keystatic/**"
---

Full standards in [keystatic.md](keystatic.md). Always-on summary:

- **One config.** Define all content in `keystatic.config.ts`. Use a `collection` for lists (posts, terms) and a `singleton` for one-off content (site settings).
- **Type fields strictly.** Use `fields.slug` for the entry name, `fields.select` for fixed values, `fields.relationship` for links between entries. Mark required fields with `validation`.
- **Match your site's schema.** If Astro or Next.js also validates the content, keep both schemas the same shape.
- **Storage.** `local` for solo editing, `github` for a team, `cloud` for Keystatic Cloud. Pick it from an env var, not by editing code per environment.
- **Secrets** (`KEYSTATIC_GITHUB_CLIENT_SECRET`, `KEYSTATIC_SECRET`) are server-only.
- **Never** leave the `/keystatic` admin open in production without GitHub or Cloud auth.
