---
name: SEO
description: Optimize HTML meta tags, headers, and content for search engine rankings.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---

# SEO Optimization Rules

## Title Tag
- Keep between 50–60 characters (including spaces and punctuation)
- Place primary keyword within first 30 characters
- Never repeat a keyword in the same title

## Meta Description
- Limit to 150–160 characters or Google truncates it
- Write benefit-focused copy, not feature lists
- End with call-to-action when appropriate

## Header Structure
- Only one H1 per page — H1 contains primary keyword but differs from title
- Follow strict hierarchy: H1 → H2 → H3 (never skip levels)
- Use keyword variations in H2s instead of repeating exact match

## Keyword Placement
- Primary keyword must appear in: title, H1, first 100 words
- Keep keyword density under 3%
- Secondary keywords go in H2 and H3 tags

## Image Optimization
- Alt text on all content images with relevant keywords when natural
- File names use hyphens: `email-tools-comparison.jpg`
- Compress images under 100KB — larger files hurt page speed

## Technical Checks
- Include viewport meta tag for mobile: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Use canonical URLs to prevent duplicate content
- Validate structured data at schema.org/validator before publishing
- Internal links use descriptive anchor text, never "click here"

## Schema Markup
- Article schema for blog posts (include author + datePublished)
- LocalBusiness schema for location-based pages
- Validate JSON-LD before deployment

## Mistakes That Trigger Penalties
- Never hide text with CSS for SEO purposes
- Never use same title tag across multiple pages
- Don't stuff keywords in alt text unnaturally
- Don't use H1 for navigation or logo text
