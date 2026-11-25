---
name: productize-north-star-metric
description: >-
  North Star Metric. Use when choosing or revising a North Star Metric, defining input
  metrics, aligning teams around product value, or deciding what the product should measure.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# North Star Metric

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

- **Skill**: `north-star-metric`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: North Star metric definition with input metrics, validation criteria, and instrumentation notes

Use when choosing or revising a North Star Metric, defining input metrics, aligning teams around product value, or deciding what the product should measure.

## Productize Contract

- **Primary lifecycle**: Measure
- **Supporting lifecycle**: none
- **Primary artifact**: North Star metric definition with input metrics, validation criteria, and instrumentation notes
- **Source method**: pm-skills-main/pm-marketing-growth/skills/north-star-metric/SKILL.md

## Method

Identify a North Star Metric and 3-5 Input Metrics that form a metrics constellation. Classifies the business game being played and validates against criteria for an effective North Star. Use when defining key metrics, setting up a metrics framework, or choosing what to measure.

## Domain Context

NSM is **NOT**: multiple metrics, a revenue/LTV metric (must be customer-centric), an OKR (that's a goal-setting technique), or a strategy (but choosing the right NSM is a strategic choice).

NSM **IS**: a single, customer-centric KPI that reflects the value customers get from the product and serves as a leading indicator of long-term business success. You can use Key Results (OKRs) to express expected change in NSM.

Free resource: [The North Star Framework 101 (PDF)](https://learn.productcompass.pm/nsm101)

## When to Use

- Defining your company's key metric framework
- Setting up a metrics tracking system
- Choosing what to measure and optimize for
- Evaluating potential North Star candidates
- Triggers: North Star metric, north star, key metric, what to measure, metrics framework, OMTM

## The Three Business Games

Before identifying your North Star, classify your business into one of these three games:

- **Attention Game**: How much time do customers spend using your product? (Examples: Facebook, Spotify, YouTube, TikTok)
- **Transaction Game**: How many transactions occur between customers and your platform? (Examples: Amazon, Uber, Airbnb, PayPal)
- **Productivity Game**: How efficiently can someone complete their work or achieve their goals? (Examples: Canva, Dropbox, Loom, Notion)

## Prompt

You are a metrics strategist specializing in North Star metrics and growth measurement frameworks.

Given the following business context: $ARGUMENTS

**Step 1: Classify the Business Game**
Determine which game this company plays: Attention, Transaction, or Productivity.

**Step 2: Identify the North Star Metric**
Suggest a single metric that meets all seven criteria for an effective North Star:

1. **Easy to Understand**: Clear definition that everyone in the organization comprehends
2. **Customer-Centric**: Reflects value delivered to customers, not just revenue or activity
3. **Sustainable Value**: Indicates habits and long-term customer engagement
4. **Vision Alignment**: Represents meaningful progress toward the company's vision and mission
5. **Quantitative**: Measurable with clear, numeric tracking
6. **Actionable**: Teams can directly influence it through product, marketing, and operational changes
7. **Leading Indicator**: Predicts future business success and revenue growth

**Step 3: Identify Input Metrics**
Define 3-5 Input Metrics (also called leading indicators) that most directly influence and drive the North Star Metric. Each input metric should:
- Be easier to move in the short term
- Directly contribute to the North Star outcome
- Help identify where optimization efforts should focus

## Tips for Best Results

- Provide details about your business model and revenue model
- Share your company's vision, mission, or long-term goals
- Include current metrics you're tracking
- Mention key customer segments and use cases
- Describe the primary value you deliver to customers

---

### Further Reading

- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
