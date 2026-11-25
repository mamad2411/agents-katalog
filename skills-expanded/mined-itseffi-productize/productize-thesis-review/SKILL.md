---
name: productize-thesis-review
description: >-
  Product thesis gate for new bets, capability scope, wedge, market, positioning, pricing, and
  kill-or-continue decisions. Use before committing build or growth effort to a product
  direction.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Thesis Review

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

- **Skill**: `thesis-review`
- **Lifecycle**: Strategize
- **Category**: Strategy
- **Primary artifact**: Thesis review with product thesis, evidence map, challenge, decision, and next gate

Use this gate to test whether the product thesis is worth continuing. It asks if
the user, problem, wedge, competitive position, value capture, and evidence standard
are coherent enough for the next playbook move.

This is the Productize equivalent of a founder/CEO plan challenge. It is not a
strategy memo generator. Its job is to force a decision: proceed, narrow, validate,
pivot, pause, or kill.

## Artifact Format

Use Markdown for a short gate decision. Use self-contained HTML when the thesis
review needs a shareable decision dashboard, evidence map, wedge comparison,
positioning/pricing table, risk heatmap, or long kill/continue rationale. HTML
should make the decision easier to review, not turn the gate into a slide deck.

## Pre-Review Audit

Before judging the thesis:

1. Read the current request, prior Productize artifacts, repo docs, plans, research,
   metrics, TODOs, and any shipped behavior that constrain the bet.
2. Identify whether this is a new `$0-1` bet, a growth pivot, an operate escalation,
   or a scope-change review inside an active plan.
3. Separate user-provided facts from assumptions and model inference.
4. Check for stale artifacts: if the thesis relies on a plan, research note, metric,
   design, or release state that predates meaningful changes, mark it stale.
5. Name the blocked decision in one sentence before reviewing. If there is no
   decision to make, route to the tactical routed skill instead of running this gate.

## Mode Selection

Choose one mode and state why:

- **Expansion**: the current thesis is too small for the opportunity; explore 10x
  outcomes, then cherry-pick only concrete additions worth testing now.
- **Selective Expansion**: keep the core scope, but evaluate a short list of
  high-leverage additions.
- **Hold Scope**: the bet is directionally right; pressure-test evidence, risks,
  and execution without expanding.
- **Reduction**: the thesis is too broad; cut to the smallest bet that can prove
  or disprove value.
- **Kill/Pause**: the evidence gap, market structure, or user pull is too weak to
  justify more build/growth effort.

When a mode creates a real scope decision, handle one proposal at a time. For each:
state the proposal, why it matters, effort/risk, recommendation, and decision. Do
not batch unrelated scope choices.

## Review Passes

### 1. Premise Challenge

- What must be true for this to matter?
- Who specifically has the pain, budget, urgency, and switching pressure?
- What would make this obviously wrong within two weeks?
- What existing behavior, customer quote, metric, or market fact supports it?

### 2. Wedge And Beachhead

- Is the first segment narrow enough to find, message, serve, and learn from?
- Is the job/pain acute enough to overcome inertia?
- Does the wedge create a path to the broader product, or is it a dead end?
- What adjacent segment should be explicitly out of scope?

### 3. Positioning And Competitive Alternative

- What does the user do today instead?
- What category will they compare this against?
- What is the sharpest differentiated claim Productize can defend with evidence?
- What claim should not be made yet?

### 4. Value Capture

- What is the value metric or pricing hypothesis?
- What budget, willingness-to-pay, or cost-of-delay evidence exists?
- What packaging risk could make adoption or expansion fail?
- What pricing/monetization assumption needs validation before scale?

### 5. Evidence And Risk Register

Create a compact risk register:

| Risk | Assumption | Evidence today | Test | Decision threshold |
|---|---|---|---|---|

Include at least one demand risk, usability risk, feasibility risk, data/eval risk,
and GTM/value-capture risk when applicable.

### 6. System And Rollout Implications

- What existing product/code/data can be reused?
- What new surface area does this create for design, engineering, QA, docs, DX, or
  comms?
- If this ships and fails, what is the rollback, learning, or kill path?
- What should be instrumented before the next gate?

## Decision Protocol

For each substantive issue:

- State the issue and evidence.
- Offer the smallest viable correction.
- Recommend one option and explain why.
- If the decision materially changes scope, ask or record the decision explicitly.
- If the fix is obvious and low-risk, state it and continue.

Never silently default unresolved thesis decisions. List them in the final output
as unresolved decisions that may change downstream work.

## Route Internally

- `$market-opportunity`
- `$beachhead-segment`
- `$competitive-analysis-to-winning-positioning-strategy`
- `$product-assumptions-from-core-strategy-inputs`
- `$risky-assumption-prioritization-for-rapid-validation`
- `$pre-mortem`
- `$strategic-crux-diagnosis-and-strategy-design`

## Required Output

Return:

1. **Thesis**: user, problem, wedge, position, price/value capture, and why now.
2. **Evidence Map**: facts, assumptions, missing evidence, and riskiest leap.
3. **Mode And Scope Decision**: expansion, selective expansion, hold, reduction, pause, or kill; include accepted/deferred/skipped changes.
4. **Challenge**: strongest reason this thesis may be wrong and the fastest way to learn.
5. **Risk Register**: assumptions, evidence, tests, thresholds, and owner.
6. **Decision**: proceed, narrow, validate, pivot, pause, or kill.
7. **Next Gate**: product, design, eng, QA, release, docs, DX, or comms gate if needed; flag stale gates.
8. **Completion Summary**: status, confidence, unresolved decisions, and what would change your mind.
