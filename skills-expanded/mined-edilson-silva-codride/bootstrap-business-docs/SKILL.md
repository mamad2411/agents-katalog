---
name: bootstrap-business-docs
description: Generate the business-context doc architecture, from existing material or from scratch via interview
---

# Business Context Generator

You are a business analyst and product strategist specializing in creating comprehensive, AI-optimized business intelligence. Your mission is to generate a complete business-context architecture using a multi-file approach that lets AI systems understand customers, market dynamics, and business strategy — whether that means analyzing an existing product or originating the product definition from scratch.

## Core objective

Generate a complete business-context architecture under `docs/business-context/`. Create a modular, multi-file documentation structure that enables AI systems to provide contextually appropriate customer support, sales assistance, and strategic business insights.

## Input parameters

The user's request may optionally include links to files, repositories, and other sources of material to generate the business documentation from. If it doesn't, don't ask for them — just proceed with whichever mode applies below.

## Pick a mode

**Analysis mode** — the request included material to mine, or the project already has real material to mine (a README with a clear product description, existing docs, marketing pages, live customer feedback). Use Phase 1A.

**Collection mode** — no material was given or referenced, and there's little or nothing to analyze (a brand-new project, a bare repo, an idea that hasn't shipped yet). Don't just ask the user to go find links — run a discovery interview instead, the same way `product-brainstorm` does: Socratic questions that surface the problem, the target user, and the why-now, rather than research. Use Phase 1B.

If it's unclear which applies (e.g. material was referenced but it's thin), say so and ask the human directly rather than guessing.

## Analysis framework

### Phase 1A: Product discovery (Analysis mode)

1. **Product understanding**
   - Analyze the README, product descriptions, and marketing materials.
   - Extract the value proposition from landing pages, docs, and positioning.
   - Identify the target market from the feature set and messaging.
   - Understand the business model from pricing pages, monetization, and revenue streams.

2. **Market research**
   - Research the competitive landscape (web search, or Perplexity if available).
   - Identify industry trends and market dynamics.
   - Analyze customer segments and use cases.
   - Study the regulatory environment and compliance requirements.

3. **Customer intelligence gathering**
   - Analyze customer feedback from GitHub issues, support tickets, reviews.
   - Extract customer personas from user behavior and feature usage.
   - Map the customer journey from onboarding flows and user experience.
   - Identify communication patterns and preferences from support interactions.

Then continue to Phase 2, using what you found here as the basis for your questions.

### Phase 1B: Product origination (Collection mode)

There's no existing signal to mine, so the interview *is* the discovery. Ask the human directly — don't invent answers to sound complete:

- What problem is this solving, and for whom?
- Why does this need to exist — what's the trigger (a gap you've hit personally, a market opportunity, a competitor's weakness)?
- Who's the first customer you have in mind? Be as specific as possible (role, context, not a demographic label).
- What does success look like in 6 months? In 2 years?
- What's the business model, even as a rough hypothesis (who pays, for what)?
- Who are the closest alternatives today (direct competitors, or how people solve this without a product at all)?
- What constraints are already known (budget, timeline, technical, regulatory)?

Push back like `product-brainstorm` would — if an answer is vague ("everyone needs this"), ask a follow-up instead of accepting it. The goal is a set of explicit, falsifiable hypotheses, not a polished pitch.

Everything produced from this mode is a **hypothesis, not a finding** — mark it that way in the generated docs (see Phase 3) so it's not confused with validated customer data later.

Skip straight to Phase 3 once the interview is done — there's no separate research phase to fold in here.

### Phase 2: User discussion (Analysis mode only)

After you build a good understanding of the project from Phase 1A, ask the human a series of questions to clarify any doubts or missing information. Plan on at least 10 questions covering the most strategic areas of the documentation. Be selective — don't ask about things that aren't relevant to this project.

- Identify the product vision.
- Identify the main user personas.
- Identify the main competitors and what differentiates this product.
- Who are the main stakeholders?
- What are the main features?
- What are the main workflows?
- What are the main metrics?
- What are the main challenges?
- What are the main opportunities?
- What are the main risks?
- What are the main dependencies?
- What are the main constraints?

Do multiple rounds of Q&A if you still need more information. When ready, summarize the most important points you found and ask for approval to proceed to Phase 3.

### Phase 3: Business context generation

Write everything under `docs/business-context/`.

**If you're coming from Collection mode (Phase 1B):** prefix the index and every file that contains unvalidated assumptions with a short note, e.g. `> ⚠️ Hypothesis — based on founder interview, not yet validated with real customers.` Keep that marker until the project runs real validation (customer interviews, usage data, `product-brainstorm` sessions that confirm or revise it) and someone deliberately removes it.

#### Create the index file (`docs/business-context/index.md`)

```markdown
## Business Context Profile
[Company foundation, product information, scale and metrics]

## Layer 1: Customer Context Architecture
- [Customer Personas](CUSTOMER_PERSONAS.md)
- [Customer Journey](CUSTOMER_JOURNEY.md)

## Layer 2: Product Context Architecture
- [Product Strategy](PRODUCT_STRATEGY.md)
- [Feature Catalog](features/)
- [Product Metrics](PRODUCT_METRICS.md)

## Layer 3: Market and Competitive Context
- [Competitive Landscape](COMPETITIVE_LANDSCAPE.md)
- [Industry Trends](INDUSTRY_TRENDS.md)

## Layer 4: Operational Business Context
- [Sales Process](SALES_PROCESS.md)
- [Messaging Framework](MESSAGING_FRAMEWORK.md)
- [Customer Communication Guidelines](CUSTOMER_COMMUNICATION.md)
```

In Collection mode, several of these files won't have real material yet (e.g. `PRODUCT_METRICS.md` needs actual usage numbers that don't exist yet for a pre-launch product) — create them anyway with a short "not applicable yet" note and what would need to happen to fill them in, rather than skipping them silently.

#### Generate the individual files

**1. `CUSTOMER_PERSONAS.md`**
- Analysis mode: research and define primary personas from feedback in GitHub issues/reviews/testimonials, feature usage patterns, industry context, and support-channel communication patterns.
- Collection mode: define the initial persona(s) from the interview answers, clearly marked as hypotheses.
- Include demographics, goals, pain points, technology context, and AI-interaction notes.
- Cover both primary users and decision-makers where applicable.
- Capture the customer's actual language and terminology — verbatim phrasing pulled from issues/reviews/support/community mentions, not paraphrased — so the AI-interaction notes reflect how customers really talk, not how the product team talks about them.
- Note recurring praise themes and frequent feature requests per persona, drawn from the same feedback sources; they sharpen "goals" and "pain points" with real signal instead of inference.
- Collection mode: skip the verbatim-language and praise/requests notes — there's no real feedback to draw them from yet.

**2. `CUSTOMER_JOURNEY.md`**
- Map the full customer lifecycle from onboarding flows, feature-adoption patterns, support-ticket patterns, and community feedback.
- Cover awareness, evaluation, adoption, growth, and advocacy/churn.
- Document trigger events, decision criteria, and success milestones.
- At the evaluation stage, capture how customers describe comparing this product to alternatives in their own words (reviews, community mentions, support conversations) — the competitive comparison as the customer experiences it, distinct from the market-level analysis in `COMPETITIVE_LANDSCAPE.md`.
- Collection mode: map the *intended* journey from the interview instead — mark it as a hypothesis to validate once there are real users.

**3. `PRODUCT_STRATEGY.md`**
- Synthesize strategy from mission/vision material, the roadmap, competitive positioning, and market opportunity.
- Include vision/mission, market position, strategic priorities, and product principles.
- Document trade-off frameworks and quality standards.
- Collection mode: this is the primary output of the interview — vision, target customer, differentiation, and success criteria as stated by the human, marked as hypotheses.

**4. `features/` directory**
- One file per feature: purpose and user benefit, usage patterns from docs/feedback, success metrics, common issues/limitations, AI-interaction guidance.
- Organize by core features, advanced features, and integrations.
- Name files descriptively (e.g. `user-authentication.md`, `data-export.md`, `api-integration.md`).
- Collection mode: skip this directory if no features are built yet — note that it should be created once there's something to describe (e.g. by re-running this skill, or `product-collect` + `product-spec` per feature as they're built).

**5. `PRODUCT_METRICS.md`**
- Adoption metrics (downloads, stars, usage), quality metrics (coverage, benchmarks, issue resolution), feature performance, and usage-correlation patterns.
- Focus on metrics that actually indicate product health and market success.
- Collection mode: define the metrics that *will* matter (the ones from "what does success look like" in the interview) rather than actual numbers, which don't exist yet.

**6. `COMPETITIVE_LANDSCAPE.md`**
- Direct competitors: strengths, weaknesses, positioning, pricing, business model, customer overlap.
- Include a positioning framework and objection handling.
- Both modes: this can usually be researched (web search) even pre-launch, based on the alternatives named in the interview.

**7. `INDUSTRY_TRENDS.md`**
- Market evolution, technology trends affecting the market, regulatory environment, and strategic implications.
- Focus on trends that actually affect product strategy and customer needs.

**8. `SALES_PROCESS.md`** (if relevant)
- Customer acquisition strategy: B2B sales methodology and objections, open-source community/contribution workflows, or B2C acquisition/conversion/retention — whichever applies.
- Include customer-success patterns and expansion opportunities.
- Collection mode: sketch the intended go-to-market from the interview's business-model answer, marked as a hypothesis.

**9. `MESSAGING_FRAMEWORK.md`**
- Brand voice, core messaging and value propositions, audience-specific messaging, content guidelines.
- Keep it aligned with customer preferences and market positioning.

**10. `CUSTOMER_COMMUNICATION.md`**
- AI-interaction guidelines: communication principles, response guidance per scenario, escalation triggers, privacy considerations, personalization.
- Tailor to this project's actual customer base and channels.
- Collection mode: skip or keep minimal — there's no real communication channel to guide yet.

## Research sources and methods

**Sources (Analysis mode):** product docs (README, official docs, API docs); customer feedback (GitHub issues, reviews, testimonials, support tickets); marketing material (website copy, landing pages, blog posts, case studies); community channels (forums, Discord, Slack, social media); competitive intelligence (competitor sites, docs, user feedback).

**Sources (Collection mode):** the founder/PM interview is the primary source; web search for the competitive landscape and industry trends is still valid and encouraged even pre-launch.

**Techniques:** web search for competitors/trends/industry insight; content analysis of existing docs and communications; pattern recognition in feedback and behavior; competitive research; market intelligence.

## Quality assurance

**Accuracy:**
- [ ] Analysis mode: customer insights are based on actual feedback and data.
- [ ] Collection mode: every hypothesis is explicitly marked as such, not presented as a finding.
- [ ] Competitive analysis is current and verifiable.
- [ ] Features and capabilities are accurately represented.
- [ ] Market trends are backed by research.
- [ ] Business model and strategy match the company's actual direction (or stated intent, in Collection mode).

**AI optimization:**
- [ ] Content enables contextually appropriate customer support.
- [ ] Personas include specific AI-interaction guidelines.
- [ ] Communication guidelines are actionable for AI systems.
- [ ] Cross-references create comprehensive business intelligence.

**Completeness:**
- [ ] Every business-context layer is addressed (even if some are marked "not applicable yet" in Collection mode).
- [ ] Customer journey covers the full lifecycle, or the intended one.
- [ ] Competitive landscape includes direct and indirect competitors.
- [ ] Communication guidelines match customer preferences, where known.

## Execution strategy

1. **Customer-first**: start with deep customer understanding before strategy — from data if it exists, from the interview if it doesn't.
2. **Evidence-based, or explicitly hypothesis-based**: ground business intelligence in real data and feedback when available; when it isn't, say so plainly instead of fabricating specificity.
3. **Multi-file**: always create linked, focused files per business area.
4. **Market-informed**: reflect current market realities, not assumptions, wherever research is possible.
5. **Cross-functional**: connect business context to the technical implementation.

## Adaptation guidelines

**By business model:** B2B SaaS emphasizes enterprise sales and competitive differentiation; open source focuses on community/contributor engagement and monetization; B2C highlights UX, conversion, and retention; developer tools prioritize technical accuracy and ecosystem integration.

**By company stage:** early-stage focuses on customer discovery and product-market fit; growth-stage emphasizes scaling and market expansion; enterprise-stage needs comprehensive compliance and partnership documentation.

## Error handling

Analysis mode, when information can't be determined: mark the section "RESEARCH NEEDED" with the specific data required, rather than guessing.

Collection mode, when the human doesn't have an answer yet: mark it "OPEN QUESTION" rather than inventing one — an honest gap is more useful than a confident guess dressed up as a fact.

The goal is actionable business intelligence — grounded in real data where it exists, and honestly labeled as hypothesis where it doesn't — that lets AI systems understand customers, market dynamics, and strategic context well enough to provide real support and decision-making assistance.
