---
name: productize-gtm-motions
description: >-
  GTM Motions. Use when selecting between PLG, sales-led, inbound, outbound, paid, community,
  partner, ABM, or hybrid go-to-market motions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# GTM Motions

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

- **Skill**: `gtm-motions`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: GTM motion selection brief with channel fit, operating requirements, and experiment plan

Use when selecting between PLG, sales-led, inbound, outbound, paid, community, partner, ABM, or hybrid go-to-market motions.

## Productize Contract

- **Primary lifecycle**: Growth
- **Supporting lifecycle**: none
- **Primary artifact**: GTM motion selection brief with channel fit, operating requirements, and experiment plan
- **Source method**: pm-skills-main/pm-go-to-market/skills/gtm-motions/SKILL.md

## Method

## Overview
Identify and evaluate the best go-to-market motions for your product. This skill analyzes seven proven GTM approaches with specific tools and tactics to help you build a balanced acquisition strategy.

## When to Use
- Selecting marketing channels for your product
- Choosing between inbound vs outbound strategy
- Building your GTM toolkit and tech stack
- Evaluating PLG vs traditional sales motion
- Planning cross-channel marketing campaigns

## The 7 GTM Motions

### 1. Inbound Marketing
Attract customers through valuable content and thought leadership.
- **Tools**: LinkedIn, SEMRush, Grammarly, HubSpot, Airtable
- **Tactics**: Blog content, webinars, whitepapers, SEO, email nurture sequences
- **Best For**: B2B SaaS, technical products, long sales cycles
- **Strength**: Builds brand authority and attracts high-intent prospects
- **Challenge**: Requires consistent content creation; slower to show results

### 2. Outbound Sales
Proactively reach target prospects through direct engagement.
- **Tools**: LinkedIn Sales Navigator, ZoomInfo, Lemlist, Apollo, Hunter
- **Tactics**: Cold email campaigns, LinkedIn outreach, phone prospecting, personalized demos
- **Best For**: Enterprise sales, high-value contracts, niche markets
- **Strength**: Predictable pipeline generation; control over target selection
- **Challenge**: Low response rates; resource-intensive; requires skilled sales team

### 3. Paid Digital Advertising
Reach target audiences through paid channels with precision targeting.
- **Tools**: Google Ads, Meta Ads, LinkedIn Ads, Newswire, Retargeting platforms
- **Tactics**: Search ads, display advertising, social ads, video advertising, retargeting
- **Best For**: Products with clear target demographics, competitive keywords
- **Strength**: Fast results; scalable; measurable ROI; precise targeting
- **Challenge**: Can be expensive; requires continuous optimization; competitive

### 4. Community Marketing
Build engaged communities where customers help each other and spread the word.
- **Tools**: Slack, Reddit, Discord, Circle, Mighty Networks, WhatsApp
- **Tactics**: Community forums, user groups, events, mentorship, ambassador programs
- **Best For**: Developer products, communities of practice, loyal user bases
- **Strength**: Builds loyalty; organic word-of-mouth; valuable feedback; low CAC
- **Challenge**: Requires active moderation; time to build critical mass

### 5. Partner Marketing
Leverage partner networks to co-market and reach new audiences.
- **Tools**: Miro, AWS Startups, Oracle Partners, Stripe, Shopify App Store
- **Tactics**: Partner integrations, co-marketing agreements, channel partnerships, resellers
- **Best For**: Complementary products, platform ecosystems, expanding market reach
- **Strength**: Access to established customer bases; shared costs; credibility
- **Challenge**: Partner alignment; revenue sharing; dependency on partners

### 6. Account-Based Marketing (ABM)
Treat high-value accounts as individual markets with personalized campaigns.
- **Tools**: Pipedrive, Hunter, Clay, 6sense, Terminus, Demandbase
- **Tactics**: Personalized messaging, account-targeted content, coordinated sales/marketing
- **Best For**: Enterprise deals, limited target accounts, high deal values
- **Strength**: Higher conversion rates; larger deal sizes; strong sales-marketing alignment
- **Challenge**: Requires detailed account research; resource intensive; not scalable to SMB

### 7. Product-Led Growth (PLG)
Drive adoption through the product experience itself with minimal sales friction.
- **Tools**: Hotjar, Amplitude, Sentry, PostHog, Intercom, Appcues
- **Tactics**: Free trials, freemium models, in-app onboarding, self-serve demos, product analytics
- **Best For**: Self-service products, SMB market, low ACV, viral potential
- **Strength**: Low CAC; aligns product and growth; strong PMF signals; scalable
- **Challenge**: Requires excellent product experience; lower price points; longer ROI

## How It Works

### Step 1: Understand Your Product
Define product characteristics:
- Price point and ACV (contract value)
- Sales cycle length
- Buyer type and decision-making process
- Product complexity and learning curve
- Target market size and concentration

### Step 2: Evaluate Market Conditions
Assess your market dynamics:
- Competitive intensity of your keywords/channels
- Target audience location and accessibility
- Budget availability for paid channels
- Your team size and capabilities
- Timeline to revenue generation

### Step 3: Score Each Motion
Rate fit for your product (1-10 scale):
- Inbound: Content creation capability, brand building timeline
- Outbound: Prospect list availability, sales team capacity
- Paid: Budget flexibility, target audience clarity, conversion potential
- Community: Existing communities, product network effects
- Partners: Complementary products, channel availability
- ABM: Deal size and account concentration
- PLG: Product trial-ability, pricing flexibility

### Step 4: Design Motion Stack
Select and prioritize 2-4 motions to execute:
- Primary motion (highest potential for your business)
- Secondary motions (complementary acquisition channels)
- Motion sequencing (which to start first)
- Resource allocation across channels

### Step 5: Build Execution Plan
Create 90-day implementation roadmap:
- Quick wins and early validation
- Team and tool requirements
- Success metrics for each motion
- Optimization and scaling strategy
- Budget and resource allocation

## Input Format
Use $ARGUMENTS to pass:
- Product description and positioning
- Target customer profile and market
- Price point and sales cycle
- Team size and capabilities
- Budget and timeline constraints
- Existing channels or data

## Output
A comprehensive GTM motions analysis including:
- Scoring of all 7 motions for your product
- Recommended motion stack (primary and secondary)
- Tool recommendations for each motion
- 90-day execution plan with milestones
- Resource and budget requirements
- Success metrics and measurement framework
- Competitive differentiation through motion choice

## Framework
Based on Product Compass GTM motion analysis. Provides a systematic approach to balancing customer acquisition across multiple channels.

## Tips
- Most successful products use 2-4 complementary motions
- Start with your strongest motion; add complexity gradually
- Paid channels fund growth while organic channels build long-term value
- Revisit motion mix quarterly as company scales
- Combine inbound (brand) with outbound (sales) for B2B strength
- Use PLG to reduce CAC; use paid to accelerate proven channels

---

### Further Reading

- [5 GTM Principles You Should Know as a PM](https://www.productcompass.pm/p/5-gtm-principles-with-frameworks-templates)
- [OpenAI's Product Leader Shares 3-Layer Distribution Framework To Win Mind & Market Share in the AI World](https://www.productcompass.pm/p/distribution-framework-ai-products)
- [Product Management vs. Product Marketing vs. Product Growth 101](https://www.productcompass.pm/p/product-management-vs-product-marketing)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
