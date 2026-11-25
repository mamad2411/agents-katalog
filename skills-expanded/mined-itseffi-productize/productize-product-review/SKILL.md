---
name: productize-product-review
description: >-
  Product gate for PM-quality scope, requirements, user value, acceptance criteria,
  priorities, metrics, and ship/learn decisions. Use when a plan needs product judgment before
  design, engineering, QA, release, or growth work proceeds.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product Review

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

- **Skill**: `product-review`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Product review with product judgment, requirement risks, priority call, decision, and handoff

Use this gate when the question is whether the product plan is coherent and
decision-ready: right user, right problem, clear scope, usable acceptance criteria,
metrics, non-goals, and learning loop.

Product Review is the PM-quality gate. It does not reopen the whole thesis unless
the requirements reveal a thesis contradiction. It turns product intent into a
plan a designer, engineer, QA tester, release owner, docs owner, or comms owner can
act on without guessing.

## Artifact Format

Use Markdown for compact scope calls. Use self-contained HTML when the product
review includes a long acceptance matrix, multi-stakeholder tradeoffs, flow/state
coverage, downstream gate readiness, or a shareable product decision report.
Prefer tables, status chips, and collapsible detail over long prose.

## Pre-Review Audit

Before reviewing:

1. Read the source artifact: PRD, plan, transcript, ticket, design, diff, research,
   metrics, or user request.
2. Identify the active playbook stage: `$0-1`, `$operate`, or `$grow`.
3. Find prior gates and mark stale ones if the plan changed since they ran.
4. Name the product decision being gated: scope approval, spec readiness, ship
   readiness, growth experiment approval, or learning-loop decision.
5. If the artifact is missing, build the smallest product brief from available
   context before reviewing it.

## Review Passes

### 1. User, Job, And Outcome

- Is the user/persona specific enough?
- Is the job or pain observable?
- Does the feature solve a user outcome, not just satisfy an internal request?
- What user behavior should change if this works?

### 2. Scope And Non-Goals

- What is P0 and must ship together?
- What can be split into a follow-up?
- What is explicitly not in scope?
- Does the scope match the evidence standard and timeline?

### 3. Requirements Quality

Check every major requirement for:

- user trigger and entry point
- happy path
- empty/loading/error/permission states
- edge cases and abuse cases
- data dependencies
- owner and open decision
- acceptance criterion

### 4. Prioritization And Tradeoffs

Use P0/P1/P2 or must/should/could, but include the tradeoff:

| Item | Priority | Why | Risk if cut | Risk if kept |
|---|---|---|---|---|

If more than one stakeholder goal competes, surface the decision instead of hiding
it in a blended scope.

### 5. Metrics And Learning

- What metric or qualitative signal proves this helped?
- What instrumentation is required?
- What is the expected learning loop after release?
- What threshold triggers iterate, rollback, grow, or new `$0-1` work?

### 6. Downstream Readiness

Check whether each downstream owner can proceed:

| Gate | Needs | Status |
|---|---|---|
| Design | flows, states, UX constraints | clear / unclear / not needed |
| Eng | contracts, data flow, dependencies | clear / unclear / not needed |
| QA | acceptance criteria, scenarios | clear / unclear / not needed |
| Release | rollout, risk, monitoring | clear / unclear / not needed |
| Docs | changed behavior, audience | clear / unclear / not needed |
| DX | developer path, examples | clear / unclear / not needed |
| Comms | audience, message, proof | clear / unclear / not needed |

## Decision Protocol

For each product issue:

- Name the product risk, not just the missing section.
- Recommend a fix: revise, split, validate, defer, or stop.
- Ask or record one decision at a time when scope, priority, or acceptance changes.
- Do not bury unresolved product choices in TODOs; list them as blockers or
  accepted risks.

## Route Internally

- `$prds-from-product-information-and-assumptions`
- `$structured-requirements-from-conversation-transcripts`
- `$acceptance-criteria-for-ui`
- `$requirements-prioritization-with-p0-p1-p2-framework`
- `$roadmap-update`
- `$feature-impact-models-from-kpis-and-assumptions`
- `$metrics-review`

## Required Output

Return:

1. **Product Judgment**: what is clear, unclear, over-scoped, or under-specified.
2. **Requirement Risks**: missing user flows, acceptance criteria, metrics, dependencies, and non-goals.
3. **Priority Call**: P0/P1/P2 or must/should/could with cut/keep tradeoffs.
4. **Acceptance Matrix**: scenarios, states, metrics, and instrumentation required.
5. **Downstream Readiness**: design, eng, QA, release, docs, DX, and comms status.
6. **Decision**: approve, revise, split, validate, or stop.
7. **Handoff**: next reviewer/gate and the artifact it needs.
8. **Completion Summary**: status, confidence, unresolved decisions, and accepted product risks.
