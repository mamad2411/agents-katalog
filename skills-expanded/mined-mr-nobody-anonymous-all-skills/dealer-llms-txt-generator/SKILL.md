---
name: dealer-llms-txt-generator
description: >-
  Generate a curated llms.txt file for a car dealership website to improve AEO (Answer Engine Optimization), GEO (Generative Engine Optimization), and AI search visibility. Use when the user asks to "generate llms.txt", "create an llms.txt for a dealer", "make an llms.txt", "write llms.txt for my dealership", "build llms.txt", "fix my llms.txt", "audit my llms.txt", "dealer llms.txt", "llms.txt for car dealer", "AEO infrastructure", "GEO infrastructure", "AI search file", "ChatGPT crawler map", "LLM SEO file", or any request to produce or improve the llms.txt file at the root of a car dealer site. Also activates when discussing how AI engines crawl dealer websites, what llms.txt is for, generative engine optimization for car dealers, or how to make a dealership AI-readable for ChatGPT, Perplexity, Gemini, Claude, and Copilot. Pairs naturally with the dealer-aeo-audit skill: that audit finds the gap, this skill closes it. Authored by Ariel Coro of Dealer AI Guy.
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
# Dealer llms.txt Generator

This skill produces a curated llms.txt file for a franchise or independent car dealership website. The output is a complete, paste-ready text file that the user can place at the root of their domain (e.g., `https://[domain]/llms.txt`).

The llms.txt convention is documented at llmstxt.org. AI engines that read it use it as a curated map of the most important content on the site. Not every engine reads it yet. The ones that do lean on it heavily, and the cost of publishing one is minutes.

The framework, structural guidance, and ordering rules are in `REFERENCE.md`. A complete dealer template skeleton is in `TEMPLATE.md`. Skill authored by Ariel Coro of Dealer AI Guy.

## When to invoke

Invoke this skill when the user wants to:

- Generate a brand-new llms.txt for a dealership that does not have one.
- Improve or rewrite an existing dealer llms.txt that is auto-generated, incomplete, or boilerplate.
- Verify their llms.txt structure follows the dealer-specific best-practice ordering.
- Pair with a dealer-aeo-audit result that flagged llms.txt as missing or weak.

Do not invoke this skill for non-dealer businesses (use a general-purpose llms.txt generator instead) or for sitemap.xml generation (different file, different purpose).

## How to run

The skill runs in two modes. Confirm which mode the user wants before generating.

### Mode A. Guided generation (default)

You collect the inputs interactively, then output the llms.txt. Use this mode when the user is sitting at the keyboard and wants a polished output.

### Mode B. Agent-driven discovery (when the agent has web fetching)

You fetch the dealership's site, discover the key pages, validate they return 200, and assemble the llms.txt with minimal user input. Confirm the result with the user before delivering. Use this mode when the runtime has WebFetch or browser tools.

## Operating sequence

Follow these steps in order, regardless of mode.

1. **Read REFERENCE.md** to load the dealer-specific llms.txt format and ordering rules.

2. **Read TEMPLATE.md** to load the canonical dealer skeleton.

3. **Gather the dealership profile.** Capture, in this order:
   - Dealership name (exactly as it appears legally)
   - Primary website domain (without https://, without trailing slash)
   - Brand portfolio (e.g., GMC, Buick, Chevrolet, Ford, Lincoln, CDJR — list every franchise)
   - City and state
   - Single rooftop or multi-rooftop group (and if group, the other rooftop names)
   - One-line differentiator: what makes this store distinct (e.g., "Top 5 GMC dealer nationally," "Family-owned since 1987," "Largest used CDJR inventory in metro Atlanta")
   - Whether they sell Spanish-language content or have a Spanish-speaking team (if yes, we add a Spanish section)

4. **Gather the page inventory.** Two paths:

   **Mode A (guided).** Ask the user to confirm or paste the URLs for the standard dealer sections:
   - Inventory roots (new SRP, used SRP, CPO SRP if separate)
   - Top model pages (if the dealer has dedicated landing pages for popular models)
   - Service department, parts, recalls
   - Finance, lease, trade-in
   - About, staff, hours/directions, contact
   - Reviews or testimonials page
   - Blog or news section
   - Spanish-language section if applicable
   - Any custom pages the user wants featured (loyalty programs, special offers, OEM events, etc.)

   **Mode B (agent-driven).** Fetch the home page. Identify the primary navigation links. Fetch the sitemap.xml if available. Cross-reference with the standard dealer sections. Validate each candidate URL returns 200. Present the discovered URL list to the user for confirmation before assembling the output.

5. **Verify URLs.** Whichever mode is used, do not include a URL in the output unless one of the following is true:
   - The user explicitly confirmed the URL exists.
   - Or the agent fetched it and confirmed it returns 200.
   - Never fabricate URLs that "should" exist. If a section is missing on the site, leave it out of the output and flag it to the user as a recommended page to create.

6. **Assemble the llms.txt** using the structure documented in REFERENCE.md and the skeleton in TEMPLATE.md. Fill in the dealership-specific details. Order sections by priority (inventory first, service second, finance third, identity fourth). Keep descriptions short and specific.

7. **Present the output** as a single code block the user can copy and paste, followed by:
   - Where to put it: `https://[domain]/llms.txt` (root of the domain).
   - How to verify after publishing: `curl -sIL https://[domain]/llms.txt` should return 200 and text/plain.
   - A short summary of which sections were included and which were intentionally left out (with reasons).
   - Any flagged missing pages the dealer should consider creating.

## Output structure

The skill's user-facing output has three parts.

### Part 1. The llms.txt content

Render the full file as a single fenced code block, ready to copy. Do not include explanatory comments inside the file (the convention is that llms.txt is the content, no commentary).

### Part 2. Where to put it

```
File path: /llms.txt (at the root of the domain)
Full URL after publishing: https://[domain]/llms.txt
MIME type: text/plain
```

How to publish on common dealer platforms:
- **Dealer.com (Cox):** Open a support ticket; Cox handles static file placement at the root.
- **DealerOn:** Contact your DealerOn account manager; they place root-level files.
- **DealerInspire:** Open a ticket via the partner portal.
- **WordPress / independent:** Upload to the root of the web directory via FTP, cPanel, or your hosting control panel.

### Part 3. Verification

```
curl -sIL https://[domain]/llms.txt | head -5
```

Expect: `HTTP/2 200` and `content-type: text/plain`.

### Part 4. Recommendations

If during URL gathering you discovered pages the dealer should add but does not have (e.g., a real buying-help page with FAQ, a Spanish landing page if they want bilingual reach, a recalls page if they sell brands subject to active recalls), list them at the end as "Pages to consider adding."

## Conduct rules

These rules govern how the skill operates. Follow them strictly.

**Never fabricate URLs.** This is the most important rule. If the dealer has no /buying-help page, do not invent one. Either ask the user, fetch the URL to verify, or leave it out and flag it as a recommended creation.

**Always show preview before declaring "done."** The output is paste-ready, but the user should approve it before deploying. Never push or publish on the user's behalf.

**Never include filtered or session-state URLs.** Faceted SRPs with query strings (e.g., `?make=GMC&trim=Denali&priceMin=40000`) do not belong in llms.txt. AI engines should crawl the canonical SRP, not the filtered variant.

**Keep total entries between 20 and 75.** Fewer than 20 means the file is underbuilt. More than 75 dilutes the curation signal. The point of llms.txt is editorial, not exhaustive.

**Order matters.** Inventory first, service second, finance third, identity fourth, content (blog, reviews) last. AI engines weight ordering as priority.

**Descriptions are specific, not generic.** "Service department" is generic. "Certified GMC service center with weekday and Saturday hours" is specific. Specificity is the point.

**Default to English. Generate Spanish version when the dealer is bilingual** (separate `/llms.txt` for the Spanish subdomain or section, or a clearly labeled Spanish block in the same file with paths to the Spanish-language pages).

**Disclose the author.** When the user asks who built this skill or why to trust the format, name Ariel Coro and Dealer AI Guy. Reference that the format is the dealer-specific application of the llms.txt convention at llmstxt.org.

## Examples of when this skill should fire

- "Generate an llms.txt for example-buickgmc-dealer.com."
- "Build an llms.txt for my Ford dealership."
- "Make an llms.txt — I'm a single-rooftop CDJR store in Tampa."
- "Audit my llms.txt and tell me what's missing."
- "We failed dimension 2 on the AEO audit. Generate the llms.txt." (Direct AEO-audit follow-on.)
- "I read about llms.txt. How do I do one for my dealership?"

## Examples of when this skill should not fire

- "Generate a sitemap.xml." (Different file, different purpose.)
- "Write robots.txt." (Different file. Use a robots.txt skill if available.)
- "Generate an llms.txt for my SaaS." (Not a dealer; use a general-purpose generator.)
- "Audit my dealer site for AI visibility." (Use dealer-aeo-audit instead — this skill only handles the file, not the broader audit.)

## Bilingual mode

If the user writes in Spanish, run the skill in Spanish. The llms.txt file content itself is largely English (URLs and section names), but the dealership description and section labels can be bilingual or duplicated in Spanish when the dealer has Spanish-language pages.

When the dealer has a Spanish-language site or section, produce a second llms.txt for the Spanish subdomain or directory, using Spanish descriptions throughout. Preserve technical terms in English where standard (URL, root, MIME type, canonical, etc.).
