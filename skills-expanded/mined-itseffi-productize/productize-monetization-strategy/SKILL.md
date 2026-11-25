---
name: productize-monetization-strategy
description: >-
  Monetization Strategy. Use when deciding how a product should make money, comparing revenue
  models, or exploring monetization options before detailed pricing.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Monetization Strategy

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `monetization-strategy`
- **Lifecycle**: Strategize
- **Category**: Business Model
- **Primary artifact**: Monetization options brief with audience fit, risks, and validation experiments

Use when deciding how a product should make money, comparing revenue models, or exploring monetization options before detailed pricing.

## Productize Contract

- **Primary lifecycle**: Strategize
- **Supporting lifecycle**: none
- **Primary artifact**: Monetization options brief with audience fit, risks, and validation experiments
- **Source method**: pm-skills-main/pm-product-strategy/skills/monetization-strategy/SKILL.md

## Method

## Metadata
- **Name**: monetization-strategy
- **Description**: Brainstorm 3-5 monetization strategies with audience fit, risks, and validation experiments. Use when exploring revenue models, pricing strategies, or business model options.
- **Triggers**: monetization strategy, revenue model, pricing strategy, how to monetize, make money

## Instructions

You are an experienced business model strategist brainstorming monetization strategies for $ARGUMENTS.

Your task is to develop 3-5 distinct monetization approaches that could work for the product or feature, evaluate fit with the target market, and outline low-effort validation experiments.

## Input Requirements
- Product or feature description
- Target market segment(s) and customer profile
- Current willingness to pay or budget constraints
- Competitive monetization approaches
- Company priorities (revenue growth, user growth, profitability)

## Monetization Framework

For each strategy, include:

### 1. Strategy Name & Description
- What is the monetization model?
- How does it work for this product?
- Who pays and what do they get?

### 2. How It Works
- Revenue model and pricing mechanics
- Value exchange between company and customer
- Payment frequency and transaction size
- Lifecycle and retention mechanisms

### 3. Audience Fit
- Why does this resonate with your target customer?
- How does it align with customer needs and preferences?
- What problems does it solve for the customer?
- Addressable market size and revenue potential

### 4. Unit Economics
- Estimated customer acquisition cost (CAC)
- Estimated customer lifetime value (LTV)
- Break-even timeline
- Target gross margin

### 5. Risks & Challenges
- Market adoption risk
- Pricing or feature sensitivity
- Competitive vulnerability
- Customer churn or resistance
- Implementation complexity

### 6. Competitive Position
- How do competitors monetize?
- What makes your approach differentiated?
- Barriers to customer switching
- Defense against competitive pricing

### 7. Validation Experiment
- Low-cost test to validate customer willingness to pay
- Method: survey, landing page, pilot, freemium, waitlist
- Success metric and decision criteria
- Timeline and resources required

## Example Monetization Strategies

### 1. Freemium (Free Base + Paid Premium)
- **How**: Free core features, premium advanced features behind paywall
- **Fit**: Best for high-volume, low-touch products (design tools, productivity, communication)
- **Risks**: Low conversion rates (typically 1-5%), features must be clear to justify upgrade
- **Experiment**: Launch freemium version, track conversion rate, gather upgrade feedback

### 2. Subscription (Recurring Monthly/Annual)
- **How**: Recurring charge for ongoing access and updates
- **Fit**: Best for products with continuous value (software, platforms, services)
- **Risks**: Customer churn, cannibalization from annual vs. monthly
- **Experiment**: Offer subscription to beta customers, measure churn rate and NPS

### 3. Usage-Based (Pay Per Use)
- **How**: Customers pay based on usage volume (API calls, storage, transactions)
- **Fit**: Best for B2B platforms, APIs, services with variable customer needs
- **Risks**: Unpredictable revenue, customer cost anxiety, usage optimization by customers
- **Experiment**: Implement usage tracking, pilot with 5-10 beta customers, model revenue

### 4. Enterprise/Seat-Based (Per User/Seat)
- **How**: Price per user, department, or seat using the product
- **Fit**: Best for B2B SaaS with team/organization adoption
- **Risks**: Sales complexity, contract length, implementation overhead
- **Experiment**: Conduct 5-10 customer interviews, validate pricing per seat, define support model

### 5. One-Time Purchase (Buy Once)
- **How**: Single upfront purchase for permanent or one-time license
- **Fit**: Best for niche products, tools, or templates (not ongoing services)
- **Risks**: Revenue concentration in launch period, no recurring revenue, updates/support questions
- **Experiment**: Launch limited offering, track conversion and customer satisfaction

### 6. Marketplace/Transaction Fee
- **How**: Take a percentage or fixed fee from transactions between buyers and sellers
- **Fit**: Best for platforms connecting supply and demand
- **Risks**: Market liquidity chicken-and-egg problem, trust and safety, competitive pressure
- **Experiment**: MVP with limited sellers, offer free period to drive initial supply, model unit economics

### 7. Advertising/Sponsorship
- **How**: Generate revenue from ads, sponsored content, or brand partnerships
- **Fit**: Best for high-traffic, consumer-facing products
- **Risks**: Brand damage from intrusive ads, user experience degradation, advertiser concentration
- **Experiment**: Test ads with small user segment, measure engagement and revenue impact

## Output Process
1. Brainstorm 3-5 distinct monetization strategies (avoid repeating similar models)
2. For each strategy:
   - Describe how it works specifically for this product
   - Assess fit with target customer and willingness to pay
   - Outline key risks and challenges
   - Estimate unit economics (CAC, LTV, timeline)
   - Compare against competitive approaches
3. For each strategy, design a low-effort validation experiment
4. Prioritize by:
   - Strategic fit (revenue, growth, profitability goals)
   - Ease of implementation
   - Market validation potential
   - Competitive advantage
5. Recommend 1-2 strategies to test first
6. Create testing roadmap and success criteria

## Strategic Considerations
- **Revenue Goals**: How much revenue is needed? By when?
- **Growth Goals**: Does monetization need to support user growth?
- **Market Dynamics**: Are customers ready to pay? For what?
- **Competitive Pressure**: How will competitors respond?
- **Unit Economics**: What gross margin is required for viability?

## Notes
- Best monetization strategies align with customer value and willingness to pay
- Test early and often; don't wait for perfect product to validate pricing
- Most products use hybrid models (e.g., freemium + upgrade, subscription + marketplace fees)
- Pricing can be changed; customer relationships are harder to rebuild
- Monitor competitors but don't race to the bottom on price

---

### Further Reading

- [Product Pricing Strategies 101](https://www.productcompass.pm/p/product-pricing-strategies-101)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
