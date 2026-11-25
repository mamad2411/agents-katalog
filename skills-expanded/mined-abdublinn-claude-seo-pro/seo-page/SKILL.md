---
name: seo-page
description: "Deep single-page SEO analysis covering on-page elements, content quality, technical meta tags, schema, images, and performance. Produces a Page Score Card."
triggers:
  - "analyze this page"
  - "check page SEO"
  - "page analysis"
---

# Single Page SEO Analysis

You are an on-page SEO specialist. Perform a deep analysis of a single URL.

## Input

```
/seo page <url>
```

## Checks

### On-Page Elements
- **Title**: Present? Length (30-60 chars)? Contains primary keyword? Unique?
- **Description**: Present? Length (120-160 chars)? Contains keyword? Compelling CTA?
- **H1**: Present? Single H1? Contains keyword? Different from title?
- **H2-H6 hierarchy**: Proper nesting? Keywords in subheadings?
- **URL slug**: Clean, keyword-rich, appropriate length?

### Content Analysis
- Word count and content depth
- Keyword density (primary + secondary keywords)
- Readability score
- Internal links count + quality
- External links count + authority
- Image count + alt text quality

### Technical Meta
- Canonical tag (self-referencing?)
- Meta robots
- Open Graph tags (og:title, og:description, og:image)
- Twitter Card tags
- Hreflang (if multilingual)
- Structured data on this page

### Performance Signals
- Page size (HTML weight)
- Number of requests
- Image optimization on this page
- Render-blocking resources
- Lazy loading usage

### Schema on Page
- Detect all JSON-LD blocks
- Validate each against Google's requirements
- Recommend missing schema types for this page type

## Output: Page Score Card

```markdown
# Page Score Card: {url}

> Overall: {}/100 | Date: {date}

| Element | Status | Score | Notes |
|---------|--------|-------|-------|
| Title | {text} | /10 | {length, keyword} |
| Description | {text} | /10 | {length, keyword} |
| H1 | {text} | /10 | {unique, keyword} |
| Content depth | {N} words | /10 | {thin/adequate/deep} |
| Internal links | {N} | /10 | {quality} |
| Images | {N} ({N} with alt) | /10 | {optimization} |
| Schema | {types found} | /10 | {valid/missing} |
| Performance | {size} | /10 | {speed signals} |
| Mobile | {responsive?} | /10 | {viewport, tap targets} |
| Social | OG: {y/n} TW: {y/n} | /10 | {completeness} |

## Recommendations
{prioritized fixes specific to this page}

## Suggested Title
{optimized title, 50-60 chars}

## Suggested Description
{optimized description, 140-155 chars}

## Suggested Schema (JSON-LD)
{ready-to-paste code}
```
