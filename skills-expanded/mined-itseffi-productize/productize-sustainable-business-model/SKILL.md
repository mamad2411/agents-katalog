---
name: productize-sustainable-business-model
description: >-
  Design or redesign a business model for sustainability. Use when a company, founder,
  innovation team, or strategist wants to create social/environmental value, reduce
  social/environmental harm, move toward circularity, use sustainable business model patterns,
  combine sustainability patterns, redesign revenue/access/financing, or asks "make this
  business model sustainable", "what sustainable model patterns fit", "how do we turn this
  sustainability challenge into opportunities", or "design a sustainable business model".
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Sustainable Business Model

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

- **Skill**: `sustainable-business-model`
- **Lifecycle**: Strategize
- **Category**: Business Model
- **Primary artifact**: Sustainable Business Model business-model memo with value capture logic, risks, and next tests

Create a business model concept that makes social, environmental, and economic value
logic explicit.

## Argument Hint

`<company, product, sustainability challenge, business model, or redesign goal>`

## Usage

```text
/sustainable-business-model $ARGUMENTS
```

## Core Rule

Do not bolt sustainability onto an unchanged model. Redesign how value is created,
delivered, captured, preserved, shared, or regenerated.

Load `references/pattern-groups.md` when selecting sustainable business model
patterns.

Load `references/output-format.md` when producing a formal concept, workshop
artifact, or handoff to `business-model-design`.

## Workflow

### 1. Frame the Sustainability Challenge

Identify:

- The current product/service, customer, user, payer, and operating model.
- Social or environmental harms, waste, exclusion, access barriers, or negative
  externalities.
- Who bears the harm and who receives the value today.
- The business constraints: margin, channel, regulation, capabilities, assets, and
  stakeholder expectations.

### 2. Translate Challenge Into Opportunity Space

Ask:

- What would have to be true for this challenge to become a viable business
  opportunity?
- Which actor could pay, contribute, reuse, repair, share, finance, distribute, or
  benefit differently?
- Which current waste stream, underused asset, excluded group, or stakeholder
  misalignment could become part of the model?

### 3. Select Pattern Groups

Choose 2-5 relevant pattern groups. Common groups include:

- Pricing and revenue.
- Financing.
- Ecodesign.
- Closing the loop.
- Giving.
- Access provision.
- Social mission.

Use pattern combinations rather than isolated tactics when the challenge is systemic.

### 4. Build Model Options

For each option, define:

- Value created: economic, social, environmental.
- Value destroyed or risk shifted.
- Stakeholders and incentives.
- Revenue and financing logic.
- Key activities/resources/partners.
- Implementation obstacles and validation questions.

### 5. Recommend a Direction

Compare options on:

- Sustainability impact.
- Business viability.
- Capability fit.
- Customer/stakeholder adoption.
- Implementation complexity.
- Evidence needed.

Default output includes one recommended model and 1-2 alternates.

## Output Rules

- Be explicit about tradeoffs and rebound effects.
- Do not equate sustainability with branding, donations, or material substitution only.
- Make the business model mechanism clear: who does what differently, who pays, and
  why it scales.
- Mark uncertain impact claims as assumptions.
- When the user needs a full operating canvas, hand off the selected model to
  `business-model-design`.
