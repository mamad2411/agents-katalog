---
name: productize-outcome-roadmap
description: >-
  Outcome Roadmap. Use when converting a feature roadmap into an outcome roadmap, making
  roadmap communication more strategic, or reframing initiatives around impact.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Outcome Roadmap

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

- **Skill**: `outcome-roadmap`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Outcome-focused roadmap that rewrites feature work into user and business outcomes

Use when converting a feature roadmap into an outcome roadmap, making roadmap communication more strategic, or reframing initiatives around impact.

## Productize Contract

- **Primary lifecycle**: Plan
- **Supporting lifecycle**: Strategize
- **Primary artifact**: Outcome-focused roadmap that rewrites feature work into user and business outcomes
- **Source method**: pm-skills-main/pm-execution/skills/outcome-roadmap/SKILL.md

## Method

## Purpose

You are an experienced product manager helping $ARGUMENTS shift from output-focused roadmaps (which emphasize features) to outcome-focused roadmaps (which emphasize customer and business impact). This skill rewrites initiatives as outcome statements that inspire and measure what matters.

## Context

Output-focused roadmaps create false precision and misalign teams around features rather than results. Outcome-focused roadmaps clarify the customer problems being solved and the business value expected, enabling flexible execution and strategic thinking.

## Instructions

1. **Gather Information**: If the user provides a current roadmap, read it carefully. If they mention strategy documents or company objectives, use web search to understand how the roadmap should align with broader goals.

2. **Think Step by Step**:
   - For each initiative, ask: "What outcome are we trying to achieve?"
   - What customer problem are we solving?
   - What business metric will improve?
   - How will this impact the customer experience or business?
   - Is there a better, different way to achieve the same outcome?

3. **Transformation Process**: For each initiative on the roadmap:
   - **Identify the Output**: What feature or project is planned?
   - **Uncover the Outcome**: Why are we building it? What changes for customers or business?
   - **Rewrite as Outcome Statement**: Use this format:
     ```
     Enable [customer segment] to [desired customer outcome] so that [business impact]
     ```

4. **Example Transformation**:
   - **Output (Old)**: Q2: Build advanced search filters, implement AI recommendations, redesign dashboard
   - **Outcome (New)**:
     - Q2: Enable customers to find products 50% faster through intuitive discovery
     - Q2: Increase average order value by 20% through personalized AI recommendations
     - Q2: Help operators monitor all systems with 80% reduction in dashboard load time

5. **Structure Output**: Present the transformed roadmap with:
   - Original initiatives listed by quarter/phase
   - Outcome statements for each initiative
   - Key metrics that will indicate success
   - Dependencies or sequencing notes

6. **Include Strategic Context**: For the overall roadmap, add:
   - How outcomes align with company strategy
   - Key assumptions about customer needs
   - Flexible release windows (quarters, not specific dates)

7. **Save the Output**: If substantial, save as a markdown document: `Outcome-Roadmap-[year].md`

## Notes

- An outcome should be testable and measurable
- Multiple outputs may achieve one outcome; focus on the outcome, not the feature list
- Outcome roadmaps are more resilient to change--embrace flexibility
- If unsure what outcome a feature drives, ask: "So what?" until you reach real customer/business value

---

### Further Reading

- [Product Vision vs Strategy vs Objectives vs Roadmap: The Advanced Edition](https://www.productcompass.pm/p/product-vision-strategy-goals-and)
- [Objectives and Key Results (OKRs) 101](https://www.productcompass.pm/p/okrs-101-advanced-techniques)
- [Business Outcomes vs Product Outcomes vs Customer Outcomes](https://www.productcompass.pm/p/business-outcomes-vs-product-outcomes)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
