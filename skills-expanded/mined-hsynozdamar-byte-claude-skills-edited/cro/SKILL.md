---
name: cro
description: "Conversion rate optimization for marketing pages and forms. Use when a landing, pricing or feature page or lead form is not converting, or when the user shares a URL for feedback."
metadata:
  version: 2.0.0
---

# Conversion Rate Optimization (CRO)

Analyze a marketing page and return actionable recommendations to lift conversion. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists, and ask only for what it does not cover.

Identify first: page type (homepage, landing, pricing, feature, blog, about), the primary conversion goal (sign up, demo, purchase, subscribe, download, contact sales), and traffic source (organic, paid, email, social). Also useful: current conversion rate, what comes after this page, available research (heatmaps, recordings), and what was already tried.

## Analysis, in order of impact

1. **Value proposition.** Can a visitor say what this is and why they should care within 5 seconds? The primary benefit is specific, differentiated and in customer language. Typical faults: features instead of benefits, too clever, saying everything instead of the most important thing.
2. **Headline.** Carries the core value, specific enough to mean something, matches the traffic source's message. Patterns: "Get [outcome] without [pain]", concrete numbers or timeframes, social proof the user can substantiate.
3. **CTA.** One clear primary action visible without scrolling, button copy that states the value ("Start Free Trial", "Get My Report", "See Pricing" over "Submit", "Sign Up", "Learn More"), a primary vs secondary hierarchy, repeated at decision points.
4. **Visual hierarchy.** A scanner gets the main message, key elements are prominent, white space is sufficient, images support the message.
5. **Trust.** Customer logos, specific attributed testimonials, case snippets with real numbers, review scores, security badges where relevant; placed near CTAs and after benefit claims.
6. **Objections.** Price/value, "will it work for me?", implementation effort, "what if it doesn't work?"; answer with FAQ, guarantees, comparisons, process transparency.
7. **Friction.** Too many form fields, unclear next steps, confusing navigation, unnecessary required info, mobile problems, slow loads.

## By page type

- **Homepage**: positioning for cold visitors, quick path to the commonest conversion, serves both "ready to buy" and "still researching".
- **Landing page**: message match with the traffic source, single CTA (remove navigation if possible), complete argument on the page.
- **Pricing page**: clear plan comparison, recommended plan marked, "which plan is right for me?" answered.
- **Feature page**: feature to benefit, use cases, clear path to try or buy.
- **Blog post**: CTAs matching the topic, inline at natural stopping points.

## Output

1. **Quick wins**: easy changes with likely immediate impact.
2. **High-impact changes**: bigger effort, significant lift.
3. **Test ideas**: hypotheses to A/B test instead of assuming.
4. **Copy alternatives**: 2 to 3 options with rationale for key headlines and CTAs.

Experiment ideas by page type (hero, trust placement, pricing presentation, forms, navigation): [references/experiments.md](references/experiments.md).

## Forms

Lead forms, field optimization, multi-step forms, error handling and form experiments: [references/form.md](references/form.md). Signup flows go to `signup`; a full copy rewrite goes to `copywriting`.
