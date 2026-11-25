---
name: dealer-comparison-page-builder
description: >-
  Build one in-depth comparison page between a car dealership and a single named competitor for SEO, AEO, GEO, and sales enablement. Use when the user asks to "build a comparison page", "dealer vs dealer page", "compare my dealership to [Competitor]", "[Dealer A] vs [Dealer B]", "competitor comparison content", "build a comparison landing page", "dealership comparison page", "alternative-to page for a dealer", or any request to produce a comparison page between two car dealerships. Produces a complete, paste-ready landing page covering positioning, brand portfolio, inventory, service capabilities, pricing transparency, customer experience, F&I, and the fair-play side-by-side. Optimized for AI engine citation (AEO/GEO) and Google ranking on "[Dealer A] vs [Dealer B]" queries. Built around fair-play rules: honest comparison, no fabricated claims, named competitor gets accurate treatment. Pairs with dealer-aeo-content-brief (which produces individual content briefs) and dealer-store-positioning (which produces the positioning that informs the comparison). Authored by Ariel Coro of Dealer AI Guy.
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
# Dealer Comparison Page Builder

This skill produces one in-depth comparison page between a car dealership and a single named competitor. The page is optimized for Google ranking on "[Dealer A] vs [Dealer B]" queries, for AI engine citation when buyers ask comparison questions, and for sales floor use when a customer is actively shopping both dealers.

The framework, fair-play rules, and page structure are in `REFERENCE.md`. The complete page template skeleton is in `TEMPLATE.md`. Authored by Ariel Coro of Dealer AI Guy.

## Why one page at a time, not batch

The user picked single-page-per-run scope deliberately. One in-depth comparison page outperforms 10 mediocre ones for AEO/SEO purposes because AI engines and Google reward depth of fair comparison over breadth of templated content. The skill is designed for the dealer to commission 5 to 15 of these pages over several weeks (one against each major named competitor), each one researched and written with care.

## Why fair-play matters

A comparison page that trashes the competitor is brand-damaging and AI engines deprioritize it. A comparison page that fairly acknowledges where the competitor is strong and where this dealer is strong reads as credible. Credibility produces citations. Credibility also produces sales floor confidence; when a customer mentions "I am shopping you against [Competitor]", the salesperson who has read a fair comparison page can navigate the conversation with respect.

This skill enforces fair-play rules. The output is honest comparison, not a hit piece.

## When to invoke

Invoke this skill when the user wants to:

- Build a comparison page against a named competitor for SEO/AEO purposes.
- Build sales enablement content for the showroom and BDC when customers are cross-shopping.
- Address a specific competitor that is winning citations or comparison queries.
- Produce a series of comparison pages, one per competitor, over several weeks.
- Replace existing competitor-attacking content with fair-play content that performs better.

Do not invoke this skill for batch generation of comparison pages (build them one at a time), for OEM model comparisons (use dealer-aeo-content-brief with the comparison page-type pattern), or for non-dealer businesses.

## How to run

Single-page-per-run. The user names the dealer and the competitor; the skill produces the page.

## Operating sequence

1. **Read REFERENCE.md** to load the comparison page architecture and fair-play rules.

2. **Read TEMPLATE.md** to load the page structure skeleton.

3. **Gather inputs.** Capture in this order:

   - **The dealer's positioning brief** (output from dealer-store-positioning if available; otherwise a short summary captured at run time).
   - **The dealer's basics:** name, brand portfolio, city, founding year, OEM awards, key differentiators.
   - **The named competitor:** legal name, primary URL, brand portfolio, city, ownership type if known, OEM awards if known.
   - **The comparison angle.** Most useful: "[Dealer A] vs [Competitor B] for [target customer]" (e.g., "[Our Dealership] vs [Competitor Dealer] for [target region] families"). The angle frames the page.
   - **What the user already knows.** Recent reviews, pricing posture, any operational signals about the competitor.
   - **Optional: dealer-customer-sentiment-analyzer output for the competitor** if the user has run a competitor review analysis.

4. **Research the competitor (Mode B if agent tools available).** If WebSearch or WebFetch is available, the skill fetches the competitor's home page, About page, service page, and a sample of recent reviews. Captures public facts: brand portfolio, hours, OEM awards displayed, key staff named publicly. Does not infer private information.

5. **Apply the fair-play rules.** For each dimension of the comparison, identify:
   - Where this dealer is genuinely stronger
   - Where the competitor is genuinely stronger
   - Where the two are comparable
   
   The output respects all three categories. A fair comparison page acknowledges at least one area where the competitor is stronger or comparable. Otherwise the page reads as biased and loses credibility.

6. **Generate the page.** Use the structure from TEMPLATE.md.

7. **Produce supporting deliverables.** Three additional outputs alongside the page itself:
   - **Sales floor talk track:** 200 to 300 words the sales team can use when a customer mentions they are also shopping the competitor.
   - **Schema markup spec:** Article + Product schema for the page.
   - **Internal link recommendations:** 3 to 5 pages on the dealer site this comparison page should link to.

## Output structure

Render in clean Markdown. The output has four parts.

### Part 1: The comparison page (the primary deliverable)

A complete, paste-ready landing page with the following sections in order. See TEMPLATE.md for the full structure.

- **H1:** "[Dealer Name] vs [Competitor Name]: Which [Brand Portfolio] Dealer Is Right for You?"
- **Opening 100 words (verbatim):** Answer the comparison question directly. Pick a recommendation. Acknowledge edge cases briefly.
- **Quick answer box:** 2 to 3 sentence summary recommendation.
- **Side-by-side comparison table:** 10 to 15 dimensions, scored honestly.
- **When [Dealer] is the better choice:** 250 to 400 words. Specific scenarios with named customer types.
- **When [Competitor] is the better choice:** 200 to 300 words. Required for credibility. Honest acknowledgment of where the competitor is stronger or genuinely comparable.
- **Brand portfolio comparison:** Models and trims each carries. Useful if portfolios differ.
- **Service department comparison:** Hours, capability, certifications, specifics.
- **Customer experience comparison:** Pulled from reviews, BDC response patterns, F&I reputation.
- **Common questions:** 6 to 10 Q&A on the comparison, structured for FAQPage schema.
- **The honest recommendation:** Restate the recommendation with the specific scenarios.
- **See [Dealer] in person:** CTA section.

### Part 2: Sales floor talk track

200 to 300 words the sales team uses when a customer mentions they are also shopping the competitor. Includes:
- How to acknowledge the competitor without disparaging
- The 2 to 3 specific points to emphasize about this dealer
- The 1 to 2 points where the competitor is comparable (so the salesperson is not blindsided)
- The question to ask the customer to surface what matters most to them

### Part 3: Schema markup spec

The structured data to add to the page:
- Article schema with mainEntity
- Product schema for each compared option (the two dealerships as Products being compared)
- FAQPage schema for the common questions section
- Required fields per schema type

### Part 4: Internal link recommendations

3 to 5 specific pages on the dealer's site to link from the comparison page, with anchor text recommendations and rationale for each. Typical recommendations: inventory page, service page, about/staff page, financing page, contact page.

## Conduct rules

These rules govern how the skill operates. Follow them strictly.

**Fair-play is mandatory.** Every comparison page must acknowledge at least one area where the competitor is stronger or genuinely comparable. A page that claims the dealer wins on every dimension is not credible and the skill will not produce it.

**Never fabricate competitor facts.** All claims about the competitor must come from public sources (their website, their GBP, their OEM listings, public press) or from the user's input. If a fact is not verifiable, leave it out or use a `[CONFIRM]` placeholder.

**Never disparage the competitor.** "Worse than", "shady", "untrustworthy" type language is off-limits even when the user has negative impressions. The page reads as if the competitor's GM would consider it accurate (even if not flattering).

**Never invent reviews or quotes.** When citing review patterns, the patterns come from real review data the user provides or the skill identifies. Hypothetical or composite reviews are not allowed.

**Pick a recommendation.** The page is more credible when it ends with a clear recommendation, even when both dealerships have merit. Hedge by acknowledging the scenarios where the competitor wins; do not hedge by refusing to recommend.

**Use the dealer's actual positioning.** When dealer-store-positioning output is available, use the voice and value props from it. Comparison page voice should match the rest of the dealer's marketing voice.

**Adapt tone to the target audience.** Most comparison pages target the research-stage buyer who is genuinely cross-shopping. The voice is informational and respectful, not salesy.

**Disclose the author when asked.** Name Ariel Coro and reference his consulting practice at Dealer Growth Hackers, where comparison pages are produced as part of competitive content programs.

**Default to English. Switch to Spanish if the user writes in Spanish or the comparison targets a bilingual market.** Preserve English brand and model names in their canonical form.

## Examples of when this skill should fire

- "Build a comparison page: [our dealership] vs [competitor dealer]."
- "Build the [Dealer A] vs [Dealer B] page."
- "Create a comparison landing page for my dealership against [Competitor]."
- "I need a fair comparison page between us and [Competitor]."
- "Build sales enablement content for when customers are cross-shopping [Competitor]."

## Examples of when this skill should not fire

- "Build a model comparison page (GMC Sierra vs Ford F-150)." (Use dealer-aeo-content-brief with the comparison pattern.)
- "Build 10 comparison pages at once." (Build them one at a time for quality.)
- "Trash the competitor in this comparison." (Fair-play rules prevent this.)
- "Compare a SaaS product to another SaaS." (Not dealer-specific.)

## Bilingual mode

When the dealership serves a bilingual market and is competing against a competitor that also serves Spanish-speaking customers, produce both an English version and a Spanish version of the comparison page. The Spanish version is not a literal translation; it adjusts for cultural context (family-buying decisions, multi-generational considerations, community involvement messaging).

Preserve English brand and model names in their canonical form in both versions.
