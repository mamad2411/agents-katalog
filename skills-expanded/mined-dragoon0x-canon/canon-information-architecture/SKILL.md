---
name: canon-information-architecture
description: Use when organizing site structure, navigation hierarchy, page grouping, URL schemas, or user flow maps. Covers card sorting results, tree testing, flat vs deep hierarchy, and labeling conventions. Trigger when the user mentions IA, information architecture, sitemap, page structure, navigation planning, or URL structure.
---

# CANON · Information Architecture

IA is the skeleton. Navigation, content, and URLs all reflect it. If the skeleton is wrong, every screen built on top of it inherits the confusion.

## Flat vs deep

| Structure | Use when |
|---|---|
| Flat (≤ 2 levels) | Simple app, marketing site, 5–15 pages |
| Medium (3 levels) | SaaS product, content-heavy site, 15–50 sections |
| Deep (4+ levels) | Enterprise tools, documentation, large e-commerce |

Prefer flat. Every additional level costs discoverability. Users who can't find something in 3 clicks tend to search instead.

## URL design

URLs are IA made visible. They should be:

- **Readable**: `/projects/42/settings` not `/p?id=42&tab=3`
- **Hierarchical**: `/team/members/invite` reflects the nesting
- **Stable**: changing URLs breaks bookmarks, SEO, and shared links
- **Lowercase**: `/About` and `/about` shouldn't be different pages

## Labeling

Labels are the IA's voice. They must be:

- **User-language, not internal jargon**: "Billing" not "Subscription management module"
- **Mutually exclusive**: users shouldn't wonder whether something lives under "Settings" or "Preferences"
- **Consistent in abstraction level**: don't mix "Dashboard" (abstract) with "Invoice #4021" (concrete) at the same nav level

## Validation methods

| Method | When | What it tests |
|---|---|---|
| Card sorting (open) | Early, before IA exists | How users mentally group items |
| Card sorting (closed) | After draft IA | Whether users agree with your grouping |
| Tree testing | After IA is built | Whether users can find items in the hierarchy |
| First-click testing | After UI exists | Whether the first click leads toward the right answer |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Mirroring the org chart | Users don't know or care about internal teams |
| More than 7 top-level nav items | Cognitive overload; group or use sidebar |
| Deep nesting (5+ levels) | Users get lost |
| Duplicate items in multiple categories | Users check one, don't find it, give up |
| URLs that expose implementation (`/api/v2/render?page=home`) | Unusable, unstable |

## Audit checklist

- [ ] ≤ 3 levels deep for most paths
- [ ] Top-level navigation ≤ 7 items
- [ ] Labels use user language, not internal jargon
- [ ] Labels at the same level are mutually exclusive
- [ ] URLs are readable, hierarchical, lowercase, stable
- [ ] No duplicate items across categories
- [ ] Validated with card sort or tree test

## Sources

- Peter Morville & Louis Rosenfeld · Information Architecture (book)
- Nielsen Norman · "Tree Testing" and "Card Sorting"
- Steve Krug · Don't Make Me Think
