---
name: renaming-services
description: Renames a service documentation file and updates all references. Use when renaming services, changing service slugs, fixing camelCase to kebab-case, or when service names change in the Coolify repository templates/compose/. Updates docs/services/, regenerates listings, and adds nginx redirects.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Rename Service Documentation

This skill guides you through renaming a service in the Coolify documentation, ensuring all references are updated correctly.

## When to Use This Skill

- Service name changed in the Coolify repository
- Fixing incorrect service naming (e.g., camelCase to kebab-case)
- Consolidating duplicate service documentation
- Correcting typos in service slugs

## Locations to Update

The slug used to live in three hand-edited places (the file, `List.vue`'s services array, and `all.md`). With the new generation pipeline, **the markdown filename is the slug**, and the listing + all.md are regenerated from it. So renaming now touches:

1. **The documentation file** (`docs/services/<old>.md` → `docs/services/<new>.md`) — the slug
2. **The logo asset** (optional, `docs/public/images/services/`) — only if you want it renamed too
3. **Nginx redirects** (`nginx/redirects.conf`) — to keep old URLs working
4. **Internal links** (anywhere in `docs/` referencing the old slug)

`docs/.vitepress/theme/components/Services/List.vue`, `docs/.vitepress/theme/data/services.json`, and `docs/services/all.md` are **regenerated** — do not hand-edit them.

## Step-by-Step Process

### 1. Rename the Documentation File

```bash
git mv docs/services/old-name.md docs/services/new-name.md
```

**Naming rules:**

- Lowercase only
- Use hyphens for spaces (kebab-case)
- Match the service name from `service-templates-latest.json`
- Do not use camelCase even if the upstream JSON does (e.g., `denoKV` → `denokv.md`)

### 2. Rename the Logo (If Needed)

The icon resolver matches the file's basename against `<slug>-logo`, `<slug>_logo`, `<slug>logo`, and bare `<slug>`. After renaming the markdown:

- If the logo was named after the **old** slug, rename it to match the new slug, **or** add an explicit `icon:` field in frontmatter pointing to the existing file.

```bash
git mv docs/public/images/services/old-name-logo.svg docs/public/images/services/new-name-logo.svg
```

### 3. Update Frontmatter (If Needed)

The slug isn't in frontmatter — it's the filename. But check:

- `icon:` — if you set it explicitly to a path that included the old slug, update it
- `title:` — usually unchanged unless the rename also reflects a display-name change

Example:

```yaml
---
title: "New Service Name"          # update if the display name changed
description: "..."
category: "..."
icon: "/docs/images/services/new-name-logo.svg"   # update if you set it explicitly
---
```

### 4. Add an Nginx Redirect

Edit `nginx/redirects.conf`:

```nginx
# Redirect old service URL to new URL
location = /docs/services/old-name { return 301 /docs/services/new-name; }

# Also redirect legacy knowledge-base path if it existed
location = /knowledge-base/services/old-name { return 301 /docs/services/new-name; }
```

Keep redirects even for renamed/removed pages — they prevent 404s from search engines and bookmarks.

### 5. Update Internal Links

Search for references to the old slug:

```bash
grep -r "old-name" docs/
```

Update any found references. Be careful: the regenerated `all.md` and `services.json` will already have the new slug after step 6 — focus on hand-written cross-links in other docs pages.

### 6. Regenerate the Listings

```bash
bun run generate:services
```

This rewrites:

- `docs/.vitepress/theme/data/services.json` (the entry now uses the new slug and, by extension, the new URL)
- `docs/services/all.md` (the entry's link now points to `/services/new-name`)

Commit both alongside the rename.

## Verification Checklist

After renaming, verify:

- [ ] New file exists: `docs/services/new-name.md`
- [ ] Old file removed (via `git mv`)
- [ ] Logo renamed or `icon:` frontmatter points to a real file
- [ ] Redirect added to `nginx/redirects.conf`
- [ ] No broken internal links: `grep -r "old-name" docs/` shows only intentional matches (e.g., the redirect itself)
- [ ] Ran `bun run generate:services`
- [ ] `services.json` and `all.md` use the new slug
- [ ] Service appears at `http://localhost:5173/docs/services/new-name`
- [ ] Old URL redirects to new URL (in production behind nginx)
- [ ] Logo displays on the listing card

## Common Scenarios

### Fixing camelCase to kebab-case

Coolify's JSON sometimes uses camelCase, but docs slugs are always lowercase kebab-case:

- `denoKV` → `denokv.md`
- `homeAssistant` → `home-assistant.md`

### Adding Version Numbers

When Coolify adds version-specific services:

- `mautic.md` → `mautic5.md` (if JSON specifies `mautic5`)

### Compound Names

When the upstream slug becomes more specific:

- `ente.md` → `ente-photos.md`

## Troubleshooting

### Service shows 404

- Check that the redirect is in `nginx/redirects.conf`
- Verify the markdown file actually exists at the new path
- Run `bun run generate:services` and confirm `services.json` has the new slug

### Old URL still works without redirect

- Nginx config may need a reload
- Check redirect syntax in `redirects.conf`

### Search engines still show old URL

- Redirects are working correctly (301 tells search engines to update)
- Takes time for search engines to re-crawl

### Card shows wrong/no logo after rename

- The logo file basename probably no longer matches resolver candidates for the new slug
- Either rename the logo to `<new-slug>-logo.<ext>` or set `icon:` in frontmatter

## What Changed

This skill used to instruct you to update `slug` in `List.vue`'s services array and to hand-edit `docs/services/all.md`. Both files are now generated from the markdown filename and frontmatter. **Do not edit either by hand** — run `bun run generate:services` instead.

## Related Skills

- `adding-service-documentation` — for creating new service docs
- `disabling-services` — for hiding deprecated services