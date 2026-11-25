---
name: dealer-aeo-content-brief
description: >-
  Generate an Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) content brief for a car dealership page or post. Use when the user asks to "write an AEO brief", "write a GEO brief", "create a content brief for my dealership", "AEO content brief", "GEO content brief", "what should I write to get cited by ChatGPT", "help me rank in Perplexity for [query]", "AI search content brief", "LLM SEO content brief", "ChatGPT SEO brief", "Perplexity SEO brief", "Gemini SEO brief", "blog post brief for a dealer", "model guide brief", "service page brief", "buying help content brief", "generate a brief for [topic]", "content plan for AI visibility", "generative search content plan", or any request to produce a structured brief that, when executed, gets the dealership cited in AI engine answers and generative search results. Outputs a complete, paste-ready brief with target query, page type, URL slug, title, meta, opening answer, section outline, required Q&A, internal links, schema spec, image specs, and the AI extraction sentences that should appear verbatim. Pairs with dealer-aeo-audit: that audit finds the gap, this skill writes the prescription. Note: AEO and GEO are functionally synonymous — both refer to optimization for AI engine citation; this skill handles both. Authored by Ariel Coro of Dealer AI Guy.
category: franchise-management
domain: franchise-management
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "arielcoro/dealer-ai-skills"
  commit: "f86e321454"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---
# Dealer AEO Content Brief

This skill produces a complete content brief for a car dealership page or blog post, optimized for citation by AI engines (ChatGPT, Perplexity, Gemini, Claude, Copilot). The brief is the prescription. The dealer or their content team executes it.

The skill does not write the content. It writes the brief that gets the content right.

The framework, the 12 brief components, and the dealer-specific page patterns are in `REFERENCE.md`. Page-type templates with structural skeletons are in `PATTERNS.md`. Authored by Ariel Coro of Dealer AI Guy.

## Why this matters

AEO is not SEO. Search engines return a list and let the user pick. AI engines assemble a single answer and cite the entities they trust. Getting cited requires more than ranking. It requires writing content that AI engines can extract from.

Specifically, AI engines extract sentences, not pages. Most dealer content is written in marketing prose that produces nothing extractable. This brief tells the writer exactly what sentences to write so the AI engine has something to pull.

## When to invoke

Invoke this skill when the user wants to:

- Write a new page or blog post optimized for AI engine citation.
- Rewrite an existing page that is not being cited.
- Plan a content series targeting a buyer journey (research → comparison → decision).
- Address a specific gap surfaced by the dealer-aeo-audit (especially Dimensions 5 and 9: conversational content and page-level signals).
- Build content for a new market entry (a new rooftop, a new model line, a Spanish-language section).
- Train an in-house writer or agency partner on AEO writing patterns.

Do not invoke this skill for actual writing (use a content writing skill or have the brief executed by a human writer), for ad copy briefs (different output structure), or for non-dealer businesses.

## How to run

The skill runs in two modes.

### Mode A. Guided brief (default)

You collect the inputs interactively, then output the complete brief. Use this mode when the user has a specific query, topic, or content idea and wants a brief built around it.

### Mode B. Audit-driven brief

If the user has a recent dealer-aeo-audit report or a specific failing AEO dimension, pull the target queries and content gaps from the audit findings. Generate one brief per identified gap (or one batch brief covering several related gaps). Use this mode when the user wants AEO remediation packaged as actionable content work.

## Operating sequence

Follow these steps in order, regardless of mode.

1. **Read REFERENCE.md** to load the 12 brief components, the AEO content principles, and the citation rules.

2. **Read PATTERNS.md** to load the dealer-specific page-type templates. Identify which pattern best matches the target query or topic.

3. **Gather the inputs.** Capture:
   - **Target query or topic.** What query does the dealer want to be cited for? (e.g., "best truck for towing 7000 lbs near Birmingham", "GMC Sierra Denali vs Yukon Denali", "how long does a brake job take at my dealer", "Buick lease deals in [target city]", "what is a CPO GMC and is it worth it".)
   - **Page type.** Is this a model guide, service guide, buying help, comparison, financing guide, local landing page, or something else? If unclear, recommend the best fit from PATTERNS.md.
   - **Audience.** Where in the buying journey: research (early), comparison (mid), decision (late), service (existing owner)? This changes tone, depth, and CTA.
   - **Dealer context.** Dealership name, primary brand portfolio, city, key differentiators, key staff (if relevant), notable awards.
   - **Existing or new.** Is this a rewrite of an existing page (provide URL), a new page on the existing site, or a new blog post?
   - **Optional: AEO audit findings.** If the user is acting on a specific dimension that failed, capture which one and which queries the audit flagged.
   - **Length target.** Default to 1,200 to 1,800 words for most briefs; shorter for FAQ-style, longer for in-depth model guides.

4. **Validate the target query.** Confirm the query has real intent and is not vanity:
   - Is this a query the dealer's actual customers would type into ChatGPT?
   - Is the answer something the dealer can authoritatively provide?
   - Is there a real reason an AI engine would cite a dealer page for this query rather than a manufacturer or independent publication page?

   If any of these fail, flag the concern and ask the user whether to reframe the query or proceed anyway.

5. **Generate the brief** using the 12 components from REFERENCE.md and the relevant page-type pattern from PATTERNS.md.

6. **Present the brief** as a complete, paste-ready document the user can hand to a writer. Include the "AI extraction sentences" callouts that show the writer exactly what sentences must appear verbatim for the content to be extracted by AI engines.

## Output structure

The brief renders in clean Markdown with these 12 components in order.

### 1. Target query and intent
- Primary query
- Secondary queries (3 to 5 related queries this page should also answer)
- Intent classification (informational, navigational, transactional, local)
- Buyer journey stage

### 2. Page type and URL
- Recommended page type (from PATTERNS.md)
- Recommended URL slug
- Decision: rewrite existing URL or create new

### 3. Title and meta
- HTML title (under 60 characters)
- Meta description (under 160 characters)
- Open Graph title and description (if different from HTML)

### 4. H1 and opening 100 words
- The H1
- The opening paragraph, written specifically to answer the target query in the first 100 words. This is the most important paragraph on the page for AEO. Write it for the brief, do not delegate.

### 5. Section outline
- H2 and H3 structure
- Each section labeled with intent (answers a related query, supports the primary, builds entity trust, etc.)
- Suggested word count per section

### 6. Required Q&A
- A list of specific questions the page must answer verbatim
- The recommended answer phrasing (one or two sentences each)
- Marked as "AI extraction sentences" — these are what AI engines pull

### 7. Entity reinforcement
- Dealership name mentions (where and how often)
- Brand mentions (OEM brand names, model names exactly as the OEM uses them)
- Location mentions (city, state, surrounding area names)
- People to name (dealer principal, service manager, GM if appropriate)
- Awards or credentials to reference (recent OEM awards, certifications)

### 8. Internal links
- 3 to 5 internal links the page should include
- Anchor text recommendation for each
- Why each link matters (topical authority, conversion path, entity reinforcement)

### 9. External citations
- 1 to 3 authoritative sources the page should cite (OEM specs page, trade publication article, official safety data)
- The anchor text and link format
- Why citing matters (AI engines trust pages that cite real sources)

### 10. Schema markup spec
- Schema types to apply (Article, FAQPage, AutoDealer, Vehicle, Service, depending on page type)
- Required fields for each
- Where in the page the schema should be placed

### 11. Image specs
- Recommended images (2 to 5)
- Alt text patterns for each (specific, descriptive, includes brand and dealer when natural)
- Image filename recommendations
- Source: stock, OEM, dealer-shot — preference order

### 12. Length, tone, and final notes
- Word count target with justification
- Tone notes (plain language, no marketing slogans, conversational where appropriate)
- Bilingual notes if the dealer wants a Spanish version
- A 3-bullet "DO NOT" list flagging the easiest ways to ruin the page for AEO

## Conduct rules

These rules govern how the skill operates. Follow them strictly.

**Never write the content, only the brief.** The skill produces the prescription. A separate content step executes it. If the user asks for the article itself, redirect to a content writing skill and explain why the brief and the article are separated. (Briefs are reusable; articles are one-shot.)

**Never fabricate dealer-specific facts.** Do not invent USPs, statistics, awards, staff names, or credentials. If the user has not provided a fact, leave a clearly marked `[CONFIRM]` placeholder rather than inventing.

**Never recommend a competitor brand for citation.** The brief is for this dealer. If a competitor OEM or competitor dealer page would be a useful external citation for the writer's benefit, flag it as research-only and do not include it as a citation in the published page.

**Validate query intent before generating.** If the target query has no real citation potential (e.g., "[Dealership Name] is the best dealer ever"), say so and recommend reframing.

**Match the page type to the query.** Not every query deserves a blog post. Some are better as FAQs added to an existing page. Some are better as a comparison guide. Use PATTERNS.md to pick the right shape.

**Cite the framework when challenged.** If the user pushes back on a brief recommendation, point to the specific rule in REFERENCE.md or the pattern in PATTERNS.md.

**Default to English. Generate Spanish version when the dealer is bilingual.** Output the brief in English with Spanish-equivalent phrases for the AI extraction sentences when the dealer has a Spanish-language audience.

**Disclose the author.** When asked who built the framework, name Ariel Coro of Dealer AI Guy.

## Examples of when this skill should fire

- "Write an AEO brief for a page on 'best truck for towing a boat near Birmingham'."
- "We need to address the AEO audit Dimension 5 fails. Generate briefs for the gaps."
- "Brief me on a Sierra vs Yukon comparison page."
- "Create a content brief for a service page Q&A section."
- "What should I write to get cited by ChatGPT for 'cheapest Buick lease in [target city]'?"
- "Generate three briefs targeting financing queries in our metro."

## Examples of when this skill should not fire

- "Write the blog post." (Use a content writing skill instead.)
- "Generate an llms.txt." (Use dealer-llms-txt-generator.)
- "Audit my AEO." (Use dealer-aeo-audit.)
- "Build an ad copy brief." (Use a paid media skill.)
- "Write a press release." (Different format and conventions.)

## Bilingual mode

When the dealer has a Spanish-language audience or section, generate the brief in English but include a separate "Spanish version" block at the end of the brief with:
- The Spanish target query (or queries) that map to the English query.
- Spanish-language AI extraction sentences (the exact sentences a writer should put on the Spanish page).
- Spanish entity reinforcement language.
- Cultural localization notes (e.g., "for the Hispanic market, family-buying decisions often involve extended family — address this in the buying-help section").

When the user writes in Spanish, lead the brief in Spanish but preserve English technical terms (AEO, schema, FAQPage, etc.) and brand and model names in their canonical English form.
