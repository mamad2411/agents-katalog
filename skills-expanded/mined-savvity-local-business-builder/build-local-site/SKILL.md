---
name: build-local-site
description: Build a complete SEO-optimized local business website (80-100+ pages) using Astro 5, Tailwind CSS v4, and Cloudflare Pages. Generates programmatic service/area combination pages, blog infrastructure, schema markup, and internal linking for maximum local search visibility.
triggers:
  - build a local business website
  - create a website for my business
  - build a plumber website
  - build an HVAC website
  - build a dentist website
  - build an electrician website
  - build a roofing website
  - build a cleaning website
  - build a landscaping website
  - build a pest control website
  - improve this local business site
  - programmatic SEO site
  - build a website for my
  - local business site builder
  - service area pages
  - create service pages for
---

# Local Business Website Builder

This skill builds complete, SEO-optimized websites for local service businesses. The output is a production-ready Astro 5 static site with 80-100+ pages, designed to rank in Google for "[service] in [area]" searches.

## What It Builds

- Homepage with hero, service grid, area map, reviews, and structured data
- Individual service pages (one per service offered)
- Individual area pages (one per city/town served)
- Combination pages for every service + area pair (the bulk of pages)
- Blog infrastructure with markdown content collections
- Contact page with form and business hours
- About page with owner bio and credentials
- XML sitemap, robots.txt, and canonical URLs
- JSON-LD schema markup on every page (LocalBusiness, Service, FAQPage, BreadcrumbList)
- Full internal linking mesh between all service, area, and combination pages

## What You Need to Provide

**Required:**
- Business name
- Owner name
- Industry/business type (plumber, HVAC, dentist, electrician, etc.)
- Phone number
- Services offered (5-10 recommended)
- Service areas/cities (8-15 recommended)
- Business address (city, state, zip)
- Year established
- License or certification number

**Optional (but recommended):**
- Business website URL (for canonical URLs and schema)
- Email address
- Business hours
- Price ranges per service
- Customer reviews (real ones only, never fabricated)
- Google Analytics ID (GA4)
- Gemini API key (for AI-generated service images)
- Cloudflare account (for free deployment)

## Quick Start

Just tell the agent about your business:

> "Build a website for my plumbing business, Texas Plumbing Solutions, in Brenham TX. We serve Washington County and surrounding areas. Our services include leak repair, water heater service, drain cleaning, repiping, and sewer line repair."

The agent will guide you through an interactive process to collect all necessary details, then generate the complete site.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Astro 5 | Static site generator with file-based routing |
| Tailwind CSS v4 | CSS-native config via @theme, @utility, @layer |
| Cloudflare Pages | Free hosting with global CDN |
| astro-icon + Lucide | Optimized SVG icons |
| @astrojs/sitemap | Auto-generated XML sitemap |

## Page Count Formula

Total pages = (services x areas) + services + areas + 5 static pages + blog posts

Example: 8 services x 10 areas = 80 combo pages + 8 service + 10 area + 5 static = **103 pages** before blog content.

## Full Reference

For the complete technical guide covering architecture, SEO rules, schema markup, Tailwind v4 patterns, data file structure, internal linking strategy, and design system details, see:

`references/local-business-guide.md`

The agent should read that reference before beginning any site build.
