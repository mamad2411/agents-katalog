---
name: productize-analyze-feature-requests
description: >-
  Analyze Feature Requests. Use when reviewing customer, sales, support, or stakeholder
  feature requests and turning them into prioritized product decisions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Analyze Feature Requests

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

- **Skill**: `analyze-feature-requests`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Feature-request triage report with themes, strategic fit, effort/risk, and backlog recommendations

Use when reviewing customer, sales, support, or stakeholder feature requests and turning them into prioritized product decisions.

## Productize Contract

- **Primary lifecycle**: Plan
- **Supporting lifecycle**: Discover
- **Primary artifact**: Feature-request triage report with themes, strategic fit, effort/risk, and backlog recommendations
- **Source method**: pm-skills-main/pm-product-discovery/skills/analyze-feature-requests/SKILL.md

## Method

## Analyze Feature Requests

Categorize, evaluate, and prioritize customer feature requests against product goals.

### Context

You are analyzing feature requests for **$ARGUMENTS**.

If the user provides files (spreadsheets, CSVs, or documents with feature requests), read and analyze them directly. If data is in a structured format, consider creating a summary table.

### Domain Context

Never allow customers to design solutions. Prioritize **opportunities (problems)**, not features. Use **Opportunity Score** (Dan Olsen) to evaluate customer-reported problems: Opportunity Score = Importance x (1  Satisfaction), normalized to 0-1. See the `prioritization-frameworks` skill for full details and templates.

### Instructions

The user will describe their product goal and provide feature requests. Work through these steps:

1. **Understand the goal**: Confirm the product objective and desired outcomes that will guide prioritization.

2. **Categorize requests into themes**: Group related requests together and name each theme.

3. **Assess strategic alignment**: For each theme, evaluate how well it aligns with the stated goals.

4. **Prioritize the top 3 features** based on:
   - **Impact**: Customer value and number of users affected
   - **Effort**: Development and design resources required
   - **Risk**: Technical and market uncertainty
   - **Strategic alignment**: Fit with product vision and goals

5. **For each top feature**, provide:
   - Rationale (customer needs, strategic alignment)
   - Alternative solutions worth considering
   - High-risk assumptions
   - How to test those assumptions with minimal effort

Think step by step. Save as markdown or create a structured output document.

---

### Further Reading

- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
