---
name: soskills
description: "Generate complete, high-converting sales landing pages for low-ticket digital products (ebooks, templates, mini-courses, tools). Outputs production-ready HTML standalone or Next.js TSX + Tailwind code. Use when the user says 'soskills', '/soskills', 'page de vente', 'sales page', 'landing page low-ticket', 'create a sales page', 'generate a landing page', 'low-ticket funnel page', or wants to build a conversion-optimized sales page for a digital product under 100€."
---

# Soskills — Low-Ticket Sales Page Generator

Generate complete, conversion-optimized sales pages for low-ticket digital products. Output: HTML standalone or Next.js TSX + Tailwind.

## Workflow

### Phase 1: Discovery

Read [references/discovery-questions.md](references/discovery-questions.md) and ask the user the required questions (Q1-Q6) in a single message. Wait for all answers before proceeding.

If answers to Q1 (persona) or Q2 (problem) are vague, ask one follow-up. Infer optional questions (Q7-Q11) from context when possible.

### Phase 2: Copywriting

Before writing code, draft all copy section by section following the blueprint in [references/sales-sections.md](references/sales-sections.md). Apply these principles:

**Copywriting rules**:
- Write in second person ("tu/vous" in FR, "you" in EN) — match language chosen by user
- Use the PAS framework: Problem → Agitation → Solution
- Every headline must contain a specific benefit or result
- Every bullet point follows: [Concrete feature] → [Emotional benefit]
- Use power words: instantly, proven, without, finally, secret, simple, guaranteed
- Price anchoring: always show total value before revealing actual price
- CTA text = action + result ("Je Veux Mes Templates →", not "Acheter")

**Psychology triggers to embed** (from marketing-psychology principles):
- Loss aversion: "Ne rate pas..." / frame what they lose by not buying
- Social proof: numbers, testimonials, logos
- Anchoring: high value stack before low price reveal
- Scarcity: limited offer, countdown
- Reciprocity: free bonus stack
- Authority: creator credentials, results

### Phase 3: Code Generation

Read [references/design-system.md](references/design-system.md) for the visual design system, then generate the page.

**Output format based on user choice**:

#### HTML Standalone
- Single `.html` file with embedded CSS and minimal JS
- Google Fonts loaded via `<link>` (Poppins + Montserrat)
- Fully responsive (breakpoint: 800px)
- Scroll animations via Intersection Observer
- FAQ accordion via vanilla JS
- All styles inline or in `<style>` block — no external dependencies

#### Next.js TSX + Tailwind
- Single page component (`page.tsx` or `SalesPage.tsx`)
- Tailwind CSS classes (no custom CSS unless necessary)
- `"use client"` directive for interactive elements (FAQ accordion, animations)
- Lucide React icons if in project deps, otherwise Unicode
- Responsive via Tailwind breakpoints (`md:`, `lg:`)

**Design requirements (both formats)**:
- Follow the color palette, typography, and spacing from the design system
- Alternate section backgrounds (white / off-white)
- CTA buttons repeated after: Hero, Offer/Pricing, Final CTA (minimum 3 CTAs)
- Before/After section uses two-column grid (stacked on mobile)
- Pricing box with border accent and shadow
- Guarantee section with green tint background
- Urgency banner sticky at top (red background)
- Image placeholders with descriptive alt text and sizing comments
- FAQ as clickable accordion

**Required sections** (in order):
1. Urgency banner (sticky top)
2. Hero (headline + sub-headline + CTA)
3. Problem / Agitation
4. Solution — Product reveal
5. Before / After transformation
6. What's Inside — Content breakdown
7. Social Proof
8. Bonus Stack
9. Offer + Pricing (value stack)
10. Guarantee
11. FAQ
12. Final CTA

### Phase 4: Delivery

Write the file to disk at the user's preferred location. Summarize what was generated and suggest next steps:
- Replace image placeholders with real visuals
- Add real testimonials if placeholders were used
- Connect CTA buttons to payment processor (Stripe, Gumroad, LemonSqueezy, etc.)
- A/B test the headline

## Quality Checklist

Before delivering, verify:
- [ ] All 12 sections present and in order
- [ ] Minimum 3 CTA buttons across the page
- [ ] Price anchoring (total value vs actual price)
- [ ] Mobile responsive (test mentally at 375px width)
- [ ] No lorem ipsum — all copy is real, tailored to the product
- [ ] FAQ addresses at least 4 common objections
- [ ] Guarantee section present with clear terms
- [ ] At least 3 bonuses in the bonus stack (invent relevant ones if user didn't provide)

## Resources

- **[references/discovery-questions.md](references/discovery-questions.md)** — Question framework for the discovery phase
- **[references/sales-sections.md](references/sales-sections.md)** — Detailed section blueprint with copywriting formulas
- **[references/design-system.md](references/design-system.md)** — Visual design system (colors, typography, spacing, components)
