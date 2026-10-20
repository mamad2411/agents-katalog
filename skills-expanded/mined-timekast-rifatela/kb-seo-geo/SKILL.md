---
name: kb-seo-geo
description: Portable reference for search visibility across traditional search (SEO/Google) and AI engines (GEO — ChatGPT, Perplexity, Claude, Gemini) — not grounded in this repo. Invoke on content-heavy or marketing-critical projects when optimizing for citability, auditing E-E-A-T, picking schema markup, or deciding AI crawler allow/block. For page perf → `kb-performance`.
last-verified: 2026-04-23
---

# SEO & GEO — Search + AI Engine Visibility

> **Scope:** unified reference for traditional search (Google) and Generative Engine Optimization (GEO — AI answers).
> **Not grounded in this repo.** TimeKast Factory starter is not marketing-focused — this skill activates in content-heavy projects.

---

## Part A — SEO Fundamentals

### 1. E-E-A-T framework

| Principle             | Signals                                   |
| --------------------- | ----------------------------------------- |
| **Experience**        | First-hand knowledge, real examples       |
| **Expertise**         | Credentials, depth of knowledge           |
| **Authoritativeness** | Backlinks, mentions, industry recognition |
| **Trustworthiness**   | HTTPS, transparency, accurate info        |

### 2. Core Web Vitals

| Metric  | Target  | Measures            |
| ------- | ------- | ------------------- |
| **LCP** | < 2.5s  | Loading performance |
| **INP** | < 200ms | Interactivity       |
| **CLS** | < 0.1   | Visual stability    |

### 3. Technical SEO — non-negotiable

| Element        | Purpose            |
| -------------- | ------------------ |
| XML sitemap    | Help crawling      |
| robots.txt     | Control access     |
| Canonical tags | Prevent duplicates |
| HTTPS          | Security signal    |

### 4. Page elements — best practice

| Element          | Best practice              |
| ---------------- | -------------------------- |
| Title tag        | 50-60 chars, keyword front |
| Meta description | 150-160 chars, compelling  |
| H1               | One per page, main keyword |
| H2–H6            | Logical hierarchy          |
| Alt text         | Descriptive, not stuffed   |

### 5. Schema markup (JSON-LD)

| Type           | Use              |
| -------------- | ---------------- |
| Article        | Blog posts, news |
| Organization   | Company info     |
| FAQPage        | Q&A content      |
| Product        | E-commerce       |
| BreadcrumbList | Navigation       |

### 6. Ranking priorities (stack-rank your effort)

| Priority | Factor                            |
| -------- | --------------------------------- |
| 1        | Quality, relevant content         |
| 2        | Backlinks from authority sites    |
| 3        | Page experience (Core Web Vitals) |
| 4        | Mobile optimization               |
| 5        | Technical SEO fundamentals        |

> **Rule:** don't chase #5 if #1 is broken. Content quality is the floor — everything else is multiplier.

---

## Part B — GEO (Generative Engine Optimization)

### 7. SEO vs GEO — what's the difference?

| Aspect   | SEO           | GEO            |
| -------- | ------------- | -------------- |
| Goal     | #1 ranking    | AI citations   |
| Platform | Google        | AI engines     |
| Metrics  | Rankings, CTR | Citation rate  |
| Focus    | Keywords      | Entities, data |

### 8. AI engine landscape

| Engine         | Citation style   | Opportunity           |
| -------------- | ---------------- | --------------------- |
| **Perplexity** | Numbered [1][2]  | Highest citation rate |
| **ChatGPT**    | Inline/footnotes | Custom GPTs           |
| **Claude**     | Contextual       | Long-form content     |
| **Gemini**     | Sources section  | SEO crossover         |

### 9. RAG retrieval factors (approximate weights)

| Factor             | Weight |
| ------------------ | ------ |
| Semantic relevance | ~40%   |
| Keyword match      | ~20%   |
| Authority signals  | ~15%   |
| Freshness          | ~10%   |
| Source diversity   | ~15%   |

### 10. Content that gets cited

| Element                 | Why it works         |
| ----------------------- | -------------------- |
| **Original statistics** | Unique, citable data |
| **Expert quotes**       | Authority transfer   |
| **Clear definitions**   | Easy to extract      |
| **Step-by-step guides** | Actionable value     |
| **Comparison tables**   | Structured info      |
| **FAQ sections**        | Direct answers       |

### 11. GEO checklist

**Content elements:**

- [ ] Question-based titles
- [ ] Summary / TL;DR at top
- [ ] Original data with sources
- [ ] Expert quotes (name + title)
- [ ] FAQ section (3-5 Q&A)
- [ ] Clear definitions
- [ ] "Last updated" timestamp
- [ ] Author with credentials

**Technical elements:**

- [ ] Article schema with dates
- [ ] Person schema for author
- [ ] FAQPage schema
- [ ] Fast loading (< 2.5s)
- [ ] Clean HTML structure

### 12. Entity building

| Action                     | Purpose              |
| -------------------------- | -------------------- |
| Google Knowledge Panel     | Entity recognition   |
| Wikipedia (if notable)     | Authority source     |
| Consistent info across web | Entity consolidation |
| Industry mentions          | Authority signals    |

### 13. AI crawler access — decide your policy

| Crawler       | Engine           |
| ------------- | ---------------- |
| GPTBot        | ChatGPT / OpenAI |
| Claude-Web    | Claude           |
| PerplexityBot | Perplexity       |
| Googlebot     | Gemini (shared)  |

| Strategy     | When                       |
| ------------ | -------------------------- |
| Allow all    | Want AI citations          |
| Block GPTBot | Don't want OpenAI training |
| Selective    | Allow some, block others   |

> **Rule:** blocking AI crawlers reduces citation surface. Only block if legal/IP constraints demand it.

---

## 14. Anti-patterns

| ❌ Don't                  | ✅ Do                                    |
| ------------------------- | ---------------------------------------- |
| Publish without dates     | Add timestamps                           |
| Vague attributions        | Name sources                             |
| Skip author info          | Show credentials                         |
| Thin content              | Comprehensive coverage                   |
| Keyword stuff             | Write for humans first                   |
| Ignore Core Web Vitals    | Performance is a ranking factor          |
| Block AI crawlers blindly | Explicit allow/block decision per engine |

---

> **Remember:** SEO gets you found. GEO gets you cited. Both require quality content + technical excellence.

---

_Cross-reference: `kb-performance` for Core Web Vitals tuning._
