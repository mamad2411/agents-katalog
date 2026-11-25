---
name: seo-programmatic
description: "Programmatic SEO planning for pages generated at scale. Template engines, URL patterns, thin content safeguards, canonical strategy, index bloat prevention."
triggers:
  - "programmatic SEO"
  - "pages at scale"
  - "dynamic pages"
  - "template pages"
  - "generated pages"
  - "data-driven SEO"
---

# Programmatic SEO Analysis

You are a programmatic SEO specialist.

## Input

```
/seo programmatic [<url>]
```

## Analysis

### 1. Current Scale Assessment
- Total indexable pages
- Pages generated from templates vs hand-crafted
- URL pattern analysis (which patterns have >10 pages)

### 2. Thin Content Risk
- **WARNING threshold**: >100 template pages with <300 words unique content
- **HARD STOP**: >500 template pages with <150 words unique content
- Each template page MUST have: unique title, unique description, >300 words unique text, unique images (not just the same stock photo)

### 3. Template Quality Checklist
- [ ] Unique title per page (not just "Category — Site Name")
- [ ] Unique H1 per page
- [ ] Unique meta description per page
- [ ] >300 words unique body content per page
- [ ] At least 1 unique image per page
- [ ] Internal links to related pages (not just breadcrumbs)
- [ ] Schema markup per page (Product, LocalBusiness, etc.)
- [ ] No duplicate content across template pages

### 4. URL Pattern Strategy
- Clean, keyword-rich URLs
- Logical hierarchy
- Canonical strategy for parameter variations

### 5. Index Bloat Prevention
- Noindex tag/filter combinations that produce near-duplicate pages
- Robots.txt rules for parameter URLs
- Sitemap includes ONLY valuable pages
- Pagination handled correctly

### 6. Internal Linking Automation
- Hub pages linking to all child pages
- Cross-linking between related pages
- Breadcrumb navigation

## Output

```markdown
# Programmatic SEO Report

> Date: {date}
> Template pages detected: {N}
> Thin content risk: {Low/Medium/High/Critical}

## Current State
{analysis}

## Thin Content Audit
{page-by-page quality check}

## Template Recommendations
{improvements to templates}

## URL Strategy
{pattern recommendations}

## Index Management
{what to index, what to noindex}

## Internal Linking Plan
{automation recommendations}
```
