---
name: productize-release
description: >-
  Release gate for ship readiness, deployment decision, changelog needs, rollback risk,
  versioning, launch coordination, and post-release learning. Use when work is moving from
  build or QA toward production.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Release

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

- **Skill**: `release`
- **Lifecycle**: Launch & Learn
- **Category**: Delivery
- **Primary artifact**: Release readiness report with scope, evidence, gate status, release decision, and post-release loop

Use this gate to decide whether to ship, hold, split, rollback, or prepare a launch
sequence. Release owns coordination across QA, docs, comms, and operating handoff.

Release is the go/no-go workflow. It does not mean "write release notes." It checks
whether the change is safe, reviewed, tested, documented, communicable, observable,
and reversible enough to reach production.

## Artifact Format

Use Markdown for a small release call. Use self-contained HTML when the release
decision needs a readiness dashboard, gate matrix, rollout/rollback visualization,
scope completion audit, verification evidence, or a shareable ship/hold artifact.
If implementation notes exist, include them as release evidence and flag stale or
unresolved entries.

## Pre-Flight

1. Detect platform, branch/base, deployment path, release artifact, and current
   production state when a repo exists.
2. Read the plan, diff, changelog, tests, QA evidence, prior gates, TODOs, and docs.
3. Identify changed user surfaces, data migrations, config/env changes, API/SDK
   changes, pricing/comms changes, and operational risks.
4. Mark stale gate outputs if the commit/scope changed since they ran.
5. Name the release decision: ship, hold, split, stage, rollback, or hotfix.

## Review Readiness Dashboard

Produce a dashboard before deciding:

| Gate | Status | Evidence | Required? | Stale? |
|---|---|---|---|---|
| Thesis | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| Product | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| Design | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| Eng | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| QA | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| Docs | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| DX | clear / missing / stale / not needed | artifact | yes/no | yes/no |
| Comms | clear / missing / stale / not needed | artifact | yes/no | yes/no |

Missing required gates block release unless the user explicitly accepts the risk.

## Release Workflow

### 1. Merge/Base Freshness

- Confirm whether the work is based on the intended release branch.
- If the base changed, state whether tests/QA need to be rerun.
- Do not hide merge conflicts, dependency changes, or drift from prior reviews.

### 2. Test And Eval Evidence

- Summarize test commands, eval suites, browser/manual QA, and coverage gaps.
- When the product has a web UI, treat `$dogfood` output as release evidence:
  pages tested, flows tested, console errors, screenshots/evidence, severity
  table, blockers, and release impact.
- Classify failures as in-scope, pre-existing, environment, flaky, or unknown.
- In-scope failures block unless explicitly accepted with rollback/mitigation.

### 3. Scope Completion Audit

Cross-reference the plan against what changed:

| Planned item | Evidence in diff/release | Status |
|---|---|---|

Classify items as implemented, intentionally deferred, missing, or no longer
relevant. Missing P0 items block release.

### 4. Scope Drift Detection

- What changed beyond the plan?
- Does the drift add product, design, engineering, QA, docs, DX, or comms risk?
- Should the release split?

### 5. Rollout And Rollback

Require:

- deployment steps
- migration/feature flag posture
- monitoring and alerting
- rollback/revert path
- owner during and after release
- customer/support impact

### 6. Docs, DX, And Comms

- Docs gate is required when behavior, setup, API, migration, or support guidance changes.
- DX gate is required when developers integrate, install, migrate, or debug the change.
- Comms gate is required for customer-facing, stakeholder-facing, pricing, or launch messages.

### 7. Post-Release Operate Handoff

Define the first operate-loop check:

- metric or signal
- support/feedback watch
- review time
- owner
- trigger for rollback, fix, growth, or new `$0-1` loop

## Decision Protocol

Use release decisions precisely:

- **Ship**: all required gates clear and rollback/monitoring are acceptable.
- **Conditional ship**: risks are known, owner accepts them, and rollback/monitoring are explicit.
- **Hold**: missing required evidence or unresolved P0/P1 risk.
- **Split**: safe subset can ship while risky scope waits.
- **Stage**: ship behind flag, cohort, or internal-only rollout.
- **Rollback/hotfix**: production behavior is already harmful.

## Route Internally

- `$pre-mortem`
- `$release-notes`
- `$post-launch-feedback-loop`
- `$metrics-review`
- `$verification`
- `$qa`
- `$dogfood` when a web UI needs browser-driven release evidence
- `$docs`
- `$comms-review`
- `$implementation-notes`

## Required Output

Return:

1. **Release Scope**: changes, affected users, dependencies, and version/changelog needs.
2. **Readiness Evidence**: tests, QA result, known risks, rollback path, and monitoring.
3. **Review Readiness Dashboard**: gate status, evidence, required/missing/stale calls.
4. **Completion Audit**: planned items, implemented evidence, missing work, and drift.
5. **Rollout Plan**: deploy, monitor, rollback, support, and owner.
6. **Decision**: ship, conditional ship, hold, split, rollback, hotfix, or stage.
7. **Post-Release Loop**: owner, metric, feedback path, review time, and next operate/grow trigger.
