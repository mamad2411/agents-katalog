---
name: taste-seo
description: Automatically audits and improves SEO for public websites, portfolios, landing pages, blogs and public web apps; title/meta descriptions, semantic HTML, crawl/index controls, structured data, Core Web Vitals, and people-first writing. Use for SEO-related user requests ("SEO optimization", technical SEO, canonical, sitemap, robots, Search Console readiness) even without visual redesign. Preserve existing branding and do not ask for aesthetic style when doing SEO-only tasks; no SEO changes to private dashboards without explicit scope.
license: MIT
metadata:
  version: "0.13.1"
---

# Taste SEO — optional standalone companion

SEO is a **technical/content capability**, never a theme or visual design style. If the main Taste Engine router is also installed, prefer its `references/seo.md` instead of duplicating autonomous instructions.

This skill activates for SEO audits and public-facing web builds. For private dashboards, native mobile apps, or backend-only tasks, skip public SEO. For an ordinary build with unclear visual direction, let the project's style selector resolve the style; do not begin UI design just because SEO can be applied. For explicit styles, keep that style.

Read [SEO integration and rules](references/seo.md) and [framework recipes](references/seo-implementation.md). Run audit with actual rendered/site output where possible. Do not claim ranking/indexing, fabricate schema or fake an audit. Keep public SEO content people-first and anti-slop.

For a website with no known domain, implement accurate titles/headings now, defer absolute canonical and OG URLs until real origin is confirmed. Never use example.com or fake credentials as if real. Maintain private noindex/auth controls.

Return separate **Implemented**, **Verified**, and **Pending** findings. A static validator can identify HTML signals; it cannot certify web visibility, real-world speed, or rankings.
