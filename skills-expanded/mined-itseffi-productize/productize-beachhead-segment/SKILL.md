---
name: productize-beachhead-segment
description: >-
  Beachhead Segment. Use when choosing the first market segment, entry wedge, launch audience,
  early ICP, or 0-to-1 customer focus.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Beachhead Segment

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

- **Skill**: `beachhead-segment`
- **Lifecycle**: Strategize
- **Category**: Venture / 0-1
- **Primary artifact**: Beachhead segment decision brief with scoring, wedge rationale, and expansion path

Use when choosing the first market segment, entry wedge, launch audience, early ICP, or 0-to-1 customer focus.

## Productize Contract

- **Primary lifecycle**: Strategize
- **Supporting lifecycle**: Growth
- **Primary artifact**: Beachhead segment decision brief with scoring, wedge rationale, and expansion path
- **Source method**: pm-skills-main/pm-go-to-market/skills/beachhead-segment/SKILL.md

## Method

## Overview
Identify the first beachhead market segment for product launch. This skill evaluates potential market segments against key criteria to find your initial winning segment that enables fast PMF validation and adjacent expansion.

## When to Use
- Choosing a first market for your product
- Targeting an initial customer segment
- Planning initial market entry strategy
- Deciding where to focus limited resources
- Validating GTM assumptions with early adopters

## Key Evaluation Criteria

### 1. Burning Pain Point
Does this segment experience an acute, unmet problem?
- Daily frustration with the status quo
- Significant productivity loss or cost impact
- Emotional urgency to find a solution
- Current workarounds are expensive or fragile
- Problem is getting worse over time

### 2. Willingness to Pay
Does this segment have budget and motivation to pay for a solution?
- Documented budget allocation for this problem area
- ROI is clear and compelling (value > cost)
- Economic impact of problem justifies solution cost
- Decision-maker has autonomy or influence over budget
- No free or DIY alternatives that fully satisfy need

### 3. Winnable Market Share
Can you realistically capture 60-70% of this segment in 3-18 months?
- Segment is large enough but not oversaturated
- Limited competition or easy differentiation
- Market players are fragmented or complacent
- Your product has clear competitive advantage
- You have unique access or distribution advantage

### 4. Referral Potential
Will customers naturally refer or recommend to others?
- Segment contains professional communities
- Customers interact with adjacent segments (expansion opportunity)
- High word-of-mouth culture in this industry
- Network effects within the segment
- Solving problem for one creates demand in adjacent segments

## How It Works

### Step 1: List Potential Segments
Brainstorm all possible target segments:
- Industry verticals (SaaS, healthcare, manufacturing, etc.)
- Company size (SMB, mid-market, enterprise)
- Job titles or roles
- Geographic regions
- Use cases or use-case variations
- Customer maturity level

### Step 2: Research Pain Points
Validate burning pain in each segment:
- Customer interviews and discovery calls
- Problem validation through surveys
- Market research and analyst reports
- Competitor positioning and customer reviews
- Quantify cost/impact of the problem
- Identify current workarounds and limitations

### Step 3: Assess Willingness to Pay
Determine budget and economic viability:
- Segment's budget for this problem category
- ROI calculation (value gained vs cost)
- Current spending on solutions or workarounds
- Budget decision-making process
- Typical deal size expectations
- Pricing sensitivity in the segment

### Step 4: Evaluate Winnability
Assess realistic market share potential:
- Total addressable market (TAM) size
- Competitive landscape and positioning
- Your differentiation or unfair advantage
- Distribution access to this segment
- Time and resources required
- Market growth and momentum

### Step 5: Identify Referral Pathways
Map expansion opportunities:
- Adjacent segments that reference segment influences
- Network effects within the segment
- Professional communities and associations
- Customer-to-customer recommendations
- Natural expansion path to adjacent markets
- Viral or network effects from solving core pain

### Step 6: Select Beachhead
Choose your primary launch segment:
- Highest combined score across four criteria
- Most achievable for your current resources
- Shortest path to PMF and revenue
- Best reference for adjacent expansion
- Most enthusiastic early customer cohort

## Input Format
Use $ARGUMENTS to pass:
- Product description and capabilities
- Initial market research and validation data
- Potential segment options
- Constraints and limitations
- Timeline and resource constraints
- Current customer data or feedback

## Output
A beachhead segment analysis including:
- Top 3-5 recommended segments with scoring
- Primary beachhead segment recommendation
- Pain point validation and evidence
- Willingness to pay assessment and pricing guidance
- Realistic market share and revenue projections
- Referral and expansion pathways to adjacent segments
- 90-day customer acquisition plan for beachhead
- Post-beachhead expansion roadmap

## Framework
Based on Geoffrey Moore's beachhead market strategy in "Crossing the Chasm." Focuses on finding the smallest winnable, referenceable market that validates PMF and enables expansion.

## Tips
- Start absurdly specific. A niche beachhead is better than a vague mass market
- Choose the segment most likely to evangelize your solution
- Validate all four criteria with at least 10 customer interviews
- Select segment with fastest path to revenue and references
- Ensure beachhead can reference to adjacent market segments
- Focus all resources on dominating the beachhead (not diluting efforts)
- Plan exit from beachhead only after 60%+ market share

---

### Further Reading

- [5 GTM Principles You Should Know as a PM](https://www.productcompass.pm/p/5-gtm-principles-with-frameworks-templates)
- [Product-Led Growth 101, Part 1/2](https://www.productcompass.pm/p/product-led-growth-101-12)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
- [How to Achieve Product-Market Fit? Part I: Market and Value Proposition](https://www.productcompass.pm/p/how-to-achieve-the-product-market)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
