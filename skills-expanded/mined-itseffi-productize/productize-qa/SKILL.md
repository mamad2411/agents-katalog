---
name: productize-qa
description: >-
  QA gate for product behavior, acceptance criteria, evals, regression risk, evidence quality,
  and ship readiness. Use when a feature, fix, eval result, or release candidate needs quality
  verification before proceeding.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# QA

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

- **Skill**: `qa`
- **Lifecycle**: Launch & Learn
- **Category**: Delivery
- **Primary artifact**: QA gate report with quality scope, evidence, issues, decision, and next gate

Use this gate to verify behavior against product expectations. QA owns evidence
quality and ship-readiness risk; it does not replace engineering fixes or release
coordination.

QA is evidence-first. Do not claim a pass without fresh verification. When the user
asks to fix bugs and the host agent can edit files, run a test -> fix -> re-test
loop. When the user asks for report-only QA, document findings and do not fix.

## Artifact Format

Use Markdown for a short pass/fail report. Use self-contained HTML when QA needs a
shareable dashboard with scenario matrix, screenshots, traces, issue severity,
health score, before/after evidence, or release-blocker status. If implementation
notes exist, verify they reflect the final tested behavior.

## Setup

1. Detect mode:
   - **Quick**: critical paths and high-risk changes only.
   - **Standard**: critical, high, and medium issues.
   - **Exhaustive**: includes cosmetic, content, accessibility, and edge polish.
   - **Regression**: compare against a baseline or previously working behavior.
   - **Report-only**: never edit files.
2. Detect target: URL, local app, diff scope, feature spec, eval set, or release
   candidate. If the target is a web UI and the request asks to use the product
   like a real user, test a URL end-to-end, capture screenshots, or inspect
   console errors, route the browser-driven exploratory pass to `$dogfood`.
3. Read product spec, acceptance criteria, test plan, TODOs, prior bug reports,
   support themes, and relevant gate outputs.
4. Detect available verification tools: unit/integration/e2e tests, browser,
   screenshots, logs, eval runner, analytics, or manual scenario review.
5. If authentication, seed data, or environment setup is missing, state the blocker
   and the safest fallback coverage.

## Baseline Workflow

### Phase 1: Initialize

- Record target, mode, scope, assumptions, and excluded surfaces.
- Identify changed files/routes/components when a diff exists.
- Create a scenario matrix before testing.

### Phase 2: Orient

- Visit or inspect the primary surfaces.
- Map top navigation, primary tasks, error states, empty states, and data flows.
- Check console/log output if available.

### Phase 3: Explore

Test like a real user:

- happy path
- first-run/empty state
- invalid inputs
- permissions/authentication
- interrupted flow
- stale page/session
- duplicate submission
- slow network or timeout
- mobile/responsive path when UI exists
- accessibility basics: keyboard, focus, labels, contrast cues

### Phase 4: Verify Acceptance

For each acceptance criterion or eval:

| Scenario | Expected | Evidence | Result | Notes |
|---|---|---|---|---|

Evidence can be command output, test results, browser screenshots, traces, logs,
metrics, or explicit reasoning when runtime execution is unavailable.

### Phase 5: Document Issues

Each issue must include:

- severity: P0/P1/P2/P3
- category: functional, UX, visual, content, performance, accessibility, data, eval
- repro steps
- expected behavior
- actual behavior
- evidence
- likely owner/gate
- fix recommendation or retest instruction

Do not report vague findings without repro or evidence.

## Health Score Rubric

Score 0-100 with explicit caveats:

- Functional correctness: 30
- Critical path completion: 20
- Data/eval validity: 15
- UX/accessibility: 15
- Performance/reliability: 10
- Content/visual polish: 5
- Observability/debuggability: 5

Any P0 blocks release. Any unresolved P1 requires a conditional pass or block
decision with owner and retest plan.

## Fix Loop

If fixing is in scope:

1. Triage issues by severity and blast radius.
2. Locate source using repo search and existing patterns.
3. Make the smallest safe fix.
4. Add or update a regression test when behavior previously worked or could recur.
5. Re-run the specific scenario.
6. Re-run broader smoke/regression checks if the fix touches shared code.
7. Record before/after evidence.

Stop and escalate if fixes require product, design, or architecture decisions.

## Final QA

Before passing:

- Re-run all affected critical paths.
- Confirm no new console/test/eval failures in covered scope.
- Confirm docs/release/comms follow-ups are called when behavior changed.
- State exactly what was not tested.

## Route Internally

- `$dogfood` for browser-driven exploratory QA of local apps, staging URLs, production URLs, sitemap coverage, screenshots, and console checks
- `$test-scenarios`
- `$verification`
- `$acceptance-criteria-for-ui`
- `$validate-data`
- `$robust-experiment-design-from-goals-and-systems`
- `$ab-test-analysis`
- `$support-tickets-as-actionable-product-improvements`
- `$implementation-notes` when testing reveals spec deviations or unresolved implementation decisions

## Required Output

Return:

1. **Quality Scope**: surfaces, user flows, data paths, and scenarios covered.
2. **Evidence**: fresh verification, screenshots/traces/metrics when available, and caveats.
3. **Scenario Matrix**: scenarios, expected behavior, evidence, result, and notes.
4. **Issues**: severity, category, repro steps, expected behavior, actual behavior, evidence, and owner.
5. **Fix / Retest Log**: fixes applied or recommended, tests added, and before/after evidence.
6. **Health Score**: score, caveats, and release impact.
7. **Decision**: pass, conditional pass, retest, block, or escalate.
8. **Next Gate**: release, docs, comms, eng, design, or product review needed.
