---
name: programmatic-seo-location-model
description: Model the geographic coverage for a programmatic local-SEO lead-gen site (any niche) — region/location hierarchy, a population (or demand) filter for qualifying locations, regions/grouping, the location data files, and the content-gated publishing rules (whole-region vs per-location vs per-hub). Use when generating or validating region/location pages for a rank-and-rent site.
---

# Programmatic SEO Location Model

Single source of truth for "where do we cover." Generalizes to any geography: US
state→city, country→metro, province→town, etc.

## Scope (compute per project)

| Metric | How to derive |
|---|---|
| Regions | e.g. 50 states + DC (some may have 0 qualifying locations) |
| Qualifying locations | cities/places passing the demand filter (e.g. population ≥ 1,000) |
| Services per location | the fixed service count N |
| Money pages | locations × N |
| Total site pages | core + services + regions + locations + (locations × N) |

A region with 0 qualifying locations still produces a region page but no location/money pages.

## Qualifying-location filter

Only locations above a demand threshold qualify (e.g. **population ≥ 1,000**, enforced by the
data-validation script). This is the rank-and-rent sweet spot — enough local search volume to
win with a localized page. Source the numbers from an authoritative dataset (e.g. US Census
ACS). **Population is internal-only** — used for the filter and as a writer reference; never
featured on published pages.

## Data files (reference implementation)

| File | Contents |
|---|---|
| `src/data/states.json` (regions) | name, abbrev, slug, region, location count |
| `src/data/cities.json` (locations) | name, region, abbrev, slug, county, population, lat/long |
| raw census/population CSV | master source for the filter |
| location generator script | regenerates JSON from the locations doc appendix |

Location record: `{ name, region, abbrev, slug, county, population, latitude, longitude }`.
Region record: `{ name, abbrev, slug, region, locations }`.

## Regions / grouping

Group regions into a few larger buckets (e.g. 4 US Census regions) for the Locations mega menu
and region-page organization. The full per-region location inventory lives in the project's
locations doc/data — read it for a specific region's list and populations.

## Content-gated publishing rules

- **Whole region publishes only when 100% complete** — region page + every location page +
  every location×service money page carry `unique: true` (an `isCompleteRegion` check).
- **Locations publish progressively, per location** — a location renders once its own page +
  all its money pages are `unique: true` (an `isCompleteLocation` check); it does not wait for
  the rest of the region.
- **Hubs publish per service** — `/services/{slug}/` renders once `hubs/{slug}.md` is `unique: true`.
- **Header Locations mega menu** is hidden until ≥1 region is fully published; it lists only
  fully-published regions, grouped, and updates automatically on next build. The same
  "complete regions" check powers the Footer, `/locations/`, and the homepage.

## Region page order

Write all of a region's location pages (and their money pages) first; write the region page
last (see the autopilot skill). A region's tracker row re-derives to `[x]` only when the region
page + every location + every money page is unique.
