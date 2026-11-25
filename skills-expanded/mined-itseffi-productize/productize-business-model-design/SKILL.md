---
name: productize-business-model-design
description: >-
  Design, compare, or document business models using the right canvas for the situation. Use
  when a founder, product team, strategist, or innovation team asks to fill a business model
  canvas, lean canvas, platform canvas, value creation and capture model, revenue/cost logic,
  customer/user/payer model, or variants of "what is the business model", "how does this make
  money", "which canvas should I use", "turn this idea into a business model", or "compare
  these business models".
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Business Model Design

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

- **Skill**: `business-model-design`
- **Lifecycle**: Strategize
- **Category**: Business Model
- **Primary artifact**: Business Model Design business-model memo with value capture logic, risks, and next tests

Create a working business model artifact, not a generic strategy essay. A business
model describes how an organization creates, delivers, and captures value.

## Argument Hint

`<venture, product, company, platform, startup idea, or blank-canvas request>`

## Usage

```text
/business-model-design $ARGUMENTS
```

## Core Rule

Choose the canvas based on the user's situation, then produce a filled-in canvas with
clear assumptions, open questions, and validation priorities.

Load `references/canvas-selection.md` when choosing between canvas types.

Load `references/canvas-templates.md` before creating blank templates, filled-in
canvases, visual layouts, tables, or printable artifacts. It contains the canonical
field labels for the standard, lean, and platform canvases.

Load `references/business-model-output-rules.md` when comparing models, creating
handoff-ready outputs, or translating a canvas into experiments.

Use the matching `assets/*.html` file when the user asks for a printable, visual, or
browser-openable canvas:

- `assets/standard-business-model-canvas.html`
- `assets/lean-business-model-canvas.html`
- `assets/platform-business-model-canvas.html`

## Extended Reference

Load `references/extended-reference.md` when the request mentions `business model canvas`, `bmc`, `all modes`, `value proposition mode`. Use this reference material to sharpen this Productize skill.

## Workflow

### 1. Identify the Business Model Context

Determine:

- Existing company, new venture, corporate startup, platform, or sustainability
  redesign.
- Customer, user, buyer, payer, producer, consumer, owner, and partner roles.
- What value is created, for whom, how it is delivered, and how value is captured.
- Whether the user wants a blank template, a filled canvas, a critique, or a
  before/after redesign.

If the user only gives a product or technology, ask what customer/user problem it
addresses before filling the model.

### 2. Select the Canvas

- **Standard Business Model Canvas**: use for most companies and product/service
  business models.
- **Lean Business Model Canvas**: use for early-stage ventures, corporate startups,
  unknown markets, and concepts that need problem/solution/risk validation.
- **Platform Business Model Canvas**: use for multi-sided platforms, marketplaces,
  ecosystems, and models where several stakeholder groups exchange value.

If two canvases apply, pick the primary one and add a short note showing what the
secondary lens would reveal.

### 3. Fill the Canvas

For each field:

- Write concrete content, not slogans.
- Separate known facts from assumptions.
- Name the stakeholder explicitly.
- Link revenue streams to payer behavior and costs to required activities/resources.
- Avoid product-centric framing when the field should describe a customer need,
  transaction, or job.

### 4. Test Internal Coherence

Check:

- Does the value proposition match the customer segment and channel?
- Are key activities/resources/partners sufficient to deliver the value proposition?
- Does revenue logic match who receives value and who pays?
- Does the cost structure reflect the actual operating model?
- For platforms, are value transactions balanced for all sides?
- For lean canvases, are the highest-risk assumptions visible and testable?

### 5. Produce the Output

Default output:

1. **Canvas selection** with rationale.
2. **Filled canvas** in editable Markdown table form.
3. **Coherence check**: strongest fit, weakest link, hidden assumption.
4. **Validation priorities**: 3-5 experiments or evidence gaps.
5. **Next decision**: what the team should decide or test next.

## Output Rules

- Preserve the exact canvas field labels from `references/canvas-templates.md`.
- Do not rename canvas fields unless the user asks for a custom artifact.
- Do not copy long source passages. Use canonical labels and original analysis.
- If facts are missing, mark them as assumptions rather than inventing them.
- When creating a visual or printable canvas, keep the same field structure as the
  matching template.
- Do not reproduce branded poster/trade-dress artwork from source PDFs. Use the clean
  bundled templates and preserve the operational structure.
