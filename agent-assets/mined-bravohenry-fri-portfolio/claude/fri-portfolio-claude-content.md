# components/content/
> L2 | Parent: src/components/CLAUDE.md

## Members

EntryList.tsx: Chronological list renderer — title, date, summary per entry, shared by diary + weekly list pages
EntryPage.tsx: Single entry renderer — back-nav, meta header, rendered markdown body via `diary-content` CSS class

## Architecture Notes

- Both components are server components (no `"use client"`)
- EntryList links to `/${type}/${slug}`, EntryPage links back to `backHref`
- Typography uses the `diary-content` CSS class from globals.css for markdown rendering (shared across diary and weekly)
- Design tokens: `font-vt323` for headings, `neon-pink`/`neon-coral` for accents, `glass-border`/`glass-bg` for hover states

[PROTOCOL]: Update this file when components are added/removed, then check parent CLAUDE.md
