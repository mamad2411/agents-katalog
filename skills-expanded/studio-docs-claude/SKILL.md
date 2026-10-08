# Rasa Docs — Authoring Conventions

This file captures the style and structure conventions for the Rasa partner documentation site. All authors and coding agents must follow these rules so the docs stay consistent.

---

## Site Structure

The docs have **two products**, configured as tabs in `docs.json`:

| Tab | Path prefix | Audience |
|-----|-------------|----------|
| Studio | `studio/` | Business users, conversation designers |
| Rasa Pro | `pro/` | Developers, engineers |

**Maestro** is a section _inside_ Rasa Pro (`pro/maestro/`), never a separate top-level product. It must never have its own version dropdown.

Within each product, navigation follows **Diátaxis** in this order:
1. **Get Started** — tutorials and quickstarts
2. **Guides** — task-oriented how-tos
3. **Concepts** — explanatory content
4. **Reference** — changelogs, API reference, config reference

---

## Authentication

The entire site is partner-gated using Mintlify Auth (`"type": "password"` in `docs.json`). Do **not** add `"public": true` to any page.

To move a section to partial auth later, add `groups: ["partners"]` to the frontmatter — do not mark pages public yet.

---

## Frontmatter Requirements

Every `.mdx` file **must** include:

```yaml
---
title: "Page Title — 50–60 characters, unique, SEO-friendly"
sidebarTitle: "Short Label"
description: "130–155 characters. Describes the page content — not a restatement of the title."
---
```

- **`title`**: 50–60 chars. Verb-led for guides ("Configure your agent"), noun-led for concepts ("What is CALM?"). Must be unique across the site.
- **`sidebarTitle`**: 1–3 words, Title Case. Never repeats the product name. Examples: "Introduction", "Quickstart", "Custom Actions", "What is Maestro".
- **`description`**: 130–155 chars. Used in llms.txt and search previews. Must add information beyond the title.

---

## Opening Paragraph

Every page **must** open with a plain-prose paragraph immediately after the frontmatter — before any component, callout, or code block. It must:

- Name the feature/product
- State what this page covers or what the reader will accomplish
- Add information beyond the title and description

❌ Bad: `This page covers authentication.`
✅ Good: `Rasa Studio authenticates Studio API requests using Keycloak's Client Credentials flow. This page walks you through creating a Keycloak client, obtaining a client secret, and using it to get a Bearer token for API calls.`

---

## Page Conventions

### Components to use

| Use case | Component |
|----------|-----------|
| Sequential instructions | `<Steps>` / `<Step>` |
| Multiple language/tool variants | `<CodeGroup>` |
| Alternative views | `<Tabs>` / `<Tab>` |
| Feature or link grids | `<CardGroup cols={2}>` / `<Card>` |
| Important notes | `<Note>` |
| Breaking changes | `<Warning>` |
| Tips | `<Tip>` |
| Collapsible FAQs | `<Accordion>` |

**Never** use raw HTML `<div>`, `<a>`, or Tailwind classes for cards or layouts. Always use `<Card>` and `<CardGroup>`.

### Code blocks

- Always include a language tag (` ```python `, ` ```yaml `, ` ```bash `)
- Use a filename title where helpful (` ```yaml config.yml `)
- Use `<CodeGroup>` for multi-language/multi-file examples
- Never manually style code blocks — Mintlify handles theming automatically

### Callouts

Use sparingly — one or two per page maximum. Don't use `<Note>` for content that belongs in the main body.

---

## Content Tone

- **Second person** ("you", "your agent") — address the reader directly
- **Active voice** and **imperative mood** for instructions ("Run `rasa train`", not "The model can be trained by running…")
- **Lead with the user's goal**, not the implementation details
- **Studio pages** are screenshot-driven (describe UI steps clearly)
- **Pro/Maestro pages** are code-first (lead with working code examples)

---

## Quickstart Rule

Quickstart pages must get the reader to a **working result in under 10 minutes of reading**. No long preamble — get to the first command within the first `<Steps>` block.

---

## Changelogs

Both products have a changelog page using the `<Update>` component:
- `studio/reference/changelog.mdx`
- `pro/reference/changelog.mdx`

New release notes go at the **top** of the file. Each entry uses:
```mdx
<Update label="v2.0.0" description="Released 2026-01-01">
  Changes here...
</Update>
```

---

## File Naming

- Lowercase, hyphen-separated: `what-is-studio.mdx`, `custom-actions.mdx`
- Match the path slug in `docs.json` exactly
- No `index.mdx` files inside product subdirectories — use the named file (e.g., `studio/what-is-studio.mdx`)

---

## docs.json Rules

- `navigation` must be an **object** with `tabs` — never an array
- Max 2 levels of groups per tab
- No empty groups — every group must have at least 2 pages
- Primary color: `#5A17EE` (use sparingly for links, active nav, primary buttons only)
- Auth: `"type": "password"` — do not remove until public launch

---

## Migration Readiness (Docusaurus → Mintlify)

The bulk Docusaurus migration is a **later phase** (the "straight swap, no restructuring" pass). We do **not** migrate content now, but every Phase 1 decision must keep that migration mechanical. The codemod and the 14 custom-component rebuilds run against the **Docusaurus source repo**, not this repo — the `sources/` folder here is a rendered scrape (kept in `.mintignore`, never built), useful only as a content reference.

To keep the later migration a near-identity path map, follow these conventions now:

**URL / path scheme — the biggest lever.**
- Preserve the existing top-level segment names from the live site: `learn/`, `pro/`, `studio/`, `reference/` (current live URLs are `rasa.com/docs/<segment>/...`).
- Target the **`/docs` base path** at public launch so migrated pages keep their exact URLs (`rasa.com/docs/learn/concepts/calm` stays put) and SEO transfers with minimal redirects.
- New Phase 1 pages use the same segments (`studio/...`) so they slot into the migrated tree without collisions.
- Note: auth is **not supported on a `/docs` subpath**, so the gated preview lives on a subdomain/`mintlify.site` URL; the move to `rasa.com/docs` happens at public launch. Expect that one domain change; avoid others.

**Links.** Always use root-relative absolute paths (`/studio/quickstart`), never relative `../x.mdx` links. Docusaurus relative `.mdx` links are the single largest codemod transform (~1,190 occurrences) — new content must not add more.

**Frontmatter remap** (Docusaurus → Mintlify): `id`/`slug` → nav path in `docs.json`; `sidebar_label` → `sidebarTitle`; `title` → `title`; `abstract`/description → `description`. Drop `llms_modules` (Mintlify generates `llms.txt` natively).

**Admonitions:** `:::note|tip|info|warning [title]` → `<Note>`/`<Tip>`/`<Info>`/`<Warning>` with a **bold** first line for the title.

**Code fences:** `lang title="file" {3-4}` → `lang file {3-4}`. Convert `# highlight-next-line` comments to explicit `{n}` line ranges (manual step).

**Diagrams:** Kroki/D2 → Mermaid code fences (native) or pre-rendered images. No third-party diagram plugins.

**Custom components:** the 14 Docusaurus `@theme` components get rebuilt **once** as Mintlify snippets in `/snippets` and imported where needed. `<Chat>` is the proven pilot (~30 LOC). Do not inline raw JSX per page.

**Redirects:** any time a URL changes, add an entry to the `redirects` array in `docs.json`; the ported 301s and the codemod path map also land there. CI runs `mint broken-links --check-redirects`.

---

## Out of Scope (Phase 1)

The following are explicitly not part of this phase:
- Version dropdowns (Pro versioning comes later)
- OpenAPI / REST API reference
- Bulk migration of existing Docusaurus content (see **Migration Readiness** above for the conventions that keep it mechanical)
- Custom CSS or components beyond Mintlify built-ins
