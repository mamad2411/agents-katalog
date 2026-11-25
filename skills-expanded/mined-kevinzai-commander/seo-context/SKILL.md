---
name: seo-context
description: "Captures domain SEO state — current rankings, competitors, tools, goals"
---

# SEO Context Capture

Run this at the start of any SEO engagement. It creates a `seo-context.md` file that all other SEO skills reference.

## Gather This Information

Ask the user or detect from the project:

### Domain & Brand
- Domain URL (primary + any subdomains)
- Brand name
- Industry / niche
- Target geographic markets

### Current SEO State
- Current monthly organic traffic (approximate)
- Top 5 ranking keywords
- Known SEO issues or penalties
- Previous SEO work done
- Google Search Console connected? (Y/N)
- Analytics platform (GA4 / Plausible / PostHog / other)

### Competitors
- Top 3 direct competitors (URLs)
- Top 3 content competitors (who ranks for your target keywords?)
- Competitor advantages to address

### Goals
- Primary SEO goal (traffic / leads / sales / brand awareness)
- Target keywords or topics (top 5-10)
- Timeline expectations (3 months / 6 months / 12 months)
- Budget/resource constraints

### Technical Stack
- CMS / framework (Next.js, WordPress, Astro, etc.)
- Hosting provider
- CDN in use?
- Current page speed score (if known)

## Output

Generate `seo-context.md` in the project root with all gathered information, structured for easy reference by other SEO skills.
