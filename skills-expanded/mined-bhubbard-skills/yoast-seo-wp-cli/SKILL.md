---
name: yoast-seo-wp-cli
description: "Managing Yoast SEO and its add-ons via the command line using WP-CLI."
---

# Yoast SEO WP-CLI Commands

Yoast SEO provides robust integration with WP-CLI, allowing developers and server administrators to perform heavy lifting, indexation, and configuration changes directly from the command line without timeout issues.

## Reference
[Yoast WP-CLI Documentation](https://developer.yoast.com/customization/yoast-seo/wp-cli)

## Core Commands

### Indexation
Yoast SEO relies on "Indexables" (custom database tables) for performance. If a site's SEO data is out of sync or if you just migrated a site, you should rebuild the indexables. Running this via WP-CLI is highly recommended for large sites to avoid PHP timeouts in the browser.

```bash
# Rebuild all indexables
wp yoast index --reindex

# Build indexables (only for unindexed content)
wp yoast index
```

### Managing Options
You can view, update, and reset Yoast SEO settings via the CLI.

```bash
# View a list of all current Yoast SEO options and their values
wp yoast options list

# Update a specific option (e.g., disable breadcrumbs)
wp yoast options update breadcrumbs-enable 0

# Reset all settings to their default values (Use with caution!)
wp yoast options reset
```

## Premium & Add-on Commands

If Yoast SEO Premium or other add-ons are installed, additional commands become available.

### Redirects (Yoast SEO Premium)
Manage redirects directly from the terminal. This is useful for bulk imports or programmatic site migrations.

```bash
# Create a new 301 redirect
wp yoast redirect create /old-url/ /new-url/ --type=301

# Delete a redirect
wp yoast redirect delete /old-url/

# List all redirects
wp yoast redirect list
```

### Video SEO Add-on
Force the Video SEO plugin to index videos across the site.

```bash
# Reindex all videos
wp yoast video index --reindex
```

## Best Practices
- **Always use WP-CLI for Indexation on Large Sites**: If a site has more than a few thousand posts, running the SEO Data Optimization from the WordPress admin dashboard will likely crash or timeout. `wp yoast index --reindex` is the safest, most stable method.
- **Automated Deployments**: You can include `wp yoast options update` commands in your deployment scripts to ensure certain settings (like forcing `noindex` on staging sites) are automatically applied based on the environment.
