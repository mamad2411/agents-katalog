---
name: local-seo-site-architecture
description: Plan site architecture for local service businesses to rank for "service + location" keywords. Use when building websites for plumbers, electricians, heating engineers, cleaners, or any local trade/service business. Triggers include requests to plan a local business website, create a sitemap for a service area business, structure pages for local SEO, or rank for "[service] [town]" searches. Outputs tiered page structures, URL hierarchies, internal linking strategies, entity consistency requirements, schema requirements, and content differentiation guidelines.
---

# Local SEO Site Architecture

Plan website structures that rank for "service + location" keyword combinations while avoiding thin content and doorway page penalties.

Source of truth: `references/local-seo-playbook-2026.md` in this skill (Whitespark 2026, Sterling Sky, Dec 2025 core update). Read it for the evidence behind these rules. A shared copy also lives at `~/.agents/skills/references/shared-seo/local-seo-playbook-2026.md` on the local machine.

## Core Principle

One dedicated page per service is the #1 local organic ranking factor. Location pages still work, but the constraint is **proof, not crawl budget**: one URL = one liability unless it earns its place with local evidence that can't be copied. Two or three strong city pages outperform fifteen templated ones, and the fifteen can now actively hurt (doorway filtering, sitewide quality assessment).

## Process

1. **Gather inputs** — services offered, locations covered, business base, and **evidence per town**: reviews from there, jobs done there, photos from there
2. **Tier the locations** — by proof first, search volume second
3. **Generate page structure** — service pillars + proof-capped location pages
4. **Define entity consistency** — one source of truth for name, NAP, services terminology
5. **Define internal linking** — hub-and-spoke
6. **Document content differentiation, schema, and E-E-A-T requirements** per page type

## Location Tiering

| Tier | Criteria | Page Strategy |
|------|----------|---------------|
| Primary | Towns you can evidence with reviews, job photos, and completed work — **cap at 3-6 for most trades** | Dedicated location page; service+location pages only for combos with real proof |
| Secondary | Genuinely served, some evidence but not enough for a page yet | Named and linked on "Areas We Cover"; promote to Primary once proof exists |
| Tertiary | Remaining coverage | Named on "Areas We Cover" page only |

**The removed-city-name test:** take the town name out of the page. Still obviously about that place? If not, it's a doorway page regardless of intent. Aim for roughly 50% genuinely unique, location-specific content per location page (BrightLocal benchmark).

## URL Structure

Service pillars at the root, location hubs at the root, matrix pages location-first:

```
/boiler-repairs/              ← service pillar (one per service, always)
/boiler-servicing/
/dartford/                    ← location hub (Primary tier only)
/dartford/boiler-repairs/     ← matrix page (only with proof for this exact combo)
/areas-we-cover/              ← everything else
```

## Page Hierarchy

### Tier 1: Service Pillar Pages
One dedicated page per service, no exceptions — the single highest-value on-page move. Written from real experience (see E-E-A-T block below).

### Tier 2: Location Hub Pages
Only for Primary-tier towns (3-6). Each carries the local proof elements below.

### Tier 3: Service+Location Matrix (restricted)
Only for combinations where you have jobs, reviews, and photos from that town for that service. Default is NOT to build these; each one must earn its existence.

### Tier 4: Brand/Specialty Sub-pages (Optional)
Only when search volume justifies. Otherwise mention on parent pages.

## Entity Consistency (deliverable)

Produce a single source of truth the whole build must match:

- Exact business name (character for character)
- NAP — identical across site footer, schema, GBP, Bing Places, Apple Maps, directories
- Canonical services terminology — same service names and descriptions on site, GBP services list, schema, and directories

Google cross-checks these sources to validate the entity; inconsistency is a demotion signal.

## GBP Link Rule (Diversity Update)

If a URL ranks in the local pack, Google may suppress it from page-one organic. So: point the GBP website link at a strong service or location page, **not** a homepage that already ranks organically for money terms. Tag it with UTM parameters so GBP traffic is measurable.

## Schema Requirements (per page type)

| Page | Schema |
|------|--------|
| Homepage | LocalBusiness (specific subtype, e.g. Plumber, HVACBusiness) with NAP exactly matching GBP + `sameAs` array (GBP, social profiles, key directory listings) |
| Location pages | LocalBusiness (subtype) with NAP matching GBP |
| Service pages | Service |
| Pages with genuine FAQs | FAQPage |
| Pages legitimately displaying reviews | Review / AggregateRating |

Schema confirms an entity Google already recognises; consistency creates the recognition.

## E-E-A-T Block (required per service and location page)

Post-December 2025 core update, this applies to competitive local queries, not just YMYL:

- A named person with a real credential (e.g. Gas Safe registration number, visible and linked)
- An original photo (real job, van, or premises — never stock; geotagging does nothing, Google strips EXIF)
- A specific testimonial (named town, named job)
- Content written from experience ("what we find when we service back boilers in older [town] properties"), not from a keyword brief

## Internal Linking Rules

```
Homepage
    ↓
┌─────────────────┬─────────────────┐
↓                 ↓                 ↓
Service Pillars ←→ Location Hubs ←→ Service+Location Pages
```

**Service Pillar pages link to:** location-specific versions of that service (where they exist), related services (repairs ↔ servicing).

**Location Hub pages link to:** service+location pages for that area, nearby location hubs.

**Service+Location pages link to:** parent service pillar, parent location hub, same service in nearby locations, related services in same location.

## Content Differentiation

Each location and matrix page must include genuinely unique elements that can't be copied between pages:

| Element | Examples |
|---------|----------|
| Local testimonials | Reviews from customers in that specific town, quoted with context |
| Job photos | Actual work completed in that area (as content and E-E-A-T evidence, not coordinates) |
| Housing stock context | "Victorian terraces common in [town] often have..." |
| Local data | Water hardness, common boiler types, council schemes, flue regulations that bite locally |
| Response times | Real drive time from business base |
| Area-specific FAQs | Natural conversational language ("Do you cover emergency call-outs in [town] on Sundays?") |
| Local landmarks | References to estates, neighbourhoods, high streets |

**Never:** copy content across pages swapping only the town name.

## When to Combine vs Separate Services

Separate pages when:
- Different search intent (repairs = emergency, servicing = planned)
- Different customer mindset (problem vs prevention)
- Sufficient search volume for each term

Combine when:
- Very low search volume for both terms
- Services are genuinely interchangeable to customers

Example: keep "boiler repairs" and "boiler servicing" separate — different intent. Combine "Hive installation" and "Tado installation" into one "smart thermostat installation" page.

## Launch Checklist Additions

- Bing Places claimed and completed (ChatGPT local search runs on Bing's index)
- IndexNow enabled (trivial on Cloudflare — toggle/API ping)
- GBP link pointed at the chosen non-homepage page, UTM tagged
- LCP under 2.5s, INP under 300ms (p75 field data)
- Crawlable text NAP in the footer, not an image

## Output Deliverables

When planning a site, produce:

1. **Sitemap document** — complete URL list organised by tier
2. **Entity consistency sheet** — canonical name, NAP, services terminology
3. **Page count summary** — with the proof justification for each location page
4. **Internal linking matrix** — which pages link to which
5. **Per-page requirements checklist** — differentiation elements, schema, E-E-A-T block

See `references/sitemap-template.md` for output format.
