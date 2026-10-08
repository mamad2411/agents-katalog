# Ace Crawl Enhancer ("Ace SEO" / `ace_seo`)

Full-stack SEO plugin and Yoast replacement. Canonical repo: `git@github.com:AceMedia/Ace-Crawl-Enhancer.git`.
For AceMedia-wide conventions (British English, commit rules, deploy patterns) use the **speedforce** skill —
this file only holds plugin-specific facts.

**Canonical plan = [docs/ROADMAP.md](docs/ROADMAP.md)** plus GitHub issues #1 (WP 7.0) and #7 (Site Kit
indexing follow-up). Agents pick up roadmap tasks from there; keep both in sync when scope changes.

## Consumers (submodule in 6 sites — treat the public surface as frozen)

ppnews (news/sport), EgbertTaylor/IEG (WooCommerce), SheffEvents (Ace-Community-Events: events/businesses/jobs),
TalkFuse.com, unicarts (WooCommerce), william-unicycle. Also rsynced (not submoduled) into SPKF
(sheffieldparkour.org). A `git push` here gets pulled into live sites on their next submodule bump —
**never break**: `_ace_seo_*` meta keys, `ace_seo_options` / `ace_sitemap_powertools_options` shapes,
`yoast_wpseo_` form-field prefix, existing `ace_seo_*` / `ace_sitemap_powertools_*` filters, or the
theme-append title convention (see gotchas).

## Native WordPress first (check before writing anything)

This plugin is not the only thing deciding what crawlers are told. WordPress core has
its own settings for most of what an SEO plugin does, and the web server outranks both.
Work that ignores a native setting doesn't conflict loudly — it produces a site that
quietly does something nobody asked for, which is how a ticked "Discourage search
engines" sat there being ignored while a staging site got indexed.

**Before adding or changing any crawl/index behaviour, answer these:**

| Native thing | Where | What it means for us |
|---|---|---|
| `blog_public` | Settings → Reading | The master switch. Honour it via `ace_seo_site_is_discouraged()`; never add a parallel "noindex site" setting. |
| A **physical `robots.txt`** | Served root (a level above `ABSPATH` on subdirectory installs) | The server returns it before PHP runs. No filter can override it. Detected and reported by `includes/admin/ace-seo-robots-file.php`. |
| `wp_robots` filter | Core, since 5.7 | Core owns the robots `<meta>` tag. Add directives through the filter; don't echo a second tag beside it. |
| `wp_sitemaps_enabled` | Core sitemaps | Core disables its own sitemaps when discouraged. Powertools routes are ours, so they need their own gate — `ace_sitemap_powertools_is_enabled`. |
| `rel_canonical` | Core | We remove it and emit our own. Removing it twice, or neither, both show up as duplicate/absent canonicals. |
| `page_on_front` / `page_for_posts` | Settings → Reading | A static front page is `is_singular()`, which routes it down branches meant for posts. |
| `exclude_from_search`, `public`, `show_in_search` | Post type / taxonomy registration | A type the site already excluded shouldn't be re-advertised by our sitemaps. |
| `permalink_structure` | Settings → Permalinks | Sitemap routes are rewrite-backed; a permalink change needs a rewrite flush. |

Two rules that follow from the table:

1. **Look for the native option before building a setting.** If WordPress already models
   it, honour it — a second switch means two sources of truth and a site that obeys
   whichever code ran last.
2. **A `<meta>` tag only exists in HTML.** Feeds, attachments, PDFs and images need
   `X-Robots-Tag`, which is why the discourage path sends both.

**Check it rather than reasoning about it** — the failures here are contradictions
*between* layers, so they survive reading any single file:

```
php bin/crawl-settings-check.php https://site.example/ https://dev.site.example/
```

Exits 1 on a real conflict (static robots.txt shadowing the plugin, noindex pages still
in a served sitemap, a feed with no directive, robots.txt advertising a 404 sitemap).
Run it before and after any indexing change, on every environment — the environments
drift from each other, and that drift is the bug.

## Architecture map

- `accelerated-crawl-enhancer.php` (2.6k lines, singleton `AceCrawlEnhancer`) — meta fields definition,
  title/meta-desc/canonical/robots pipeline, template variables, Yoast migration, background DB optimisation.
- `includes/ace-sitemap-powertools.php` (3.4k lines, procedural `ace_sitemap_powertools_*`) — core-sitemap
  extensions, caching (Ace-Redis-Cache aware), news/authors/tags routes, exclusions, legacy redirects.
- `includes/frontend/` — `class-ace-seo-frontend.php` (head output + OG/Twitter + Jetpack override +
  JSON-LD graph), `class-ace-seo-schema.php` (Organization/Person/LocalBusiness + orphaned Product/FAQ
  builders), `class-ace-seo-breadcrumbs.php` (visual trail only), `class-ace-seo-performance.php`
  (guest meta cache + deferred footer schema).
- `includes/admin/` — settings/metabox/dashboard views (PHP + vanilla JS in `assets/js/`),
  `class-ace-seo-api-helper.php` (OpenAI + PageSpeed), `class-ace-seo-ai-assistant.php` (AJAX AI endpoints),
  Site Kit readers (`class-ace-seo-sitekit.php`, `class-ace-seo-google-data.php`).
- One DB table: `{prefix}ace_seo_analytics`. Crons: `ace_seo_optimize_database` (once),
  `ace_seo_daily_performance_check`.

## Build & verify

- `npm run build` — wp-scripts (breadcrumbs block + SaveBar into `build/`) + sass for admin CSS.
  Most admin JS is unbundled vanilla in `assets/js/` — edit directly, no build needed.
- Verify head output on a consuming site: `curl -s <url> | grep -iE 'og:|twitter:|canonical|ld\+json'`;
  parse JSON-LD blocks and validate types. The WordPress Playground MCP works for isolated plugin testing.
- Live sites sit behind Varnish/Cloudflare — origin-check with `?v=RANDOM`, then
  `sudo /usr/local/sbin/acehost-cache-warm <domain>` after any live change.

## Gotchas (hard-won — do not rediscover these)

- **Manual `_ace_seo_title` on singular posts must be stored WITHOUT the brand** — the theme appends
  the site name. All live sites (unicarts, SPKF…) store brand-free titles relying on this. Since
  1.0.6 the `is_singular` branch clears `site`/`tagline` ONLY for template-derived titles (templates
  contain `{site_name}`); manual titles keep the theme-append behaviour. Do not make that clearing
  unconditional — it strips the brand from every consumer site's manual titles.
- The frontend de-dupes OG tags via a full-page output buffer + regex (`filter_head_output`) — fragile;
  archives that want og:description must mark output `data-ace-seo="1"` to survive it.
- Sitemap hardcodes an `ace_event` taxonomy exclusion (powertools lines ~33/102).
- Schema is emitted from FOUR places (frontend graph, schema class, performance footer cache, breadcrumbs
  none) — the guest footer path can double-emit Article. Roadmap phase 1 consolidates this; until then,
  add new types into the frontend `@graph`, not a new emitter.
- ace_seo's core `rel_canonical` removal mis-times (hooked too late) — consumer themes work around it;
  keep that in mind when touching canonical output.
- `test-*.php` / `fix-slashes.php` in the root are legacy dev scripts scheduled for removal (roadmap 0) —
  don't extend them.
