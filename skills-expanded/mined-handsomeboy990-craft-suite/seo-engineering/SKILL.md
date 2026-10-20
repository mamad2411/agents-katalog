---
name: seo-engineering
description: Makes a public site discoverable and correctly represented: crawlability and rendering strategy, one canonical URL per page, titles and descriptions, semantic structure, structured data, sitemaps and robots rules, alternate language links, pagination and faceted URLs, redirects and status codes, and the performance signals search engines measure. Use for any public web surface, and before any URL structure changes.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, frontend-engineering]
  outputs: [url-strategy, metadata-plan, structured-data, crawl-directives, redirect-map]
---

# SEO Engineering

The technical half of search visibility: making sure a page can be fetched,
rendered, understood and attributed to one address. Content and authority are
someone else's work; the defects here are engineering defects and they are the
ones that silently remove a site from results.

Applies to public surfaces only. An authenticated application needs none of
this, and should actively refuse indexing.

## 1. Crawlability first

```
the page returns 200 and its content without JavaScript, or the rendering
  strategy is one search engines handle, decided deliberately
robots rules allow the pages that should be found, and only those
no accidental noindex on a production template, which is the most common
  catastrophic defect in this discipline
the site is reachable at one hostname, with the others redirecting
internal links are real anchors with real addresses, not click handlers
important pages are reachable within a few links from the entry point
pagination and infinite scroll expose crawlable addresses
```

## 2. Rendering strategy

| Strategy | Fits | Watch |
|---|---|---|
| static generation | content that changes rarely | rebuild triggers, stale content |
| server rendering | content that changes per request | response time, caching |
| incremental regeneration | large catalogues | invalidation correctness |
| client rendering | authenticated applications | not indexable in practice, and that is fine |

For a public page whose traffic depends on search, the content is in the
response body. Anything else is a wager on someone else's renderer.

## 3. One canonical address

```
one page, one address, chosen and declared
duplicates consolidated: trailing slash, case, query parameters, index paths
tracking parameters do not create new pages
faceted and filtered views declared canonical to their base, or made
  genuinely distinct and indexable when they have their own demand
pagination pages are self canonical, never canonical to page one
alternate language versions cross reference each other, and each is canonical
  to itself
```

Getting this wrong splits one page's authority across five addresses, or
worse, consolidates five distinct pages onto one.

## 4. Metadata

```
title      unique per page, front loaded with the distinguishing words
description unique, written for a human deciding whether to click
robots     per page where it differs from the site rule
canonical  absolute, self referencing by default
alternates one per locale, plus a default, mutually consistent
social     title, description, image, type, with an image that exists and
           has the right dimensions
```

Every one of those is generated from data, never written by hand per page,
and it is verified on the rendered output rather than in the template.

## 5. Structure and semantics

```
one main heading per page, describing the page
headings forming a real outline, not a styling ladder
landmarks: header, navigation, main, footer
lists as lists, tables as tables with headers
images with alternative text that describes the content
links whose text says where they go
```

This overlaps entirely with `accessibility-testing`, which is not a
coincidence: a document a screen reader can navigate is a document a crawler
can understand.

## 6. Structured data

```
only for what the page actually is: article, product, organisation, event,
  recipe, breadcrumb, FAQ
generated from the same source as the visible content, never diverging from it
validated against the vocabulary, and tested on real pages
no markup describing content the user cannot see
removed when the corresponding feature is removed from the page
```

Structured data that contradicts the page is worse than none.

## 7. Sitemaps and directives

```
sitemap generated from the routes that exist, not maintained by hand
excludes anything noindexed, redirected or removed
last modified dates that are true
split when large, with an index
robots file: rules per user agent, sitemap reference, no accidental blanket
  disallow, and no attempt to hide anything sensitive with it
a blocked page cannot be read, so a noindex on it is never seen: the two
  directives are chosen deliberately, never both
```

## 8. URL changes and redirects

Any change of address is a migration:

```
a redirect map produced before the change, one to one where possible
permanent redirects for permanent moves, temporary only when it is temporary
never chain more than one hop
never redirect everything to the home page: that loses the page entirely
internal links updated to the new address, not left relying on the redirect
the old sitemap retired, the new one submitted
monitoring for errors and lost traffic for at least one indexing cycle
```

## 9. Performance signals

Search engines measure what users feel: loading, interaction responsiveness
and layout stability. The work belongs to `performance-engineering`; this
skill states which pages must meet the thresholds and verifies them on real
devices and real networks rather than on a developer machine.

## 10. Prohibitions

- Never ship a production template carrying a noindex directive.
- Never let two addresses serve the same content without a canonical.
- Never generate metadata that contradicts the visible page.
- Never add structured data for content that is not on the page.
- Never use a robots disallow as a security or privacy control.
- Never redirect a removed page to the home page as a default.
- Never change a URL structure without a redirect map.
- Never index an authenticated or staging environment.

## 11. Protocol

1. Establish which surfaces are public and which must refuse indexing.
2. Choose the rendering strategy and verify the content in the response.
3. Define the URL structure and the canonical rules, including facets.
4. Generate metadata from data, per page, and verify on rendered output.
5. Fix the document structure, which also serves accessibility.
6. Add structured data only where it describes the page.
7. Generate the sitemap from the real routes, and write the robots rules.
8. For any address change, produce the redirect map first.
9. Verify the performance thresholds on the pages that matter.
10. Check the rendered result with a crawler view, not with the source
    template.

## 12. Auto-critique

Score from 0 to 5: crawlability verified on rendered output, rendering
strategy justified, canonical correctness, metadata uniqueness and generation,
document structure, structured data matching the page, sitemap and robots
coherence, redirect map for any change, staging and authenticated surfaces
excluded.

Threshold: no axis below 3, average at least 4. A production noindex, or a
site whose content is absent from the response body while depending on search
traffic, is an automatic failure.

## 13. Interfaces

- Upstream: `requirements-analysis` for which surfaces are public,
  `architecture-design` for the rendering strategy.
- Lateral: `frontend-engineering` for the templates, `internationalization`
  for alternate language links, `accessibility-testing` for the shared
  semantics, `performance-engineering` for the measured signals.
- Downstream: `deployment-engineering` for staging exclusion,
  `migration-engineering` for URL changes, `observability` for crawl and
  error monitoring.
