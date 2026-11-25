---
name: productize-gtm-strategy
description: >-
  GTM Strategy. Use when creating a full go-to-market plan for a product, feature, market
  entry, launch, or repositioning effort.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# GTM Strategy

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

- **Skill**: `gtm-strategy`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: Go-to-market plan with audience, positioning, channels, metrics, and launch timeline

Use when creating a full go-to-market plan for a product, feature, market entry, launch, or repositioning effort.

## Productize Contract

- **Primary lifecycle**: Growth
- **Supporting lifecycle**: Launch & Learn
- **Primary artifact**: Go-to-market plan with audience, positioning, channels, metrics, and launch timeline
- **Source method**: pm-skills-main/pm-go-to-market/skills/gtm-strategy/SKILL.md

## Method

## Overview
Create a comprehensive go-to-market strategy for a product launch. This skill covers marketing channels, messaging development, success metrics definition, and launch planning.

## When to Use
- Planning a product launch
- Creating a GTM plan from scratch
- Defining a launch strategy for a new market
- Developing product-to-market fit strategy
- Preparing a product go-live roadmap

## How It Works

### Step 1: Gather Research Data
The system will help you load and analyze early research about your product and target market. Provide:
- Product description and key features
- Target market segment details
- Market research or validation data
- Competitive landscape information
- Any available customer interviews or survey data

### Step 2: Define Marketing Channels
Evaluate which channels best reach your target audience:
- Digital marketing channels (paid search, social media, display)
- Content and inbound channels (blog, SEO, thought leadership)
- Sales and outbound channels (direct outreach, partnerships)
- Community and grassroots channels
- Product-led and viral channels

### Step 3: Develop Messaging
Create audience-specific messaging that resonates:
- Core value proposition for target segment
- Key differentiators and competitive advantages
- Pain point validation and solution mapping
- Proof points and social proof strategies
- Channel-specific messaging variations

### Step 4: Define Success Metrics
Establish measurable KPIs to track launch success:
- Awareness metrics (impressions, reach, brand recall)
- Engagement metrics (CTR, cost per engagement, time on site)
- Conversion metrics (signups, demos requested, trials started)
- Revenue metrics (MRR, customer acquisition cost, lifetime value)
- Market metrics (market share, segment penetration)

### Step 5: Create Launch Plan
Build a phased launch timeline:
- Pre-launch preparation (messaging, channels, timeline)
- Launch day activities and announcements
- Post-launch momentum (content, partnerships, communities)
- Measurement and optimization cadence
- Success criteria and go/no-go decision points

## Input Format
Use $ARGUMENTS to pass:
- Product name and description
- Target market segment
- Research data or file path
- Launch timeline and constraints
- Budget or resource limitations

## Output
A structured GTM strategy document including:
- Recommended marketing channels with justification
- Channel-specific messaging and positioning
- Launch timeline with key milestones
- KPI targets and measurement framework
- Risk mitigation strategies
- 90-day execution roadmap

## Framework
This skill applies Product Compass GTM strategy methodology, focusing on market selection, channel fit, and message-market fit for sustainable product growth.

## Tips
- Start with your most confident customer segment
- Validate assumptions through customer interviews before full launch
- Focus on a few channels excellently rather than many channels poorly
- Establish baseline metrics before launch to measure impact
- Plan for feedback loops and optimization

---

### Further Reading

- [5 GTM Principles You Should Know as a PM](https://www.productcompass.pm/p/5-gtm-principles-with-frameworks-templates)
- [OpenAI's Product Leader Shares 3-Layer Distribution Framework To Win Mind & Market Share in the AI World](https://www.productcompass.pm/p/distribution-framework-ai-products)
- [Product-Led Growth 101, Part 1/2](https://www.productcompass.pm/p/product-led-growth-101-12)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
- [How to Achieve Product-Market Fit? Part I: Market and Value Proposition](https://www.productcompass.pm/p/how-to-achieve-the-product-market)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
