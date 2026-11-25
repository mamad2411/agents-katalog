---
name: productize-lean-canvas
description: >-
  Lean Canvas. Use when turning a startup idea or early product concept into a Lean Canvas
  with hypotheses and validation priorities.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Lean Canvas

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

- **Skill**: `lean-canvas`
- **Lifecycle**: Think
- **Category**: Business Model
- **Primary artifact**: Lean Canvas with problem, solution, UVP, metrics, channels, revenue, costs, and risk priorities

Use when turning a startup idea or early product concept into a Lean Canvas with hypotheses and validation priorities.

## Productize Contract

- **Primary lifecycle**: Think
- **Supporting lifecycle**: Strategize
- **Primary artifact**: Lean Canvas with problem, solution, UVP, metrics, channels, revenue, costs, and risk priorities
- **Source method**: pm-skills-main/pm-product-strategy/skills/lean-canvas/SKILL.md

## Method

## Metadata
- **Name**: lean-canvas
- **Description**: Generate a Lean Canvas business model with detailed sections for problem, solution, metrics, cost structure, UVP, unfair advantage, channels, segments, and revenue.
- **Triggers**: lean canvas, startup canvas, lean model, business hypothesis

## Instructions

You are a business model strategist designing a Lean Canvas for $ARGUMENTS.

Your task is to create a comprehensive Lean Canvas that outlines the business hypothesis and key business model assumptions for the product.

## Input Requirements
- Product or feature description
- Target customer segment(s)
- Market context and problem space
- Any available metrics or business constraints

## Lean Canvas Template

### Section 1: Product Definition

**1. Problem**
- Top 3 customer problems or needs
- Customer pains and frustrations
- Current unsatisfactory solutions

**2. Solution**
- Top 3 features or approaches
- How each feature addresses the problem
- Why this solution is novel or better

**3. Unique Value Proposition (UVP)**
- Concise, memorable statement
- Why customers choose you over alternatives
- What makes you different (not just "better")

**4. Unfair Advantage**
- What defensibility exists?
- Barriers to competition (network effects, brand, IP, switching costs)
- What competitors can't easily replicate

### Section 2: Market & Traction

**5. Customer Segments**
- Who is the target customer?
- Early adopters and first segment
- Customer personas or archetypes
- How large is the addressable market?

**6. Channels**
- How do you reach customers?
- Primary acquisition channels
- Distribution and sales approach
- How do customers find you?

**7. Revenue Streams**
- How do you make money?
- Pricing model or revenue per customer
- Customer lifetime value (LTV)
- Revenue growth assumptions

### Section 3: Economics & Validation

**8. Cost Structure**
- Fixed costs (salaries, infrastructure, facilities)
- Variable costs (COGS, transaction costs, support)
- Key cost drivers
- Cost per customer acquisition (CAC)

**9. Key Metrics**
- Activation: How do users get value quickly?
- Retention: How many users stick around?
- Revenue: How do we measure financial success?
- North Star metric for the business

## Output Process
1. Define the core problem(s) being solved
2. Outline 2-3 solution approaches
3. Craft a compelling UVP
4. Identify what creates competitive advantage
5. Target 1-2 customer segments
6. Map acquisition channels
7. Define revenue model and pricing
8. Estimate cost structure
9. Identify 3-5 critical metrics to track
10. Surface key assumptions and hypotheses
11. Suggest validation experiments (landing page, interviews, MVP)

### Domain Context

**Lean Canvas vs Business Model Canvas vs Startup Canvas**:

Lean Canvas (Ash Maurya) is a startup-focused adaptation of the Business Model Canvas that replaces Partners/Activities/Resources with Problem/Solution/Unfair Advantage. It's fast and hypothesis-driven, but has known limitations:

- **Redundancy**: "Problem" overlaps with Market Segments (markets are defined by problems/JTBD), and "Solution" overlaps with Value Proposition (which by definition includes features). This can create confusion about what goes where.
- **Missing strategic sections**: No vision (why should your team wake up every day?), no trade-offs (what you choose NOT to do), no relative costs (low cost vs unique value positioning), no key metrics.
- **Narrow defensibility**: "Unfair Advantage" focuses on one defensive element, but strong strategy is hard to copy as an integrated whole -- not because of a single advantage.
- **No coherence check**: Doesn't address whether all strategic choices reinforce each other.

**When to use Lean Canvas**: Quick hypothesis testing when you need speed over completeness. Best as a brainstorming tool, not a strategy document.

**Consider instead**: **Startup Canvas** (Pawe Huryn) separates strategy (9 sections from the Product Strategy Canvas) from business model (Cost Structure + Revenue Streams). Recommended when you need both strategic clarity AND a business model for a new product.

## Notes
- The Lean Canvas is designed for rapid hypothesis testing
- Focus on addressing the riskiest assumptions first
- Update the canvas as you learn and validate
- Each section should be specific and measurable where possible
- This canvas helps align founding teams on business strategy

---

### Further Reading

- [Startup Canvas: Product Strategy and a Business Model for a New Product](https://www.productcompass.pm/p/startup-canvas)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
