---
name: productize-startup-canvas
description: >-
  Startup Canvas. Use when evaluating a startup concept or new product that needs product
  strategy and business model logic in one founder-ready artifact.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Startup Canvas

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

- **Skill**: `startup-canvas`
- **Lifecycle**: Think
- **Category**: Venture / 0-1
- **Primary artifact**: Startup Canvas combining product strategy, business model, risks, and next validation steps

Use when evaluating a startup concept or new product that needs product strategy and business model logic in one founder-ready artifact.

## Productize Contract

- **Primary lifecycle**: Think
- **Supporting lifecycle**: Strategize
- **Primary artifact**: Startup Canvas combining product strategy, business model, risks, and next validation steps
- **Source method**: pm-skills-main/pm-product-strategy/skills/startup-canvas/SKILL.md

## Method

## Metadata
- **Name**: startup-canvas
- **Description**: Generate a Startup Canvas for a new product. Combines the 9-section Product Strategy Canvas with a Business Model (Cost Structure + Revenue Streams). Designed specifically for startups and new products.
- **Triggers**: startup canvas, new product canvas, startup strategy, startup business model

## Domain Context

### Startup Canvas vs Business Model Canvas vs Lean Canvas

Popular approaches like Business Model Canvas (Strategyzer) and Lean Canvas (Ash Maurya) mix strategy and business model into one artifact. The **Startup Canvas** (Pawe Huryn) separates them: 9 strategy sections from the Product Strategy Canvas + Cost Structure & Revenue Streams.

**Why not Business Model Canvas?**
- No vision -- why should your team wake up every day?
- No Can't/Won't test -- what stops competitors from copying you?
- No trade-offs -- what you choose NOT to do creates focus
- No key metrics -- how do you know the strategy is working?
- Key Partnerships and Key Resources are rarely useful for early-stage products

**Why not Lean Canvas?**
- Introduces redundancy: "Problem" overlaps with Market Segments (markets are defined by problems), "Solution" overlaps with Value Proposition (which by definition includes features)
- No vision, no trade-offs, no relative costs
- "Unfair Advantage" is too narrow -- the entire strategy should be hard to copy, not just one element
- Doesn't address the holistic fit of strategic choices reinforcing each other

**When to use which:**
- **Business Model Canvas**: Established businesses, corporate strategy, investor materials
- **Lean Canvas**: Quick hypothesis testing when you just need speed
- **Startup Canvas**: New products where you need both strategic clarity AND a business model -- the recommended approach

## Instructions

You are a product strategist and startup advisor designing a Startup Canvas for $ARGUMENTS.

Your task is to create a comprehensive Startup Canvas that covers both the strategic choices and the business model for a new product.

## Input Requirements
- Product or startup idea
- Target market and customer insights
- Competitive landscape
- Founder/team constraints and resources

## Startup Canvas Template

### Part 1: Product Strategy (9 Sections)

**1. Vision**
- How can we inspire people? What are we aspiring to achieve? What values do we uphold?
- Start simple. Your vision will evolve alongside the strategy.

**2. Market Segments**
- The market is defined by the problems people have (not demographics).
- Jobs to Be Done (JTBD), desired outcomes, constraints.
- What will be your first customer segment? Why this one first?

**3. Relative Costs**
- Do you optimize for low cost (like Southwest Airlines) or unique value (like Starbucks)?
- Low costs don't necessarily mean low prices.

**4. Value Proposition**
For each market segment:
- **What before**: Existing, problematic state
- **How**: Features and capabilities that change the situation
- **What after**: The benefits and outcomes
- **Alternatives**: Your unique value vs. competitors and substitutes (consider a Value Curve)

**5. Trade-offs**
- What will you NOT do? Trade-offs create focus and amplify value.
- Especially important for startups where it's tempting to chase every opportunity.

**6. Key Metrics**
- A few key metrics to measure if the product and strategy are working.
- North Star Metric and One Metric That Matters (OMTM) for this quarter.

**7. Growth**
- Product-Led Growth or Sales-Led Growth?
- Preferred channels: Social Media, SEO, Influencers, Resellers?

**8. Capabilities**
- What competencies and resources do you need to acquire?
- What do you build vs. partner for?

**9. Can't/Won't**
- What makes you think competitors can't or won't copy your strategy?
- The entire strategy should be difficult to copy -- not just one element.
- Do all elements fit together and reinforce each other?

### Part 2: Business Model

**10. Cost Structure**
- Rent, hardware, licenses, technology, marketing, subscriptions, salaries.
- Which are recurring? How will they scale?

**11. Revenue Streams**
- How much money from each channel?
- Pricing approach: penetration, value-based, competitive, usage-based, SaaS?
- Is the revenue model scalable? What are the biggest uncertainties?

## Output Process
1. Define the vision and aspirational impact
2. Identify 2-3 target market segments with JTBD
3. Establish cost positioning (low cost vs premium)
4. Develop value propositions for each segment
5. List explicit trade-offs
6. Set North Star and quarterly OMTM
7. Outline growth strategy and channels
8. Document required capabilities
9. Explain defensibility (Can't/Won't test)
10. Estimate cost structure and revenue streams
11. Validate strategy coherence: do all elements reinforce each other?
12. Surface hypotheses that must be true for success
13. Suggest low-effort experiments to test key assumptions

## Notes
- The Startup Canvas separates strategy from business model -- keep them distinct but connected
- Strategy should pass the Can't/Won't test: your competitors can't or won't copy the integrated set of choices
- After drafting the first version, identify and start testing hypotheses
- Mix and adapt approaches to suit your specific needs rather than following any canvas rigidly

---

### Templates

- [Startup Canvas (PPTX)](https://docs.google.com/presentation/d/1lA0SPflj5JT6jFV_jIDsqZJAYYperTFx/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### Further Reading

- [Startup Canvas: Product Strategy and a Business Model for a New Product](https://www.productcompass.pm/p/startup-canvas)
- [Product Strategy Canvas](https://www.productcompass.pm/p/product-strategy-canvas)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
- [Business Model Canvas Examples: Google Maps, Airbnb, Uber](https://www.productcompass.pm/p/business-model-canvas-examples)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
