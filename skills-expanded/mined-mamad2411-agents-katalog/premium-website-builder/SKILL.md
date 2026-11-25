---
name: premium-website-builder
description: Design and spec modern, conversion-focused landing pages and business websites — including copy, section structure, visual hierarchy, CTA placement, and social proof strategy. Use when the user wants to build or redesign a website, needs a landing page for a product/service/offer, or wants a complete page brief to hand to a developer or feed into a no-code builder (Webflow, Framer, Instatic, Carrd). Outputs a full page spec with copy and design direction, not raw HTML. Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."
---

# Premium Website Builder

Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."

> Build modern, conversion-focused landing pages and business websites — from positioning through copy, section layout, CTA placement, and visual direction.

## What this skill produces

A complete page spec ready to hand to a developer or paste into a no-code builder:
- **Positioning statement** (who it's for, what problem it solves, why this solution)
- **Hero section**: headline, sub-headline, primary CTA, supporting image/video direction
- **Section-by-section structure**: every block from hero to footer with its purpose
- **Copy for each section**: written, not described
- **CTA strategy**: placement, button text, offer framing at each stage
- **Social proof plan**: what to show, where, how to frame it when it's thin
- **Visual direction**: color mood, typography style, imagery type — enough to brief a designer

## The conversion-first structure

| Section | Purpose | What it must answer |
|---|---|---|
| Hero | Stop and orient | What is this? Who is it for? |
| Problem | Create resonance | You understand my pain |
| Solution | Introduce the offer | This is how it gets fixed |
| Features/How it works | Build belief | This is real and specific |
| Social proof | Remove risk | Others got the result |
| Pricing/Offer | Make it buyable | I know exactly what I get |
| FAQ | Kill objections | The last reason not to |
| Final CTA | Close | One more clear ask |

## Copy-paste prompt to use

```
You are a conversion copywriter and landing page architect who has studied the highest-converting pages in SaaS, coaching, services, and e-commerce.

My offer: [DESCRIBE WHAT YOU SELL — product, service, course, etc.]
Target audience: [WHO IS THIS FOR — be specific, not "entrepreneurs"]
Core problem I solve: [ONE SENTENCE]
Main differentiator: [WHY THIS OVER ALTERNATIVES]
Social proof I have: [TESTIMONIALS / CASE STUDIES / CLIENT LOGOS / OR "NONE YET"]
Primary goal of this page: [BOOK A CALL / BUY NOW / SIGN UP FREE / JOIN WAITLIST]

Build me a complete landing page spec:
1. Positioning statement (1 sentence)
2. Hero section — headline, sub-headline, CTA button text, hero image direction
3. Full section-by-section structure (name each section + its single job)
4. Written copy for each section (not descriptions — actual words)
5. CTA placement and framing at each stage
6. Social proof strategy (even if I have little)
7. Visual direction — color mood, type style, imagery type
8. The 3 most important things this page must NOT do (anti-patterns for my niche)

Write the copy as if you're writing for a real business, not a template.
```

## No-code builder targeting

- **Instatic**: open-source, self-hostable, visual builder → HTML + CSS output (from `open-source-devtools-2026`)
- **Framer / Webflow**: paste the spec into the AI builder or brief a designer with it
- **Carrd**: simple single-page sites — this spec works for that too
- **Lovable**: pairs well with the `saas-mvp-24h` skill's Phase 2 design step

## Related skills

- **saas-mvp-24h**: Phase 2 (Design) uses a similar prompt for the SaaS landing page + product UI combo
- **product-marketing-context**: Capture positioning and ICP before running this skill — feeds the "target audience" and "core problem" inputs
- **sales-enablement**: If the page is for a service business, pair with this for the proposal/pitch layer
- **thumbnail-maker**: A high-performing thumbnail drives traffic to this page — run both together for a launch
