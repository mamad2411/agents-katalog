---
name: productize-0-1
description: >-
  Productize 0-1 orchestrator for turning a raw product idea or new capability bet into a
  working first product slice. Use for founder, PM, CPO, AI product leader, or AI builder work
  that must combine product framing, capability scoping, curated data, application setup, eval
  design, eval runs, behavior analysis, fixes, and ship/learn decisions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# 0-1 Product Build Loop

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

- **Skill**: `0-1`
- **Lifecycle**: Think
- **Category**: Venture / 0-1
- **Primary artifact**: 0-1 product build brief with capability scope, curated data, app setup, eval matrix, behavior analysis, fixes, ship gate, and next learning loop

Use this skill when the user wants to build a new product, create a first version,
turn a vague idea into a working capability, or reshape an existing product around a
new capability. This is not a strategy handoff. Run the product-build loop.

## Core Principle

0-1 product work is a loop, not a sequence ending in "handoff to build".

The loop is:

1. Scope capability and curate data.
2. Set up the application.
3. Design evals.
4. Run evals.
5. Analyze behavior and spot error patterns.
6. Apply fixes.
7. Repeat until the ship gate is met, then launch and learn.

For AI products and agentic workflows, treat evals, traces, curated examples, edge
cases, and instrumentation as part of the product, not as a QA step after product
definition.

## Artifact Format

Use Markdown for short loop notes or repo-native docs. Use self-contained HTML
when the 0-1 work creates a long plan, visual comparison, eval dashboard, PR
explainer, implementation-notes file, or shareable review artifact. When the user
asks for running implementation notes during build, activate `$implementation-notes`
and keep the requested `implementation-notes.md` or `implementation-notes.html`
current as decisions and deviations arise.

## Route Internally

Use the narrowest Productize skill for each part of the loop:

### 1. Scope Capability And Curate Data

- `$product-ideas-from-user-responses`
- `$problem-framing-before-jumping-to-solutions`
- `$beachhead-segment`
- `$market-opportunity`
- `$competitive-analysis-to-winning-positioning-strategy`
- `$positioning-statements-from-competitive-analysis-and-value`
- `$pricing-strategy`
- `$monetization-strategy`
- `$product-assumptions-from-core-strategy-inputs`
- `$risky-assumption-prioritization-for-rapid-validation`
- `$data-context-extractor`

Output: first capability, target user, job/pain, wedge, competitive position,
pricing/value-capture assumptions, input data, evidence gaps, high-risk assumptions,
and minimum useful dataset or examples.

### 2. Set Up Application

- `$app-design-from-project-requirements`
- `$frontend-design`
- `$backend-design`
- `$technical-architecture-brief-from-product-requirements-doc`
- `$writing-plans`
- `$tdd`
- `$implementation-notes` when the user asks for running notes during build

Output: app shell, system boundaries, data flow, UI flow, state model, build plan,
and first implementation slice.

### 3. Design Evals

- `$test-scenarios`
- `$verification`
- `$acceptance-criteria-for-ui`
- `$robust-experiment-design-from-goals-and-systems`
- `$success-metrics-for-design-decisions`
- `$event-tracking-schemas-from-ui-and-metrics-requirements`

Output: eval matrix, test scenarios, behavioral traces to inspect, acceptance gates,
instrumentation, and product success criteria.

### 4. Run Evals

- `$verification`
- `$test-scenarios`
- `$validate-data`
- `$ab-test-analysis` when there is experiment data

Output: fresh evidence, pass/fail results, screenshots or trace evidence when
available, metric caveats, and unresolved risks.

### 5. Analyze Behavior And Error Patterns

- `$systematic-debugging`
- `$feature-results-analysis-from-draft-to-final-report`
- `$metric-drops-diagnosis-with-rigorous-stepwise-decomposition`
- `$post-launch-feedback-loop`
- `$support-tickets-as-actionable-product-improvements`

Output: behavior pattern map, root causes, error clusters, missing data, product
confusion, UX friction, prompt/model failure modes, and priority fixes.

### 6. Apply Fixes

- `$tdd`
- `$frontend-design`
- `$backend-design`
- `$design-critique`
- `$verification`
- `$implementation-notes` when fixes interpret or depart from the spec

Output: applied code/design/product changes when the host agent can edit files,
or a concrete fix plan with owners, files, tests, and verification steps when it
cannot.

### 7. Ship And Learn

- `$pre-mortem`
- `$release-notes`
- `$post-launch-feedback-loop`
- `$metrics-review`

Output: ship/no-ship decision, launch notes, learning plan, telemetry review, and
next loop.

## Gate Cadence

Run the relevant Productize reviewer or gate at each decision point:

| 0-1 move | Gate |
|---|---|
| Move 1: Scope capability and curate data | `$thesis-review` + `$product-review` |
| Move 2a: Design | `$design-review` |
| Move 2b: Architect | `$eng-review` |
| Move 2c: Spec | `$product-review` |
| Move 2d: Build | `$eng-review` + `$qa` |
| Move 3: Design evals | `$qa` + `$product-review` |
| Deploy | `$release` |
| Move 4: Run evals | `$qa` |
| Move 5: Analyze | `$eng-review` |
| Move 6: Apply fixes | `$design-review` + `$qa` |
| Move 7: Ship and learn | `$release` + `$docs` + `$comms-review` |

## Operating Rules

1. Do not stop after naming the idea, wedge, or PRD. Continue into capability, app,
   eval, behavior, and fix planning unless the user explicitly asks to stop earlier.
2. The first capability must be small enough to build and evaluate. If it is too
   broad, cut scope before writing the spec.
3. Define evals before claiming the app is ready. For AI products, include golden
   examples, adversarial examples, human review criteria, and observable behavior.
4. If a repo is available and the user asked to build, make code changes through the
   host agent. If no repo exists, produce the scaffold and build plan.
5. Every loop must end with one of: ship, repeat, pivot, pause, or kill.

## Required Output

Return:

1. **0-1 Route**: selected internal skills and why.
2. **Capability Scope**: target user, job/pain, first capability, non-goals, and wedge.
3. **Curated Data / Evidence**: available inputs, needed examples, edge cases, and risky gaps.
4. **Application Setup**: UI, backend, data flow, state, implementation slice, and files or modules when a repo exists.
5. **Eval Matrix**: scenarios, acceptance gates, instrumentation, metrics, and review criteria.
6. **Run / Analyze / Fix Loop**: current eval result, behavior/error patterns, fixes applied or planned, and verification.
7. **Ship Gate**: ship, repeat, pivot, pause, or kill; include the next learning loop.

If the user asks a broad 0-1 question, produce the first useful loop slice instead
of a generic venture strategy memo.
