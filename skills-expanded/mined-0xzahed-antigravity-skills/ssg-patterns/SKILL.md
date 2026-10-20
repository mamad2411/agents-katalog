---
name: ssg-patterns
description: Implement static site generation. Use when building content-driven
  sites that can be prebuilt.
metadata:
  tags: ssg
---

# Static Site Generation

## Use this skill when
- Building blogs, docs, and marketing sites
- Generating pages at build time
- Optimizing for CDN caching and performance

## Do not use this skill when
- Content is user-specific or real-time
- Pages change frequently beyond build cadence

## Instructions
1. Generate pages at build time from data sources (CMS, files, APIs).
2. Use ISR/regeneration for content that changes periodically.
3. Provide fallback/on-demand generation for rarely visited pages.
4. Inline critical CSS and preload key assets.
5. Servve via CDN for maximum caching.
6. Keep build times reasonable; split large sites into incremental builds.

## Output Format
- Content model | build pipeline | regeneration strategy | cache config

## Common Mistakes
- SSG for user-specific pages
- Build times exploding as content grows
- Caching that serves stale content forever
