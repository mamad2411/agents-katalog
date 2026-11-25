---
name: productize-competitive-brief
description: >-
  Create a competitive analysis brief for one or more competitors or a feature area. Use when
  informing product strategy or feature prioritization, building sales battle cards, prepping
  board or investor materials, or deciding where to differentiate versus achieve parity.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Competitive Brief

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

- **Skill**: `competitive-brief`
- **Lifecycle**: Strategize
- **Category**: Marketing
- **Primary artifact**: Competitive Brief strategy memo with choices, tradeoffs, risks, and recommended next move

Create a competitive analysis brief for one or more competitors or a feature area.

## Argument Hint

`<competitor or feature area>`

## Usage

```text
/competitive-brief $ARGUMENTS
```

## Extended Reference

Load `references/extended-reference.md` when the request mentions `competitive battlecard`, `sales battlecard`, `objection handling`, `win loss`. Use this reference material to sharpen this Productize skill.

## Workflow

### 1. Scope the Analysis

Ask the user:
- **Competitor(s)**: Which specific competitor(s) to analyze? Or a feature area to compare across competitors?
- **Focus**: Full product comparison, specific feature area, pricing/packaging, go-to-market, or positioning?
- **Context**: What decision will this inform? Product strategy, sales enablement, investor/board materials, or feature prioritization?

### 2. Research

Use web research when available:
- Product pages and feature lists
- Pricing pages and packaging
- Recent product launches, blog posts, and changelogs
- Press coverage and analyst reports
- Customer reviews and ratings from G2, Capterra, TrustRadius, or similar sources
- Job postings as signals of strategic direction
- Social media and community discussions

If a knowledge base is connected:
- Search for existing competitive analysis documents
- Find win/loss reports or sales battle cards
- Pull prior competitive research

If chat is connected:
- Search for competitive mentions in sales or product channels
- Find recent deal feedback involving competitors

### 3. Generate the Brief

#### Competitor Overview

For each competitor:
- Company summary: founding, size, funding/revenue if public, target market
- Product positioning: how they describe themselves, who they target
- Recent momentum: launches, funding, partnerships, customer wins

#### Feature Comparison

Compare capabilities across key areas relevant to the analysis. Use the feature comparison matrix guidance below for rating scales and templates.

#### Positioning Analysis

Analyze how each competitor positions themselves: target customer, category claim, key differentiator, and value proposition. Use the positioning statement template and message architecture levels below.

#### Strengths and Weaknesses

For each competitor:
- **Strengths**: Where they genuinely excel. What customers praise.
- **Weaknesses**: Where they fall short. What customers complain about.
- Be honest and evidence-based. Do not dismiss competitors or inflate their weaknesses.

#### Opportunities

Based on the analysis:
- Where are there gaps in competitor offerings we could exploit?
- What are customers asking for that no one provides well?
- Where are competitors making bets we disagree with?
- What market shifts could advantage our approach?

#### Threats

- Where are competitors investing heavily?
- What competitive moves could disrupt our position?
- Where are we most vulnerable?
- What would a nightmare-scenario competitive move look like?

#### Strategic Implications

Tie the analysis back to product strategy:
- What should we build, accelerate, or deprioritize based on this analysis?
- Where should we differentiate versus achieve parity?
- How should we adjust positioning or messaging?
- What should we monitor going forward?

### 4. Follow Up

After generating the brief:
- Ask if the user wants to dive deeper on any section
- Offer to create a one-page summary for executives
- Offer to create sales battle cards for competitive deals
- Offer to draft a "how to win against [competitor]" guide
- Offer to set up a monitoring plan for competitive moves

## Competitive Landscape Mapping

### Identifying the Competitive Set

Define competitors at multiple levels:

**Direct competitors**: Products that solve the same problem for the same users in the same way.
- These are the products your customers actively evaluate against you.
- They appear in deals, customer comparisons, and review-site matchups.

**Indirect competitors**: Products that solve the same problem differently.
- Different approach to the same user need, such as spreadsheets versus a dedicated project management tool.
- Include non-consumption: sometimes the competitor is doing nothing or using a manual process.

**Adjacent competitors**: Products that do not compete today but could.
- Companies with similar technology, customer base, or distribution that could expand into your space.
- Larger platforms that could add your functionality as a feature.
- Startups attacking a niche that could grow into your core market.

**Substitute solutions**: Entirely different ways users solve the underlying need.
- Hiring a person instead of buying software.
- Using a general-purpose tool such as Excel or email instead of a specialized one.
- Outsourcing the process entirely.

### Landscape Map

Position competitors on meaningful dimensions:

Common axes:
- Breadth versus depth: suite versus point solution
- SMB versus enterprise: market segment focus
- Self-serve versus sales-led: go-to-market approach
- Simple versus powerful: product complexity
- Horizontal versus vertical: general purpose versus industry-specific

Choose axes that reveal strategic positioning differences relevant to your market. The right axes make competitive dynamics visible.

### Monitoring the Landscape

Track competitive movements over time:
- Product launches and feature releases: changelogs, blog posts, press releases
- Pricing and packaging changes
- Funding rounds and acquisitions
- Key hires and job postings
- Customer wins and losses, especially your wins/losses
- Analyst and review coverage
- Partnership announcements

## Feature Comparison Matrices

### Building a Feature Comparison

1. Define capability areas: Group features into functional categories that matter to buyers, not your internal architecture. Use the categories buyers use when evaluating.
2. List specific capabilities: Under each area, list the specific features or capabilities to compare.
3. Rate each competitor: Use a consistent rating scale.

### Rating Scale Options

Simple, recommended for most cases:
- Strong: Market-leading capability. Deep functionality, well-executed.
- Adequate: Functional capability. Gets the job done but is not differentiated.
- Weak: Exists but limited. Significant gaps or poor execution.
- Absent: Does not have this capability.

Detailed, for deep-dive comparisons:
- 5: Best in class. Defines the standard others aspire to.
- 4: Strong. Fully featured and well-executed.
- 3: Adequate. Meets basic needs without differentiation.
- 2: Limited. Exists but with significant gaps.
- 1: Minimal. Barely functional or in early beta.
- 0: Absent. Not available.

### Comparison Matrix Template

```text
| Capability Area | Our Product | Competitor A | Competitor B |
|----------------|-------------|-------------|-------------|
| [Area 1]       |             |             |             |
|   [Feature 1]  | Strong      | Adequate    | Absent      |
|   [Feature 2]  | Adequate    | Strong      | Weak        |
| [Area 2]       |             |             |             |
|   [Feature 3]  | Strong      | Strong      | Adequate    |
```

### Tips for Feature Comparison

- Rate based on real product experience, customer feedback, and reviews, not just marketing claims.
- Features exist on a spectrum. "Has feature X" is less useful than "How well does it do X?"
- Weight the comparison by what matters to target customers, not by total feature count.
- Update regularly because feature comparisons get stale fast.
- Be honest about where competitors are ahead. A comparison that always shows us winning is not credible.
- Include why each capability area matters. Not all features matter equally to buyers.

## Positioning Analysis Frameworks

### Positioning Statement Analysis

For each competitor, extract their positioning:

Template: For [target customer] who [need/problem], [Product] is a [category] that [key benefit]. Unlike [competitor/alternative], [Product] [key differentiator].

Sources for positioning:
- Homepage headline and subheadline
- Product description on app stores or review sites
- Sales pitch decks if available from prospects or public materials
- Analyst briefing materials
- Earnings call language for public companies

### Message Architecture Analysis

How does each competitor communicate value?

- **Level 1 - Category**: What category do they claim? CRM, project management, collaboration platform, etc.
- **Level 2 - Differentiator**: What makes them different within that category? AI-powered, all-in-one, developer-first, etc.
- **Level 3 - Value Proposition**: What outcome do they promise? Close deals faster, ship products faster, never miss a deadline, etc.
- **Level 4 - Proof Points**: What evidence do they provide? Customer logos, metrics, awards, case studies.

### Positioning Gaps and Opportunities

Look for:
- **Unclaimed positions**: Value propositions no competitor owns that matter to buyers.
- **Crowded positions**: Claims every competitor makes that have lost meaning.
- **Emerging positions**: New value propositions driven by market changes such as AI, remote work, or compliance.
- **Vulnerable positions**: Claims competitors make that they cannot fully deliver on.

## Win/Loss Analysis Methodology

### Conducting Win/Loss Analysis

Win/loss analysis reveals why you actually win and lose deals. It is the most actionable competitive intelligence.

Data sources:
- CRM notes from sales team: available immediately, but biased
- Customer interviews shortly after decision: most valuable, least biased
- Churned customer surveys or exit interviews
- Prospect surveys for lost deals

### Win/Loss Interview Questions

For wins:
- What problem were you trying to solve?
- What alternatives did you evaluate?
- Why did you choose us over alternatives?
- What almost made you choose someone else?
- What would we need to lose for you to reconsider?

For losses:
- What problem were you trying to solve?
- What did you end up choosing? Why?
- Where did our product fall short?
- What could we have done differently?
- Would you reconsider us in the future? Under what conditions?

### Analyzing Win/Loss Data

- Track win/loss reasons over time. Are patterns changing?
- Segment by deal type: enterprise versus SMB, new versus expansion, industry vertical.
- Identify the top 3-5 reasons for wins and losses.
- Distinguish product reasons such as features and quality from non-product reasons such as pricing, brand, relationship, and timing.
- Calculate competitive win rates by competitor: what percentage of deals involving each competitor do you win?

### Common Win/Loss Patterns

- **Feature gap**: Competitor has a specific capability you lack that is a dealbreaker.
- **Integration advantage**: Competitor integrates with tools the buyer already uses.
- **Pricing structure**: Not always cheaper; sometimes a different pricing model such as per-seat versus usage-based fits better.
- **Incumbent advantage**: Buyer sticks with what they have because switching cost is too high.
- **Sales execution**: Better demo, faster response, more relevant case studies.
- **Brand/trust**: Buyer chooses the safer or more well-known option.

## Market Trend Identification

### Sources for Trend Identification

- Industry analyst reports: Gartner, Forrester, IDC for market sizing and trends.
- Venture capital: What are VCs funding? Investment themes signal where smart money sees opportunity.
- Conference themes: What are industry events focusing on? What topics draw the biggest audiences?
- Technology shifts: New platforms, APIs, or capabilities that enable new product categories.
- Regulatory changes: New regulations that create requirements or opportunities.
- Customer behavior changes: How are user expectations evolving?
- Talent movement: Where are top people going? What skills are in demand?

### Trend Analysis Framework

For each trend identified:

1. **What is changing?** Describe the trend clearly and specifically.
2. **Why now?** What is driving this change: technology, regulation, behavior, economics?
3. **Who is affected?** Which customer segments or market categories?
4. **What is the timeline?** Is this happening now, in 1-2 years, or 3-5 years?
5. **What is the implication for us?** How should this influence product strategy?
6. **What are competitors doing?** How are competitors responding to this trend?

### Separating Signal From Noise

- **Signals**: Trends backed by behavioral data, growing investment, regulatory action, or customer demand.
- **Noise**: Trends backed only by media hype, conference buzz, or competitor announcements without customer traction.
- Test trends against your own customer data: are your customers asking for this or experiencing this change?
- Be wary of trend-of-the-year hype cycles. Many trends that dominate industry conversation do not materially affect customers for years.

### Strategic Response Options

For each significant trend:
- **Lead**: Invest early and try to define the category or approach. High risk, high reward.
- **Fast follow**: Wait for early signals of customer demand, then move quickly. Lower risk but harder to differentiate.
- **Monitor**: Track the trend but do not invest yet. Set triggers for when to act.
- **Ignore**: Explicitly decide this trend is not relevant to your strategy. Document why.

The right response depends on competitive position, customer base, resources, and trend speed.

## Output Format

Use clear headers and tables for feature comparisons. Keep strategic implications concise and actionable.

Return this structure:

```text
# Competitive Brief: [Competitor(s) or Feature Area]

## Scope
- Competitor(s) or feature area:
- Focus:
- Decision context:
- Sources used:
- Date:

## Executive Summary
- Bottom line:
- Biggest competitive strength:
- Biggest competitive weakness:
- Highest-priority strategic implication:

## Competitive Landscape
[Direct, indirect, adjacent, and substitute competitors.]

## Competitor Overview
[Overview per competitor.]

## Feature Comparison
[Capability matrix plus notes on evidence and caveats.]

## Positioning Analysis
[Positioning statement, message architecture, gaps, and opportunities.]

## Strengths and Weaknesses
[Evidence-based strengths and weaknesses per competitor.]

## Opportunities
[Strategic opportunities and customer gaps.]

## Threats
[Competitive threats and nightmare scenarios.]

## Win/Loss Signals
[Available win/loss patterns, questions to investigate, and deal implications.]

## Market Trends
[Relevant trends, signal/noise assessment, and strategic response.]

## Strategic Implications
[Build, accelerate, deprioritize, differentiate, parity, positioning, and monitoring recommendations.]

## Follow-Ups
[Recommended deeper dives, executive summary, battle card, how-to-win guide, or monitoring plan.]
```

## Tips

- Be honest about competitor strengths. Dismissing competitors makes the analysis useless.
- Focus on what matters to customers, not what matters to product teams.
- Pricing is hard to compare fairly. Note caveats such as different packaging, usage-based versus seat-based pricing, and enterprise custom pricing.
- Job postings are underrated competitive intelligence. A competitor hiring ML engineers signals a strategic direction.
- Customer reviews are valuable because they reveal what real users love and hate, less filtered by marketing.
- The most valuable part of competitive analysis is the "so what": strategic implications. Do not skip it.
- Competitive analysis has a shelf life. Note the date and flag areas that change quickly.
