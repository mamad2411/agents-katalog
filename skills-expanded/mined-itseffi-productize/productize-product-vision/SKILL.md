---
name: productize-product-vision
description: >-
  Product Vision. Use when defining, sharpening, or stress-testing a product vision that needs
  to motivate teams and align stakeholders.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product Vision

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

- **Skill**: `product-vision`
- **Lifecycle**: Strategize
- **Category**: Stakeholder Communication
- **Primary artifact**: Product Vision strategy memo with choices, tradeoffs, risks, and recommended next move

Use when defining, sharpening, or stress-testing a product vision that needs to motivate teams and align stakeholders.

## Productize Contract

- **Primary lifecycle**: Strategize
- **Supporting lifecycle**: Align
- **Primary artifact**: Product vision statement with audience, future state, strategic principles, and alignment notes
- **Source method**: pm-skills-main/pm-product-strategy/skills/product-vision/SKILL.md

## Method

## Metadata
- **Name**: product-vision
- **Description**: Brainstorm an inspiring, achievable, and emotional product vision. Use when defining or refining product vision, aligning teams around a north star, or creating a vision statement.
- **Triggers**: product vision, vision statement, create vision, inspiring vision, north star vision

### Domain Context

A product **vision** answers: "How can we inspire people? What are we aspiring to achieve? What values do we uphold?" Vision evolves with strategy -- it's a living statement, not a one-time exercise. It should make people feel something, not just understand the direction.

## Instructions

You are a veteran product leader developing a compelling product vision.

Your task is to brainstorm a product vision for $ARGUMENTS.

## Input Requirements
- Information about your company and product (you may read files from the user's workspace)
- Current state, market positioning, or any relevant context

## Output
Provide a vision statement that is:
1. **Inspiring** - Motivates teams to wake up and commit to the goal
2. **Achievable** - Realistic based on resources, market, and capabilities
3. **Emotional** - Creates meaning and connection

## Process
1. Review provided company and product information
2. Identify the core problem being solved
3. Envision the ideal future state for customers and the company
4. Draft multiple vision options (3-5 variations)
5. Select the strongest vision and briefly explain your rationale
6. Highlight how this vision aligns with company values and market opportunity

## Notes
- A great vision is memorable and can be communicated in one sentence
- Balance ambition with credibility
- Consider the perspective of customers, employees, and investors
- Avoid jargon; use clear, emotionally resonant language

---

### Further Reading

- [Product Vision vs Strategy vs Objectives vs Roadmap: The Advanced Edition](https://www.productcompass.pm/p/product-vision-strategy-goals-and)
- [Introducing the Product Strategy Canvas](https://www.productcompass.pm/p/new-product-strategy-canvas)
- [From Strategy to Objectives Masterclass](https://www.productcompass.pm/p/product-vision-strategy-objectives-course) (video course)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
