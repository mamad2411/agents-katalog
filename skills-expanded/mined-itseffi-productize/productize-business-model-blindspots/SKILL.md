---
name: productize-business-model-blindspots
description: >-
  Audit hidden assumptions and cognitive barriers in a business model. Use when a founder,
  executive, strategist, or product team may be trapped by product-centric thinking, marketing
  myopia, dominant logic, outdated assumptions, unclear customer need, a failing or
  unexpectedly successful business model, or asks "what are we missing", "why is this model
  not working", "what business are we really in", or "challenge our assumptions".
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Business Model Blindspots

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

- **Skill**: `business-model-blindspots`
- **Lifecycle**: Discover
- **Category**: Business Model
- **Primary artifact**: Business Model Blindspots business-model memo with value capture logic, risks, and next tests

Expose the mental models, product-centric assumptions, and outdated theories that
block business model innovation.

## Argument Hint

`<company, business model, strategy, failed initiative, surprising success, or assumption set>`

## Usage

```text
/business-model-blindspots $ARGUMENTS
```

## Core Rule

Do not start by proposing a new business model. First make the current theory visible:
what the team believes about customers, needs, markets, technology, capabilities,
economics, and identity.

Load `references/diagnostic-questions.md` for detailed diagnostic questions.

Load `references/output-format.md` when producing a formal audit or workshop artifact.

## Workflow

### 1. Reconstruct the Current Theory

Identify the implicit beliefs behind the model:

- Who the customer, user, buyer, payer, and beneficiary are.
- What need or job the business exists to serve.
- What the organization believes it gets paid for.
- What capabilities it believes matter most.
- What market, technology, regulation, or behavior assumptions must remain true.
- What the organization believes it is and is not allowed to become.

### 2. Detect Product-Centric Framing

Look for:

- Defining the business by the current product category.
- Treating substitutes or non-consumption as irrelevant.
- Assuming growth because the market or population grows.
- Assuming technical superiority guarantees demand.
- Confusing customer need with current product form.

Reframe from product to underlying customer need or job.

### 3. Test the Theory for Fitness

Check whether assumptions:

- Fit observable reality.
- Fit each other.
- Are known and understood by decision-makers.
- Are being tested continuously.

Warning signs:

- Unexpected failure.
- Unexpected success.
- Rapid growth that changes the business.
- Market, technology, regulation, or customer behavior shifts.
- Persistent exceptions explained away as edge cases.

### 4. Identify Dominant Logic Traps

Surface decision rules such as:

- "Our customers are always..."
- "We make money by..."
- "The three things that matter are..."
- "We cannot serve..."
- "Partners/users/suppliers will never..."

Challenge each rule with counterexamples, alternative segments, and changed
conditions.

### 5. Produce an Assumption Audit

Default output:

1. Current theory of the business.
2. Product-centric or market-myopic framing risks.
3. Hidden assumptions table.
4. Contradictions and warning signs.
5. Reframed customer need/job.
6. Tests to validate or falsify the most dangerous assumptions.

## Output Rules

- Separate observations from interpretations.
- Do not call an assumption wrong unless there is evidence.
- Mark unknowns as unknowns and turn them into tests.
- Focus on business model consequences, not generic strategy critique.
- When the user asks for a redesign, run the audit first, then hand off to
  `business-model-design`.
