---
name: audit-seo
description: Audit on-page SEO by inspecting the rendered DOM. Checks title, meta description, h1 structure, html lang, viewport, canonical, robots, OpenGraph + Twitter Card tags, JSON-LD validity, hreflang, and favicon. Returns findings grouped by severity (critical / high / medium / low).
---

# /audit-seo

Single-backend skill. Calls **`audit_seo`** on the rolepod-uiproof
MCP server. No fallback (D-024).

## When to use

- Verifying that a page has the SEO basics before launch.
- After a templating / SSR change that touches `<head>` content.
- Catching a stray `noindex` or broken JSON-LD before merge.
- Running alongside `/audit-a11y` and `/audit-page-budget` as a
  Verify-phase triple.

## When NOT to use

- Off-page SEO (backlinks, domain authority, sitemap fetching) — out of
  scope for an in-browser auditor.
- Crawl-budget / robots.txt inspection beyond the `<meta name="robots">`
  on the audited URL.
- Pages that fail to load (server 500, network error) — fix the page
  first.

## Inputs

- `url` — URL to audit.
- `viewport` — optional `{ width, height }`.
- `checks[]` — subset of `title | meta_description | h1 | lang | viewport | canonical | robots | og_tags | twitter_tags | json_ld | hreflang | favicon`. Default: all of them.
- `report_format` — `json` (default) | `markdown`. Markdown writes an
  extra `seo-report.md` alongside the JSON.

## Outputs

- `run_id` — folder under the run root (see Evidence routing).
- `counts` — findings by severity (`critical | high | medium | low`).
- `findings[]` — each `{ check, severity, message, evidence? }`.
- `status` — `pass` (no findings) | `warn` (only medium/low) | `fail`
  (any critical or high).
- `report_path` — path to `seo-report.json`.
- `markdown_path` — set only when `report_format='markdown'`.

## Process

1. Build `audit_seo` input from the user's intent (URL, optional
   `checks` subset).
2. Call the tool.
3. Surface critical / high findings inline; reference the report path
   for the full list.

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/audit_seo_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-audit-seo/`

Either way the run directory contains `seo-report.json` (and
`seo-report.md` when requested) plus a `manifest.json` per Extension
Protocol v1 so the parent's `check-work` skill can aggregate the result
into the verify report.

## If the tool is unavailable

Surface plainly:

> The `/audit-seo` skill needs the **rolepod-uiproof** MCP server, which is
> not currently available. Confirm the plugin is installed and try again.

Do not attempt another backend (D-024).

## Examples

### Full audit on a landing page

```json
{
  "url": "https://example.com"
}
```

### Title + meta only, markdown report

```json
{
  "url": "https://example.com",
  "checks": ["title", "meta_description"],
  "report_format": "markdown"
}
```

### JSON-LD validity sweep across product pages

```json
{
  "url": "https://example.com/product/abc",
  "checks": ["json_ld"]
}
```
