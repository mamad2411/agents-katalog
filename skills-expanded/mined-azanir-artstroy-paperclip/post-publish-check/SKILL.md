---
name: post-publish-check
description: Verify a newly published article is fully live, indexed, and technically correct. Checks HTTP status, RSS/sitemap presence, OG tags, canonical URL, Pagefind index, and basic broken links. Required before the `live` label is applied.
---

# Post-Publish Check

The post-publish check is the Publisher's verification that a new article is actually live and correctly configured. It runs immediately after the human-approved PR merges and the deploy pipeline completes.

A failed check means the `live` label is NOT applied — Distribution Manager cannot syndicate until this passes.

## Trigger

Run after receiving confirmation that:
1. Human approved and merged the `publish/{slug}` PR
2. GitHub Actions deploy pipeline completed successfully (green checkmark)

Wait at least 90 seconds after the pipeline completes before running checks (allow CDN propagation).

## Checks

### 1. HTTP Status
```
GET https://artstroy.net/{slug}
Expected: HTTP 200
```
Any non-200 response = FAIL. If 404, the Astro build didn't include the article (check `isDraft: false` was set correctly). If 500, infrastructure issue — escalate to CTO.

### 2. Sitemap Presence
```
GET https://artstroy.net/sitemap.xml
Expected: contains "/{slug}"
```
If the slug is missing from the sitemap, Googlebot won't discover the article. This is a FAIL — investigate whether Astro's sitemap integration is generating correctly.

### 3. RSS Feed Presence
```
GET https://artstroy.net/rss.xml (or /feed.xml)
Expected: contains article title or slug
```

### 4. OG Tags Validation

Fetch the article page HTML and verify:
- `<meta property="og:title" content="{article title}">` — present, matches frontmatter
- `<meta property="og:description" content="...">` — present, ≤180 chars
- `<meta property="og:image" content="https://artstroy.net/{slug}/imgs/og.png">` — present
- `<meta property="og:type" content="article">` — present
- `<link rel="canonical" href="https://artstroy.net/{slug}">` — present

Any missing required OG tag = FAIL.

### 5. OG Image Accessibility
```
GET https://artstroy.net/{slug}/imgs/og.png
Expected: HTTP 200, Content-Type: image/png
```
The og.png must be accessible. A 404 here means the Designer's assets weren't committed, or the deploy didn't include the `imgs/` directory.

### 6. Pagefind Search Index

The Pagefind index is built at `bun run build` time. Verify it includes the new article:
- Navigate to `https://artstroy.net` and open the search UI
- Query a distinctive keyword from the article title
- The new article should appear in results

If it doesn't appear: the Pagefind index may not have been rebuilt. The deploy must re-run `bun run build` (which runs `astro build` which triggers Pagefind index generation). This is a FAIL — create an issue for DevOps.

### 7. Cover Image Accessibility
```
GET https://artstroy.net/{slug}/imgs/cover.avif
Expected: HTTP 200, Content-Type: image/avif
```

### 8. Basic Broken Link Check

Check links within the article body only (not site-wide):
```bash
npx broken-link-checker https://artstroy.net/{slug} --exclude "mailto:"
```
Any internal 404 = FAIL. External 404 = WARNING (note it, don't block).

## Result Report

```markdown
## Post-Publish Check — /{slug}

| Check | Result | Notes |
|---|---|---|
| HTTP 200 | ✅ / ❌ | |
| Sitemap | ✅ / ❌ | |
| RSS feed | ✅ / ❌ | |
| OG:title | ✅ / ❌ | |
| OG:description | ✅ / ❌ | |
| OG:image tag | ✅ / ❌ | |
| OG:image file | ✅ / ❌ | |
| Canonical URL | ✅ / ❌ | |
| Pagefind | ✅ / ❌ | |
| Cover image | ✅ / ❌ | |
| Broken links | ✅ none / ⚠️ {count} external / ❌ {count} internal | |

**Result: PASSED ✅ / FAILED ❌**
```

**If PASSED:** Apply `live` label to the publish issue. Notify EIC that the article is live and QA + Distribution Manager may proceed.

**If FAILED:** Do NOT apply `live` label. Create a `publish-fix` issue assigned to the relevant agent (DevOps for deploy issues, Designer for missing images, Frontend Engineer for broken links), referencing the post-publish check report. Rerun this check after the fix is deployed.
