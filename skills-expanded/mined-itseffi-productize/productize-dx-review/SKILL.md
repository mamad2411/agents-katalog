---
name: productize-dx-review
description: >-
  Developer experience gate for APIs, CLIs, SDKs, docs, examples, onboarding, error messages,
  setup paths, integration friction, and time-to-hello-world. Use when developers are a
  primary user or adoption path.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# DX Review

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

- **Skill**: `dx-review`
- **Lifecycle**: Build With AI
- **Category**: AI Execution
- **Primary artifact**: DX review with developer persona, integration path, friction findings, decision, and handoff

Use this gate when the product surface is developer-facing. DX owns whether a
developer can understand, integrate, debug, and trust the product quickly.

DX Review is the developer-facing product gate. It combines plan review and live
audit: if a target is available, test the actual path; if not, score the plan and
name what evidence is missing.

## Artifact Format

Use Markdown for a short DX finding list. Use self-contained HTML when the review
needs a time-to-hello-world path map, setup funnel, API/CLI examples, error-message
audit, scorecard, or shareable developer onboarding report. Include copyable
commands and examples when that makes the artifact more useful.

## Applicability Gate

Run DX Review when the product includes an API, CLI, SDK, library, integration,
developer docs, automation platform, workflow builder, plugin, webhooks, or anything
where developers must understand and integrate the product.

If developers are not a primary user or adoption path, route to `$design-review`,
`$docs`, `$eng-review`, or `$product-review` instead.

## Step 0: Target Discovery

Find or ask for:

- product type: API, CLI, SDK, library, platform, docs, integration, or workflow tool
- target developer persona
- install/setup path
- hello-world path
- docs URL or repo docs
- examples/samples
- auth/key setup
- error surfaces
- support/community path
- plan baseline if a prior DX review exists

## DX Principles

Review against:

- zero friction at T0
- time to hello world
- learn by doing
- copy-paste examples that work
- guessable names and contracts
- errors that explain problem, cause, fix, and link
- progressive disclosure
- credible migration/upgrade path
- support path when stuck
- measurement of developer success

## TTHW Benchmarks

Use Time To Hello World as the anchor metric:

- **Excellent**: under 5 minutes with no sales call and no unnecessary setup.
- **Good**: 5-15 minutes with clear docs and one obvious path.
- **Risky**: 15-30 minutes or multiple ambiguous setup paths.
- **Broken**: over 30 minutes, missing docs/examples, or blocked by auth/setup.

State whether TTHW is measured, inferred, or unknown.

## Review Passes

### Pass 1: Getting Started

- Can a new developer identify the first step?
- Is setup linear and recoverable?
- Are prerequisites explicit?
- Does the first successful result arrive fast?

### Pass 2: API / CLI / SDK Design

- Are names, arguments, responses, and errors predictable?
- Are defaults safe?
- Are examples realistic?
- Is versioning or compatibility visible?

### Pass 3: Error Messages And Debugging

For each key error surface:

| Error | Problem | Cause | Fix | Link/next step |
|---|---|---|---|---|

Errors that only say "failed" or expose internals without a fix are blockers.

### Pass 4: Documentation And Learning

- Is there a clear conceptual model?
- Are quickstart, guides, reference, and examples separated appropriately?
- Can developers search and navigate without guessing vocabulary?
- Are screenshots, snippets, and commands current?

### Pass 5: Upgrade And Migration

- How do developers move from old to new behavior?
- Are breaking changes named?
- Is there a rollback or compatibility story?
- Are deprecations timed and discoverable?

### Pass 6: Developer Environment And Tooling

- Local dev path
- sandbox/playground
- logs/traces
- CLI help/autocomplete
- editor integration
- CI examples
- test stubs or fixtures

### Pass 7: Community And Support

- Where does a stuck developer go?
- Are issues, examples, FAQ, and contact paths obvious?
- Is the escalation path appropriate for the product stage?

### Pass 8: Measurement

- What developer activation event matters?
- Is TTHW measured?
- Are docs searches, failed auth/setup, API errors, and support contacts instrumented?
- What feedback loop improves DX after release?

## Scorecard

Score each pass 0-10 and include evidence:

| Dimension | Score | Evidence | Top fix |
|---|---:|---|---|

Overall score:

- 8-10: strong enough to ship/grow
- 6-7: usable with clear follow-ups
- 4-5: risky; likely adoption friction
- 0-3: blocks developer adoption

## Boomerang Check

If a plan claimed a DX target, compare plan vs reality:

- promised TTHW vs measured/inferred TTHW
- promised docs/examples vs actual
- promised errors/debugging vs actual
- promised migration/support vs actual

Do not let a plan score substitute for live evidence when a live path exists.

## Route Internally

- `$technical-architecture-brief-from-product-requirements-doc`
- `$backend-design`
- `$spec-writing`
- `$verification`
- `$docs`
- `$skimmable-writing-transformation`
- `$technical-translation-and-stakeholder-communication`

## Required Output

Return:

1. **Developer Persona**: who is integrating, their goal, and their time-to-value constraint.
2. **DX Path**: install/setup, hello world, docs, examples, errors, debugging, and support path.
3. **TTHW**: measured, inferred, or unknown; include benchmark and blocker.
4. **Scorecard**: eight pass scores with evidence and top fix.
5. **Friction Findings**: blockers, confusing names, missing examples, bad errors, trust gaps, and migration/support risks.
6. **Boomerang Comparison**: plan vs reality when a prior DX promise exists.
7. **Decision**: approve, revise, block, or test with developers.
8. **Handoff**: docs, eng, product, release, QA, or comms follow-up.
