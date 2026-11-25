---
name: ai-seo-optimizer
description: >
  Analyzes any website page (product, service, blog, homepage, landing page, or any other page type) 
  against Google's official AI Optimization Guide and debunked myths (AEO/GEO/chunking/LLMS.txt), 
  as well as broader AI search landscape standards (Perplexity, ChatGPT, Gemini, Copilot).
  
  USE THIS SKILL whenever a user wants to:
  - Audit a page URL or pasted content for AI search visibility
  - Check if a page follows Google's latest AI optimization guidelines
  - Get an SEO/GEO audit report with issues, fixes, action plan, and page score
  - Analyze product pages, service pages, blog posts, homepages, landing pages, or any web page
  - Identify what's a myth vs. what actually matters for generative AI search
  - Get optimized rewrites of page content (when explicitly requested)
  - Bulk-analyze multiple pages in one session
  
  Trigger this skill even when the user says "check my page for AI SEO", "will Google's AI show my page", 
  "audit this URL for GEO", "is my content optimized for AI search", "review my product page for AI visibility",
  or any variation of wanting to know how a page performs for generative AI search features.
  
  Responds in the user's language. Assumes advanced SEO/GEO knowledge — no hand-holding on terminology.
---

# AI SEO Optimizer Skill

Audits web pages against Google's official AI Optimization Guide (May 2025), myth-busts common GEO/AEO 
misconceptions, and evaluates cross-platform AI search visibility (Google AI Overviews, Perplexity, 
ChatGPT Search, Gemini, Copilot).

---

## Input Handling

### Accepting Input
- **URL input**: Use `web_fetch` to retrieve the page content. Extract: title, meta description, H1–H3 
  structure, body text, image alt tags, internal/external links, and any schema markup present.
- **Pasted content**: Analyze the raw text/HTML directly.
- **Bulk input**: Multiple URLs or multiple content blocks — process each one individually, then produce 
  a Bulk Summary table at the end (see Output Format section).
- **Page type detection**: Identify page type automatically (product, service, blog/article, homepage, 
  landing page, other). Adjust audit lens accordingly — see `references/page-type-guidance.md`.

### If URL fetch fails
Inform the user the URL couldn't be fetched and ask them to paste the page content directly.

---

## Analysis Framework

Analyze every page across **three pillars**. Read `references/analysis-framework.md` for full criteria 
and scoring rubrics.

### Pillar 1 — Google AI Optimization Guide Compliance
Based directly on Google's official guide (May 2025). Key areas:
- Content uniqueness & non-commodity status
- First-hand expertise signals (E-E-A-T)
- Content organization (headings, paragraphs, structure)
- Image/video presence and optimization
- Technical crawlability & indexability
- Page experience (CWV, mobile, latency)
- Duplicate content issues
- Local/ecommerce structured data (where applicable)

### Pillar 2 — Myth Audit (What NOT to do)
Flag if the page shows evidence of practices Google has officially debunked:
- LLMS.txt or AI-specific machine-readable files
- Artificial "chunking" of content for AI
- Keyword stuffing / long-tail variation farming
- Inauthentic third-party "mention" seeking
- Over-reliance on structured data as an AI ranking lever
- Rewriting content specifically for AI phrasing patterns
- AEO/GEO as a discipline separate from foundational SEO

### Pillar 3 — Cross-Platform AI Search Visibility
Beyond Google — evaluate for:
- Perplexity (prefers authoritative, citable, structured content with clear sourcing)
- ChatGPT Search / Bing (favors well-linked, authoritative domains; Bing-indexed)
- Gemini (Google ecosystem — aligns with Pillar 1)
- Copilot (Bing-based — similar to ChatGPT Search signals)
- General AI citation likelihood: Is the content extractable? Quotable? Does it have original data/stats?

---

## Scoring System

Score each pillar out of 10. Produce an **Overall AI Visibility Score** out of 100 (weighted):
- Pillar 1 (Google compliance): 50 points
- Pillar 2 (Myth/anti-pattern cleanliness): 20 points  
- Pillar 3 (Cross-platform AI visibility): 30 points

### Score Bands
| Score | Grade | Meaning |
|-------|-------|---------|
| 85–100 | A | Well-optimized for AI search |
| 70–84 | B | Solid foundation, minor gaps |
| 55–69 | C | Moderate issues, prioritize fixes |
| 40–54 | D | Significant gaps, needs rework |
| 0–39 | F | Critical failures, major overhaul needed |

---

## Output Format

### Single Page Audit

```
## AI Visibility Audit — [Page Title / URL]
**Page Type**: [Detected type]
**Language**: [Detected language]

---

### Overall Score: [X/100] — Grade [A/B/C/D/F]

| Pillar | Score | Grade |
|--------|-------|-------|
| Google AI Optimization Compliance | X/50 | |
| Myth/Anti-Pattern Cleanliness | X/20 | |
| Cross-Platform AI Visibility | X/30 | |

---

### Pillar 1: Google AI Optimization Compliance [X/50]

**✅ What's Working**
- [Specific positive finding with brief explanation]

**❌ Issues Found**
For each issue:
- **Issue**: [Clear description]
- **Why it matters**: [Grounded in Google's guide — cite the specific principle]
- **Fix**: [Specific, actionable recommendation]

---

### Pillar 2: Myth Audit [X/20]

**Anti-patterns detected** (if any):
- **[Anti-pattern name]**: [What was found on the page] → [Why this doesn't work per Google]

**Clean** (if none found): No debunked optimization practices detected.

---

### Pillar 3: Cross-Platform AI Visibility [X/30]

**Google AI Overviews**: [assessment]
**Perplexity**: [assessment]  
**ChatGPT Search / Bing**: [assessment]
**Gemini**: [assessment]
**Copilot**: [assessment]

Key gaps for AI citation likelihood:
- [Finding + fix]

---

### Priority Action Plan

**🔴 Critical (Do First)**
1. [Action] — Impact: [which pillar/score]

**🟡 Important (Do Next)**
2. [Action]

**🟢 Nice to Have**
3. [Action]

---

### Rewrite Offer
*If the user hasn't asked for a rewrite yet:*
> Want me to rewrite [specific section — e.g., intro, meta description, H1] to address these issues? 
> Just say which section.
```

### Bulk Analysis Output

After individual audits, append:

```
---
## Bulk Summary

| Page | Type | Score | Grade | Top Priority Issue |
|------|------|-------|-------|--------------------|
| [URL/name] | [type] | [X/100] | [A-F] | [Single most critical fix] |

**Recommended order of fixes across all pages**: [prioritized list]
```

---

## Rewrite Mode

When the user explicitly asks for optimized content (e.g., "rewrite the intro", "give me a better meta 
description", "rewrite this section"):

1. Produce the rewritten version
2. Below it, add a **"Changes Made"** section explaining each edit and which audit issue it addresses
3. Flag any issues that cannot be fixed through content rewriting alone (e.g., technical crawlability)

Do NOT proactively rewrite content unless asked. Only offer it at the end of the audit.

---

## Multilingual Behavior

- Detect the language of the page content
- Respond in the same language the user wrote in
- If user writes in English but page is in another language, respond in English but note the page language
- Apply the same audit framework regardless of language — Google's AI systems apply globally

---

## Page-Type Specific Lenses

Read `references/page-type-guidance.md` for detailed per-type criteria. Summary:

- **Product pages**: Focus on unique product descriptions (non-manufacturer copy), structured data 
  (Product schema), image quality, review signals, Merchant Center alignment
- **Service pages**: Focus on E-E-A-T signals, geographic relevance, first-hand expertise, case studies
- **Blog/articles**: Focus on unique POV, author authority, original research/data, content depth
- **Homepages**: Focus on brand authority signals, clear content hierarchy, crawl efficiency
- **Landing pages**: Focus on content substance (not thin), crawlability, snippet eligibility

---

## Key Principles (Always Apply)

1. **Google confirmed**: AEO and GEO are not new disciplines — they are foundational SEO applied to 
   AI contexts. Never recommend "AI-specific" tactics that contradict this.
2. **Indexability is prerequisite**: A page must be indexed and snippet-eligible before any AI 
   optimization matters. Check this first.
3. **Content substance over AI tricks**: Non-commodity, first-hand, uniquely valuable content 
   outweighs any technical AI optimization tactic.
4. **No hallucinated scores**: Only flag issues you can actually identify from the content provided. 
   Note what cannot be assessed without additional access (e.g., server-side rendering, actual CWV data).

---

## Reference Files

- `references/analysis-framework.md` — Full scoring rubrics and criteria for all three pillars
- `references/page-type-guidance.md` — Per page-type audit lenses and specific checks
- `references/myth-registry.md` — Complete registry of debunked AEO/GEO practices with Google's 
  official position on each
