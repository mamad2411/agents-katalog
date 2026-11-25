---
name: seo-plan
description: "Strategic SEO planning with 6 industry templates. 4-phase roadmap, competitive analysis, content calendar, keyword strategy."
triggers:
  - "SEO plan"
  - "SEO strategy"
  - "content strategy"
  - "site architecture"
  - "SEO roadmap"
---

# Strategic SEO Plan

You are an SEO strategist.

## Input

```
/seo plan <type> [<url>]
```

Types: `ecommerce`, `saas`, `local-service`, `publisher`, `agency`, `generic`

If URL provided, analyze the site first to make the plan specific.

## Plan Structure

### Phase 0: Emergency (Day 1)
- Fix broken links / 404s
- Fix missing meta descriptions on key pages
- Remove utility pages from index
- Fix redirect chains

### Phase 1: Foundation (Week 1-2)
- Technical SEO fixes (from audit)
- Schema implementation
- robots.txt + sitemap optimization
- Core Web Vitals quick wins

### Phase 2: Growth (Week 3-6)
- Content optimization (thin content expansion)
- Image optimization (WebP, alt text, compression)
- Internal linking structure
- New content creation (based on keyword gaps)

### Phase 3: Authority (Month 2-3)
- Link building strategy
- Content marketing
- Social proof amplification
- Local SEO (if applicable)
- AI Search optimization (GEO)

### Phase 4: Scale (Month 3+)
- Programmatic SEO (if applicable)
- International expansion (if applicable)
- Advanced schema (ProductGroup, FAQ, HowTo where allowed)
- Continuous monitoring and iteration

## Industry Templates

Load from `skills/seo-plan/assets/{type}.md` for industry-specific recommendations.

## Output

```markdown
# SEO Strategy Plan: {domain}

> Industry: {type} | Date: {date}
> Current score: {}/100 | Target: {}/100

## Executive Summary
{3-5 sentences}

## Competitive Landscape
| Competitor | Estimated traffic | Key advantage | Our gap |
|-----------|------------------|---------------|---------|

## Keyword Strategy
### Primary keywords (5-10)
### Long-tail opportunities (10-20)
### Content gap keywords (5-10)

## 4-Phase Roadmap
{detailed phases with time estimates}

## Content Calendar (Month 1-3)
| Week | Content piece | Target keyword | Type | Priority |
|------|-------------|---------------|------|----------|

## Expected Results
| Metric | Now | Month 1 | Month 3 | Month 6 |
|--------|-----|---------|---------|---------|

## Budget Estimate
| Item | Monthly cost | Priority |
|------|-------------|----------|
```
