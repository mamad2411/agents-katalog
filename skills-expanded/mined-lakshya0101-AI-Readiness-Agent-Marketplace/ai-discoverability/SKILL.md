---
name: ai-discoverability
description: Specialized audit skill evaluating technical crawler reachability, robots.txt AI permissions, structured JSON-LD data, entity identity clarity, and brand citation extractability.
---

# AI Discoverability Skill

> **Module**: `ai-discoverability`  
> **Lead**: Aditya (`feature/aditya-discoverability`)  
> **Current Status**: **Fully Implemented (Reach, Read, Extract, Understand, Identify, Trust)**

## Overview

The `ai-discoverability` skill performs an evidence-backed technical audit evaluating whether automated AI systems, search crawlers, and LLM indexing pipelines can reach, parse, extract, understand, and cite web content.

It serves as the first specialized evaluation dimension within the Brand AI Readiness Agent Marketplace, consumed directly by the audit orchestrator.

---

## Public Entrypoint

The canonical programmatic entrypoint is:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("skills/ai-discoverability/scripts")))
from audit_discoverability import audit_discoverability

payload = audit_discoverability(site="https://example.com", options=None)
```

Or via CLI:

```bash
python skills/ai-discoverability/scripts/audit_discoverability.py https://example.com
```

### Input Contract
- `site` (`str`): Target website URL (e.g. `"https://example.com"`).
- `options` (`dict`, optional): Configuration parameters (`timeout`, `user_agent`, `max_pages`, `max_redirects_threshold`).

### Output Envelope Contract
Returns the orchestrator-compatible module payload dictionary:

```json
{
  "skill": "ai-discoverability",
  "status": "success",
  "findings": [ ... ],
  "error": null,
  "limitations": [ ... ]
}
```

On fatal failure (e.g. invalid target domain or unresolvable host):

```json
{
  "skill": "ai-discoverability",
  "status": "failure",
  "findings": [],
  "error": "Failed to connect to target URL https://invalid-target.test: Network error: Name or service not known",
  "limitations": [ ... ]
}
```

---

## Current Status & Capabilities

### Implemented: REACH Stage
1. **Target URL Validation & Normalization**: Missing scheme normalization, fragment stripping, domain structure validation, and clean error payloads for invalid URLs.
2. **HTTP Response & Redirect Inspection**: Tracks full redirect chains, response status codes, content types, and HTTPS enforcement. Conservative: normal redirects produce zero false-positive findings.
3. **Robots.txt Analysis**: RFC 9309 group semantics, multi-agent declarations, Allow/Disallow path specificity, and AI bot permission matrix (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `CCBot`, `Google-Extended`, `Bytespider`, `Applebot-Extended`, `Amazonbot`).
4. **Sitemap Discovery & Validation**: Discovers sitemaps via robots.txt and `/sitemap.xml`, validates XML structure and `<loc>` entries, and catches broken advertised sitemaps.
5. **Internal Link Collection**: Extracts and normalizes same-origin links, categorizes internal vs external links.
6. **Bounded Representative Page Reachability & Broken Page Detection**: Samples up to 5 prioritized representative pages, tests reachability, and detects broken links (404/5xx) with conservative retry/transient error handling.
7. **Crawl Metadata Capture**: Separate deterministic crawl metadata collected for downstream audit stages.

### Implemented: READ Stage
1. **Visible Textual Extraction & Sanitization**:
   - Strips non-textual nodes (`<script>`, `<style>`, `<noscript>`, `<template>`).
   - Ignores elements hidden by CSS (`display:none`, `visibility:hidden`, `hidden` attribute).
   - Normalizes whitespace, collapses multiline sequences, and strips HTML entities.
2. **Deterministic Payload Metrics**:
   - Computes raw `html_bytes`, `visible_text_chars`, and `text_to_html_ratio` percentage.
   - Counts structural elements: headings (`h1`-`h6`), paragraphs (`p`), list items (`li`), links (`a`), script tags (`script`).
3. **Client-Side Rendering (CSR) & SPA Shell Detection**:
   - Identifies frontend framework root mount points (`#root`, `#app`, `#__next`, `[data-reactroot]`, `<app-root>`).
   - Measures container inner content length to distinguish between empty shells and hydrated server-rendered markup.
   - Detects loading placeholders ("Loading...", "Please wait...") and noscript warnings ("Please enable JavaScript to run this app").
4. **Multi-Factor Finding Rules (Zero False Positives)**:
   - **No Penalties for Modern JavaScript**: Script-heavy architectures (Next.js SSR, Nuxt, Remix, hydration bundles) produce zero findings if server-rendered textual copy is present.
   - **Empty SPA Shell Barrier** (`high` severity, `rendering_dependency` subcategory): Triggered only when an empty SPA mount container or noscript/loading indicator is combined with multiple bundle scripts and zero substantive server-rendered headings/content.
   - **Heavily Client-Dependent Payload** (`medium` severity, `rendering_dependency` subcategory): Triggered only when visible text is severely minimal (< 450 chars), ratio is below 1.5%, multiple scripts are present, and no structural headings exist.
5. **Representative Page Sampling**: Audits root page and representative internal pages for read barriers, annotating limitations regarding static HTTP inspection without a headless browser.

### Implemented: EXTRACT Stage
1. **JSON-LD Schema.org Parsing**: Extracts `application/ld+json` blocks, handling single objects, arrays, and `@graph`. Deterministically identifies `@type` declarations (e.g. `Organization`, `WebSite`, `Product`, `Article`). Emits findings for malformed JSON without crashing.
2. **Meaningful Schema Gaps**: Conservatively identifies pages acting as products or articles (via URL, semantic tags, and textual cues) but lacking the corresponding structured representation.
3. **OpenGraph & Social Metadata**: Extracts `og:*` and `twitter:*` meta tags. Identifies conflicting URL signals (e.g., canonical vs `og:url`).
4. **Semantic Landmarks**: Analyzes usage of HTML5 landmarks (`<main>`, `<article>`, `<header>`, `<footer>`, `<nav>`) and equivalent `role=""` attributes. Flags documents lacking a discernible primary content region.
5. **Structured Observations**: Compiles an `extract_metadata` payload for downstream stages without storing redundant raw HTML or JSON blobs.


### Implemented: UNDERSTAND Stage
1. **Heading Analysis**: Evaluates heading sequence (`H1`-`H6`) for structural gaps, missing primary headers, empty tags, and aggressively repetitive generic labels.
2. **Subject Consistency**: Cross-references `<title>`, primary `<h1>`, and `og:title` to ensure the core topic is unambiguous to machines. Safely ignores harmless capitalization or punctuation differences.
3. **Contextual Sufficiency**: Detects when an important subject is introduced (via schema or H1) but the page provides insufficient substantive text to explain it to an AI.
4. **False Positive Defenses**: Safely handles modern multiple-H1 structures, concise landing pages, and common navigation headers without spamming errors.


### Implemented: IDENTIFY Stage
1. **Entity Name Consistency**: Extracts Organization, WebSite, and Product identity strings and compares them against H1 and Title tags to detect strong contradictions.
2. **Canonical URL Logic**: Detects cross-domain canonical URLs and mismatches between the JSON-LD declared URLs and the actual site origin.
3. **sameAs Quality Control**: Scans `sameAs` linkages to flag improperly formatted non-URL text while forgiving missing entries.
4. **False Positive Defenses**: Safely normalizes URLs (www, trailing slashes) and Brand names (Inc, LLC, capitalization) to prevent spammy alerts over trivial differences.


### Implemented: TRUST Stage
1. **Commercial & Transparency**: Strictly classifies commercial intent (`Product`, `Service`, `Offer`, or keywords) to evaluate privacy/legal links. Explicitly forgives `Organization`-only informational sites.
2. **Security / HTTP Deduplication**: Confirms HTTPS presence, recording security headers (HSTS, CSP, etc.) purely as observations, and seamlessly integrating with the Reach stage to prevent duplicate HTTPS findings.
3. **Attribution Analysis**: Demands clear Authorship/Publisher identity *only* for explicitly identified News/Article pages (using schema or robust tags).
4. **Date Consistency & Freshness**: Cross-references `datePublished` and `dateModified`. Emits staleness warnings only when age strictly conflicts with intended timeliness (protecting historical archives).
5. **Internal Corroboration**: Contrasts factual claims across multiple internal pages to detect consistency breakdowns, intelligently forgiving legitimate sub-brand variations.
*Note: Performs INTERNAL DETERMINISTIC CORROBORATION ONLY. Deliberately excludes external web research.*

---

## Core Operational Invariants

- **Read-Only**: Passive HTTP GET analysis only; zero state mutations or form submissions.
- **Zero Hallucination**: No speculative or empty findings; every finding requires concrete observable proof.
- **Polite Crawling**: Respects timeouts, bounds representative crawl depth (default: 5 pages), and caches duplicate requests.
