---
name: site-structure-inventory
description: Inspect a specified live website to inventory production pages, URL families, navigation, observed hierarchy, crawl and index directives, and coverage gaps. Use for first discovery, migration verification, or an incremental refresh.
metadata:
  version: 1.0.0
---

# Site Structure Inventory

Start with the official domain, allowed hosts and locales, access level, and scope (initial inventory, full review or changes since a dated baseline). Any public reference site is a valid subject. Return observed production structure. For target architecture, hand the inventory to [website-structure](https://github.com/kostja94/marketing-skills/tree/main/skills/strategies/structure/website-structure). For marketing interpretation use [competitor-research](https://github.com/kostja94/marketing-skills/tree/main/skills/competitor-research) when relevant.

## Discover and converge

1. Seed the queue with the homepage, desktop and mobile menus, footer, robots.txt, all sitemap indexes and children, and principal hubs. Inspect rendered targets: dropdowns, buttons, image links, breadcrumbs, cards, FAQ, related items, pagination and error/login page navigation.
2. Follow internal links recursively. On blogs, directories, tools, templates, category and author hubs, inspect pagination, load more, infinite scroll and public content requests. Check feeds, llms.txt, canonical, hreflang, Open Graph URLs, structured data (breadcrumbs, items and IDs), manifests, alternate links, prefetches and public route/slug data. For client-rendered pages inspect rendered DOM or public JSON/GraphQL responses. Preserve first discovery and additional sources.
3. Normalize host, protocol, ports, slashes, encoding, fragments and tracking parameters according to observed server behavior. Preserve case-sensitive routes, meaningful content parameters and distinct locales. Inspect first and last pagination boundaries, next links, canonicals and language alternates. Sample filter spaces; use real production slugs. Avoid unbounded guessing, account enumeration or high concurrency.
4. Add newly discovered redirect/canonical/locale targets to the queue. With permission, cross-check CMS states, search-console URLs, analytics, site search, server/CDN and 404 logs for unlinked pages. External search, backlinks, crawler indexes and archives supply leads; verify on the live host. Treat authorized repository routes, slug registries, rewrites and prototypes as separate plan candidates until verified in production.
5. Stop at a full pass with no new canonical candidates within the checked sources, or at an explicit resource/access boundary. State which condition occurred. Report a complete census only with a reproducible reconciliation of production routes, publishing registry, CMS and live pages.

## Validate instances and families

For small sets, check every distinct candidate. For large families, record URL pattern, page type, hub/generation mechanism, count and its source (or confirmed minimum), date and 3–5 representative instances covering first/last items, pagination, locales and unusual states. Expand sampling around anomalies. Distinguish enumerated from individually verified counts. A sitemap total measures that file's coverage.

Record for each checked instance: URL, type, discovery sources, HTTP status and redirect chain, meaningful rendered content, canonical, robots.txt permission, meta robots and HTTP indexing directives, sitemap membership, public internal reachability, expected hub membership, live evidence and check date. Separate eligibility from observed search-engine indexing. Use unknown for untested dimensions.

Combine compatible states for the same URL, time and conditions: canonical production page, auxiliary file, observed orphan candidate, missing from expected hub, conflicting signals, accessible but publication uncertain, legacy redirect, noindex, robots restriction, soft 404, actual 404/410. Keep CMS drafts/archives, historical URLs and deployment plans distinguishable. A 200 response can be an empty shell; navigability, canonical choice, CMS publication and index eligibility each need their own evidence. Document redirect loops, wrong locale/host canonicals and contradictions such as a live child under a coming-soon hub. Preserve competing observations, dates, safe conclusion and required follow-up.

## Deliver and refresh

Report scope, hosts, sources/permissions/unchecked surfaces, dated production inventory or family table, observed IA tree, nav/hub/body reachability, redirect history, crawl and index signals, auxiliary files, orphans, omissions, conflicts and pending candidates. Keep any future plan separate. The tree conveys hierarchy; the ledger supports URL-level claims. Record observed edges here and hand target link design to the internal-link workflow. Keep large exports separate from the readable report. For a customer project reuse its site-structure module; leave feature specifications, keyword decisions and deployment details with their owners.

Recheck affected families after host, locale, navigation, CMS, hub, sitemap, canonical, redirect or release changes; also refresh for client handoff, resumed work or newly discovered URLs. Preserve creation date, update the evidence cutoff, separate historical state, and report only additions, status changes and new evidence on repeat runs.