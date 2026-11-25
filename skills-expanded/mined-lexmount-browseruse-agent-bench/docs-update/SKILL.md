---
name: docs-update
description: "Update Mintlify documentation in docs/ for browseruse-bench, including adding new pages, enforcing .mdx files, and keeping English/Chinese navigation parity. Use when adding or editing docs pages, fixing missing/incorrect language variants, or updating docs/docs.json navigation."
---

# Docs Update

Use this workflow to create or update Mintlify docs under `docs/`, including:
- site-level setup (`docs/docs.json`, theme, branding),
- bilingual content parity (`en` and `zh`),
- navigation consistency and link correctness.

If user asks for "Mintlify style docs", this skill is sufficient for most cases. Use official Mintlify docs only when syntax/fields are unclear or a new feature is requested.

## 1. Identify update type first

- **Page-only update**: Content changes only; update paired language page and navigation if needed.
- **Section update**: Add/rename groups and pages in both languages.
- **Site bootstrap/update**: Create or update `docs/docs.json`, logo/favicon paths, navbar/footer, tabs.

## 2. Standard directory layout

- Guides and general docs:
  - English: `docs/en/...`
  - Chinese: `docs/zh/...`
- API Reference:
  - English: `docs/api-reference/...` or `docs/en/api-reference/...` (follow existing repo convention)
  - Chinese: `docs/zh/api-reference/...`
- Assets:
  - Images/icons: `docs/images/...`
  - Logos: `docs/logo/...`
  - Favicon: usually `docs/favicon.svg`

Prefer matching existing project conventions; do not mix two API reference layouts in one repo.

## 3. Enforce `.mdx` pages

- All content pages must be `.mdx`.
- If a page exists as `.md`, rename to `.mdx` and update references.
- `docs/docs.json` page paths must omit file extensions.

## 4. Frontmatter baseline (required)

Every content page should start with:

```mdx
---
title: "Page Title"
description: "Short summary of this page"
icon: "optional-icon"
---
```

Rules:
- Localize `title` and `description`.
- Use `icon` only when section convention already uses icons.
- Keep descriptions concise and meaningful for search/snippets.

## 5. Bilingual parity rules (`en` / `zh`)

- For each new `en` page, add a matching `zh` page at the same relative path.
- Keep group structure and page order aligned across languages.
- If translation is not ready, add a localized placeholder page:
  - Chinese placeholder: `该页面正在翻译中。`
  - English placeholder: `This page is pending translation.`

## 6. `docs/docs.json` update checklist

When creating or updating `docs/docs.json`, validate:
- Top-level metadata exists and is coherent:
  - `"$schema": "https://mintlify.com/docs.json"`
  - `theme`, `name`, `colors`, `favicon`
- Navigation defines both language entries where bilingual docs are required.
- Tabs/groups/pages are present and ordering is parallel for `en` and `zh`.
- Page paths are extensionless and exactly match file paths.
- `logo`, `navbar`, and `footer` links are valid.

If repo has existing `docs/docs.json`, minimally edit and preserve established style.

## 7. Internal links and paths

- Use language-specific links:
  - English: `/en/...` and matching API path style of the repo
  - Chinese: `/zh/...`
- Use absolute doc links for cross-page navigation, avoid fragile relative traversal.
- Verify renamed pages do not leave stale links.

## 8. Recommended page skeletons

For a new product docs set, create at minimum:
- `docs/en/introduction.mdx`
- `docs/en/quickstart.mdx`
- `docs/zh/introduction.mdx`
- `docs/zh/quickstart.mdx`
- `docs/docs.json`

Then expand with:
- architecture / concepts
- examples
- API reference
- FAQ or troubleshooting

## 9. Validation before finishing

Run lightweight checks:
- Ensure all referenced pages in `docs/docs.json` exist.
- Ensure all new pages include frontmatter.
- Ensure no newly added `.md` content pages remain (except intentionally non-content files like README notes).
- Ensure EN/ZH navigation parity (unless user explicitly asked for single-language docs).

If local Mintlify CLI is available, run preview/lint command and report result.

## 10. Quick completion checklist

- `docs/docs.json` created/updated and valid.
- New/updated pages are `.mdx`.
- Frontmatter is present and localized.
- EN/ZH page parity is complete (or placeholders added).
- Navigation entries resolve to real files.
- Internal links match language routes.
