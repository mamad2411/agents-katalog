---
name: adding-service-documentation
description: Documents new Coolify one-click services by creating markdown pages in docs/services/, downloading logos to docs/public/images/services/, and regenerating the services listing. Use when adding service documentation, creating service pages, onboarding services from templates/compose/, or refreshing the services catalog.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Add Service Documentation

This skill guides you through documenting a new service in the Coolify documentation repository.

## When to Use This Skill

- Adding documentation for a new service from the Coolify repository
- Creating service pages with proper formatting and images
- Following documentation standards for service pages

## Architecture: Frontmatter-Driven Generation

The services listing is **generated**, not hand-edited. There is no manual catalog to maintain.

| Generator | Reads | Writes |
|---|---|---|
| `scripts/generate-service-list.mjs` | every `docs/services/*.md` frontmatter | `docs/.vitepress/theme/data/services.json` (consumed by `List.vue`) |
| `scripts/generate-services-page.mjs` | every `docs/services/*.md` frontmatter | `docs/services/all.md` |

Both scripts share `scripts/services-data.mjs`, which:
- Parses each markdown's YAML frontmatter
- Auto-resolves the logo by scanning `docs/public/images/services/` for files matching `<slug>-logo`, `<slug>_logo`, `<slug>logo`, the bare `<slug>`, or the same variants of the `title`
- Falls back to the first image referenced in the markdown body if frontmatter has no `icon` and no asset matches
- Marks a service as disabled if frontmatter has `disabled: true` or the body contains `SERVICE HIDDEN | NOT AVAILABLE | REMOVED FROM COOLIFY | TEMPORARILY DISABLED`

The generators run automatically on `bun run dev`, `bun run build`, and `bun run preview`. You can also run them on demand with `bun run generate:services`.

## Quick Start Workflow

1. **Identify the service** from Coolify's GitHub repository (`templates/compose/`)
2. **Extract metadata** from the YAML template header
3. **Download the logo** from GitHub and save to `docs/public/images/services/` using a name the resolver will pick up
4. **Create documentation** at `docs/services/{service-slug}.md` with the required frontmatter (`title`, `description`, `category`)
5. **Regenerate listings** with `bun run generate:services` (or just `bun run dev` — it runs the generators first)
6. **Commit** the new markdown, the logo, and the regenerated `services.json` and `all.md`

## File Structure

```
Coolify Repository (GitHub):
├── templates/compose/
│   └── service-name.yaml        # Service template with metadata
└── public/svgs/
    └── service-logo.svg          # Service logo

https://github.com/coollabsio/coolify/tree/main/templates/compose
https://github.com/coollabsio/coolify/tree/main/public/svgs

Documentation Repository:
├── docs/
│   ├── services/
│   │   ├── service-name.md       # Service documentation page (you create)
│   │   └── all.md                # Generated — DO NOT hand-edit
│   ├── public/images/services/
│   │   └── service-logo.svg      # Logo (you add)
│   └── .vitepress/theme/
│       ├── data/services.json    # Generated — DO NOT hand-edit
│       └── components/Services/
│           └── List.vue          # Renders services.json (no service entries inside it)
└── scripts/
    ├── generate-service-list.mjs
    ├── generate-services-page.mjs
    └── services-data.mjs
```

## Required Files for a New Service

You only edit two things; the rest is generated:

1. **Service documentation** (`docs/services/{slug}.md`) — with frontmatter
2. **Service logo** (`docs/public/images/services/`)

After your edits, `bun run generate:services` produces:
- `docs/.vitepress/theme/data/services.json`
- `docs/services/all.md`

Commit all four files together.

## Required Frontmatter

```yaml
---
title: "Service Name"
description: "Short description used on the listing card and in all.md."
og:
  description: "Optional longer SEO/social-card description."
category: "Analytics"
icon: "/docs/images/services/service-name-logo.svg"
---
```

| Field | Required | Purpose |
|---|---|---|
| `title` | yes | Card title; also `name` in `services.json` |
| `description` | yes | Card description and `all.md` entry |
| `category` | yes | Group heading in `all.md`; filter in the listing |
| `icon` | optional | Only needed when the auto-resolver can't find a matching logo |
| `og.description` | optional | Longer text for social cards |
| `disabled` | optional | `true` hides the service from the listing while keeping the page accessible |

## Detailed Instructions

**Service-specific:**
- [METADATA.md](./METADATA.md) — Extracting service info from the upstream YAML template
- [DOCUMENTATION.md](./DOCUMENTATION.md) — Writing the markdown body and frontmatter
- [IMAGES.md](./IMAGES.md) — Service logo handling and the icon resolver
- [CATALOG.md](./CATALOG.md) — Categories, the generation pipeline, and disabled services
- [TEMPLATES.md](./TEMPLATES.md) — Ready-to-use markdown templates

**Shared guidelines:**
- [FRONTMATTER.md](../_shared/FRONTMATTER.md) — Title, description, Open Graph
- [IMAGES.md](../_shared/IMAGES.md) — General image syntax
- [LINKS.md](../_shared/LINKS.md) — Internal and external link formatting
- [CONTAINERS.md](../_shared/CONTAINERS.md) — VitePress callout containers

## Important Rules

1. **Never hand-edit `docs/services/all.md` or `docs/.vitepress/theme/data/services.json`** — both are regenerated and your changes will be overwritten.
2. **Download logos locally**: never link to external image URLs.
3. **Skip ignored services**: if the upstream YAML has `# ignore: true`, don't document it.
4. **Images**: use `![alt](path)` for the logo; use `<ZoomableImage>` only for screenshots.
5. **UTM parameters**: append `?utm_source=coolify.io` to all external links.
6. **File naming**: lowercase, kebab-case slug; the filename is the slug.
7. **Logo naming**: name the asset so the resolver finds it without an explicit `icon` field. `<slug>.svg`, `<slug>-logo.svg`, or `<slug>_logo.svg` all work.

## Testing

```bash
# Regenerate listings explicitly (optional — dev does this for you)
bun run generate:services

# Start dev server (runs generate:services first)
bun run dev

# Verify:
# - Service appears on the listing page (/docs/services/)
# - Logo displays
# - Service page loads at /docs/services/{slug}
# - Service appears under the right category in /docs/services/all
# - Category filter includes it

# Build for production
bun run build
```

## Troubleshooting

**Logo not showing:**
- Check that the file lives in `docs/public/images/services/` and the basename matches one of the resolver candidates (`<slug>`, `<slug>-logo`, `<slug>_logo`, `<slug>logo`, `<title>`, `<title>-logo`).
- If the auto-resolver can't be made to work, set `icon:` explicitly in frontmatter using a `/docs/images/services/...` path.
- Path must start with `/docs/images/services/` (not `/public/`).

**Service missing from the listing:**
- Re-run `bun run generate:services` and check the resulting `services.json` and `all.md`.
- Ensure your frontmatter has `title`, `description`, and `category`.
- Ensure the file isn't named `all.md`, `introduction.md`, or `overview.md` — those are excluded.
- Confirm `disabled: true` is not set, and that the body doesn't contain a hide pattern (`SERVICE HIDDEN`, `NOT AVAILABLE`, `REMOVED FROM COOLIFY`, `TEMPORARILY DISABLED`).

**Wrong category grouping in `all.md`:**
- The `category` field is matched verbatim. See [CATALOG.md](./CATALOG.md) for the existing list.

## Related Commands

- `/new-services` — automated service documentation generator
- Inspect existing services in `docs/services/` for reference frontmatter shapes