---
name: disabling-services
description: Hides or disables a service from the documentation listing while preserving the page for SEO and bookmarks. Use when deprecating services, marking services unavailable, setting disabled:true in frontmatter, or adding warning callouts to service pages. Keeps docs/services/ pages accessible via direct URL.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Disable Service Documentation

This skill guides you through hiding a service from the documentation listing while preserving the documentation page for SEO and users who find it via search.

## When to Use This Skill

- Service is deprecated in Coolify
- Service is temporarily unavailable
- Service is removed from Coolify's service catalog
- Service has been replaced by another service

## Why Keep the Documentation File?

**DO NOT delete the documentation file.** Keep it because:

1. **SEO preservation** — users may find the page via search engines
2. **Bookmark support** — users may have bookmarked the page
3. **Historical reference** — users may need to understand what the service was
4. **Future reinstatement** — service may become available again

## How "Disabled" Is Detected

`scripts/services-data.mjs` marks a service as disabled (and `generate-services-page.mjs` excludes it from `all.md`) if **either**:

- The frontmatter contains `disabled: true`, **or**
- The markdown body matches one of these patterns (case-insensitive):
  - `SERVICE HIDDEN`
  - `SERVICE NOT AVAILABLE`
  - `SERVICE REMOVED FROM COOLIFY`
  - `SERVICE TEMPORARILY DISABLED`

This means a warning callout with one of those phrases (e.g. `::: warning SERVICE NOT AVAILABLE`) will hide the service automatically — no separate `disabled: true` is needed. Conversely, you can hide a service silently (no warning) by setting `disabled: true` alone.

`List.vue` reads the generated `services.json`, sees `disabled: true`, and filters the entry out of the visible listing while leaving the page reachable by direct URL.

## Step-by-Step Process

### 1. Edit the Service's Frontmatter

Open `docs/services/{slug}.md` and add `disabled: true`:

```yaml
---
title: "Service Name"
description: "..."
category: "Category"
icon: "/docs/images/services/service-logo.svg"
disabled: true
---
```

This is the canonical, explicit signal. Use it whenever you intend the service to be hidden, even if you also add a warning callout — explicit beats implicit.

### 2. Add a Warning Callout to the Page Body

Insert a warning at the **top** of the body (after frontmatter, before the H1):

```markdown
---
title: "Service Name"
description: "..."
category: "Category"
disabled: true
---

::: warning SERVICE NOT AVAILABLE
This service is currently not available in Coolify's service catalog.
:::

# Service Name

...
```

The callout title (e.g. `SERVICE NOT AVAILABLE`) must include one of the phrases the regex looks for if you also want the body-pattern detector to catch it. Stick to one of:

- `SERVICE HIDDEN`
- `SERVICE NOT AVAILABLE`
- `SERVICE REMOVED FROM COOLIFY`
- `SERVICE TEMPORARILY DISABLED`

### 3. Add Context (Recommended)

If you know why, give users a path forward:

```markdown
::: warning SERVICE DEPRECATED
This service has been deprecated and replaced by [New Service](/services/new-service).
Please use the new service for all new deployments.
:::
```

Or for temporary unavailability:

```markdown
::: warning SERVICE TEMPORARILY DISABLED
This service is temporarily unavailable due to upstream changes.
Check the [Coolify changelog](https://coolify.io/changelog) for updates.
:::
```

### 4. Keep Redirects (If Any)

If the service had redirects in `nginx/redirects.conf`, **keep them**. They ensure users following old URLs still land on the page.

### 5. Regenerate the Listings

```bash
bun run generate:services
```

This updates `docs/.vitepress/theme/data/services.json` (the service entry now carries `disabled: true`) and `docs/services/all.md` (the entry is removed from its category section). Commit both regenerated files.

## Warning Message Templates

### Generic unavailable

```markdown
::: warning SERVICE NOT AVAILABLE
This service is currently not available in Coolify's service catalog.
:::
```

### Deprecated with replacement

```markdown
::: warning SERVICE DEPRECATED
This service has been deprecated and replaced by [Alternative Service](/services/alternative).
Please migrate to the new service.
:::
```

> Note: The phrase `SERVICE DEPRECATED` is **not** in the auto-detect regex. If you use this title and don't set `disabled: true`, the service won't be hidden. Either set `disabled: true` (recommended) or use one of the recognized phrases.

### Temporarily removed

```markdown
::: warning SERVICE TEMPORARILY DISABLED
This service is temporarily unavailable. Check the [Coolify Discord](https://discord.gg/coolify) for updates.
:::
```

### Removed due to issues

```markdown
::: danger SERVICE REMOVED FROM COOLIFY
This service has been removed from Coolify due to [reason].
If you were using this service, please [migration instructions or alternative].
:::
```

## Verification Checklist

After disabling, verify:

- [ ] `disabled: true` added to frontmatter
- [ ] Warning callout added at the top of the body
- [ ] Documentation file still exists (NOT deleted)
- [ ] Ran `bun run generate:services`
- [ ] `docs/.vitepress/theme/data/services.json` shows `"disabled": true` for this service
- [ ] `docs/services/all.md` no longer lists the service
- [ ] Service no longer appears in the listing at `http://localhost:5173/docs/services/`
- [ ] Direct URL still works: `http://localhost:5173/docs/services/{slug}`
- [ ] Warning is visible at the top of the page
- [ ] Both regenerated files are committed alongside the frontmatter change

## Re-enabling a Service

To make a service available again:

1. Remove `disabled: true` from frontmatter
2. Remove the warning callout from the markdown body (or change its title to something the auto-detect regex won't match)
3. Run `bun run generate:services`
4. Commit the page change plus the regenerated `services.json` and `all.md`

## Example: Full Disabled Service

```markdown
---
title: "Legacy Service"
description: "A service that is no longer available."
category: "Utilities"
icon: "/docs/images/services/legacy-service-logo.svg"
disabled: true
---

::: warning SERVICE NOT AVAILABLE
This service has been deprecated as of January 2025 and is no longer available in Coolify.
Consider using [Alternative Service](/services/alternative) instead.
:::

# Legacy Service

![Legacy Service](/docs/images/services/legacy-service-logo.svg)

## What was Legacy Service?

Legacy Service was a tool for... [rest of documentation]
```

## What Changed

This skill used to instruct you to:

- Add `disabled: true` to the entry in `List.vue`
- Manually remove the entry from `docs/services/all.md`

Both `List.vue`'s services array and `all.md` are now generated from frontmatter. **Do not edit either file by hand.** The single source of truth is the service's markdown file.

## Related Skills

- `adding-service-documentation` — for creating new service docs
- `renaming-services` — for renaming services