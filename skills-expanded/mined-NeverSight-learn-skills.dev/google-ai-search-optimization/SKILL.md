---
name: google-ai-search-optimization
description: Official Google Search guidance for optimizing websites for generative AI features such as AI Overviews and AI Mode. Use when an AI agent needs to explain, audit, plan, or implement SEO work for Google AI Search visibility; evaluate AEO/GEO claims; advise on llms.txt, structured data, content quality, crawlability, JavaScript SEO, media SEO, ecommerce/local details, Merchant Center, Business Profile, or agent-friendly site readiness.
---

# Google AI Search Optimization

## Overview

Use this skill to turn Google's public guidance on generative AI features in Search into practical recommendations, audits, content plans, and implementation tasks.

Anchor every recommendation in this model: Google AI Overviews and AI Mode are extensions of Google Search. They rely on Google's Search index, ranking, quality, crawling, and serving systems, with AI techniques such as retrieval-augmented generation and query fan-out layered on top.

Treat AEO and GEO as industry labels for search optimization work, not as separate Google systems. For Google Search, optimizing for generative AI search means optimizing for the overall Search experience.

## Source Handling

If the user asks for the latest guidance, current policy, exact wording, or source citations, verify against the official sources before answering. Start with `references/google-ai-search-principles.md` for the source map and browse only official Google, Google Search Central, Google Help, Merchant Center, web.dev, or directly linked protocol pages unless the user asks for broader research.

Do not present this skill as a replacement for the live docs. Google Search guidance changes.

## Workflow

1. Classify the request:
   - Explain: summarize how Google's generative AI Search features work.
   - Audit: evaluate a site, page, content plan, or SEO recommendation.
   - Plan: create a roadmap, content brief, technical backlog, or prioritized checklist.
   - Implement: modify site code, metadata, structured data, media markup, crawl controls, or content.
   - Myth-check: evaluate AEO/GEO claims, llms.txt, schema claims, AI rewriting, mentions, or chunking advice.

2. Gather only the needed context:
   - For a site audit, inspect crawlability, rendered content, titles, headings, internal links, canonicalization, robots/noindex, sitemaps, page experience, media, structured data, and Search Console constraints if available.
   - For a content task, identify audience, purpose, firsthand expertise, unique value, trust signals, media opportunities, and whether the content would satisfy the visitor without another search.
   - For ecommerce or local tasks, inspect Merchant Center/product data, Product structured data, Business Profile/business details, support details, shipping/returns, reviews, and inventory or offer freshness where relevant.
   - For JavaScript sites, check whether important text, links, media, and structured data appear in rendered HTML and each meaningful screen has a URL.

3. Apply the core recommendations:
   - Build crawlable, indexable, snippet-eligible pages that return successful HTTP status codes.
   - Create non-commodity, helpful, reliable, people-first content with unique experience or expertise.
   - Organize content for humans with descriptive titles, headings, links, URLs, and page structure.
   - Use semantic HTML where practical for readability, accessibility, and navigation; do not overstate perfect HTML validity as a requirement.
   - Add high-quality images and videos when they genuinely help the user, and optimize those assets for discovery.
   - Use structured data for eligible rich results and clearer content meaning, but not as a special AI ranking hack.
   - Keep product, business, local, and support information accurate in Google-facing systems.
   - Improve page experience across mobile, security, speed, layout stability, intrusive elements, and main-content clarity.
   - Monitor with Search Console and test with URL Inspection, Rich Results Test, and PageSpeed Insights when relevant.

4. Explicitly reject unsupported shortcuts:
   - Do not recommend `llms.txt` or special AI text files as required for Google AI Search visibility.
   - Do not require content "chunking" into tiny pages or fragments for AI systems.
   - Do not rewrite pages only to target AI systems, long-tail query variants, or query fan-out guesses.
   - Do not create many near-duplicate pages for every possible fan-out query.
   - Do not seek fake mentions, manufactured citations, or reputation signals.
   - Do not overfocus on schema.org markup as if there were AI-specific schema.
   - Do not claim that meeting requirements guarantees crawling, indexing, ranking, or inclusion in AI features.
   - Do not imply every page needs overt SEO work to succeed; prioritize the changes that improve user value, discovery, indexing, and understanding.

5. Produce output that is useful in the user's context:
   - For audits, lead with prioritized findings, then fixes, rationale, and validation steps.
   - For strategy, split work into content, technical, media, ecommerce/local, and measurement tracks.
   - For content briefs, require original expertise, evidence, audience value, media support, and trust signals.
   - For code changes, make narrow edits that improve crawlability, metadata, structured data, accessibility, or page experience, then validate.

## References

Read `references/google-ai-search-principles.md` when you need the underlying model, source map, recommendations, or myth-busting detail.

Read `references/audit-playbook.md` when performing a site/page audit, building an implementation roadmap, or creating a repeatable checklist.
