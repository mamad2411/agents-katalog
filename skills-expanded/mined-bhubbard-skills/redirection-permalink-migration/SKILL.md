---
name: redirection-permalink-migration
description: Guidance on migrating permalink structures. Use when changing the site's global permalink settings and needing to avoid mass 404 errors.
---

# Redirection: Permalink Migration

If a site changes its global permalink structure (e.g., moving from `/2024/05/12/post-name/` to just `/post-name/`), doing so without redirects will cause catastrophic 404 errors and SEO rankings drops.

## The Site Migration Tool
The Redirection plugin features a "Site Migration" tool specifically for this.
1. Go to Redirection > Site.
2. Under "Migrate Permalinks", enter your **old** permalink structure (e.g., `/%year%/%monthnum%/%day%/%postname%/`).
3. Save the changes.

## How it works
The plugin will mathematically intercept any incoming URL matching the old structure, query the database to find the corresponding post, and automatically issue a 301 redirect to the post's new, current URL. This eliminates the need to write complex Regular Expressions manually.
