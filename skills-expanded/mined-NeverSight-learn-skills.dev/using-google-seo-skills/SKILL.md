---
name: using-google-seo-skills
description: Discovers and routes Google Search Central–grounded SEO skills. Use when starting a session or deciding which SEO skill applies. Standalone pack — not affiliated with Google.
---

# Using Google SEO Skills

## Overview

Meta-skill for this pack. Pick the right workflow, enforce source-cited SEO work, and refuse spam tactics.

## When to Use

- Starting an SEO session or unclear which skill applies
- After `/seo-brief`, `/seo-audit`, or similar commands

**Not for:** Non-SEO engineering tasks unrelated to search appearance or indexability.

## Official sources

- https://developers.google.com/search/docs

## Process

1. Identify the phase: Discover → Scope → Fix → Verify → Review → Ship.
2. Route using this tree:

```
Task arrives
  ├── Unclear goals / stakeholders?     → seo-interview
  ├── Traffic drop / unknown issues?    → seo-audit-plan
  ├── Crawl / robots / sitemap?         → crawling-and-indexing
  ├── Duplicates / canonical / redirects? → canonicalization
  ├── Title / meta / robots / headings? → page-metadata
  ├── JS rendering / lazy-load?         → javascript-seo
  ├── Mobile / interstitials / UX?      → mobile-and-page-experience
  ├── LCP / INP / CLS?                  → core-web-vitals
  ├── JSON-LD / rich results?           → structured-data
  ├── Helpful content / thin pages?     → on-page-content-quality
  ├── Bylines / trust / authorship?     → eeat-and-trust
  ├── Spam / abuse / manipulative ask?  → spam-and-abuse-prevention
  ├── Images / video appearance?        → images-and-video-seo
  ├── hreflang / locales?               → international-seo
  ├── Product / store SEO?              → ecommerce-seo
  ├── GSC / operators / monitoring?     → search-console-ops
  ├── AI Overviews / gen AI content?    → generative-ai-search
  ├── Writing or rewriting a page?      → seo-content-authoring
  └── Pre-publish / launch?             → seo-fix-and-ship
```

3. Load the skill’s `SKILL.md` and follow Process in order.
4. Apply `references/definition-of-done-seo.md` on every change.
5. This pack is **standalone** (does not depend on other skill packs).
6. Slash commands (`/seo-brief` … `/seo-cwv`) define the **phase**. Follow the command file’s “Load these files” list — do not search randomly for skills.
7. Write plans and evidence under `seo-plan/` (see `seo-plan/README.md`) before large site edits; `/seo-cwv` and `/seo-schema` must plan there first.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know SEO; skip the router." | Routing prevents wrong-skill advice and missed blockers. |
| "Any blog tip is fine if it ranks." | Prefer Search Central; mark unverified claims. |
| "Spam tactics are OK if the client asks." | Refuse and cite spam policies. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Correct skill(s) identified
- [ ] Official sources opened or cited for claims
- [ ] Definition of Done considered
