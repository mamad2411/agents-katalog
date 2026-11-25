---
name: seo-category-pointer
description: "Pointer to a library of 4 specialized Seo skills. Use when working on seo-related tasks."
risk: none
---

# Seo Capability Library 🎯

This is a **pointer skill**. The 4 specialized Seo skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **nextjs-seo-indexing** — Fix SEO indexing issues, crawl budget problems, and Search Console coverage errors for Next.js apps. Covers canonical tags, noindex audits, sitemap health, static rendering, and internal linking.
- **schema-markup-generator** — Generate and implement JSON-LD structured data for web apps, blogs, FAQs, and SaaS sites. Supports WebSite, SoftwareApplication, BlogPosting, FAQPage, HowTo, and more.
- **social-metadata-hardening** — Fix social sharing previews so URLs render as rich cards on Facebook, LinkedIn, X/Twitter, WhatsApp, Telegram, and more. Covers OG tags, Twitter cards, absolute image URLs, and debugging.
- **tools-page-seo-optimizer** — Framework-agnostic SEO workflow for any site with multiple tool, product, or feature pages. Covers duplicate content, unique meta tags, heading hierarchy, internal linking, URL slugs, E-E-A-T, content registry pattern for scaling 50–500 pages, and blog content strategy for position 50–68 keywords.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/seo/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/seo`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
